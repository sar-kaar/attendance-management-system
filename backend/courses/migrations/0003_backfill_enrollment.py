# Data migration: backfill Enrollment rows from existing attendance history.
# Every distinct (student, course) pair already in attendance_attendance
# gets an active Enrollment row, else old data fails new validate() check
# in AttendanceSerializer. Hand-written same reason as 0002 (no exec tool).
# Irreversible by design (reverse is no-op) — backfilled rows are inferred,
# not authoritative; don't auto-delete on rollback.

from django.db import migrations


def backfill_enrollments(apps, schema_editor):
    Attendance = apps.get_model('attendance', 'Attendance')
    Enrollment = apps.get_model('courses', 'Enrollment')

    seen = set()
    for student_id, course_id in Attendance.objects.values_list('student_id', 'course_id').distinct():
        key = (student_id, course_id)
        if key in seen:
            continue
        seen.add(key)
        Enrollment.objects.get_or_create(
            student_id=student_id,
            course_id=course_id,
            defaults={'is_active': True},
        )


def noop_reverse(apps, schema_editor):
    # Intentional no-op: backfilled rows are inferred from history, not
    # authoritative enrollment decisions. Don't delete on rollback.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_enrollment'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(backfill_enrollments, noop_reverse),
    ]
