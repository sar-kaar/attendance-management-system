from rest_framework import serializers

from courses.models import Enrollment

from .models import Attendance, AttendanceCode, ECAActivity


class AttendanceCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceCode
        fields = ['id', 'code', 'label', 'description', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class ECAActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ECAActivity
        fields = ['id', 'name', 'category', 'date', 'description', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    eca_activity_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_course_name(self, obj):
        return f"{obj.course.code} - {obj.course.name}"

    def get_eca_activity_name(self, obj):
        return obj.eca_activity.name if obj.eca_activity_id else None

    def validate(self, attrs):
        status_val = attrs.get('status') or getattr(self.instance, 'status', None)
        activity = attrs.get('eca_activity') if 'eca_activity' in attrs else getattr(
            self.instance, 'eca_activity', None
        )
        if activity and status_val != 'eca':
            raise serializers.ValidationError(
                {'eca_activity': "Only attendance records with status 'eca' can reference an activity."}
            )
        return self._validate_enrollment(attrs)

    def _validate_enrollment(self, attrs):
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
