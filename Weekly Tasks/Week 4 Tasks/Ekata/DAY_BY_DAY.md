# Week 4 (Jul 27–Aug 2) — Sprint 2: Core Attendance
## Ekata Rimal — Frontend

**Sprint Goal:** student management, course management, and attendance marking UI, all against the real endpoints from `REALITY_CHECK.md`.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 21 (Mon, Jul 27) — Student List + Add/Edit
- [ ] List page hitting `GET /api/students/`
- [ ] Add/edit form matching the real Student fields (first_name, last_name, email, student_id, phone, date_of_birth, address) — `face_encoding` is not user-editable, leave it out
- [ ] Only show add/edit controls if role is admin or faculty

```bash
git checkout -b feature/student-ui develop
git add frontend/src/pages/Students.*
git commit -m "[US-04] Add student list and add/edit UI"
git push origin feature/student-ui
```

---

### Day 22 (Tue, Jul 28) — Course List + Add/Edit
- [ ] List page hitting `GET /api/courses/`
- [ ] Add/edit form matching real Course fields (name, code, description, credits, faculty)
- [ ] Faculty dropdown should only list users with role=faculty — ask Abhishek if there's an endpoint for that, or use `/api/auth/` admin list if one exists, otherwise flag it as a gap

```bash
git checkout -b feature/course-ui develop
git add frontend/src/pages/Courses.*
git commit -m "[US-05] Add course list and add/edit UI"
git push origin feature/course-ui
```

---

### Day 23 (Wed, Jul 29) — Attendance Marking UI
- [ ] Pick course + date → list students → mark present/absent/late per student
- [ ] Submit as one call to `POST /api/attendance/mark_bulk/` with the real payload shape (`course_id`, `date`, `records: [{student_id, status}]`)

```bash
git checkout -b feature/attendance-ui develop
git add frontend/src/pages/AttendanceMark.*
git commit -m "[US-06] Add attendance marking UI using mark_bulk"
git push origin feature/attendance-ui
```

---

### Day 24 (Thu, Jul 30) — Attendance View
- [ ] Student attendance history page hitting `/api/attendance/my_attendance/?student_id=`
- [ ] Simple report view hitting `/api/attendance/report/?course=&start_date=&end_date=`

```bash
git add frontend/src/pages/AttendanceView.*
git commit -m "[US-06] Add attendance view and basic report page"
git push origin feature/attendance-ui
```

---

### Day 25 (Fri, Jul 31) — Integration & Review
- [ ] PR all branches into `develop`
- [ ] Live test full flow with Abhishek: add student → add course → mark attendance → view report

```bash
git checkout develop
git merge feature/student-ui
git merge feature/course-ui
git merge feature/attendance-ui
git push origin develop
```

### Day 26 (Sat, Aug 1) — Sprint Review & Retro
- [ ] Demo the full flow
- [ ] Prep Week 5: camera UI for face registration/recognition
