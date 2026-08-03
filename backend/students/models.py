from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from accounts.models import User, phone_validator

student_id_validator = RegexValidator(
    regex=r'^MIT-\d{4}-\d{3}$',
    message='Student ID must look like MIT-2024-001 (MIT-YYYY-NNN).',
)

MIN_STUDENT_AGE_YEARS = 10
MAX_STUDENT_AGE_YEARS = 100


def validate_date_of_birth(value):
    """A date-of-birth is meaningless outside a plausible human lifespan
    anchored to today - reject future dates (an unborn student) and dates so
    far back or so recent that they can't belong to an enrolled student."""
    today = date.today()
    if value > today:
        raise ValidationError('Date of birth cannot be in the future.')

    age_years = (today - value).days / 365.25
    if age_years > MAX_STUDENT_AGE_YEARS:
        raise ValidationError(
            f'Date of birth is more than {MAX_STUDENT_AGE_YEARS} years ago - please check it.'
        )
    if age_years < MIN_STUDENT_AGE_YEARS:
        raise ValidationError(
            f'Date of birth means an age under {MIN_STUDENT_AGE_YEARS} years - please check it.'
        )


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True, validators=[student_id_validator])
    phone = models.CharField(max_length=10, blank=True, validators=[phone_validator])
    date_of_birth = models.DateField(null=True, blank=True, validators=[validate_date_of_birth])
    address = models.TextField(blank=True)
    program = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=100, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    face_encoding = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
