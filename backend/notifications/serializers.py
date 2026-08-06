from rest_framework import serializers

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    # The view upserts on `token` via update_or_create, so drop the UniqueValidator
    # that ModelSerializer would otherwise auto-add from the model's unique=True —
    # otherwise re-registering an existing token 400s instead of re-pointing it.
    token = serializers.CharField(max_length=255, validators=[])

    class Meta:
        model = Device
        fields = ['id', 'token', 'platform', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_active', 'created_at', 'updated_at']
