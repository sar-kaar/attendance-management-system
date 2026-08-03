from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from students.models import MAX_STUDENT_AGE_YEARS, MIN_STUDENT_AGE_YEARS, Student


class DateOfBirthValidationTest(TestCase):
    """Date of birth must be a plausible date within a human lifespan: not in
    the future, and not so far back or so recent that no enrolled student
    could actually have it."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin_dob', password='test1234', role='admin')
        self.client.force_authenticate(user=self.admin)

    def _payload(self, dob):
        return {
            'first_name': 'Test', 'last_name': 'Student', 'email': 'dobtest@example.com',
            'student_id': 'MIT-2024-999', 'date_of_birth': dob.isoformat(),
        }

    def test_future_date_rejected(self):
        student = Student(first_name='A', last_name='B', email='a@b.com',
                          student_id='MIT-2024-001', date_of_birth=date.today() + timedelta(days=1))
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_too_far_in_past_rejected(self):
        too_old = date.today().replace(year=date.today().year - MAX_STUDENT_AGE_YEARS - 1)
        student = Student(first_name='A', last_name='B', email='a@b.com',
                          student_id='MIT-2024-001', date_of_birth=too_old)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_too_recent_rejected(self):
        too_young = date.today().replace(year=date.today().year - MIN_STUDENT_AGE_YEARS + 1)
        student = Student(first_name='A', last_name='B', email='a@b.com',
                          student_id='MIT-2024-001', date_of_birth=too_young)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_plausible_date_accepted(self):
        student = Student(first_name='A', last_name='B', email='a@b.com',
                          student_id='MIT-2024-001', date_of_birth=date(2000, 1, 1))
        student.full_clean()  # should not raise

    def test_api_rejects_future_dob(self):
        resp = self.client.post('/api/students/', self._payload(date.today() + timedelta(days=5)))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_of_birth', resp.data)

    def test_api_accepts_valid_dob(self):
        resp = self.client.post('/api/students/', self._payload(date(1999, 6, 15)))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
