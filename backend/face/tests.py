import json
import io
import sys
import numpy as np
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance

try:
    import face_recognition  # noqa: F401
except ImportError:
    # face_recognition/dlib isn't installed in CI or every dev machine (heavy
    # native build, not required since face/views.py imports it lazily at
    # runtime). Stub it so @patch('face_recognition....') still resolves.
    sys.modules['face_recognition'] = MagicMock()

User = get_user_model()


def _mock_face_image():
    buf = io.BytesIO()
    buf.write(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)
    buf.seek(0)
    buf.name = 'test.png'
    return buf


def _fake_encoding():
    return np.random.rand(128).tolist()


class FaceRegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin_face', password='test1234', role='admin'
        )
        self.client.force_authenticate(user=self.admin)
        self.student = Student.objects.create(
            first_name='Face', last_name='Test', email='face@test.com', student_id='F001'
        )

    @patch('face.views._encode_image')
    def test_register_face_success(self, mock_encode):
        mock_encode.return_value = np.random.rand(128)
        resp = self.client.post('/api/face/register/', {
            'student_id': 'F001',
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('message', resp.data)
        self.student.refresh_from_db()
        self.assertIsNotNone(self.student.face_encoding)

    def test_register_face_missing_fields(self):
        resp = self.client.post('/api/face/register/', {}, format='multipart')
        self.assertEqual(resp.status_code, 400)

    def test_register_face_student_not_found(self):
        with patch('face.views._encode_image', return_value=np.random.rand(128)):
            resp = self.client.post('/api/face/register/', {
                'student_id': 'NONEXISTENT',
                'image': _mock_face_image(),
            }, format='multipart')
            self.assertEqual(resp.status_code, 404)

    @patch('face.views._encode_image')
    def test_register_face_no_face_detected(self, mock_encode):
        mock_encode.return_value = None
        resp = self.client.post('/api/face/register/', {
            'student_id': 'F001',
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('No face detected', str(resp.data))


class FaceRecognizeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin_rec', password='test1234', role='admin'
        )
        self.client.force_authenticate(user=self.admin)
        self.known_enc = np.random.rand(128)
        self.student = Student.objects.create(
            first_name='Rec', last_name='Test', email='rec@test.com', student_id='R001',
            face_encoding=json.dumps(self.known_enc.tolist()),
        )

    @patch('face_recognition.face_distance')
    @patch('face.views._encode_image')
    def test_recognize_match(self, mock_encode, mock_distance):
        mock_encode.return_value = self.known_enc.copy()
        mock_distance.return_value = np.array([0.3])
        resp = self.client.post('/api/face/recognize/', {
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['matched'])
        self.assertEqual(resp.data['student_id'], 'R001')

    @patch('face_recognition.face_distance')
    @patch('face.views._encode_image')
    def test_recognize_no_match(self, mock_encode, mock_distance):
        mock_encode.return_value = np.random.rand(128)
        mock_distance.return_value = np.array([0.9])
        resp = self.client.post('/api/face/recognize/', {
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.data['matched'])

    def test_recognize_no_image(self):
        resp = self.client.post('/api/face/recognize/', {}, format='multipart')
        self.assertEqual(resp.status_code, 400)

    @patch('face.views._encode_image')
    def test_recognize_no_face_in_image(self, mock_encode):
        mock_encode.return_value = None
        resp = self.client.post('/api/face/recognize/', {
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 400)

    def test_recognize_no_registered_faces(self):
        Student.objects.all().delete()
        with patch('face.views._encode_image', return_value=np.random.rand(128)):
            resp = self.client.post('/api/face/recognize/', {
                'image': _mock_face_image(),
            }, format='multipart')
            self.assertEqual(resp.status_code, 404)


class FaceAttendanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin_face_att', password='test1234', role='admin'
        )
        self.client.force_authenticate(user=self.admin)
        self.known_enc = np.random.rand(128)
        self.student = Student.objects.create(
            first_name='FA', last_name='Test', email='fa@test.com', student_id='FA001',
            face_encoding=json.dumps(self.known_enc.tolist()),
        )
        self.course = Course.objects.create(name='Test Course', code='TC01')
        Enrollment.objects.create(student=self.student, course=self.course)

    @patch('face_recognition.face_distance')
    @patch('face.views._encode_image')
    def test_mark_attendance_success(self, mock_encode, mock_distance):
        mock_encode.return_value = self.known_enc.copy()
        mock_distance.return_value = np.array([0.3])
        resp = self.client.post('/api/face/mark-attendance/', {
            'course_id': self.course.id,
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['marked'])
        self.assertTrue(Attendance.objects.filter(
            student=self.student, course=self.course
        ).exists())

    @patch('face_recognition.face_distance')
    @patch('face.views._encode_image')
    def test_mark_attendance_not_enrolled(self, mock_encode, mock_distance):
        new_enc = np.random.rand(128)
        # Remove face encoding from enrolled student so only unenrolled student matches
        self.student.face_encoding = None
        self.student.save(update_fields=['face_encoding'])
        Student.objects.create(
            first_name='Not', last_name='Enrolled', email='ne@test.com', student_id='NE001',
            face_encoding=json.dumps(new_enc.tolist()),
        )
        mock_encode.return_value = new_enc
        mock_distance.return_value = np.array([0.3])
        resp = self.client.post('/api/face/mark-attendance/', {
            'course_id': self.course.id,
            'image': _mock_face_image(),
        }, format='multipart')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['matched'])
        self.assertFalse(resp.data['marked'])

    def test_mark_attendance_missing_fields(self):
        resp = self.client.post('/api/face/mark-attendance/', {}, format='multipart')
        self.assertEqual(resp.status_code, 400)

    def test_mark_attendance_course_not_found(self):
        with patch('face.views._encode_image', return_value=np.random.rand(128)):
            resp = self.client.post('/api/face/mark-attendance/', {
                'course_id': 9999,
                'image': _mock_face_image(),
            }, format='multipart')
            self.assertEqual(resp.status_code, 404)


class RegisteredFacesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin_reg', password='test1234', role='admin'
        )
        self.client.force_authenticate(user=self.admin)

    def test_list_registered(self):
        Student.objects.create(
            first_name='Yes', last_name='Encoded', email='ye@test.com', student_id='YE1',
            face_encoding=json.dumps(_fake_encoding()),
        )
        Student.objects.create(
            first_name='No', last_name='Encoded', email='ne@test.com', student_id='NE1',
        )
        resp = self.client.get('/api/face/registered/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['students'][0]['student_id'], 'YE1')
