from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User

from .models import Device
from .services import send_to_user


class DeviceRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='dev', email='dev@example.com', password='devpass123', role='student',
        )
        self.other = User.objects.create_user(
            username='other', email='other@example.com', password='otherpass123', role='student',
        )
        self.client.force_authenticate(self.user)

    def test_register_creates_device(self):
        resp = self.client.post('/api/devices/register/', {'token': 'tok-1', 'platform': 'android'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Device.objects.filter(user=self.user, token='tok-1').count(), 1)

    def test_register_is_idempotent(self):
        self.client.post('/api/devices/register/', {'token': 'tok-1', 'platform': 'android'})
        self.client.post('/api/devices/register/', {'token': 'tok-1', 'platform': 'ios'})
        devices = Device.objects.filter(token='tok-1')
        self.assertEqual(devices.count(), 1)
        self.assertEqual(devices.first().platform, 'ios')  # updated, not duplicated

    def test_register_repoints_token_to_new_user(self):
        # Same physical token later used by a different account re-points ownership.
        self.client.post('/api/devices/register/', {'token': 'shared', 'platform': 'android'})
        self.client.force_authenticate(self.other)
        self.client.post('/api/devices/register/', {'token': 'shared', 'platform': 'android'})
        self.assertEqual(Device.objects.filter(token='shared').count(), 1)
        self.assertEqual(Device.objects.get(token='shared').user, self.other)

    def test_register_requires_auth(self):
        self.client.force_authenticate(None)
        resp = self.client.post('/api/devices/register/', {'token': 'x', 'platform': 'ios'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_rejects_bad_platform(self):
        resp = self.client.post('/api/devices/register/', {'token': 'x', 'platform': 'nokia'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unregister_removes_own_device(self):
        self.client.post('/api/devices/register/', {'token': 'tok-1', 'platform': 'android'})
        resp = self.client.post('/api/devices/unregister/', {'token': 'tok-1'})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(token='tok-1').exists())

    def test_unregister_cannot_touch_other_users_device(self):
        Device.objects.create(user=self.other, token='theirs', platform='ios')
        resp = self.client.post('/api/devices/unregister/', {'token': 'theirs'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Device.objects.filter(token='theirs').exists())

    def test_list_returns_only_own_devices(self):
        self.client.post('/api/devices/register/', {'token': 'mine', 'platform': 'android'})
        Device.objects.create(user=self.other, token='theirs', platform='ios')
        resp = self.client.get('/api/devices/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        tokens = [d['token'] for d in resp.data]
        self.assertEqual(tokens, ['mine'])


class PushServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='pu', email='pu@example.com', password='pupass123', role='student',
        )

    @override_settings(PUSH_PROVIDER='console')
    def test_console_provider_counts_active_devices(self):
        Device.objects.create(user=self.user, token='a', platform='android')
        Device.objects.create(user=self.user, token='b', platform='ios')
        Device.objects.create(user=self.user, token='c', platform='web', is_active=False)
        # console provider sends nothing but reports the active fan-out count.
        self.assertEqual(send_to_user(self.user, 'Hi', 'Body'), 2)

    def test_no_devices_returns_zero(self):
        self.assertEqual(send_to_user(self.user, 'Hi', 'Body'), 0)
