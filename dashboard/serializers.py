from rest_framework import serializers
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance
from accounts.models import User


class ProgramSerializer(serializers.Serializer):
    program = serializers.CharField()


class SectionSerializer(serializers.Serializer):
    section = serializers.CharField()


class StudentSearchResultSerializer(serializers.ModelSerializer):
    enrollments = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name',
            'email', 'program', 'section', 'is_active', 'enrollments',
        ]

    def get_enrollments(self, obj):
        enrollments = Enrollment.objects.filter(
            student=obj, is_active=True
        ).select_related('course')
        return [
            {'course_id': e.course.id, 'course_code': e.course.code, 'course_name': e.course.name}
            for e in enrollments
        ]


class StudentAttendanceBreakdownSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    courses = serializers.ListField()


class AttendanceStatsSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_code = serializers.CharField()
    course_name = serializers.CharField()
    faculty_name = serializers.CharField(allow_null=True)
    classes_run = serializers.IntegerField()
    enrolled_count = serializers.IntegerField()
    marked_count = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    late_count = serializers.IntegerField()
    lp_count = serializers.IntegerField()
    eca_count = serializers.IntegerField()
    avg_headcount = serializers.FloatField()
    overall_percentage = serializers.FloatField()
    status = serializers.CharField()
    worst_day = serializers.CharField(allow_null=True)


class AtRiskStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    student_code = serializers.CharField()
    course_id = serializers.IntegerField()
    course_code = serializers.CharField()
    course_name = serializers.CharField()
    total_classes = serializers.IntegerField()
    present_count = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()


class FacultyPerformanceSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    faculty_name = serializers.CharField()
    subjects_count = serializers.IntegerField()
    students_managed = serializers.IntegerField()
    overall_percentage = serializers.FloatField()
    worst_subject = serializers.CharField(allow_null=True)
    courses = serializers.ListField()


class ChronicLatecomerSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    student_code = serializers.CharField()
    course_id = serializers.IntegerField()
    course_code = serializers.CharField()
    course_name = serializers.CharField()
    late_count = serializers.IntegerField()
    lp_count = serializers.IntegerField()
    eca_count = serializers.IntegerField()
    total_late_related = serializers.IntegerField()


class IncompleteRecordSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_code = serializers.CharField()
    course_name = serializers.CharField()
    enrolled_count = serializers.IntegerField()
    marked_count = serializers.IntegerField()
    unmarked_count = serializers.IntegerField()
    missing_dates = serializers.ListField()


class MasterDataImportResultSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    skipped = serializers.IntegerField()
    errors = serializers.ListField()
