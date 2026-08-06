from django.db import models

from accounts.models import User


class Device(models.Model):
    """A push-notification target: one registered device per (user, token).

    Mobile clients register their FCM/Expo push token on login and unregister on
    logout. A token is globally unique — if it moves to a different user (e.g. a
    shared device), registering re-points it — so `token` is the unique key."""

    class Platform(models.TextChoices):
        IOS = 'ios', 'iOS'
        ANDROID = 'android', 'Android'
        WEB = 'web', 'Web'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=Platform.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'id']

    def __str__(self):
        return f"{self.user} · {self.platform} · {self.token[:12]}…"
