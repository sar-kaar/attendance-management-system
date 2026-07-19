from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone', 'first_name', 'last_name']
        read_only_fields = ['role']

    def create(self, validated_data):
        validated_data['role'] = 'student'
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    student_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'first_name', 'last_name', 'is_active', 'student_id']

    def get_student_id(self, obj):
        profile = getattr(obj, 'student_profile', None)
        return profile.student_id if profile else None


class AdminUserSerializer(serializers.ModelSerializer):
    """Used by admins to create/update faculty and student login accounts,
    optionally linking a student account to an existing Student record."""

    password = serializers.CharField(write_only=True, required=False, min_length=6)
    student_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    linked_student_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'role', 'phone',
            'first_name', 'last_name', 'is_active', 'student_id', 'linked_student_id',
        ]

    def get_linked_student_id(self, obj):
        profile = getattr(obj, 'student_profile', None)
        return profile.student_id if profile else None

    def _link_student(self, user, student_id):
        from students.models import Student
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            raise serializers.ValidationError(
                {'student_id': f'No student record found with ID {student_id}'}
            )
        student.user = user
        student.save(update_fields=['user'])

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        student_id = validated_data.pop('student_id', None)
        if not password:
            raise serializers.ValidationError({'password': 'Password is required to create a user.'})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if user.role == 'student' and student_id:
            self._link_student(user, student_id)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        student_id = validated_data.pop('student_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if instance.role == 'student' and student_id:
            self._link_student(instance, student_id)
        return instance
