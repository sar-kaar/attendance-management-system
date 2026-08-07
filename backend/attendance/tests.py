from datetime import date, timedelta

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from courses.models import Course, Enrollment
from students.models import Student

from .models import Attendance, ECAActivity


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

    def test_report_filters_by_course(self):
        self.client.force_authenticate(user=self.admin)
        other_course = Course.objects.create(
            name='Data Structures', code='CSE201', faculty=self.faculty
        )
        Attendance.objects.create(
            student=self.student, course=self.course, date=self.today, status='present'
        )
        Attendance.objects.create(
            student=self.student, course=other_course, date=self.today, status='absent'
        )
        response = self.client.get(f'/api/attendance/report/?course={self.course.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_records'], 1)
        self.assertEqual(response.data['present'], 1)
        self.assertEqual(response.data['absent'], 0)

    def test_report_filters_by_student(self):
        self.client.force_authenticate(user=self.admin)
        other_student = Student.objects.create(
            first_name='Jane', last_name='Smith',
            email='jane@test.com', student_id='STU002'
        )
        Attendance.objects.create(
            student=self.student, course=self.course, date=self.today, status='present'
        )
        Attendance.objects.create(
            student=other_student, course=self.course, date=self.today, status='absent'
        )
        response = self.client.get(f'/api/attendance/report/?student={self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_records'], 1)
        self.assertEqual(response.data['present'], 1)
        self.assertEqual(response.data['absent'], 0)


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
        Student.objects.create(
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
            email='john@test.com', student_id='STU001',
            user=self.user,
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405'
        )
        Attendance.objects.create(
            student=self.student, course=self.course,
            date=date.today(), status='present'
        )

        # A second student, deliberately not linked to self.user.
        self.other_student = Student.objects.create(
            first_name='Jane', last_name='Roe',
            email='jane@test.com', student_id='STU002'
        )
        Attendance.objects.create(
            student=self.other_student, course=self.course,
            date=date.today(), status='absent'
        )

        self.client.force_authenticate(user=self.user)

    def test_student_gets_own_records_without_student_id(self):
        """A linked student needs no student_id — the profile resolves it."""
        response = self.client.get('/api/attendance/my_attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_read_another_students_records(self):
        """student_id must be ignored for students, not honoured."""
        response = self.client.get(
            f'/api/attendance/my_attendance/?student_id={self.other_student.id}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['student'], self.student.id)

    def test_unlinked_student_account_gets_404(self):
        orphan = User.objects.create_user(
            username='orphan', password='testpass123', role='student'
        )
        self.client.force_authenticate(user=orphan)
        response = self.client.get('/api/attendance/my_attendance/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_still_requires_student_id(self):
        admin = User.objects.create_user(
            username='ma_admin', password='testpass123', role='admin'
        )
        self.client.force_authenticate(user=admin)
        response = self.client.get('/api/attendance/my_attendance/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_read_any_student_records(self):
        admin = User.objects.create_user(
            username='ma_admin2', password='testpass123', role='admin'
        )
        self.client.force_authenticate(user=admin)
        response = self.client.get(
            f'/api/attendance/my_attendance/?student_id={self.other_student.id}'
        )
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


class AttendanceCountsTest(TestCase):
    """Verifies the shared attendance-percentage policy: 'present', 'late',
    and 'lp' all count as attended; 'eca' is excluded from the denominator
    entirely; only 'absent' counts against the student.
    """

    def setUp(self):
        self.student = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001'
        )
        self.course = Course.objects.create(name='Software Engineering', code='CSE405')

    def _mark(self, statuses):
        for i, s in enumerate(statuses):
            Attendance.objects.create(
                student=self.student, course=self.course,
                date=date.today() - timedelta(days=i), status=s,
            )

    def test_late_present_counts_as_attended(self):
        from .stats import attendance_counts
        self._mark(['present', 'lp', 'lp', 'absent'])
        counts = attendance_counts(Attendance.objects.filter(course=self.course))
        # 3 attended (present + 2x lp) out of 4 effective records.
        self.assertEqual(counts['attended'], 3)
        self.assertEqual(counts['effective_total'], 4)
        self.assertEqual(counts['percentage'], 75.0)

    def test_eca_excluded_from_denominator(self):
        from .stats import attendance_counts
        self._mark(['present', 'eca', 'eca', 'absent'])
        counts = attendance_counts(Attendance.objects.filter(course=self.course))
        # eca days are dropped entirely: 1 attended out of 2 effective records,
        # not 1 out of 4.
        self.assertEqual(counts['attended'], 1)
        self.assertEqual(counts['effective_total'], 2)
        self.assertEqual(counts['percentage'], 50.0)

    def test_zero_effective_records_gives_zero_percent(self):
        from .stats import attendance_counts
        self._mark(['eca', 'eca'])
        counts = attendance_counts(Attendance.objects.filter(course=self.course))
        self.assertEqual(counts['effective_total'], 0)
        self.assertEqual(counts['percentage'], 0)

    def test_report_and_dashboard_endpoints_agree_with_lp_and_eca(self):
        """Same underlying data must produce the same percentage everywhere."""
        admin = User.objects.create_user(username='admin2', password='x', role='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=admin)
        self._mark(['present', 'lp', 'eca', 'absent'])

        report = self.client.get(f'/api/attendance/report/?course={self.course.id}')
        dashboard = self.client.get('/api/attendance/dashboard/')

        # present + lp = 2 attended, eca excluded, absent counts against ->
        # effective_total = 3, percentage = 2/3 = 66.7.
        self.assertEqual(report.data['attendance_percentage'], 66.7)
        self.assertEqual(dashboard.data['overall']['percentage'], 66.7)
        self.assertEqual(report.data['total_records'], dashboard.data['overall']['total'])
        self.assertEqual(report.data['present'], dashboard.data['overall']['present'])


class ECAActivityTest(TestCase):
    """GitHub #23 (US-12): ECA tracking needed a real backend model, not just
    the existing Attendance.Status.ECA flag - these lock in that model and
    its link back to attendance records."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='eca_admin', password='x', role='admin')
        self.faculty = User.objects.create_user(username='eca_faculty', password='x', role='faculty')
        self.student_user = User.objects.create_user(username='eca_student', password='x', role='student')
        self.student = Student.objects.create(
            first_name='Eca', last_name='Tester', email='eca@test.com', student_id='STU-ECA-1'
        )
        self.course = Course.objects.create(name='Chemistry', code='CHEM101', faculty=self.faculty)
        Enrollment.objects.create(student=self.student, course=self.course)
        self.today = date.today()

    def test_list_requires_auth(self):
        response = self.client.get('/api/attendance/eca-activities/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_cannot_create_activity(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post('/api/attendance/eca-activities/', {
            'name': 'Debate Club', 'category': 'club', 'date': str(self.today),
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_create_activity(self):
        self.client.force_authenticate(user=self.faculty)
        response = self.client.post('/api/attendance/eca-activities/', {
            'name': 'Inter-college Football', 'category': 'sports', 'date': str(self.today),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        activity = ECAActivity.objects.get(id=response.data['id'])
        self.assertEqual(activity.created_by, self.faculty)

    def test_attendance_can_reference_activity_only_with_eca_status(self):
        activity = ECAActivity.objects.create(name='Science Fair', category='academic', date=self.today)
        self.client.force_authenticate(user=self.admin)

        ok = self.client.post('/api/attendance/', {
            'student': self.student.id, 'course': self.course.id, 'date': str(self.today),
            'status': 'eca', 'eca_activity': activity.id,
        })
        self.assertEqual(ok.status_code, status.HTTP_201_CREATED, ok.data)

        rejected = self.client.post('/api/attendance/', {
            'student': self.student.id, 'course': self.course.id,
            'date': str(self.today + timedelta(days=1)),
            'status': 'present', 'eca_activity': activity.id,
        })
        self.assertEqual(rejected.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('eca_activity', rejected.data)

    def test_dashboard_eca_tracking_endpoint(self):
        activity = ECAActivity.objects.create(name='Debate Finals', category='club', date=self.today)
        Attendance.objects.create(
            student=self.student, course=self.course, date=self.today,
            status='eca', eca_activity=activity,
        )
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/dashboard/eca/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        row = response.data[0]
        self.assertEqual(row['student_id'], self.student.id)
        self.assertEqual(row['activity_count'], 1)
        self.assertEqual(row['activities'][0]['activity_name'], 'Debate Finals')

    def test_dashboard_eca_tracking_excludes_students_with_no_activities(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/dashboard/eca/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class AbsenceNotificationTest(TestCase):
    """B7: marking a student absent pushes to their linked user; other statuses don't."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin2', password='testpass123', role='admin')
        self.student_user = User.objects.create_user(
            username='studentb', password='testpass123', role='student')
        self.faculty = User.objects.create_user(
            username='facultyb', password='testpass123', role='faculty')
        self.student = Student.objects.create(
            first_name='Jane', last_name='Roe', email='jane@test.com',
            student_id='STU900', user=self.student_user)
        self.course = Course.objects.create(
            name='Networks', code='CSE500', faculty=self.faculty)
        Enrollment.objects.create(student=self.student, course=self.course)
        self.client.force_authenticate(user=self.admin)

    def _mark(self, status_value):
        return self.client.post('/api/attendance/', {
            'student': self.student.id, 'course': self.course.id,
            'date': str(date.today()), 'status': status_value})

    def test_absent_triggers_push_to_linked_user(self):
        from unittest.mock import patch
        with patch('attendance.views.send_to_user') as mock_send:
            resp = self._mark('absent')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args.args[0], self.student_user)

    def test_present_does_not_trigger_push(self):
        from unittest.mock import patch
        with patch('attendance.views.send_to_user') as mock_send:
            self._mark('present')
        mock_send.assert_not_called()

    def test_push_failure_does_not_break_marking(self):
        from unittest.mock import patch
        with patch('attendance.views.send_to_user', side_effect=RuntimeError('boom')):
            resp = self._mark('absent')
        # Attendance still recorded despite the push blowing up.
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Attendance.objects.filter(student=self.student, status='absent').exists())
