# Real Database Schema (Django/SQLite)

Verified Jul 9 (Day 3) against actual `*/models.py` files across `accounts`, `students`, `courses`, `attendance`. This documents what exists today, not a planned design. Five tables total (Enrollment added Jul 9, see section 5).

## 1. accounts_user

Custom user model, `AbstractUser` subclass, set as `AUTH_USER_MODEL`.

| Field | Type | Notes |
|---|---|---|
| id | BigAutoField (PK) | auto-increment |
| username | CharField(150) | unique, from AbstractUser |
| email | EmailField | from AbstractUser |
| password | CharField(128) | hashed, from AbstractUser |
| first_name, last_name | CharField(150) | from AbstractUser |
| role | CharField(10) | choices: `admin`, `faculty`, `student`; default `student` |
| phone | CharField(15) | blank allowed |
| profile_picture | ImageField | upload_to=`profiles/`, nullable |
| is_active, is_staff, is_superuser | BooleanField | Django defaults |
| date_joined | DateTimeField | auto_now_add |
| groups, user_permissions | ManyToMany | Django defaults |

## 2. students_student

| Field | Type | Notes |
|---|---|---|
| id | BigAutoField (PK) | auto-increment |
| first_name, last_name | CharField(100) | |
| email | EmailField | unique |
| student_id | CharField(20) | unique |
| phone | CharField(15) | blank allowed |
| date_of_birth | DateField | nullable |
| address | TextField | blank allowed |
| enrollment_date | DateField | auto_now_add |
| is_active | BooleanField | default True |
| face_encoding | TextField | nullable, stores OpenCV face encoding as string |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

Note: `Student` is a separate model from `accounts_user`, not linked by FK. A student's login account (if any) and their student record are not connected in the schema today.

## 3. courses_course

| Field | Type | Notes |
|---|---|---|
| id | BigAutoField (PK) | auto-increment |
| name | CharField(200) | |
| code | CharField(20) | unique |
| description | TextField | blank allowed |
| credits | IntegerField | default 3 |
| faculty | ForeignKey → accounts_user | SET_NULL on delete, limited to `role='faculty'` |
| is_active | BooleanField | default True |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

## 4. attendance_attendance

| Field | Type | Notes |
|---|---|---|
| id | BigAutoField (PK) | auto-increment |
| student | ForeignKey → students_student | CASCADE, related_name=`attendances` |
| course | ForeignKey → courses_course | CASCADE, related_name=`attendances` |
| date | DateField | |
| status | CharField(10) | choices: `present`, `absent`, `late` |
| marked_by | CharField(20) | default `manual` |
| marked_by_user_id | IntegerField | nullable, not an FK, just stores an id |
| remarks | TextField | blank allowed |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

Composite unique constraint: (`student`, `course`, `date`). One attendance record per student per course per day.

## Relationships

```
accounts_user (faculty role) --1:N--> courses_course
students_student --1:N--> attendance_attendance
courses_course --1:N--> attendance_attendance
```

`accounts_user` and `students_student` are not directly related. A `student`-role user account and a `Student` record are independent today.

## 5. courses_enrollment

Added Jul 9 (Day 3). Resolved the earlier gap before UI work started.

| Field | Type | Notes |
|---|---|---|
| id | BigAutoField (PK) | auto-increment |
| student | ForeignKey → students_student | CASCADE, related_name=`enrollments` |
| course | ForeignKey → courses_course | CASCADE, related_name=`enrollments` |
| enrolled_date | DateField | auto_now_add |
| is_active | BooleanField | default True |

Composite unique constraint: (`student`, `course`). One enrollment per student per course.

Backfill migration `0003_backfill_enrollment` populated rows from existing attendance history — every distinct (student, course) pair in `attendance_attendance` got an active Enrollment row.

**Done (Jul 10, Day 4):** `AttendanceSerializer.validate()` now rejects marking attendance for unenrolled students, and `AttendanceViewSet.mark_bulk` filters out non-enrolled students per record (returned in a `skipped` list) instead of creating attendance for them.

## Updated Relationships

```
accounts_user (faculty role) --1:N--> courses_course
students_student --1:N--> attendance_attendance
students_student --1:N--> courses_enrollment
courses_course --1:N--> attendance_attendance
courses_course --1:N--> courses_enrollment
```

## Endpoints touching these tables

See `Guidelines/REALITY_CHECK.md` "API Endpoints" table for the full list; all of `/api/students/`, `/api/courses/`, `/api/attendance/*` map onto the five tables above. The Enrollment table is not yet exposed via REST — it exists as a constraint backing. An `/api/enrollments/` endpoint can be added when the frontend needs it.
