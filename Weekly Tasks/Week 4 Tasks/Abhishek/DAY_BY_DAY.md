# Week 4 (Jul 27–Aug 2) — Sprint 2: Core Attendance
## Abhishek Rokaya — Backend

**Sprint Goal:** student/course/attendance CRUD hardened and documented for the frontend; Enrollment table question resolved.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 21 (Mon, Jul 27) — Enrollment Decision
**Before you start:** check if Prizma got a teacher answer on the Enrollment gap from Week 2/3.

- [ ] If teacher wants it: add an `Enrollment` model (student FK, course FK, unique together) in a new migration, wire `AttendanceViewSet` to check enrollment before allowing a mark
- [ ] If out of scope: document the decision in `docs/er-diagram.md` and move on

```bash
git checkout -b feature/enrollment-decision develop
git add .
git commit -m "[US-04] Resolve enrollment table decision"
git push origin feature/enrollment-decision
```

---

### Day 22 (Tue, Jul 28) — Validation & Filtering
- [ ] Add filtering to `/api/students/` (by `is_active`, search by name/student_id)
- [ ] Add filtering to `/api/courses/` (by `is_active`, `faculty`)
- [ ] Add serializer-level validation (e.g. student_id format, course code format) if missing

```bash
git checkout -b feature/crud-hardening develop
git add students/ courses/
git commit -m "[US-04] Add filtering and validation to student/course endpoints"
git push origin feature/crud-hardening
```

---

### Day 23 (Wed, Jul 29) — Attendance Edge Cases
- [ ] Test `mark_bulk` with a bad course id, missing student_id, duplicate marks on the same day — confirm the unique_together constraint returns a clean error, not a 500
- [ ] Add a proper `try/except` around `mark_bulk` for bad `course_id`

```bash
git add attendance/
git commit -m "[US-06] Handle attendance edge cases and bad input"
git push origin feature/crud-hardening
```

---

### Day 24 (Thu, Jul 30) — Tests
- [ ] Write test cases for students, courses, attendance apps: CRUD works, permission checks work (student can't create, admin/faculty can), `mark_bulk` and `report` actions work

```bash
git add students/tests.py courses/tests.py attendance/tests.py
git commit -m "[test] Add CRUD and permission tests for core apps"
git push origin feature/crud-hardening
```

---

### Day 25 (Fri, Jul 31) — Integration & Review
- [ ] PR both branches into `develop`
- [ ] Confirm with Ekata her UI matches real field names and filter query params

```bash
git checkout develop
git merge feature/enrollment-decision
git merge feature/crud-hardening
git push origin develop
```

### Day 26 (Sat, Aug 1) — Sprint Review & Retro
- [ ] Demo hardened CRUD + enrollment decision
- [ ] Prep Week 5: face recognition is the real new work starting now
