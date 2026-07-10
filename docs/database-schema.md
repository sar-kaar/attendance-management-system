[docs] Real Database Schema (Django/SQLite)

Verified Jul 9 (Day 3) against actual `*/models.py` files across `accounts`, `students`, `courses`, `attendance`. This documents what exists today, not a planned design. Four tables total. No `Enrollment` table.

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

## Known gap: no Enrollment table

There is no `enrollment` / `enrollments` table linking students to courses. `attendance_attendance` references both `student` and `course` directly, so in practice any student can be marked present/absent/late in any course, regardless of whether they are actually taking it. Nothing in the schema prevents this today.

**Decision (Jul 9, Day 3):** deferring the `Enrollment` table for now rather than adding it same-day as an undiscussed schema change. Reasoning: it touches the `attendance` API contract that Ekata's UI branches (`feature/US-05-student-ui`, `feature/US-06-attendance-ui`) will build against, and the team's actual first kickoff meeting is tonight (Jul 9). Recommend raising it there as `feature/US-05-enrollment-decision` (already reserved for Week 4 in `GIT_WORKFLOW.md` Section 7) and deciding as a team whether to add it before or after the UI work starts. This is a call for the team, not a unilateral one, so it is logged here rather than acted on. If the team decides to add it, it will need: a migration, a decision on whether it replaces the implicit student+course relationship in `attendance` queries, and an update to this doc and `REALITY_CHECK.md`.

## Endpoints touching these tables

See `Guidelines/REALITY_CHECK.md` "API Endpoints" table for the full list; all of `/api/students/`, `/api/courses/`, `/api/attendance/*` map directly onto the four tables above with no additional join tables.
