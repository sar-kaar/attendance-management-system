import csv
import io

from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Course, Enrollment
from notifications.services import send_to_user
from students.models import Student

from .models import Attendance, AttendanceCode, ECAActivity
from .serializers import (
    AttendanceCodeSerializer,
    AttendanceSerializer,
    BulkAttendanceSerializer,
    ECAActivitySerializer,
)
from .stats import attendance_counts


class IsAdminOrFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'faculty']


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-date', 'student__first_name')
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'my_attendance']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrFaculty()]

    def perform_create(self, serializer):
        record = serializer.save()
        self._notify_if_absent(record)

    def _notify_if_absent(self, record):
        """B7: push the student when they're marked absent. Best-effort — a push
        failure must never break attendance marking, so swallow everything."""
        if record.status != Attendance.Status.ABSENT:
            return
        target = getattr(record.student, 'user', None)
        if target is None:
            return
        try:
            send_to_user(
                target,
                title='Marked absent',
                body=f'You were marked absent in {record.course.name} on {record.date}.',
                data={'type': 'attendance', 'course_id': record.course_id, 'date': str(record.date)},
            )
        except Exception:  # noqa: BLE001 - notifications are non-critical
            pass

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'faculty':
            qs = qs.filter(course__faculty=user)
        elif user.role == 'student':
            profile = getattr(user, 'student_profile', None)
            qs = qs.filter(student=profile) if profile else qs.none()
        course_id = self.request.query_params.get('course')
        date = self.request.query_params.get('date')
        student_id = self.request.query_params.get('student')
        if course_id:
            qs = qs.filter(course_id=course_id)
        if date:
            qs = qs.filter(date=date)
        if student_id:
            qs = qs.filter(student_id=student_id)
        return qs

    @action(detail=False, methods=['post'])
    def mark_bulk(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        course = Course.objects.get(id=data['course_id'])
        if request.user.role == 'faculty' and course.faculty_id != request.user.id:
            return Response({'error': 'You are not assigned to this course'}, status=403)

        enrolled_students = {
            e.student.student_id: e.student
            for e in Enrollment.objects.filter(course=course, is_active=True).select_related('student')
        }

        created = []
        skipped = []
        for record in data['records']:
            sid = record['student_id']
            if sid not in enrolled_students:
                skipped.append({
                    'student_id': sid,
                    'reason': 'not enrolled in this course',
                })
                continue
            student = enrolled_students[sid]
            att, _ = Attendance.objects.update_or_create(
                student=student,
                course=course,
                date=data['date'],
                defaults={
                    'status': record['status'],
                    'marked_by': record.get('marked_by', 'manual'),
                    'marked_by_user_id': request.user.id,
                    'remarks': record.get('remarks', ''),
                }
            )
            created.append(att)

        response_data = AttendanceSerializer(created, many=True).data
        return Response(
            {'created': response_data, 'skipped': skipped},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'])
    def my_attendance(self, request):
        if request.user.role == 'student':
            profile = getattr(request.user, 'student_profile', None)
            if not profile:
                return Response({'error': 'No student record is linked to this account'}, status=404)
            qs = Attendance.objects.filter(student=profile).order_by('-date')
            return Response(AttendanceSerializer(qs, many=True).data)

        if request.user.role not in ['admin', 'faculty']:
            return Response({'error': 'Not permitted'}, status=403)
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id required'}, status=400)
        qs = Attendance.objects.filter(student_id=student_id).order_by('-date')
        if request.user.role == 'faculty':
            qs = qs.filter(course__faculty=request.user)
        return Response(AttendanceSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        # course/student filtering is already applied by get_queryset() below,
        # which reads the same query params.
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        qs = self.get_queryset()
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        counts = attendance_counts(qs)
        return Response({
            'total_records': counts['effective_total'],
            'present': counts['attended'],
            'absent': counts['absent'],
            'attendance_percentage': counts['percentage'],
        })

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        today = timezone.now().date()
        courses_qs = Course.objects.filter(is_active=True)
        attendance_qs = Attendance.objects.all()
        if request.user.role == 'faculty':
            courses_qs = courses_qs.filter(faculty=request.user)
            attendance_qs = attendance_qs.filter(course__faculty=request.user)
            total_students = Student.objects.filter(
                is_active=True, enrollments__course__faculty=request.user
            ).distinct().count()
        else:
            total_students = Student.objects.filter(is_active=True).count()
        total_courses = courses_qs.count()
        today_counts = attendance_counts(attendance_qs.filter(date=today))
        overall_counts = attendance_counts(attendance_qs)

        recent = attendance_qs.select_related('student', 'course').order_by('-date', '-created_at')[:10]

        return Response({
            'total_students': total_students,
            'total_courses': total_courses,
            'today': {
                'total': today_counts['effective_total'],
                'present': today_counts['attended'],
                'absent': today_counts['absent'],
                'percentage': today_counts['percentage'],
            },
            'overall': {
                'total': overall_counts['effective_total'],
                'present': overall_counts['attended'],
                'absent': overall_counts['absent'],
                'percentage': overall_counts['percentage'],
            },
            'recent_attendance': [
                {
                    'student': f"{a.student.first_name} {a.student.last_name}",
                    'course': a.course.code,
                    'date': str(a.date),
                    'status': a.status,
                }
                for a in recent
            ],
        })

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        course_id = request.query_params.get('course')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        qs = self.get_queryset()
        if course_id:
            qs = qs.filter(course_id=course_id)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow([
            'Student ID', 'Student Name', 'Course', 'Date',
            'Status', 'Marked By', 'Remarks'
        ])
        for att in qs.select_related('student', 'course'):
            writer.writerow([
                att.student.student_id,
                f"{att.student.first_name} {att.student.last_name}",
                att.course.code,
                str(att.date),
                att.status,
                att.marked_by,
                att.remarks,
            ])

        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
        return response

    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        course_id = request.query_params.get('course')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        qs = self.get_queryset()
        if course_id:
            qs = qs.filter(course_id=course_id)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Attendance Report", styles['Title']))
        elements.append(Spacer(1, 20))

        course_name = "All Courses"
        if course_id:
            try:
                course_name = Course.objects.get(id=course_id).__str__()
            except Course.DoesNotExist:
                pass
        elements.append(Paragraph(f"Course: {course_name}", styles['Normal']))
        if start_date:
            elements.append(Paragraph(f"From: {start_date}  To: {end_date or 'Present'}", styles['Normal']))
        elements.append(Spacer(1, 20))

        counts = attendance_counts(qs)
        elements.append(Paragraph(
            f"Total Records: {counts['effective_total']} | Present: {counts['attended']} | "
            f"Absent: {counts['absent']} | Attendance: {counts['percentage']}%",
            styles['Normal'],
        ))
        elements.append(Spacer(1, 20))

        data = [['Student ID', 'Name', 'Course', 'Date', 'Status']]
        for att in qs.select_related('student', 'course')[:100]:
            data.append([
                att.student.student_id,
                f"{att.student.first_name} {att.student.last_name}",
                att.course.code,
                str(att.date),
                att.status,
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'
        return response


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class ECAActivityViewSet(viewsets.ModelViewSet):
    queryset = ECAActivity.objects.all()
    serializer_class = ECAActivitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrFaculty()]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if category:
            qs = qs.filter(category=category)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AttendanceCodeViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceCodeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdmin()]

    def get_queryset(self):
        qs = AttendanceCode.objects.all()
        if self.action == 'list' and self.request.user.role != 'admin':
            qs = qs.filter(is_active=True)
        return qs
