# ER Diagram — Attendance Management System

Built from verified `docs/database-schema.md` (Jul 10, Day 4). 5 tables, including `Enrollment` (added Jul 9, Day 3 — see Changelog).

## Diagram (Mermaid ERD)

```mermaid
erDiagram
    ACCOUNTS_USER {
        BigAutoField id PK
        CharField username UK
        EmailField email
        CharField password
        CharField first_name
        CharField last_name
        CharField role "admin|faculty|student"
        CharField phone
        ImageField profile_picture
        Boolean is_active
        Boolean is_staff
        Boolean is_superuser
        DateTime date_joined
    }

    STUDENTS_STUDENT {
        BigAutoField id PK
        CharField first_name
        CharField last_name
        EmailField email UK
        CharField student_id UK
        CharField phone
        DateField date_of_birth
        TextField address
        DateField enrollment_date
        Boolean is_active
        TextField face_encoding
        DateTime created_at
        DateTime updated_at
    }

    COURSES_COURSE {
        BigAutoField id PK
        CharField name
        CharField code UK
        TextField description
        Integer credits
        Integer faculty_id FK
        Boolean is_active
        DateTime created_at
        DateTime updated_at
    }

    ATTENDANCE_ATTENDANCE {
        BigAutoField id PK
        Integer student_id FK
        Integer course_id FK
        DateField date
        CharField status "present|absent|late"
        CharField marked_by
        Integer marked_by_user_id
        TextField remarks
        DateTime created_at
        DateTime updated_at
    }

    COURSES_ENROLLMENT {
        BigAutoField id PK
        Integer student_id FK
        Integer course_id FK
        DateField enrolled_date
        Boolean is_active
    }

    ACCOUNTS_USER ||--o{ COURSES_COURSE : "teaches (faculty role, SET_NULL)"
    STUDENTS_STUDENT ||--o{ ATTENDANCE_ATTENDANCE : "has (CASCADE)"
    COURSES_COURSE ||--o{ ATTENDANCE_ATTENDANCE : "has (CASCADE)"
    STUDENTS_STUDENT ||--o{ COURSES_ENROLLMENT : "enrolls (CASCADE)"
    COURSES_COURSE ||--o{ COURSES_ENROLLMENT : "enrolls (CASCADE)"
```

Render: paste block into https://mermaid.live, or view directly on GitHub (native Mermaid support in `.md` files).

## Notes / Constraints

- `attendance_attendance` has composite unique constraint on (`student`, `course`, `date`) — one record per student per course per day. Not expressible in base Mermaid ERD notation, noted here instead.
- `accounts_user` and `students_student` are **not** FK-linked. A student-role login account and a `Student` record are independent today (unrelated to the Enrollment changelog below).
- `courses_course.faculty` → `accounts_user`, `on_delete=SET_NULL`, `limit_choices_to={role: 'faculty'}`.
- `attendance_attendance.marked_by_user_id` is a plain `IntegerField`, not an FK — stores an id only, no referential integrity.

## Changelog

- **Jul 9 (Day 3):** `courses_enrollment` table added. Composite unique constraint (`student`, `course`). Backfill migration `0003_backfill_enrollment` populated rows from existing attendance history.
- **Jul 10 (Day 4):** `AttendanceSerializer.validate()` now rejects marking attendance for unenrolled students; `AttendanceViewSet.mark_bulk` filters out non-enrolled students per record (returned in a `skipped` list).
- Not yet exposed via REST: no `/api/enrollments/` endpoint yet. Add when frontend needs it.

## Source of Truth

Cross-check target: `python manage.py inspectdb` against this diagram + `docs/database-schema.md` — listed as remaining/not yet actioned in `HANDOFF.md`. This diagram was built from model definitions as documented, not from a live `inspectdb` run.
