# HANDOFF — Attendance Management System

> Last updated: 2026-07-20

---

## Project Overview

| Field | Value |
|---|---|
| Course | CSE 405 Software Project Management |
| GitHub repo | https://github.com/sar-kaar/attendance-management-system |
| GitLab repo (CI/CD) | https://gitlab.com/rokayaabi123/attendance-management-system |
| Trello | https://trello.com/b/ecB6ppQa/attendance-management-system |
| Live backend | https://ams-backend.azurewebsites.net |
| Layout | `backend/` (Django + DRF) and `frontend/` (React + Vite) as independent top-level projects |
| Django apps | `accounts`, `students`, `courses`, `attendance`, `face`, `dashboard` |

---

## Team & Assignments

| Member | Role | GitHub | Trello ID |
|---|---|---|---|
| Abhishek Rokaya | Backend / Admin | `sar-kaar` | `65a0b5c780c6cf7c94c87ec8` |
| Prizma Subedi | PM | `Prizma515` | `686b2ba0d197f3d3f50da2a5` |
| Ekata Rimal | Frontend | `ekatarimal` | `6a4b0ce1a1620a0fd86adcd4` |

---

## Status: backend + frontend both substantially built and deployed

This is well ahead of the Week-by-week plan in `Guidelines/01_WEEKLY_ROADMAP.md` and
`Guidelines/03_PROJECT_TRACKER.csv` — those documents are static plans written in
advance and are now stale (as of 2026-07-20 they still show Sprint 1 "in progress"
for basic register/login). **Treat this file and `Guidelines/REALITY_CHECK.md` as the
source of truth for actual status, not the tracker CSV.**

### API endpoints (all working)

| Module | Endpoint | Status |
|---|---|---|
| Auth | `/api/auth/register/`, `/api/auth/login/`, `/api/auth/token/refresh/` | Done |
| Email OTP verification | `/api/auth/otp/*` (Brevo SMTP) | Done |
| Social sign-in | Google / Facebook OAuth (settings-gated) | Done |
| Users | `/api/auth/users/` | Done |
| Students | `/api/students/` | Done |
| Courses | `/api/courses/` | Done |
| Enrollments | `/api/courses/enrollments/` | Done (US-15) |
| Attendance CRUD | `/api/attendance/` | Done |
| Attendance Bulk | `/api/attendance/bulk/` | Done |
| Attendance Report | `/api/attendance/report/` | Done |
| Attendance Export (CSV/PDF) | `/api/attendance/export/csv/`, `/export/pdf/` | Done |
| Attendance Codes | `/api/attendance/codes/` | Done (US-14) |
| Face Recognition | `/api/face/` | Done — provider-selectable: local `dlib` or Azure AI Face API (`FACE_PROVIDER` env var) |
| Dashboard | `/api/dashboard/*` (US-06 to US-13, PR #30) | Done, backend-complete |

### Recent work (this session, 2026-07-20)

- Added `backend/face/providers.py` — Azure AI Face API as an alternative to local
  `dlib`/`face_recognition`, selected via `FACE_PROVIDER=local|azure`. Lets face
  recognition work on hosts that can't build `dlib` (e.g. constrained App Service
  plans).
- Replaced native `alert()`/`confirm()` with the app's toast/confirm dialogs across
  `Attendance`, `AttendanceCodes`, `Courses`, `Enrollments`, and `Students` pages for
  consistent success/error feedback.
- (Prior commits today) Social sign-in + email verification UI, dashboard layout
  rework, OTP hardening, Azure mail-config sync on deploy.

### Deployment

- **Host**: Azure App Service `ams-backend` (resource group `ams-rg`), frontend
  static assets to storage account `amsfrontendweb`.
- **CI/CD**: GitLab CI (`.gitlab-ci.yml`) — tests run on `main`, `develop`, and merge
  requests; frontend build + backend deploy run only on `main`.
- **GitHub** (`origin`) is used for team visibility, issues, and PRs; **GitLab**
  (`gitlab`) drives the actual deploy pipeline. Both remotes are kept in sync.
- Mail/OTP secrets are synced from GitLab CI/CD masked variables into Azure App
  Service settings at deploy time — nothing secret is committed.

### Test status

Backend test suite runs in GitLab CI on every push to `main`/`develop` and on MRs
(`python manage.py test`, with `face-recognition` installed `--no-deps` for the face
app tests). Check the latest GitLab pipeline for current pass/fail counts rather than
a number cached here.

---

## Pending work

### Prizma (PM) — still incomplete (GitHub issues open)

| Issue | Title |
|---|---|
| #7 T-002 | Requirements Gathering |
| #5 T-003 | SRS Document (IEEE 830) |
| #11 T-005 | Wireframes and Mockups |
| #8 T-007 | Project Charter |
| #12 T-008 | Team Norms and Comms Plan |

### Ekata (Frontend) — still incomplete

| Issue | Title |
|---|---|
| #1 | US-10: Dashboard UI |
| #23 | US-12: ECA Tracking |

### GitHub issue hygiene (found this session, not yet acted on)

- PR #30 (*"Dashboard API — US-06 to US-13"*, merged 2026-07-18) implemented the
  backend for issues **#19 (US-06), #17 (US-07), #18 (US-08), #20 (US-09), #21
  (US-11), #22 (US-13)** but none of them were closed. Recommend closing once
  confirmed working.
- Two open issues are both titled "US-10": **#1** ("Dashboard UI", frontend, genuinely
  open) and **#24** ("Chronic Latecomers Detection", backend, covered by PR #30). Just
  a numbering collision from reused labels — not urgent, but confusing in triage.

---

## Architecture notes

- **Database**: SQLite (local dev) / production DB per Azure App Service config.
- **Auth**: SimpleJWT (access + refresh) + email OTP verification (Brevo SMTP) +
  Google/Facebook social sign-in.
- **User model**: custom `accounts.User` with roles: `admin`, `faculty`, `student`.
- **Face recognition**: `FACE_PROVIDER` env var selects `local` (dlib/face_recognition,
  no network call) or `azure` (Azure AI Face API, needs `AZURE_FACE_ENDPOINT` /
  `AZURE_FACE_KEY` / `AZURE_FACE_PERSON_GROUP`). Local is the default.
- **Seed data**: `python manage.py seed_data`.
- **Static files**: WhiteNoise (backend) / Azure storage (frontend build).

---

## Next steps

1. Push `develop` (currently ahead locally) to both `origin` and `gitlab`.
2. Close the stale-but-implemented dashboard issues (#19, #17, #18, #20, #21, #22)
   after a quick sanity check against `/api/dashboard/*`.
3. Chase Prizma on T-002/003/005/007/008 — none started, all overdue against the
   Week 1–2 deadlines in `Guidelines/04_DELIVERABLES_CHECKLIST.md`.
4. Chase Ekata on US-10 (Dashboard UI, #1) and US-12 (ECA Tracking, #23).
5. Consider requesting `read:project` scope on the `gh` token if a GitHub Projects
   board is wanted for tracking (`gh auth refresh -s read:project`).
6. Retire or refresh `Guidelines/03_PROJECT_TRACKER.csv` — it no longer reflects
   reality and risks misleading anyone who reads it as current status.

---

## Prior session log

Earlier session-by-session debug notes (dlib install, `.gitignore` fix, file-location
fix, Google Sheets → GitHub issue generation, architecture diagrams) have been
trimmed from this file now that all of that work is long resolved and merged. See
git history (`git log -- HANDOFF.md`) for the full archive if needed.
