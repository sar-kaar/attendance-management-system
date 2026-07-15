# NEXT_STEPS.md — Run on Windows

## What Was Done (Linux Session)

### 1. Student model — added `program` & `section`
**File:** `students/models.py`
```python
program = models.CharField(max_length=100, blank=True)
section = models.CharField(max_length=100, blank=True)
```

### 2. Attendance model — added `LP` & `ECA` statuses
**File:** `attendance/models.py`
```python
LATE_PRESENT = 'lp', 'Late Present'
ECA = 'eca', 'Extra-Curricular Activity'
```

### 3. GitHub Actions CI Pipeline
**File:** `.github/workflows/ci.yml`
- Triggers on push/PR to `develop`
- Runs: `makemigrations --check`, `manage.py check`, `manage.py test`
- Skips `dlib`/`face_recognition` install (heavy, not needed for tests)
- Sets env vars for `SECRET_KEY`, `DEBUG`, etc.

### 4. face/views.py — lazy imports
**File:** `face/views.py`
- Moved `import face_recognition` and `import numpy` inside functions
- Django can now load without face_recognition installed
- Tests run without dlib/face_recognition

---

## Step 1: Create Migration (run on Windows)

```powershell
cd D:\CSE Project\Attendance Management System\attendance-management-system
.venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
python manage.py check
```

Expected: 2 new migrations (students + attendance), no errors.

---

## Step 2: Verify

```python
python manage.py shell -c "
from students.models import Student
from attendance.models import Attendance
print('Student fields:', [f.name for f in Student._meta.get_fields()])
print('Attendance statuses:', Attendance.Status.choices)
"
```

Expected:
- Student fields include `program`, `section`
- Attendance statuses include `('lp', 'Late Present')`, `('eca', 'Extra-Curricular Activity')`

---

## Step 3: Build Features (Sprint 1 — P0)

All these are in `docs/requirements-dashboard-features.md` with full specs.

### Priority Order

| # | Feature | US | What to Build | Files to Create/Edit |
|---|---------|-----|---------------|---------------------|
| 1 | Student Academic Dashboard | US-06 | `/api/dashboard/students/` — search + per-subject breakdown | `attendance/views.py` (new action), `attendance/urls.py` |
| 2 | Attendance Stats Overview | US-07 | `/api/dashboard/stats/` — subject-level stats with program/section filters | `attendance/views.py` (new action) |
| 3 | Faculty Performance | US-08 | `/api/dashboard/faculty-performance/` — faculty ranked by attendance | `attendance/views.py` (new action) |
| 4 | At-Risk Detection | US-09 | `/api/dashboard/at-risk/` — students below 60% threshold | `attendance/views.py` (new action) |
| 5 | Chronic Latecomers | US-10 | `/api/dashboard/chronic-latecomers/` — 3+ late marks | `attendance/views.py` (new action) |
| 6 | Incomplete Records | US-13 | `/api/dashboard/incomplete-records/` — missing data detection | `attendance/views.py` (new action) |
| 7 | Enrollment REST | US-15 | Already built — just verify it works | `courses/views.py` (already done) |

### Implementation Notes

- All dashboard endpoints go in `attendance/views.py` as `@action` methods on `AttendanceViewSet`
- Add them to `attendance/urls.py` router
- Filter by `program` and `section` query params (now available on Student model)
- Use `Attendance.Status.ECA` and `Attendance.Status.LP` in calculations
- ECA counts as **present** in attendance percentage
- LP counts as **present** but flagged separately

---

## Step 4: Sprint 2 (P1) — After Sprint 1

| # | Feature | US |
|---|---------|-----|
| 8 | ECA Tracking | US-12 |
| 9 | Attendance Key Config | US-14 |
| 10 | Master Data Bulk Import | US-11 |

---

## Step 5: Sprint 3 — Frontend

| # | Feature |
|---|---------|
| 11 | React + Vite + MUI setup |
| 12 | Login/Register pages |
| 13 | Dashboard UI |
| 14 | Student Management UI |
| 15 | Attendance Marking UI |

---

## Git Status

```
Modified:
  students/models.py    (added program, section)
  attendance/models.py  (added LP, ECA statuses)
  face/views.py         (lazy imports for face_recognition)

New Files:
  .github/workflows/ci.yml  (CI pipeline)
  NEXT_STEPS.md             (this file)
```

Commit after migration is verified on Windows:
```powershell
git add students/models.py attendance/models.py face/views.py .github/workflows/ci.yml NEXT_STEPS.md
git commit -m "feat: add program/section to Student, LP/ECA to Attendance, CI pipeline"
git push
```
