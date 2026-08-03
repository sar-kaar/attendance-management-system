"""Shared attendance-percentage logic.

A single definition of "attended" is used everywhere a percentage is shown,
so a student can't see one number on their own dashboard and a different
one on the at-risk or faculty-performance reports:

- 'present', 'late', and 'lp' (late-present) all count as attended.
- 'absent' counts against the student.
- 'eca' (excused activity) is excluded from the denominator entirely: an
  excused day should neither help nor hurt the percentage.
"""
from django.db.models import Count, Q

ATTENDED_STATUSES = ('present', 'late', 'lp')


def attendance_counts(queryset):
    """Aggregate a queryset of Attendance rows into status counts plus a
    consistent attended / effective_total / percentage.
    """
    agg = queryset.aggregate(
        present=Count('id', filter=Q(status='present')),
        absent=Count('id', filter=Q(status='absent')),
        late=Count('id', filter=Q(status='late')),
        lp=Count('id', filter=Q(status='lp')),
        eca=Count('id', filter=Q(status='eca')),
    )
    attended = agg['present'] + agg['late'] + agg['lp']
    effective_total = attended + agg['absent']
    percentage = round((attended / effective_total * 100), 1) if effective_total > 0 else 0
    return {
        **agg,
        'attended': attended,
        'effective_total': effective_total,
        'percentage': percentage,
    }


def daily_attendance_percentages(queryset):
    """Per-date (attended, total, percentage), with 'eca' days excluded."""
    rows = (
        queryset.exclude(status='eca')
        .values('date')
        .annotate(
            attended=Count('id', filter=Q(status__in=ATTENDED_STATUSES)),
            total=Count('id'),
        )
    )
    results = []
    for row in rows:
        pct = round((row['attended'] / row['total'] * 100), 1) if row['total'] > 0 else 0
        results.append({
            'date': row['date'],
            'attended': row['attended'],
            'total': row['total'],
            'percentage': pct,
        })
    return results
