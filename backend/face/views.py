import json
import logging
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from students.models import Student
from courses.models import Enrollment
from attendance.models import Attendance

logger = logging.getLogger(__name__)


class FaceProcessingError(Exception):
    """Raised when an image can't be processed due to a real error (missing
    library, corrupt upload, etc.) as opposed to simply finding no face."""


def _decode_face_encoding(encoding_str):
    import numpy as np
    if not encoding_str:
        return None
    return np.array(json.loads(encoding_str))


def _encode_image(image_file):
    import io

    try:
        import face_recognition
    except ImportError:
        logger.exception('face_recognition library is not available')
        raise FaceProcessingError(
            'Face recognition is not available on the server right now.'
        )

    try:
        image_bytes = image_file.read()
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    except Exception:
        logger.exception('Failed to decode uploaded image')
        raise FaceProcessingError(
            'Could not read the uploaded image. Please upload a valid JPEG/PNG photo.'
        )

    try:
        encodings = face_recognition.face_encodings(image)
    except Exception:
        logger.exception('face_recognition failed while processing image')
        raise FaceProcessingError('Failed to process the image for face detection.')

    if not encodings:
        return None
    return encodings[0]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
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
        encoding = _encode_image(image)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if encoding is None:
        return Response(
            {'error': 'No face detected in the image. Please upload a clear photo with a visible face.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    student.face_encoding = json.dumps(encoding.tolist())
    student.save(update_fields=['face_encoding'])

    return Response({
        'message': f'Face registered for {student.first_name} {student.last_name}',
        'student_id': student.student_id,
        'encoding_dim': len(encoding),
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def recognize_face(request):
    image = request.FILES.get('image')
    tolerance = float(request.data.get('tolerance', 0.6))

    if not image:
        return Response(
            {'error': 'image is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        unknown_encoding = _encode_image(image)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if unknown_encoding is None:
        return Response(
            {'error': 'No face detected in the image'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    students_with_faces = Student.objects.filter(
        face_encoding__isnull=False
    ).exclude(face_encoding='')

    if not students_with_faces.exists():
        return Response(
            {'error': 'No students have registered their faces yet'},
            status=status.HTTP_404_NOT_FOUND,
        )

    best_match = None
    best_distance = float('inf')

    import face_recognition
    for student in students_with_faces:
        known_encoding = _decode_face_encoding(student.face_encoding)
        if known_encoding is None:
            continue
        distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
        if distance < best_distance:
            best_distance = distance
            best_match = student

    if best_match and best_distance <= tolerance:
        return Response({
            'matched': True,
            'student_id': best_match.student_id,
            'student_name': f'{best_match.first_name} {best_match.last_name}',
            'confidence': round(float(1 - best_distance), 4),
            'distance': round(float(best_distance), 4),
        })

    return Response({
        'matched': False,
        'confidence': 0,
        'message': 'No matching face found',
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
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
        unknown_encoding = _encode_image(image)
    except FaceProcessingError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if unknown_encoding is None:
        return Response(
            {'error': 'No face detected in the image'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    students_with_faces = Student.objects.filter(
        face_encoding__isnull=False, is_active=True
    ).exclude(face_encoding='')

    best_match = None
    best_distance = float('inf')

    import face_recognition
    for student in students_with_faces:
        known_encoding = _decode_face_encoding(student.face_encoding)
        if known_encoding is None:
            continue
        distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
        if distance < best_distance:
            best_distance = distance
            best_match = student

    if not best_match or best_distance > tolerance:
        return Response({
            'matched': False,
            'message': 'No matching student found',
            'marked': False,
        }, status=status.HTTP_200_OK)

    is_enrolled = Enrollment.objects.filter(
        student=best_match, course=course, is_active=True
    ).exists()
    if not is_enrolled:
        return Response({
            'matched': True,
            'student_id': best_match.student_id,
            'student_name': f'{best_match.first_name} {best_match.last_name}',
            'marked': False,
            'reason': 'Student is not enrolled in this course',
        }, status=status.HTTP_200_OK)

    attendance, created = Attendance.objects.update_or_create(
        student=best_match,
        course=course,
        date=date,
        defaults={
            'status': 'present',
            'marked_by': 'face_recognition',
        },
    )

    return Response({
        'matched': True,
        'student_id': best_match.student_id,
        'student_name': f'{best_match.first_name} {best_match.last_name}',
        'confidence': round(float(1 - best_distance), 4),
        'marked': True,
        'attendance_status': attendance.status,
        'new_record': created,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
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
