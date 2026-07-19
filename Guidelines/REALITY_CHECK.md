# REALITY_CHECK.md — Source of Truth

## Stack
- **Backend**: Django 5.2.16 + Django REST Framework (DRF) + SimpleJWT
- **Database**: SQLite (default)
- **Face Recognition**: OpenCV (`opencv-python`, `opencv-contrib-python`) + `face_recognition`/`dlib` (added Jul 10, local install only — see Build Requirements note below)
- **Reports**: reportlab (PDF generation)
- **Auth**: JWT (access token: 1 day, refresh token: 7 days)

## Django Apps
| App | Purpose |
|-----|---------|
| `accounts` | User model (AbstractUser), registration, JWT login, profile |
| `students` | Student CRUD, face encoding storage |
| `courses` | Course CRUD, faculty assignment |
| `attendance` | Attendance marking, bulk marking, reports |

## Database Schema
### accounts_user
| Field | Type | Notes |
|-------|------|-------|
| id | BigAutoField (PK) | Auto-increment |
| username | CharField(150) | Unique |
| email | EmailField | |
| role | CharField(10) | Choices: `admin`, `faculty`, `student` (default: `student`) |
| phone | CharField(15) | blank |
| profile_picture | ImageField | upload_to=`profiles/`, nullable |
| password | CharField(128) | Hashed |
| first_name, last_name | CharField(150) | |
| is_active, is_staff, is_superuser | BooleanField | Django defaults |
| date_joined | DateTimeField | auto_now_add |
| groups, user_permissions | M2M | Django defaults |

### students_student
| Field | Type | Notes |
|-------|------|-------|
| id | BigAutoField (PK) | Auto-increment |
| first_name, last_name | CharField(100) | |
| email | EmailField | Unique |
| student_id | CharField(20) | Unique |
| phone | CharField(15) | blank |
| date_of_birth | DateField | nullable |
| address | TextField | blank |
| enrollment_date | DateField | auto_now_add |
| is_active | BooleanField | default=True |
| face_encoding | TextField | nullable, stores OpenCV encoding as string |
| created_at, updated_at | DateTimeField | auto_now_add / auto_now |

### courses_course
| Field | Type | Notes |
|-------|------|-------|
| id | BigAutoField (PK) | Auto-increment |
| name | CharField(200) | |
| code | CharField(20) | Unique |
| description | TextField | blank |
| credits | IntegerField | default=3 |
| faculty | ForeignKey → User | limit_choices_to={`role: 'faculty'`}, SET_NULL on delete |
| is_active | BooleanField | default=True |
| created_at, updated_at | DateTimeField | auto_now_add / auto_now |

### courses_enrollment
| Field | Type | Notes |
|-------|------|-------|
| id | BigAutoField (PK) | Auto-increment |
| student | ForeignKey → Student | CASCADE, related_name=`enrollments` |
| course | ForeignKey → Course | CASCADE, related_name=`enrollments` |
| enrolled_date | DateField | auto_now_add |
| is_active | BooleanField | default=True, dropped courses stay in history |
| **Unique** | (student, course) | Composite unique, no dup enrollment |

Not hard-FK'd from attendance — enforced in `AttendanceSerializer.validate()` + `mark_bulk` view instead.

### attendance_attendance
| Field | Type | Notes |
|-------|------|-------|
| id | BigAutoField (PK) | Auto-increment |
| student | ForeignKey → Student | CASCADE, related_name=`attendances` |
| course | ForeignKey → Course | CASCADE, related_name=`attendances` |
| date | DateField | |
| status | CharField(10) | Choices: `present`, `absent`, `late` |
| marked_by | CharField(20) | default=`manual` |
| marked_by_user_id | IntegerField | nullable |
| remarks | TextField | blank |
| created_at, updated_at | DateTimeField | auto_now_add / auto_now |
| **Unique** | (student, course, date) | Composite unique |

## API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register/ | AllowAny | Register new user |
| POST | /api/auth/login/ | AllowAny | JWT token obtain |
| POST | /api/auth/token/refresh/ | AllowAny | Refresh JWT token |
| GET | /api/auth/me/ | IsAuthenticated | Current user profile |
| GET/POST | /api/students/ | IsAuthenticated (list), Admin/Faculty (create) | Student CRUD |
| GET/PUT/DELETE | /api/students/:id/ | IsAuthenticated (read), Admin/Faculty (write) | Student detail |
| GET/POST | /api/courses/ | IsAuthenticated (list), Admin/Faculty (create) | Course CRUD |
| GET/PUT/DELETE | /api/courses/:id/ | IsAuthenticated (read), Admin/Faculty (write) | Course detail |
| GET/POST | /api/attendance/ | IsAuthenticated (list), Admin/Faculty (create) | Attendance CRUD |
| GET/PUT/DELETE | /api/attendance/:id/ | IsAuthenticated (read), Admin/Faculty (write) | Attendance detail |
| POST | /api/attendance/mark_bulk/ | Admin/Faculty | Bulk mark attendance |
| GET | /api/attendance/my_attendance/?student_id= | IsAuthenticated | Student's own attendance |
| GET | /api/attendance/report/?course=&student=&start_date=&end_date= | Admin/Faculty | Attendance report with stats |
| GET | /admin/ | Staff | Django admin interface |

## Roles
- **admin**: Full CRUD on all entities
- **faculty**: Can manage students, courses, attendance. Cannot manage other faculty/admins.
- **student**: Can view own attendance, own profile. Cannot modify anything.

## User Story → Feature Branch Mapping
| US | Feature | Branch |
|----|---------|--------|
| US-01 | Auth & Registration | (on develop) |
| US-02 | Student Management | (on develop) |
| US-03 | Course Management | (on develop) |
| US-04 | Manual Attendance Marking | (on develop) |
| US-05 | Attendance Dashboard | TBD |
| US-06 | Reporting & Export | TBD |
| US-07 | Face Registration | `feature/US-07-face-registration-api` |
| US-08 | Face Recognition Attendance | TBD |
| US-09 | Report API | `feature/US-09-report-api` |
| US-10 | Dashboard UI | `feature/US-10-dashboard-ui` |
| US-11 | Email/SMS Notifications | TBD |
| US-12 | QR Code Attendance | TBD |
| US-13 | Bulk Import | TBD |
| US-14 | Analytics & Insights | TBD |
| US-15 | System Administration | TBD |

## Branch Strategy
- `main` — production-ready
- `develop` — integration branch (current active)
- `feature/US-NN-name` — feature branches
- `docs/name` — documentation branches
- `bugfix/name` — bug fix branches
- `chore/name` — maintenance branches
- `hotfix/name` — urgent production fixes
- PRs created via `gh pr create`

## Enrollment Table — added Jul 9 (Day 3)
`courses.Enrollment` added before UI work started, not deferred to tonight's kickoff meeting. Reasoning: adding later breaks the `attendance` API contract once Ekata's UI branches build against it; adding now is one migration + one model; nothing blocks since no UI code exists yet. See `docs/database-schema.md` "Resolved: Enrollment table added" section for full detail (model, migrations, serializer/view enforcement, backfill).

Branch used: `feature/US-05-enrollment-decision` (pulled forward from its Week 4 reserved slot in `GIT_WORKFLOW.md` Section 7).

Migrations verified: `0002_enrollment` and `0003_backfill_enrollment` both applied successfully (Jul 10). `AttendanceSerializer.validate()` now enforces enrollment on create/update, and `mark_bulk` skips non-enrolled students (returns them in a `skipped` list) instead of failing the whole batch or silently marking them. Added Jul 10 (Day 4).

## Build Requirements — dlib (updated Jul 19)
`dlib` (required by `face_recognition`) compiles from C++ source on `pip install dlib` — fails without build tools, and is NOT in `requirements.txt` (deliberately excluded from CI/production; `face/views.py` imports it lazily so the app runs fine without it).

**Windows — recommended (no CMake/Visual Studio needed):**
```powershell
pip install dlib-bin              # prebuilt wheel, provides the `dlib` module
pip install face_recognition_models
pip install --no-deps face_recognition   # --no-deps: its declared "dlib" dep would try to build from source otherwise
```
Verify: `python -c "import dlib, face_recognition; print('ok')"`

**Alternative (build from source):** install CMake (add to PATH) + Visual Studio Build Tools ("Desktop development with C++" workload), then plain `pip install dlib face_recognition`. Slower, more failure-prone — only needed if `dlib-bin` doesn't have a wheel for your Python version.

macOS: `brew install cmake` first. Linux: `sudo apt install cmake build-essential`.

Face registration/recognition endpoints exist and work (`face` app, `/api/face/*`) — this section only matters for running them **locally**; they're not required for the rest of the app to run.

## Frontend
No frontend code exists in the repo yet. Ekata has initialized a React + Vite + MUI project locally with wireframes for login, register, dashboard, student management, and attendance marking screens.

## Note on file location (added Jul 10, Session 6)
This file previously lived at the project root (`Guidelines/REALITY_CHECK.md`, one level above this repo) — **outside git entirely**, so it could never be committed. Copied into the repo at `attendance-management-system/Guidelines/REALITY_CHECK.md` on Jul 10 so it's actually version-controlled. The root copy still exists too; treat this in-repo copy as canonical going forward and update both until the root copy is deleted.
