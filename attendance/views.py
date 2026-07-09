from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Attendance
from .serializers import AttendanceSerializer, BulkAttendanceSerializer
from students.models import Student
from courses.models import Course


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
        created = []
        for record in data['records']:
            att, _ = Attendance.objects.update_or_create(
                student_id=record['student_id'],
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
        return Response(AttendanceSerializer(created, many=True).data, status=status.HTTP_201_CREATED)

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
