from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from students.models import Student
from courses.models import Course, Enrollment


class FacultyScopingTest(TestCase):
    """Faculty must only ever see data for courses they are assigned to."""

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='admin', password='testpass123', role='admin'
        )
        self.faculty = User.objects.create_user(
            username='faculty', password='testpass123', role='faculty'
        )
        self.other_faculty = User.objects.create_user(
            username='other_faculty', password='testpass123', role='faculty'
        )

        # Student enrolled in self.faculty's course.
        self.own_student = Student.objects.create(
            first_name='Own', last_name='Student',
            email='own@test.com', student_id='STU001',
            program='CSE', section='A',
        )
        # Student enrolled only in other_faculty's course.
        self.other_student = Student.objects.create(
            first_name='Other', last_name='Student',
            email='other@test.com', student_id='STU002',
            program='CSE', section='A',
        )

        self.own_course = Course.objects.create(
            name='Software Engineering', code='CSE405', faculty=self.faculty
        )
        self.other_course = Course.objects.create(
            name='Databases', code='CSE302', faculty=self.other_faculty
        )

        Enrollment.objects.create(student=self.own_student, course=self.own_course)
        Enrollment.objects.create(student=self.other_student, course=self.other_course)

    def _search_ids(self, response):
        return {row['student_id'] for row in response.data}

    # --- student_search scoping ---

    def test_faculty_search_excludes_other_faculty_students(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.get('/api/dashboard/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = self._search_ids(response)
        self.assertIn('STU001', ids)
        self.assertNotIn('STU002', ids)

    def test_admin_search_sees_all_students(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/dashboard/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = self._search_ids(response)
        self.assertIn('STU001', ids)
        self.assertIn('STU002', ids)

    def test_faculty_cannot_reach_other_student_by_search_term(self):
        """Scoping must survive an explicit search for the other student."""
        self.client.force_authenticate(user=self.faculty)
        response = self.client.get('/api/dashboard/students/', {'search': 'STU002'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('STU002', self._search_ids(response))

    def test_faculty_search_does_not_duplicate_multi_enrolled_student(self):
        """A student in two of the same faculty's courses must appear once."""
        second_course = Course.objects.create(
            name='Algorithms', code='CSE301', faculty=self.faculty
        )
        Enrollment.objects.create(student=self.own_student, course=second_course)
        self.client.force_authenticate(user=self.faculty)
        response = self.client.get('/api/dashboard/students/')
        returned = [row['student_id'] for row in response.data]
        self.assertEqual(returned.count('STU001'), 1)

    # --- student_attendance_breakdown scoping ---

    def test_faculty_cannot_view_other_student_breakdown(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.get(
            f'/api/dashboard/students/{self.other_student.id}/attendance/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_faculty_can_view_own_student_breakdown(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.get(
            f'/api/dashboard/students/{self.own_student.id}/attendance/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- master_data_import is admin-only ---

    def test_faculty_cannot_import_master_data(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.post(
            '/api/dashboard/master-data/import/', [], format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_import_master_data(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            '/api/dashboard/master-data/import/', [], format='json'
        )
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- faculty_performance scoping ---

    def test_faculty_performance_shows_only_self(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.get('/api/dashboard/faculty-performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_performance_shows_all_faculty(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/dashboard/faculty-performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
