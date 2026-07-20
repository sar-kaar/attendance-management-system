import json
import logging
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from students.models import Student
from courses.models import Enrollment
from attendance.models import Attendance
from .providers import provider_name, FaceProcessingError

logger = logging.getLogger(__name__)


class IsAdminOrFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in ['admin', 'faculty'])


# ---------------------------------------------------------------------------
# Provider seams
# ---------------------------------------------------------------------------

def _azure_client():
    from .providers import AzureFaceClient
    return AzureFaceClient()


def _persist_face(student, image_file):
    """Register a face image for *student*. Returns provider-specific metadata dict
    stored in student.face_encoding."""
    image_bytes = image_file.read()

    if provider_name() == 'azure':
        client = _azure_client()
        person_id = client.register(student, image_bytes)
        return {'azure_person_id': person_id}

    # local (dlib)
    import io
    try:
        import face_recognition
    except ImportError:
        raise FaceProcessingError(
            'Face recognition is not available on the server right now.'
        )
    try:
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    except Exception:
        logger.exception('Failed to decode uploaded image')
        raise FaceProcessingError(
            'Could not read the uploaded image. Please upload a valid JPEG/PNG photo.'
        )
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        return None
    return encodings[0].tolist()


def _extract_probe(image_file):
    """Return a provider-specific 'probe' from the uploaded image.

    local  → numpy-compatible list (128-d encoding)
    azure  → transient faceId string

    Returns (probe, None) on success or (None, error_response) on failure.
    """
    image_bytes = image_file.read()

    if provider_name() == 'azure':
        client = _azure_client()
        face_id = client.detect_face_id(image_bytes)
        if face_id is None:
            return None, (
                {'error': 'No face detected in the image'},
                status.HTTP_400_BAD_REQUEST,
            )
        return face_id, None

    # local (dlib)
    import io
    try:
        import face_recognition
    except ImportError:
        raise FaceProcessingError(
            'Face recognition is not available on the server right now.'
        )
    try:
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    except Exception:
        logger.exception('Failed to decode uploaded image')
        raise FaceProcessingError(
            'Could not read the uploaded image. Please upload a valid JPEG/PNG photo.'
        )
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        return None, (
            {'error': 'No face detected in the image. Please upload a clear photo with a visible face.'},
            status.HTTP_400_BAD_REQUEST,
        )
    return encodings[0], None


def _find_best_match(probe, students, tolerance=0.6):
    """Match *probe* against *students* and return (student, confidence) or (None, 0).

    For Azure, the confidence is Azure's own 0–1 score.
    For local, confidence = 1 - face_distance (so higher is better, matching Azure convention).
    """
    if provider_name() == 'azure':
        client = _azure_client()
        person_id, confidence = client.identify(probe, confidence_threshold=tolerance)
        if person_id is None:
            return None, 0.0
        for student in students:
            try:
                stored = json.loads(student.face_encoding or 'null')
                if isinstance(stored, dict) and stored.get('azure_person_id') == person_id:
                    return student, confidence
            except ValueError:
                continue
        return None, 0.0

    # local (dlib)
    import numpy as np
    import face_recognition

    best_match = None
    best_distance = float('inf')
    probe_array = np.array(probe)

    for student in students:
        encoding_str = student.face_encoding
        if not encoding_str:
            continue
        try:
            known = np.array(json.loads(encoding_str))
        except (ValueError, TypeError):
            continue
        distance = face_recognition.face_distance([known], probe_array)[0]
        if distance < best_distance:
            best_distance = distance
            best_match = student

    if best_match and best_distance <= tolerance:
        return best_match, round(float(1 - best_distance), 4)
    return None, 0.0


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def register_face(request):
    student_id = request.data.get('student_id')
    image = request.FILES.get('image')

    if not student_id or not image:
        return Response(
            {'error': 'student_id and image are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response(
            {'error': f'Student {student_id} not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = _persist_face(student, image)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if result is None:
        return Response(
            {'error': 'No face detected in the image. Please upload a clear photo with a visible face.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    student.face_encoding = json.dumps(result) if not isinstance(result, str) else json.dumps(result)
    student.save(update_fields=['face_encoding'])

    return Response({
        'message': f'Face registered for {student.first_name} {student.last_name}',
        'student_id': student.student_id,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def recognize_face(request):
    image = request.FILES.get('image')
    tolerance = float(request.data.get('tolerance', 0.6))

    if not image:
        return Response(
            {'error': 'image is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        probe, err = _extract_probe(image)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if err:
        return Response(err[0], status=err[1])

    students_with_faces = Student.objects.filter(
        face_encoding__isnull=False
    ).exclude(face_encoding='')

    if not students_with_faces.exists():
        return Response(
            {'error': 'No students have registered their faces yet'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        match, confidence = _find_best_match(probe, students_with_faces, tolerance)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if match:
        return Response({
            'matched': True,
            'student_id': match.student_id,
            'student_name': f'{match.first_name} {match.last_name}',
            'confidence': confidence,
        })

    return Response({
        'matched': False,
        'confidence': 0,
        'message': 'No matching face found',
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def mark_attendance_by_face(request):
    course_id = request.data.get('course_id')
    image = request.FILES.get('image')
    tolerance = float(request.data.get('tolerance', 0.6))
    date = request.data.get('date', str(timezone.now().date()))

    if not course_id or not image:
        return Response(
            {'error': 'course_id and image are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        from courses.models import Course
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(
            {'error': f'Course {course_id} not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.user.role == 'faculty' and course.faculty_id != request.user.id:
        return Response(
            {'error': 'You are not assigned to this course'},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        probe, err = _extract_probe(image)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if err:
        return Response(err[0], status=err[1])

    students_with_faces = Student.objects.filter(
        face_encoding__isnull=False, is_active=True
    ).exclude(face_encoding='')

    try:
        match, confidence = _find_best_match(probe, students_with_faces, tolerance)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not match:
        return Response({
            'matched': False,
            'message': 'No matching student found',
            'marked': False,
        }, status=status.HTTP_200_OK)

    is_enrolled = Enrollment.objects.filter(
        student=match, course=course, is_active=True
    ).exists()
    if not is_enrolled:
        return Response({
            'matched': True,
            'student_id': match.student_id,
            'student_name': f'{match.first_name} {match.last_name}',
            'marked': False,
            'reason': 'Student is not enrolled in this course',
        }, status=status.HTTP_200_OK)

    attendance, created = Attendance.objects.update_or_create(
        student=match,
        course=course,
        date=date,
        defaults={
            'status': 'present',
            'marked_by': 'face_recognition',
        },
    )

    return Response({
        'matched': True,
        'student_id': match.student_id,
        'student_name': f'{match.first_name} {match.last_name}',
        'confidence': confidence,
        'marked': True,
        'attendance_status': attendance.status,
        'new_record': created,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def registered_faces(request):
    students = Student.objects.exclude(face_encoding__isnull=True).exclude(face_encoding='')
    data = [
        {
            'student_id': s.student_id,
            'name': f'{s.first_name} {s.last_name}',
            'face_registered': True,
        }
        for s in students
    ]
    return Response({
        'count': len(data),
        'students': data,
    })
