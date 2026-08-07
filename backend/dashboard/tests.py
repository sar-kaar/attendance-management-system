from datetime import date, timedelta

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from attendance.models import Attendance
from courses.models import Course, Enrollment
from students.models import Student


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


class AttendancePercentageConsistencyTest(TestCase):
    """The same underlying attendance records must produce the same
    percentage everywhere it's shown: student breakdown, attendance-stats,
    at-risk, and faculty-performance all share one definition of "attended"
    (present + late + lp, with eca excluded from the denominator).
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin', password='testpass123', role='admin'
        )
        self.faculty = User.objects.create_user(
            username='faculty', password='testpass123', role='faculty'
        )
        self.student = Student.objects.create(
            first_name='John', last_name='Doe',
            email='john@test.com', student_id='STU001',
        )
        self.course = Course.objects.create(
            name='Software Engineering', code='CSE405', faculty=self.faculty
        )
        Enrollment.objects.create(student=self.student, course=self.course)

        # present, lp (counts as attended), eca (excluded), absent
        # -> attended=2, effective_total=3, percentage=66.7
        statuses = ['present', 'lp', 'eca', 'absent']
        for i, s in enumerate(statuses):
            Attendance.objects.create(
                student=self.student, course=self.course,
                date=date.today() - timedelta(days=i), status=s,
            )
        self.client.force_authenticate(user=self.admin)

    def test_percentages_match_across_dashboards(self):
        expected_pct = 66.7

        breakdown = self.client.get(f'/api/dashboard/students/{self.student.id}/attendance/')
        self.assertEqual(breakdown.data['courses'][0]['attendance_percentage'], expected_pct)
        self.assertEqual(breakdown.data['courses'][0]['total_classes'], 3)

        stats = self.client.get('/api/dashboard/attendance-stats/')
        course_stats = next(r for r in stats.data if r['course_id'] == self.course.id)
        self.assertEqual(course_stats['overall_percentage'], expected_pct)

        at_risk = self.client.get('/api/dashboard/at-risk/', {'threshold': 100})
        row = next(r for r in at_risk.data if r['student_id'] == self.student.id)
        self.assertEqual(row['attendance_percentage'], expected_pct)
        self.assertEqual(row['total_classes'], 3)

        perf = self.client.get('/api/dashboard/faculty-performance/')
        faculty_row = next(r for r in perf.data if r['user_id'] == self.faculty.id)
        self.assertEqual(faculty_row['overall_percentage'], expected_pct)
        self.assertEqual(faculty_row['courses'][0]['attendance_percentage'], expected_pct)
