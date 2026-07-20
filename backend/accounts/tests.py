from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail
from .models import User, OTP
from .services import OTPService


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
