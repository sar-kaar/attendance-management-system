from unittest.mock import patch
from django.test import TestCase, override_settings
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail
from .models import User, OTP
from .services import OTPService
from .social import SocialAuthError, verify_google_token, verify_facebook_token


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'student',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_register_success(self):
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_short_password(self):
        payload = self.valid_payload.copy()
        payload['password'] = '123'
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_default_role_is_student(self):
        self.client.post(self.register_url, self.valid_payload)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.role, 'student')


class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login/'
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='faculty'
        )

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser', 'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nouser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            role='student', first_name='Test', last_name='User'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['role'], 'student')

    def test_profile_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class OTPTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.send_url = '/api/auth/otp/send/'
        self.verify_url = '/api/auth/otp/verify/'
        self.email = 'test@example.com'
        # DRF keeps throttle history in the cache, which is process-global and
        # would otherwise leak across tests: every test hits the same endpoint
        # from the same client IP, so the 6th send in this class would 429 on
        # throttle state left by earlier tests rather than its own behaviour.
        cache.clear()

    def test_send_otp_success(self):
        response = self.client.post(self.send_url, {
            'email': self.email,
            'purpose': 'email_verification'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.email])

    def test_send_otp_invalid_email(self):
        response = self.client.post(self.send_url, {
            'email': 'not-an-email',
            'purpose': 'email_verification'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_otp_invalid_purpose(self):
        response = self.client.post(self.send_url, {
            'email': self.email,
            'purpose': 'invalid_purpose'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_otp_success(self):
        send_resp = self.client.post(self.send_url, {
            'email': self.email,
            'purpose': 'email_verification'
        })
        self.assertEqual(send_resp.status_code, status.HTTP_200_OK)
        otp_code = mail.outbox[0].body.split('verification code is: ')[1].split('\n')[0].strip()

        response = self.client.post(self.verify_url, {
            'email': self.email,
            'code': otp_code,
            'purpose': 'email_verification'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_verify_otp_invalid_code(self):
        self.client.post(self.send_url, {
            'email': self.email,
            'purpose': 'email_verification'
        })
        response = self.client.post(self.verify_url, {
            'email': self.email,
            'code': '000000',
            'purpose': 'email_verification'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_verify_otp_wrong_purpose(self):
        self.client.post(self.send_url, {
            'email': self.email,
            'purpose': 'email_verification'
        })
        otp_code = mail.outbox[0].body.split('verification code is: ')[1].split('\n')[0].strip()
        response = self.client.post(self.verify_url, {
            'email': self.email,
            'code': otp_code,
            'purpose': 'password_reset'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_otp_service_generate_code(self):
        code = OTPService.generate_code()
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_otp_service_create_otp(self):
        otp = OTPService.create_otp('test@example.com', 'email_verification')
        self.assertEqual(otp.email, 'test@example.com')
        self.assertEqual(otp.purpose, 'email_verification')
        self.assertEqual(len(otp.code), 6)
        self.assertFalse(otp.is_used)

    def test_otp_service_verify_otp(self):
        otp = OTPService.create_otp('test@example.com', 'email_verification')
        success, message = OTPService.verify_otp('test@example.com', otp.code, 'email_verification')
        self.assertTrue(success)
        self.assertEqual(message, 'OTP verified successfully')
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)

    def test_otp_service_verify_wrong_code(self):
        otp = OTPService.create_otp('test@example.com', 'email_verification')
        success, message = OTPService.verify_otp('test@example.com', '000000', 'email_verification')
        self.assertFalse(success)
        self.assertIn('Invalid code', message)

    def test_otp_max_attempts(self):
        otp = OTPService.create_otp('test@example.com', 'email_verification')
        for _ in range(3):
            OTPService.verify_otp('test@example.com', '000000', 'email_verification')
        otp.refresh_from_db()
        self.assertEqual(otp.attempts, 3)
        success, message = OTPService.verify_otp('test@example.com', '000000', 'email_verification')
        self.assertFalse(success)
        self.assertIn('Maximum attempts', message)


class SocialLoginTest(TestCase):
    """The provider call itself is patched; what these cover is that we only
    trust a verified result, and what we do with it afterwards."""

    def setUp(self):
        self.client = APIClient()
        self.google_url = '/api/auth/google/'
        self.facebook_url = '/api/auth/facebook/'
        cache.clear()

    GOOGLE_PROFILE = {'email': 'newuser@mitnepal.edu.np',
                      'first_name': 'New', 'last_name': 'User'}

    @patch('accounts.views.verify_google_token')
    def test_google_login_creates_user_and_returns_jwt(self, mock_verify):
        mock_verify.return_value = self.GOOGLE_PROFILE
        resp = self.client.post(self.google_url, {'token': 'valid-google-token'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)
        self.assertTrue(resp.data['created'])
        user = User.objects.get(email='newuser@mitnepal.edu.np')
        self.assertEqual(user.role, 'student')
        # Provider-only accounts must not be reachable by password.
        self.assertFalse(user.has_usable_password())

    @patch('accounts.views.verify_google_token')
    def test_google_login_reuses_existing_account_by_email(self, mock_verify):
        existing = User.objects.create_user(
            username='existing', email='newuser@mitnepal.edu.np',
            password='test1234', role='faculty')
        mock_verify.return_value = self.GOOGLE_PROFILE
        resp = self.client.post(self.google_url, {'token': 'valid-google-token'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data['created'])
        self.assertEqual(User.objects.filter(email='newuser@mitnepal.edu.np').count(), 1)
        # An existing role must survive a social sign-in.
        existing.refresh_from_db()
        self.assertEqual(existing.role, 'faculty')

    @patch('accounts.views.verify_google_token')
    def test_google_login_rejects_unverified_token(self, mock_verify):
        mock_verify.side_effect = SocialAuthError('Google sign-in failed verification.')
        resp = self.client.post(self.google_url, {'token': 'forged'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.data)
        self.assertEqual(User.objects.count(), 0)

    def test_google_login_requires_token(self):
        resp = self.client.post(self.google_url, {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('accounts.views.verify_facebook_token')
    def test_facebook_login_creates_user(self, mock_verify):
        mock_verify.return_value = {'email': 'fbuser@example.com',
                                    'first_name': 'Fb', 'last_name': 'User'}
        resp = self.client.post(self.facebook_url, {'token': 'valid-fb-token'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='fbuser@example.com').exists())

    @patch('accounts.views.verify_facebook_token')
    def test_disabled_account_cannot_sign_in_socially(self, mock_verify):
        User.objects.create_user(username='banned', email='banned@example.com',
                                 password='test1234', is_active=False)
        mock_verify.return_value = {'email': 'banned@example.com',
                                    'first_name': '', 'last_name': ''}
        resp = self.client.post(self.facebook_url, {'token': 'valid-fb-token'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @patch('accounts.views.verify_google_token')
    def test_username_collision_gets_unique_suffix(self, mock_verify):
        User.objects.create_user(username='clash', email='other@example.com',
                                 password='test1234')
        mock_verify.return_value = {'email': 'clash@example.com',
                                    'first_name': '', 'last_name': ''}
        resp = self.client.post(self.google_url, {'token': 'valid-google-token'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='clash@example.com')
                        .exclude(username='clash').exists())


class SocialTokenVerificationTest(TestCase):
    """Guards on verify_* themselves - the checks that stop a token minted for
    somebody else's app being replayed against ours."""

    @override_settings(GOOGLE_CLIENT_ID='')
    def test_google_unconfigured_is_rejected_not_silently_allowed(self):
        with self.assertRaises(SocialAuthError):
            verify_google_token('anything')

    def test_google_empty_token_rejected(self):
        with self.assertRaises(SocialAuthError):
            verify_google_token('')

    @override_settings(FACEBOOK_APP_ID='123', FACEBOOK_APP_SECRET='shh')
    @patch('requests.get')
    def test_facebook_token_for_another_app_is_rejected(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data': {'is_valid': True, 'app_id': '999999'}}
        with self.assertRaises(SocialAuthError):
            verify_facebook_token('token-from-another-app')

    @override_settings(FACEBOOK_APP_ID='123', FACEBOOK_APP_SECRET='shh')
    @patch('requests.get')
    def test_facebook_invalid_token_rejected(self, mock_get):
        mock_get.return_value.json.return_value = {'data': {'is_valid': False}}
        with self.assertRaises(SocialAuthError):
            verify_facebook_token('expired')


class OTPAbuseProtectionTest(TestCase):
    """The send endpoint is AllowAny and sends real mail, so it carries two
    independent limits: a per-email cooldown and a per-IP throttle."""

    def setUp(self):
        self.client = APIClient()
        self.send_url = '/api/auth/otp/send/'
        cache.clear()

    def test_resend_within_cooldown_is_rejected(self):
        first = self.client.post(self.send_url, {
            'email': 'cooldown@example.com', 'purpose': 'email_verification'})
        self.assertEqual(first.status_code, status.HTTP_200_OK)

        second = self.client.post(self.send_url, {
            'email': 'cooldown@example.com', 'purpose': 'email_verification'})
        self.assertEqual(second.status_code, 429)
        self.assertIn('wait', str(second.data).lower())
        # The blocked request must not have sent a second mail.
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(OTP_RESEND_COOLDOWN_SECONDS=0)
    def test_ip_throttle_blocks_after_rate_limit(self):
        # Cooldown disabled and each address used once, so only the per-IP
        # throttle (5/hour) can stop these.
        statuses = [
            self.client.post(self.send_url, {
                'email': f'flood{i}@example.com', 'purpose': 'email_verification'}).status_code
            for i in range(6)
        ]
        self.assertEqual(statuses[:5], [status.HTTP_200_OK] * 5)
        self.assertEqual(statuses[5], 429)
        self.assertEqual(len(mail.outbox), 5)
