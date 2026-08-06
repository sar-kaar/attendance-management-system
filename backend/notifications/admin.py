from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'is_active', 'updated_at')
    list_filter = ('platform', 'is_active')
    search_fields = ('user__username', 'user__email', 'token')
