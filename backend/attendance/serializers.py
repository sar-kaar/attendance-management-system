from rest_framework import serializers
from .models import Attendance, AttendanceCode
from courses.models import Enrollment


class AttendanceCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceCode
        fields = ['id', 'code', 'label', 'description', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_course_name(self, obj):
        return f"{obj.course.code} - {obj.course.name}"

    def validate(self, attrs):
        student = attrs.get('student') or getattr(self.instance, 'student', None)
        course = attrs.get('course') or getattr(self.instance, 'course', None)
        if student and course:
            is_enrolled = Enrollment.objects.filter(
                student=student, course=course, is_active=True
            ).exists()
            if not is_enrolled:
                raise serializers.ValidationError(
                    f"Student {student} is not enrolled in course {course}. "
                    "Attendance cannot be marked."
                )
        return attrs


class BulkAttendanceSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    date = serializers.DateField()
    records = serializers.ListField(child=serializers.DictField())

    def validate_records(self, value):
        for record in value:
            if 'student_id' not in record or 'status' not in record:
                raise serializers.ValidationError("Each record must have student_id and status")
        return value
