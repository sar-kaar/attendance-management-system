import csv
import io
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import Attendance, AttendanceCode
from .serializers import AttendanceSerializer, BulkAttendanceSerializer, AttendanceCodeSerializer
from students.models import Student
from courses.models import Course, Enrollment


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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'faculty':
            qs = qs.filter(course__faculty=self.request.user)
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
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id required'}, status=400)
        qs = Attendance.objects.filter(student_id=student_id).order_by('-date')
        return Response(AttendanceSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        course_id = request.query_params.get('course')
        student_id = request.query_params.get('student')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        qs = self.get_queryset()
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        total = qs.count()
        present = qs.filter(status='present').count() + qs.filter(status='late').count()
        absent = qs.filter(status='absent').count()
        percentage = round((present / total * 100), 1) if total > 0 else 0
        return Response({
            'total_records': total,
            'present': present,
            'absent': absent,
            'attendance_percentage': percentage,
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
        today_attendance = attendance_qs.filter(date=today)
        today_present = today_attendance.filter(status='present').count() + today_attendance.filter(status='late').count()
        today_absent = today_attendance.filter(status='absent').count()
        today_total = today_attendance.count()
        today_pct = round((today_present / today_total * 100), 1) if today_total > 0 else 0

        total_records = attendance_qs.count()
        overall_present = attendance_qs.filter(status='present').count() + attendance_qs.filter(status='late').count()
        overall_absent = attendance_qs.filter(status='absent').count()
        overall_pct = round((overall_present / total_records * 100), 1) if total_records > 0 else 0

        recent = attendance_qs.select_related('student', 'course').order_by('-date', '-created_at')[:10]

        return Response({
            'total_students': total_students,
            'total_courses': total_courses,
            'today': {
                'total': today_total,
                'present': today_present,
                'absent': today_absent,
                'percentage': today_pct,
            },
            'overall': {
                'total': total_records,
                'present': overall_present,
                'absent': overall_absent,
                'percentage': overall_pct,
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

        total = qs.count()
        present = qs.filter(status='present').count() + qs.filter(status='late').count()
        absent = qs.filter(status='absent').count()
        pct = round((present / total * 100), 1) if total > 0 else 0
        elements.append(Paragraph(f"Total Records: {total} | Present: {present} | Absent: {absent} | Attendance: {pct}%", styles['Normal']))
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
