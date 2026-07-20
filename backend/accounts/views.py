from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer, UserSerializer, AdminUserSerializer,
    OTPSendSerializer, OTPVerifySerializer, SocialTokenSerializer,
)
from .models import User
from .services import OTPService
from .social import (
    SocialAuthError, get_or_create_social_user,
    verify_google_token, verify_facebook_token,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'admin')


class AdminUserViewSet(viewsets.ModelViewSet):
    """Admin-only management of faculty and student login accounts."""

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get('role')
        if role:
            qs = qs.filter(role=role)
        return qs

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('password')
        if not new_password or len(new_password) < 6:
            return Response({'error': 'password must be at least 6 characters'}, status=400)
        user.set_password(new_password)
        user.save(update_fields=['password'])
        return Response({'message': 'Password reset successfully'})


class OTPSendView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OTPSendSerializer
    throttle_scope = 'otp_send'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        purpose = serializer.validated_data['purpose']

        otp, message = OTPService.send_otp(email, purpose)
        if not otp:
            # Cooldown is the caller asking too soon, not a server fault.
            code = 429 if 'wait' in message.lower() else 500
            return Response({'error': message}, status=code)

        return Response({'message': message})


class OTPVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OTPVerifySerializer
    throttle_scope = 'otp_verify'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success, message = OTPService.verify_otp(
            serializer.validated_data['email'],
            serializer.validated_data['code'],
            serializer.validated_data['purpose']
        )

        if not success:
            return Response({'error': message}, status=400)

        return Response({'message': message})


class _SocialLoginView(generics.GenericAPIView):
    """Exchange a verified provider credential for our own JWT pair.

    Subclasses implement `verify`. The provider token is validated server-side
    first; only then do we mint tokens, so the browser can never assert an
    identity we have not independently confirmed with the provider.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = SocialTokenSerializer
    throttle_scope = 'social_login'

    def verify(self, token):
        raise NotImplementedError

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            profile = self.verify(serializer.validated_data['token'])
            user, created = get_or_create_social_user(
                profile['email'], profile['first_name'], profile['last_name'],
            )
        except SocialAuthError as e:
            return Response({'error': str(e)}, status=400)

        if not user.is_active:
            return Response({'error': 'This account has been disabled.'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'created': created,
        })


class GoogleLoginView(_SocialLoginView):
    # Resolved through the module at call time so the verifier stays a single
    # named seam, patchable in tests without reaching into the class.
    def verify(self, token):
        return verify_google_token(token)


class FacebookLoginView(_SocialLoginView):
    def verify(self, token):
        return verify_facebook_token(token)
