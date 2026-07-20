from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, AdminUserSerializer, OTPSendSerializer, OTPVerifySerializer
from .models import User
from .services import OTPService


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

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        purpose = serializer.validated_data['purpose']

        otp, message = OTPService.send_otp(email, purpose)
        if not otp:
            return Response({'error': message}, status=500)

        return Response({'message': message})


class OTPVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OTPVerifySerializer

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
