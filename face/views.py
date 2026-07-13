import json
import numpy as np
import face_recognition
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from students.models import Student
from courses.models import Enrollment
from attendance.models import Attendance


def _decode_face_encoding(encoding_str):
    if not encoding_str:
        return None
    return np.array(json.loads(encoding_str))


def _encode_image(image_file):
    try:
        import io
        image_bytes = image_file.read()
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return None
        return encodings[0]
    except Exception:
        return None


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

    encoding = _encode_image(image)
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

    unknown_encoding = _encode_image(image)
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

    unknown_encoding = _encode_image(image)
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
