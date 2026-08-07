from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device
from .serializers import DeviceSerializer


class DeviceRegisterView(APIView):
    """B5: register (or re-point) the caller's push token.

    Idempotent: the same token registered again updates its owner/platform and
    re-activates it, so a client can safely call this on every login."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device, _created = Device.objects.update_or_create(
            token=serializer.validated_data['token'],
            defaults={
                'user': request.user,
                'platform': serializer.validated_data['platform'],
                'is_active': True,
            },
        )
        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)


class DeviceUnregisterView(APIView):
    """B5: unregister a push token on logout. Only the owner may unregister."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response(
                {'detail': 'token is required.'}, status=status.HTTP_400_BAD_REQUEST
            )
        deleted, _ = Device.objects.filter(user=request.user, token=token).delete()
        if not deleted:
            return Response(
                {'detail': 'No such device for this user.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceListView(APIView):
    """List the caller's registered devices."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        devices = Device.objects.filter(user=request.user)
        return Response(DeviceSerializer(devices, many=True).data)
