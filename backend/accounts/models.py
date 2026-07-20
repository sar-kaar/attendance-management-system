from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        FACULTY = 'faculty', 'Faculty'
        STUDENT = 'student', 'Student'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class OTP(models.Model):
    class Purpose(models.TextChoices):
        EMAIL_VERIFICATION = 'email_verification', 'Email Verification'
        PASSWORD_RESET = 'password_reset', 'Password Reset'
        LOGIN_2FA = 'login_2fa', 'Two-Factor Authentication'

    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=Purpose.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'purpose', 'is_used']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.purpose} - {'Used' if self.is_used else 'Active'}"

    def is_valid(self):
        from django.utils import timezone
        return not self.is_used and self.attempts < self.max_attempts and timezone.now() < self.expires_at

    def increment_attempts(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])

    def mark_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])
