from rest_framework import serializers
from .models import Course, Enrollment
from students.serializers import StudentSerializer


class CourseSerializer(serializers.ModelSerializer):
    faculty_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_faculty_name(self, obj):
        if obj.faculty:
            return f"{obj.faculty.first_name} {obj.faculty.last_name}".strip() or obj.faculty.username
        return None


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_name', 'course_name', 'enrolled_date', 'is_active']
        read_only_fields = ['enrolled_date']
        validators = []

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}".strip()

    def get_course_name(self, obj):
        return obj.course.name

    def validate(self, data):
        student = data.get('student') or getattr(self.instance, 'student', None)
        course = data.get('course') or getattr(self.instance, 'course', None)
        if student and course:
            existing = Enrollment.objects.filter(student=student, course=course, is_active=True)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("Student is already enrolled in this course.")
        return data
