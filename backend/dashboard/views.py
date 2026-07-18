from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Coalesce
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance
from accounts.models import User
from .serializers import (
    ProgramSerializer, SectionSerializer, StudentSearchResultSerializer,
    StudentAttendanceBreakdownSerializer, AttendanceStatsSerializer,
    AtRiskStudentSerializer, FacultyPerformanceSerializer,
    ChronicLatecomerSerializer, IncompleteRecordSerializer,
)


class IsAdminOrFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'faculty']


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def program_list(request):
    programs = Student.objects.filter(is_active=True).values_list('program', flat=True).distinct().order_by('program')
    return Response(ProgramSerializer([{'program': p} for p in programs if p], many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def section_list(request):
    program = request.query_params.get('program')
    qs = Student.objects.filter(is_active=True)
    if program:
        qs = qs.filter(program=program)
    sections = qs.values_list('section', flat=True).distinct().order_by('section')
    return Response(SectionSerializer([{'section': s} for s in sections if s], many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def student_search(request):
    search = request.query_params.get('search', '').strip()
    program = request.query_params.get('program')
    section = request.query_params.get('section')
    qs = Student.objects.filter(is_active=True)
    if search:
        qs = qs.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(student_id__icontains=search) |
            Q(email__icontains=search)
        )
    if program:
        qs = qs.filter(program=program)
    if section:
        qs = qs.filter(section=section)
    return Response(StudentSearchResultSerializer(qs[:50], many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def student_attendance_breakdown(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    enrollments = Enrollment.objects.filter(student=student, is_active=True).select_related('course')
    courses_data = []
    for enrollment in enrollments:
        attendances = Attendance.objects.filter(student=student, course=enrollment.course)
        total = attendances.count()
        present = attendances.filter(status='present').count()
        absent = attendances.filter(status='absent').count()
        late = attendances.filter(status='late').count()
        lp = attendances.filter(status='lp').count()
        eca = attendances.filter(status='eca').count()
        percentage = round((present / total * 100), 1) if total > 0 else 0
        courses_data.append({
            'course_id': enrollment.course.id,
            'course_code': enrollment.course.code,
            'course_name': enrollment.course.name,
            'total_classes': total,
            'present': present,
            'absent': absent,
            'late': late,
            'late_present': lp,
            'eca': eca,
            'attendance_percentage': percentage,
        })

    return Response(StudentAttendanceBreakdownSerializer({
        'student_id': student.id,
        'student_name': f"{student.first_name} {student.last_name}",
        'courses': courses_data,
    }).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def attendance_stats(request):
    courses = Course.objects.filter(is_active=True).select_related('faculty')
    stats = []
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course, is_active=True)
        enrolled_count = enrollments.count()
        attendances = Attendance.objects.filter(course=course)
        classes_run = attendances.values('date').distinct().count()
        marked_count = attendances.count()
        present_count = attendances.filter(status='present').count()
        absent_count = attendances.filter(status='absent').count()
        late_count = attendances.filter(status='late').count()
        lp_count = attendances.filter(status='lp').count()
        eca_count = attendances.filter(status='eca').count()
        avg_headcount = round(marked_count / classes_run, 1) if classes_run > 0 else 0
        total_attended = present_count + late_count + lp_count
        overall_pct = round((total_attended / marked_count * 100), 1) if marked_count > 0 else 0

        if overall_pct >= 80:
            course_status = 'good'
        elif overall_pct >= 60:
            course_status = 'warning'
        elif marked_count > 0:
            course_status = 'critical'
        else:
            course_status = 'no_data'

        worst_day = None
        if classes_run > 0:
                day_stats = (
                    attendances.values('date')
                    .annotate(
                        present=Count('id', filter=Q(status='present')),
                        total=Count('id'),
                    )
                    .annotate(pct=F('present') * 100.0 / F('total'))
                    .order_by('pct')
                )
                if day_stats.exists():
                    worst = day_stats.first()
                    worst_day = f"{worst['date']} ({round(worst['pct'], 1)}%)"

        faculty_name = None
        if course.faculty:
            faculty_name = f"{course.faculty.first_name} {course.faculty.last_name}".strip() or course.faculty.username

        stats.append({
            'course_id': course.id,
            'course_code': course.code,
            'course_name': course.name,
            'faculty_name': faculty_name,
            'classes_run': classes_run,
            'enrolled_count': enrolled_count,
            'marked_count': marked_count,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'lp_count': lp_count,
            'eca_count': eca_count,
            'avg_headcount': avg_headcount,
            'overall_percentage': overall_pct,
            'status': course_status,
            'worst_day': worst_day,
        })

    return Response(AttendanceStatsSerializer(stats, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def at_risk_students(request):
    threshold = float(request.query_params.get('threshold', 60))
    courses = Course.objects.filter(is_active=True)
    at_risk = []
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course, is_active=True).select_related('student')
        for enrollment in enrollments:
            attendances = Attendance.objects.filter(student=enrollment.student, course=course)
            total = attendances.count()
            if total == 0:
                continue
            present = attendances.filter(status='present').count() + attendances.filter(status='late').count()
            pct = round((present / total * 100), 1)
            if pct < threshold:
                at_risk.append({
                    'student_id': enrollment.student.id,
                    'student_name': f"{enrollment.student.first_name} {enrollment.student.last_name}",
                    'student_code': enrollment.student.student_id,
                    'course_id': course.id,
                    'course_code': course.code,
                    'course_name': course.name,
                    'total_classes': total,
                    'present_count': present,
                    'attendance_percentage': pct,
                })
    at_risk.sort(key=lambda x: x['attendance_percentage'])
    return Response(AtRiskStudentSerializer(at_risk, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def faculty_performance(request):
    faculties = User.objects.filter(role='faculty', is_active=True)
    performance = []
    for faculty in faculties:
        courses = Course.objects.filter(faculty=faculty, is_active=True)
        subjects_count = courses.count()
        if subjects_count == 0:
            continue
        all_attendances = Attendance.objects.filter(course__in=courses)
        students_managed = Enrollment.objects.filter(
            course__in=courses, is_active=True
        ).values('student').distinct().count()
        total = all_attendances.count()
        present = all_attendances.filter(status='present').count() + all_attendances.filter(status='late').count()
        overall_pct = round((present / total * 100), 1) if total > 0 else 0

        worst_subject = None
        worst_pct = 101
        courses_data = []
        for course in courses:
            course_att = Attendance.objects.filter(course=course)
            c_total = course_att.count()
            c_present = course_att.filter(status='present').count() + course_att.filter(status='late').count()
            c_pct = round((c_present / c_total * 100), 1) if c_total > 0 else 0
            if c_pct < worst_pct:
                worst_pct = c_pct
                worst_subject = course.name
            courses_data.append({
                'course_id': course.id,
                'course_code': course.code,
                'course_name': course.name,
                'total_classes': c_total,
                'attendance_percentage': c_pct,
            })

        faculty_name = f"{faculty.first_name} {faculty.last_name}".strip() or faculty.username
        performance.append({
            'user_id': faculty.id,
            'faculty_name': faculty_name,
            'subjects_count': subjects_count,
            'students_managed': students_managed,
            'overall_percentage': overall_pct,
            'worst_subject': worst_subject,
            'courses': courses_data,
        })

    return Response(FacultyPerformanceSerializer(performance, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def chronic_latecomers(request):
    threshold = int(request.query_params.get('threshold', 3))
    courses = Course.objects.filter(is_active=True)
    latecomers = []
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course, is_active=True).select_related('student')
        for enrollment in enrollments:
            attendances = Attendance.objects.filter(
                student=enrollment.student, course=course
            )
            late_count = attendances.filter(status='late').count()
            lp_count = attendances.filter(status='lp').count()
            eca_count = attendances.filter(status='eca').count()
            total_late_related = late_count + lp_count + eca_count
            if total_late_related >= threshold:
                latecomers.append({
                    'student_id': enrollment.student.id,
                    'student_name': f"{enrollment.student.first_name} {enrollment.student.last_name}",
                    'student_code': enrollment.student.student_id,
                    'course_id': course.id,
                    'course_code': course.code,
                    'course_name': course.name,
                    'late_count': late_count,
                    'lp_count': lp_count,
                    'eca_count': eca_count,
                    'total_late_related': total_late_related,
                })
    latecomers.sort(key=lambda x: x['total_late_related'], reverse=True)
    return Response(ChronicLatecomerSerializer(latecomers, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def incomplete_records(request):
    courses = Course.objects.filter(is_active=True)
    incomplete = []
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course, is_active=True)
        enrolled_count = enrollments.count()
        if enrolled_count == 0:
            continue
        marked_dates = Attendance.objects.filter(course=course).values_list('date', flat=True).distinct()
        missing_dates = []
        for date in marked_dates:
            marked_students = Attendance.objects.filter(course=course, date=date).values_list('student_id', flat=True)
            unmarked = enrollments.exclude(student_id__in=marked_students)
            if unmarked.exists():
                missing_dates.append({
                    'date': str(date),
                    'unmarked_count': unmarked.count(),
                    'unmarked_students': [
                        f"{s.student.first_name} {s.student.last_name}"
                        for s in unmarked.select_related('student')[:5]
                    ],
                })
        total_marked = Attendance.objects.filter(course=course).count()
        if missing_dates:
            incomplete.append({
                'course_id': course.id,
                'course_code': course.code,
                'course_name': course.name,
                'enrolled_count': enrolled_count,
                'marked_count': total_marked,
                'unmarked_count': sum(d['unmarked_count'] for d in missing_dates),
                'missing_dates': missing_dates[:10],
            })
    return Response(IncompleteRecordSerializer(incomplete, many=True).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdminOrFaculty])
def master_data_import(request):
    dry_run = request.query_params.get('dry_run', 'false').lower() == 'true'
    data = request.data
    if not isinstance(data, list):
        return Response({'error': 'Expected a JSON array of records'}, status=400)

    created = 0
    updated = 0
    skipped = 0
    errors = []

    with transaction.atomic():
        for i, record in enumerate(data):
            try:
                student_id = record.get('student_id')
                course_code = record.get('course_code')
                first_name = record.get('first_name', '')
                last_name = record.get('last_name', '')
                email = record.get('email', '')
                program = record.get('program', '')
                section = record.get('section', '')

                if not student_id or not course_code:
                    errors.append({'index': i, 'error': 'student_id and course_code required'})
                    skipped += 1
                    continue

                course, _ = Course.objects.get_or_create(
                    code=course_code,
                    defaults={'name': record.get('course_name', course_code)},
                )
                student, student_created = Student.objects.update_or_create(
                    student_id=student_id,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email or f"{student_id}@placeholder.com",
                        'program': program,
                        'section': section,
                    },
                )
                if student_created:
                    created += 1
                else:
                    updated += 1

                Enrollment.objects.get_or_create(
                    student=student, course=course,
                    defaults={'is_active': True},
                )
            except Exception as e:
                errors.append({'index': i, 'error': str(e)})
                skipped += 1

        if dry_run:
            transaction.set_rollback(True)

    return Response({
        'created': created,
        'updated': updated,
        'skipped': skipped,
        'errors': errors,
        'dry_run': dry_run,
    })
