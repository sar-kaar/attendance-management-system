# Week 2 (Jul 13–19) — Sprint 1: Dashboard Analytics APIs
## Abhishek Rokaya — Backend

**Updated plan based on Google Sheets analysis (Jul 10).** 10 new user stories (US-06 to US-15) were discovered from existing Google Sheets dashboards (SUM I Dashboard, Testing Dashboard, Student Master Dashboard). This week focuses on implementing the backend APIs for these features.

**Already done (carried over from Week 1):** SECRET_KEY → .env, CORS restricted, requirements installed, Enrollment model + migration, Attendance validation, system-architecture.md, database-schema.md.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`. Use feature branches: `feature/US-XX-description`.

---

### Day 7 (Mon, Jul 13) — Dashboard app + Student Academic Dashboard API
**Before you start:** `git checkout develop && git pull`.

- [ ] Create new Django app: `python manage.py startapp dashboard`
- [ ] Register `dashboard` in INSTALLED_APPS
- [x] **US-15 (#25):** Create Enrollment ViewSet with nested serializer (student_name, course_code+name) — DONE in courses/views.py + courses/serializers.py
- [x] Add enrollment filtering: `?student=<id>&course=<id>&is_active=true` — DONE in EnrollmentViewSet.get_queryset()
- [x] Register enrollment router in urls — DONE in courses/urls.py (registered as /api/enrollments/)

```bash
git checkout -b feature/US-15-enrollment-endpoint develop
git add dashboard/ courses/views.py courses/serializers.py courses/urls.py
git commit -m "[feat] Expose Enrollment REST endpoint with filtering"
git push origin feature/US-15-enrollment-endpoint
```

---

### Day 8 (Tue, Jul 14) — Dashboard: Program/Section filters + Student Search
- [ ] **US-06 (#19) Part 1:** Dashboard program/section search endpoints
- [ ] `GET /api/dashboard/programs/` — distinct programs from Student model
- [ ] `GET /api/dashboard/sections/?program=<program>` — distinct sections filtered by program
- [ ] `GET /api/dashboard/students/?search=<name>` — student search with enrollment info
- [ ] `GET /api/dashboard/students/<id>/` — per-student attendance breakdown by subject

**Actual work done this day (different from plan):**
- [x] Face recognition app created: `python manage.py startapp face` — register, recognize, mark_attendance endpoints
- [x] Attendance export endpoints: `GET /api/attendance/export/csv/`, `GET /api/attendance/export/pdf/`
- [x] LP/ECA statuses added to Attendance model (LP, ECA choices)
- [x] Student program/section fields added to Student model

---

### Day 9 (Wed, Jul 15) — Attendance Stats Overview + At-Risk
- [ ] **US-07 (#17):** `GET /api/dashboard/attendance-stats/` — per-subject stats
  - Group attendance by course, compute: classes_run, enrolled_count, marked_count, avg_headcount, worst_day, overall_%, status (🟢/🟡/🔴/⚪)
- [ ] **US-09 (#20):** `GET /api/dashboard/at-risk/?threshold=60` — students <60% in any subject
  - Ordered by % ascending, per-subject breakdown

**Actual work done this day (different from plan):**
- [x] Unit tests for accounts app (90 lines — register, login, token refresh, role-based permissions)
- [x] Unit tests for attendance app (226 lines — CRUD, mark_bulk, validate enrollment)
- [x] Postman collection created: `docs/postman_collection.json` + `docs/postman_environment.json`

---

### Day 10 (Thu, Jul 16) — Faculty Performance + Chronic Latecomers + Incomplete Records
- [ ] **US-08 (#18):** `GET /api/dashboard/faculty-performance/` — per-faculty analytics
  - Group by faculty: subjects count, students managed, avg present, overall %, worst subject
- [ ] **US-10 (#24):** `GET /api/dashboard/chronic-latecomers/?threshold=3` — 3+ lates per subject
  - LP breakdown, combined total, ordered by total descending
- [ ] **US-13 (#22):** `GET /api/dashboard/incomplete-records/` — subjects with issues

**Actual work done this day (different from plan):**
- [x] Unit tests for face app (213 lines — registration, recognition, duplicate detection, edge cases)
- [x] Integration tests (359 lines — full workflow: register student → create course → enroll → mark attendance → dashboard stats → export)

---

### Day 11 (Fri, Jul 17) — Master Data Import + ECA + Attendance Key
- [ ] **US-11 (#21):** `POST /api/dashboard/master-data/import/` — bulk import from sheet format
  - Accept JSON array, create/update courses/students/enrollments/users
  - Dry-run mode: `?dry_run=true`
  - Return: created/updated/skipped/errors counts
- [ ] **US-12 (#23):** ECA model + CRUD endpoint
- [ ] **US-14 (#26):** AttendanceCode model + CRUD endpoint
- [ ] Run `python manage.py check` — fix warnings
- [ ] Run `python manage.py test` — run existing tests

**Actual work done this day (different from plan):**
- [x] CI pipeline configured: `.github/workflows/ci.yml` — lint, test, build on push/PR
- [x] Wireframes created: `docs/wireframes/` — 50+ HTML files (all pages, all roles, responsive)
- [x] `python manage.py check` — 0 errors
- [x] `python manage.py test` — all tests pass
- [x] All work merged to develop (PRs #21, #22, #23, #24, #25 all merged)

---

### Day 12–13 (Sat–Sun) — Buffer
- [x] All feature branches merged into `develop`
- [x] All existing tests passing
- [ ] Dashboard endpoints (US-06 to US-14) — **NOT DONE, deferred to Week 3+**
- [ ] Update `docs/api-endpoints.md` with new dashboard endpoints
- [x] Read Week 3 tasks
