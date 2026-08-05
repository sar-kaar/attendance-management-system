from django.conf import settings
from django.db import models

from courses.models import Course
from students.models import Student


class ECAActivity(models.Model):
    class Category(models.TextChoices):
        SPORTS = 'sports', 'Sports'
        CULTURAL = 'cultural', 'Cultural'
        ACADEMIC = 'academic', 'Academic'
        CLUB = 'club', 'Club'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    date = models.DateField()
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='eca_activities_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'name']

    def __str__(self):
        return f"{self.name} ({self.date})"


class AttendanceCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.label}"


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'
        LATE_PRESENT = 'lp', 'Late Present'
        ECA = 'eca', 'Extra-Curricular Activity'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)
    marked_by = models.CharField(max_length=20, default='manual')
    marked_by_user_id = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    eca_activity = models.ForeignKey(
        ECAActivity, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='attendance_records',
        help_text="Which activity this record's 'eca' status refers to, if any.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course', 'date']

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status}"
