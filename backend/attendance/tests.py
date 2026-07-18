from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import User
from students.models import Student
from courses.models import Course, Enrollment
from .models import Attendance


class AttendanceViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='admin', password='testpass123', role='admin'
        )
        self.faculty = User.objects.create_user(
            username='faculty', password='testpass123', role='faculty'
        )
        self.student_user = User.objects.create_user(
            username='student', password='testpass123', role='student'
        )

        self.student = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001'
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405', faculty=self.faculty
        )
        self.enrollment = Enrollment.objects.create(
            student=self.student, course=self.course
        )

        self.today = date.today()
        self.attendance_data = {
            'student': self.student.id,
            'course': self.course.id,
            'date': str(self.today),
            'status': 'present',
        }

    def test_attendance_list_requires_auth(self):
        response = self.client.get('/api/attendance/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_attendance_list_authenticated(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_create_attendance(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post('/api/attendance/', self.attendance_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_create_attendance(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.post('/api/attendance/', self.attendance_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_attendance(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/attendance/', self.attendance_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_attendance_unique_constraint(self):
        self.client.force_authenticate(user=self.admin)
        self.client.post('/api/attendance/', self.attendance_data)
        response = self.client.post('/api/attendance/', self.attendance_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BulkAttendanceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin', password='testpass123', role='admin'
        )
        self.student1 = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001'
        )
        self.student2 = Student.objects.create(
            first_name='Jane', last_name='Smith',
            email='jane@test.com', student_id='STU002'
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405'
        )
        self.enrollment1 = Enrollment.objects.create(
            student=self.student1, course=self.course
        )
        self.enrollment2 = Enrollment.objects.create(
            student=self.student2, course=self.course
        )
        self.client.force_authenticate(user=self.admin)

    def test_bulk_mark_all_enrolled(self):
        payload = {
            'course_id': self.course.id,
            'date': str(date.today()),
            'records': [
                {'student_id': 'STU001', 'status': 'present'},
                {'student_id': 'STU002', 'status': 'absent'},
            ]
        }
        response = self.client.post('/api/attendance/mark_bulk/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['created']), 2)
        self.assertEqual(len(response.data['skipped']), 0)

    def test_bulk_mark_skips_unenrolled(self):
        unenrolled = Student.objects.create(
            first_name='Bob', last_name='Lee',
            email='bob@test.com', student_id='STU003'
        )
        payload = {
            'course_id': self.course.id,
            'date': str(date.today()),
            'records': [
                {'student_id': 'STU001', 'status': 'present'},
                {'student_id': 'STU003', 'status': 'present'},
            ]
        }
        response = self.client.post('/api/attendance/mark_bulk/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['created']), 1)
        self.assertEqual(len(response.data['skipped']), 1)
        self.assertEqual(response.data['skipped'][0]['reason'], 'not enrolled in this course')


class EnrollmentValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin', password='testpass123', role='admin'
        )
        self.student = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001'
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405'
        )
        self.client.force_authenticate(user=self.admin)

    def test_cannot_mark_attendance_for_unenrolled_student(self):
        payload = {
            'student': self.student.id,
            'course': self.course.id,
            'date': str(date.today()),
            'status': 'present',
        }
        response = self.client.post('/api/attendance/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MyAttendanceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='student', password='testpass123', role='student'
        )
        self.student = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001'
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405'
        )
        Attendance.objects.create(
            student=self.student, course=self.course,
            date=date.today(), status='present'
        )
        self.client.force_authenticate(user=self.user)

    def test_my_attendance_requires_student_id(self):
        response = self.client.get('/api/attendance/my_attendance/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_my_attendance_returns_student_records(self):
        response = self.client.get(f'/api/attendance/my_attendance/?student_id={self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AttendanceReportTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin', password='testpass123', role='admin'
        )
        self.student = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001'
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405'
        )
        for i in range(5):
            Attendance.objects.create(
                student=self.student, course=self.course,
                date=date.today() - timedelta(days=i),
                status='present' if i < 3 else 'absent'
            )
        self.client.force_authenticate(user=self.admin)

    def test_report_returns_stats(self):
        response = self.client.get(f'/api/attendance/report/?course={self.course.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_records'], 5)
        self.assertEqual(response.data['present'], 3)
        self.assertEqual(response.data['absent'], 2)
        self.assertEqual(response.data['attendance_percentage'], 60.0)

    def test_report_filters_by_date_range(self):
        today = date.today()
        response = self.client.get(
            f'/api/attendance/report/?course={self.course.id}'
            f'&start_date={today - timedelta(days=2)}&end_date={today}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_records'], 3)
