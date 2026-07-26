# Attendance Management System — 7-Week Roadmap (overview)

**Stack:** Django 5 + DRF + SimpleJWT + SQLite + OpenCV (face rec) + reportlab (PDF). Frontend not chosen yet — decide Week 2.
**Roles:** admin, faculty, student.
**Source of truth for current backend state:** `REALITY_CHECK.md` in this folder.

Day-by-day tasks per person live in `Weekly Tasks/Week N Tasks/<Name>/DAY_BY_DAY.md`. This file is the sprint-level summary only — check the day files for actual steps.

---

## Week 1 (Jul 7–12) — Initiation
Kickoff, GitHub/Trello setup, dev environments, SRS draft, requirements. Backend already got ahead of plan this week — Abhishek scaffolded all 4 Django apps (accounts, students, courses, attendance) with models, JWT auth, and CRUD endpoints already working. See `REALITY_CHECK.md`.

## Week 2 (Jul 13–19) — Sprint 0: Design
Goal: design docs finished, frontend framework decided, backend documented and secured.
- Abhishek: ER diagram matching the real 4 tables (no Enrollment table yet — flag as open question), Postman collection for the real endpoints, move SECRET_KEY to `.env`, research face recognition approach (OpenCV + face encoding storage, no code yet).
- Ekata: pick a frontend framework with the team, wireframes for the real screens (login, dashboard, students, courses, attendance, reports) using real roles.
- Prizma: Project Charter, Risk Register, Stakeholder Register, SRS finalized against the real stack.

## Week 3 (Jul 20–26) — Sprint 1: Auth
Goal: auth is already built — this sprint is verify, secure, and connect frontend to it.
- Abhishek: test register/login/refresh/me endpoints, fix CORS_ALLOW_ALL_ORIGINS, write basic tests, document real request/response shapes (login returns `{access, refresh}`).
- Ekata: build login + register pages against the real endpoints, store JWT, protected routing by role.
- Prizma: standups, sprint review, update backlog to reflect backend head start.

## Week 4 (Jul 27–Aug 2) — Sprint 2: Core Attendance
Goal: frontend for student/course/attendance management (APIs already exist).
- Abhishek: harden existing CRUD (validation, filtering, permission tests), decide on Enrollment table with the team.
- Ekata: student list/add/edit, course list/add/edit, attendance marking UI using `/api/attendance/mark_bulk/`.
- Prizma: mid-sprint refinement, sprint review, status report.

## Week 5 (Aug 3–9) — Sprint 3: Face Recognition
Goal: face registration + recognition actually built (this is the real gap).
- Abhishek: face registration endpoint (store encoding on Student), face match endpoint, integrate with attendance marking.
- Ekata: camera capture UI, registration flow, recognition-attendance flow.
- Prizma: track this as the highest-risk sprint, confirm fallback plan (manual attendance) with the team.

## Week 6 (Aug 10–16) — Sprint 4: Reports & Testing
Goal: CSV/PDF export, dashboard stats, full integration test pass.
- Abhishek: CSV export, PDF export (reportlab), dashboard stats endpoint.
- Ekata: dashboard charts, report page with filters, export buttons.
- Prizma: coordinate system testing, start user manual.

## Week 7 (Aug 17–25) — Sprint 5: Finalization
Goal: production-ready, documented, submitted.
- Abhishek: move SECRET_KEY/DEBUG/ALLOWED_HOSTS to real production config, deploy, API docs (Swagger/OpenAPI).
- Ekata: UI polish, user manual screenshots.
- Prizma: Final Report, presentation, submission checklist.

---

## Risk Register (top items)

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Face recognition accuracy low | Medium | High | Manual attendance fallback stays available |
| No Enrollment table — any student markable in any course | Medium | Medium | Decide with teacher in Week 2–3: add it or document as accepted scope |
| Hardcoded SECRET_KEY / open CORS | Low now, High if shipped | High | Fix before Week 7 deploy, not after |
| Frontend framework undecided | Low | Medium | Decide Week 2, don't let it slip into Week 3 |
| Team member unavailable | Low | High | Cross-train, keep code documented |

## Communication Plan

| Channel | Purpose | Frequency |
|---|---|---|
| Discord | Daily updates, quick questions | Daily |
| GitHub | Code, PRs, issues | Per commit |
| Trello | Task tracking | Updated daily |
| Standup | Align the team | Daily, 9 AM |
| Email | Teacher communication | As needed |
