import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance

User = get_user_model()


class FullFlowIntegrationTest(TestCase):
    """End-to-end test: register user -> create student -> create course ->
       enroll -> mark attendance -> check report -> export."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='flow_admin', password='test1234', role='admin'
        )
        self.faculty = User.objects.create_user(
            username='flow_faculty', password='test1234', role='faculty',
            first_name='Flow', last_name='Faculty'
        )
        self.student_user = User.objects.create_user(
            username='flow_student', password='test1234', role='student',
            first_name='Flow', last_name='Student'
        )

    def test_full_admin_flow(self):
        self.client.force_authenticate(user=self.admin)

        # 1. Get profile
        resp = self.client.get('/api/auth/me/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['role'], 'admin')

        # 2. Create student
        resp = self.client.post('/api/students/', {
            'first_name': 'Integration', 'last_name': 'Test',
            'email': 'int@test.com', 'student_id': 'INT001'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        student_id = resp.data['id']

        # 3. Create course
        resp = self.client.post('/api/courses/', {
            'name': 'Integration Course', 'code': 'INT101',
            'credits': 3, 'faculty': self.faculty.id
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        course_id = resp.data['id']

        # 4. Enroll student
        resp = self.client.post('/api/enrollments/', {
            'student': student_id, 'course': course_id
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        enrollment_id = resp.data['id']

        # 5. Mark attendance (single)
        resp = self.client.post('/api/attendance/', {
            'student': student_id, 'course': course_id,
            'date': '2026-07-14', 'status': 'present'
        }, format='json')
        self.assertEqual(resp.status_code, 201)

        # 6. Mark attendance (bulk)
        resp = self.client.post('/api/attendance/mark_bulk/', {
            'course_id': course_id, 'date': '2026-07-15',
            'records': [{'student_id': 'INT001', 'status': 'late'}]
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(resp.data['created']), 1)

        # 7. Check report
        resp = self.client.get(f'/api/attendance/report/?course={course_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['total_records'], 2)
        self.assertGreater(resp.data['attendance_percentage'], 0)

        # 8. Check dashboard
        resp = self.client.get('/api/attendance/dashboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['total_students'], 1)
        self.assertEqual(resp.data['total_courses'], 1)

        # 9. Export CSV
        resp = self.client.get(f'/api/attendance/export_csv/?course={course_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('text/csv', resp['Content-Type'])

        # 10. Export PDF
        resp = self.client.get(f'/api/attendance/export_pdf/?course={course_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/pdf', resp['Content-Type'])

        # 11. Deactivate enrollment
        resp = self.client.patch(f'/api/enrollments/{enrollment_id}/', {
            'is_active': False
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.data['is_active'])

        # 12. Verify attendance record exists
        self.assertEqual(Attendance.objects.count(), 2)


class FacultyFlowIntegrationTest(TestCase):
    """Faculty can create students, enroll, mark attendance."""

    def setUp(self):
        self.client = APIClient()
        self.faculty = User.objects.create_user(
            username='fac_flow', password='test1234', role='faculty'
        )
        self.client.force_authenticate(user=self.faculty)

    def test_faculty_flow(self):
        # Create student
        resp = self.client.post('/api/students/', {
            'first_name': 'Fac', 'last_name': 'Student',
            'email': 'fs@test.com', 'student_id': 'FS001'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        sid = resp.data['id']

        # Create course
        resp = self.client.post('/api/courses/', {
            'name': 'Fac Course', 'code': 'FC01'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        cid = resp.data['id']

        # Enroll
        resp = self.client.post('/api/enrollments/', {
            'student': sid, 'course': cid
        }, format='json')
        self.assertEqual(resp.status_code, 201)

        # Bulk mark
        resp = self.client.post('/api/attendance/mark_bulk/', {
            'course_id': cid, 'date': '2026-07-14',
            'records': [{'student_id': 'FS001', 'status': 'present'}]
        }, format='json')
        self.assertEqual(resp.status_code, 201)

        # Report
        resp = self.client.get(f'/api/attendance/report/?course={cid}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['total_records'], 1)


class StudentFlowIntegrationTest(TestCase):
    """Student can view own attendance but cannot create records."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='stu_admin', password='test1234', role='admin'
        )
        self.student_user = User.objects.create_user(
            username='stu_user', password='test1234', role='student'
        )
        self.student = Student.objects.create(
            first_name='Stu', last_name='Dent', email='sd@test.com', student_id='SD001'
        )
        self.course = Course.objects.create(name='SD Course', code='SD01')
        Enrollment.objects.create(student=self.student, course=self.course)
        Attendance.objects.create(
            student=self.student, course=self.course,
            date='2026-07-14', status='present'
        )

    def test_student_view_own_attendance(self):
        self.client.force_authenticate(user=self.student_user)
        resp = self.client.get(f'/api/attendance/my_attendance/?student_id={self.student.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_student_cannot_create_attendance(self):
        self.client.force_authenticate(user=self.student_user)
        resp = self.client.post('/api/attendance/', {
            'student': self.student.id, 'course': self.course.id,
            'date': '2026-07-15', 'status': 'present'
        }, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_student_cannot_enroll(self):
        self.client.force_authenticate(user=self.student_user)
        resp = self.client.post('/api/enrollments/', {
            'student': self.student.id, 'course': self.course.id
        }, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_student_cannot_create_student(self):
        self.client.force_authenticate(user=self.student_user)
        resp = self.client.post('/api/students/', {
            'first_name': 'No', 'last_name': 'Access',
            'email': 'na@test.com', 'student_id': 'NA001'
        }, format='json')
        self.assertEqual(resp.status_code, 403)


class AuthFlowIntegrationTest(TestCase):
    """Register -> login -> access -> refresh -> logout flow."""

    def setUp(self):
        self.client = APIClient()

    def test_register_login_me_refresh(self):
        # Register
        resp = self.client.post('/api/auth/register/', {
            'username': 'new_user', 'email': 'new@test.com',
            'password': 'test1234', 'first_name': 'New', 'last_name': 'User'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['role'], 'student')

        # Login
        resp = self.client.post('/api/auth/login/', {
            'username': 'new_user', 'password': 'test1234'
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        access = resp.data['access']
        refresh = resp.data['refresh']

        # Access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        resp = self.client.get('/api/auth/me/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['username'], 'new_user')

        # Refresh token
        resp = self.client.post('/api/auth/token/refresh/', {
            'refresh': refresh
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)

    def test_wrong_password(self):
        resp = self.client.post('/api/auth/login/', {
            'username': 'admin', 'password': 'wrong'
        }, format='json')
        self.assertEqual(resp.status_code, 401)

    def test_unauthenticated_access(self):
        resp = self.client.get('/api/students/')
        self.assertEqual(resp.status_code, 401)

    def test_register_prevents_admin_role(self):
        resp = self.client.post('/api/auth/register/', {
            'username': 'evil', 'email': 'evil@test.com',
            'password': 'test1234', 'role': 'admin'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['role'], 'student')


class EnrollmentValidationIntegrationTest(TestCase):
    """Enrollment: duplicate prevention, deactivation, reactivation."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='enr_admin', password='test1234', role='admin'
        )
        self.client.force_authenticate(user=self.admin)
        self.student = Student.objects.create(
            first_name='E', last_name='Student', email='es@test.com', student_id='ES001'
        )
        self.course = Course.objects.create(name='E Course', code='EC01')

    def test_duplicate_enrollment_blocked(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        resp = self.client.post('/api/enrollments/', {
            'student': self.student.id, 'course': self.course.id
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_deactivate_enables_re_enrollment(self):
        enr = Enrollment.objects.create(student=self.student, course=self.course)
        # Deactivate
        resp = self.client.patch(f'/api/enrollments/{enr.id}/', {
            'is_active': False
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        # Re-enroll should now work
        resp = self.client.post('/api/enrollments/', {
            'student': self.student.id, 'course': self.course.id
        }, format='json')
        self.assertEqual(resp.status_code, 201)


class AttendanceWorkflowIntegrationTest(TestCase):
    """Attendance: bulk mark with enrolled/unenrolled, filters, export."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='att_admin', password='test1234', role='admin'
        )
        self.client.force_authenticate(user=self.admin)

        self.s1 = Student.objects.create(
            first_name='A', last_name='One', email='a1@test.com', student_id='A001'
        )
        self.s2 = Student.objects.create(
            first_name='B', last_name='Two', email='b2@test.com', student_id='A002'
        )
        self.course = Course.objects.create(name='Att Course', code='AC01')
        Enrollment.objects.create(student=self.s1, course=self.course)
        # s2 NOT enrolled

    def test_bulk_with_unenrolled(self):
        resp = self.client.post('/api/attendance/mark_bulk/', {
            'course_id': self.course.id, 'date': '2026-07-14',
            'records': [
                {'student_id': self.s1.student_id, 'status': 'present'},
                {'student_id': self.s2.student_id, 'status': 'present'},
            ]
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(resp.data['created']), 1)
        self.assertEqual(len(resp.data['skipped']), 1)
        self.assertEqual(resp.data['skipped'][0]['reason'], 'not enrolled in this course')

    def test_attendance_filter_by_date(self):
        Attendance.objects.create(
            student=self.s1, course=self.course, date='2026-07-14', status='present'
        )
        Attendance.objects.create(
            student=self.s1, course=self.course, date='2026-07-15', status='absent'
        )
        resp = self.client.get('/api/attendance/?date=2026-07-14')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)

    def test_report_across_dates(self):
        Attendance.objects.create(
            student=self.s1, course=self.course, date='2026-07-14', status='present'
        )
        Attendance.objects.create(
            student=self.s1, course=self.course, date='2026-07-15', status='absent'
        )
        resp = self.client.get(f'/api/attendance/report/?course={self.course.id}')
        self.assertEqual(resp.data['total_records'], 2)
        self.assertEqual(resp.data['present'], 1)
        self.assertEqual(resp.data['absent'], 1)

    def test_csv_export_content(self):
        Attendance.objects.create(
            student=self.s1, course=self.course, date='2026-07-14', status='present'
        )
        resp = self.client.get(f'/api/attendance/export_csv/?course={self.course.id}')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn('Student ID', content)
        self.assertIn('A001', content)
