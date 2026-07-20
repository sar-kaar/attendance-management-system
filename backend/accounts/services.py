from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import OTP
import random


class OTPService:
    """Service layer for OTP operations."""

    @staticmethod
    def generate_code():
        return f"{random.randint(100000, 999999)}"

    @staticmethod
    def create_otp(email, purpose):
        OTP.objects.filter(email=email, purpose=purpose, is_used=False).update(is_used=True)

        expires_at = timezone.now() + timezone.timedelta(
            minutes=getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        )

        otp = OTP.objects.create(
            email=email,
            code=OTPService.generate_code(),
            purpose=purpose,
            expires_at=expires_at,
        )
        return otp

    @staticmethod
    def send_otp_email(otp):
        purpose_labels = {
            'email_verification': 'Email Verification',
            'password_reset': 'Password Reset',
            'login_2fa': 'Two-Factor Authentication',
        }

        subject = f"Your {purpose_labels.get(otp.purpose, 'OTP')} Code"
        message = f"""
Your verification code is: {otp.code}

This code will expire in {10} minutes.
If you didn't request this, please ignore this email.
"""
        html_message = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50;">{purpose_labels.get(otp.purpose, 'OTP')} Code</h2>
        <p>Your verification code is:</p>
        <div style="background: #f4f4f4; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
            {otp.code}
        </div>
        <p>This code will expire in <strong>10 minutes</strong>.</p>
        <p>If you didn't request this, please ignore this email.</p>
        <hr style="margin: 20px 0;">
        <p style="font-size: 12px; color: #888;">AMS Attendance Management System</p>
    </div>
</body>
</html>
"""

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [otp.email],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    @classmethod
    def send_otp(cls, email, purpose):
        otp = cls.create_otp(email, purpose)
        sent = cls.send_otp_email(otp)
        if not sent:
            return None, "Failed to send email. Please try again."
        return otp, "OTP sent successfully"

    @staticmethod
    def verify_otp(email, code, purpose):
        try:
            otp = OTP.objects.filter(
                email=email,
                purpose=purpose,
                is_used=False
            ).latest('created_at')
        except OTP.DoesNotExist:
            return False, "Invalid or expired OTP"

        if not otp.is_valid():
            if otp.is_used:
                return False, "OTP already used"
            if otp.attempts >= otp.max_attempts:
                return False, "Maximum attempts exceeded"
            if timezone.now() >= otp.expires_at:
                return False, "OTP expired"

        if otp.code != code:
            otp.increment_attempts()
            return False, f"Invalid code. {otp.max_attempts - otp.attempts} attempts remaining"

        otp.mark_used()
        return True, "OTP verified successfully"