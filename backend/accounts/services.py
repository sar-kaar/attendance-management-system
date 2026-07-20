import logging
import secrets

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import OTP

logger = logging.getLogger(__name__)


class OTPService:
    """Service layer for OTP operations."""

    @staticmethod
    def generate_code():
        # secrets, not random: these codes gate password resets and 2FA, and
        # random's Mersenne Twister is predictable from observed output.
        return f"{secrets.randbelow(1000000):06d}"

    @staticmethod
    def recent_otp(email, purpose):
        """Most recent unused OTP for this email/purpose, if any."""
        return OTP.objects.filter(
            email=email, purpose=purpose, is_used=False
        ).order_by('-created_at').first()

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

        expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)

        subject = f"Your {purpose_labels.get(otp.purpose, 'OTP')} Code"
        message = f"""
Your verification code is: {otp.code}

This code will expire in {expiry_minutes} minutes.
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
        <p>This code will expire in <strong>{expiry_minutes} minutes</strong>.</p>
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
            # Log the cause: SMTP auth failures and unverified-sender rejections
            # are the common ones, and a bare False makes them undiagnosable in
            # production where DEBUG is off.
            logger.exception('Failed to send OTP email to %s (purpose=%s)',
                             otp.email, otp.purpose)
            return False

    @classmethod
    def send_otp(cls, email, purpose):
        # Per-email cooldown. The IP throttle on the view can't stop someone
        # mailbombing one address from rotating IPs, and this also protects the
        # shared Brevo daily quota.
        cooldown = getattr(settings, 'OTP_RESEND_COOLDOWN_SECONDS', 60)
        previous = cls.recent_otp(email, purpose)
        if previous:
            age = (timezone.now() - previous.created_at).total_seconds()
            if age < cooldown:
                wait = int(cooldown - age)
                return None, f"Please wait {wait} seconds before requesting another code."

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