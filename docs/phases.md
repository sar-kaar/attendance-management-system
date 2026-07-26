# Implementation Phases — Attendance Management System

> **Purpose:** Breaks delivery into incremental phases with atomic tasks, so both human contributors and AI agents can pick up one well-scoped unit of work at a time.
> **Scope:** Whole project. Status reflects reality as of 2026-07-26 — cross-check [memory.md](memory.md) before starting new work, since that file is updated more frequently than this one.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [How to Use This Document](#how-to-use-this-document)
- [Phase 1 — Repository & Project Setup](#phase-1--repository--project-setup)
- [Phase 2 — Authentication](#phase-2--authentication)
- [Phase 3 — Core Domain CRUD (Students, Courses, Enrollments)](#phase-3--core-domain-crud-students-courses-enrollments)
- [Phase 4 — Attendance](#phase-4--attendance)
- [Phase 5 — Face Recognition](#phase-5--face-recognition)
- [Phase 6 — Dashboard & Reporting](#phase-6--dashboard--reporting)
- [Phase 7 — Notifications](#phase-7--notifications-not-started)
- [Phase 8 — Testing Hardening](#phase-8--testing-hardening)
- [Phase 9 — Deployment & CI/CD](#phase-9--deployment--cicd)
- [Phase 10 — Engineering Hygiene (this effort)](#phase-10--engineering-hygiene-this-effort)

## How to Use This Document

Each phase lists **Objectives**, **Deliverables**, **Files Affected**, **Dependencies**, **Estimated Complexity**, and **Acceptance Criteria**. Tasks within a phase are atomic — sized for one focused change/PR, not a whole phase at once. Phases 1–6, 8, 9 are **done**; they're documented retroactively so the project's history and file ownership are traceable. Phase 7 and parts of Phase 10 are open.

## Phase 1 — Repository & Project Setup

**Status:** Done

- **Objectives:** Stand up Django backend and React frontend as independent top-level projects; wire local dev (`run.bat`/root `package.json` `concurrently`).
- **Deliverables:** `backend/` Django project skeleton, `frontend/` Vite+React skeleton, root dev-runner.
- **Files affected:** `backend/manage.py`, `backend/config/*`, `frontend/package.json`, `frontend/vite.config.js`, root `package.json`.
- **Dependencies:** None.
- **Complexity:** Low.
- **Acceptance criteria:** `npm run dev` at repo root starts both servers; `backend/.env.example` and `frontend/.env.example` document every required variable.

## Phase 2 — Authentication

**Status:** Done

- **Objectives:** Custom user model with roles; JWT auth; email OTP verification; social sign-in.
- **Deliverables:** `accounts` app — register/login/refresh/me, OTP send/verify, Google/Facebook login, admin user management.
- **Files affected:** `backend/accounts/*`, `frontend/src/pages/{Login,Register,VerifyEmail}.jsx`, `frontend/src/context/AuthContext.jsx`, `frontend/src/components/SocialLogin.jsx`.
- **Dependencies:** Phase 1.
- **Complexity:** Medium (OTP + two OAuth providers + JWT rotation).
- **Acceptance criteria:** A new user can register, verify via OTP, log in, and reach an authenticated page; social login works when `GOOGLE_CLIENT_ID`/`FACEBOOK_APP_ID` are configured.

### Atomic tasks (if extending)

- [ ] Add a new social provider → new `SocialLoginView` subclass in `accounts/social.py` + `accounts/urls.py` entry + `SocialLogin.jsx` button — one PR.
- [ ] Add password-reset flow → new OTP-purpose branch reusing existing OTP model/throttle scopes, not a parallel mechanism.

## Phase 3 — Core Domain CRUD (Students, Courses, Enrollments)

**Status:** Done

- **Objectives:** Student/Course CRUD with role-gated write access; Enrollment as the student↔course link enforcing attendance eligibility.
- **Deliverables:** `students`, `courses` apps; `Enrollment` model + backfill migration.
- **Files affected:** `backend/students/*`, `backend/courses/*`, `frontend/src/pages/{Students,Courses,Enrollments}.jsx`.
- **Dependencies:** Phase 2 (role-based permissions).
- **Complexity:** Low–Medium.
- **Acceptance criteria:** Admin/faculty can CRUD students/courses; enrolling a student in a course is required before attendance can be marked for that pair.

## Phase 4 — Attendance

**Status:** Done

- **Objectives:** Manual + bulk attendance marking, enrollment-gated; attendance codes for self-check-in; report generation + CSV/PDF export.
- **Deliverables:** `attendance` app — CRUD, `mark_bulk`, `AttendanceCodeViewSet`, `report`, `export/csv`, `export/pdf`.
- **Files affected:** `backend/attendance/*`, `frontend/src/pages/{Attendance,AttendanceCodes,Reports}.jsx`.
- **Dependencies:** Phase 3 (Enrollment).
- **Complexity:** Medium (bulk-skip logic, PDF generation via reportlab).
- **Acceptance criteria:** Marking attendance for a non-enrolled student is rejected (single) or skipped-and-reported (bulk); exports produce valid CSV/PDF for a given filter set.

## Phase 5 — Face Recognition

**Status:** Done

- **Objectives:** Register a student's face; recognize a face and mark attendance from it; support both a local (`dlib`) and cloud (Azure AI Face API) provider.
- **Deliverables:** `face` app — `register`, `recognize`, `mark-attendance`, `registered` endpoints; `face/providers.py` provider abstraction.
- **Files affected:** `backend/face/*`, `frontend/src/pages/FaceRecognition.jsx`.
- **Dependencies:** Phase 3 (Student), Phase 4 (Attendance).
- **Complexity:** High (external dependency build issues, two-provider abstraction, browser webcam capture).
- **Acceptance criteria:** With `FACE_PROVIDER=local` and `dlib` installed, register→recognize→mark-attendance works end-to-end; the app still boots and serves non-face endpoints when `dlib` is absent (lazy import).

### Atomic tasks (open)

- [ ] Verify `FACE_PROVIDER=azure` end-to-end against a real Azure Face resource (flagged open in `NEXT_STEPS.md`) — not yet confirmed beyond local testing.
- [ ] Decide whether `azure` should become the deployed default given `dlib` can't build on the current App Service plan.

## Phase 6 — Dashboard & Reporting

**Status:** Backend done; frontend UI in progress

- **Objectives:** Aggregation endpoints for program/section breakdowns, attendance stats, at-risk students, chronic latecomers, faculty performance, incomplete-record detection, and bulk master-data import.
- **Deliverables:** `dashboard` app (backend, done — PR #30, covers US-06/07/08/09/11/13); `frontend/src/pages/Dashboard.jsx` + `StudentDashboard.jsx` (in progress, GitHub issue #1 / US-10 still open).
- **Files affected:** `backend/dashboard/*`, `frontend/src/pages/{Dashboard,StudentDashboard}.jsx`, `frontend/src/styles/dashboard.css`.
- **Dependencies:** Phases 3–5 (aggregates over students/courses/attendance/enrollment data).
- **Complexity:** Medium (multiple aggregation queries) for backend; Medium (chart.js integration, role-specific views) for remaining frontend work.
- **Acceptance criteria:** Each `dashboard` endpoint returns correct aggregates against seeded data (`manage.py seed_data`); frontend Dashboard renders role-appropriate widgets — **not yet fully met on the frontend side**, see [memory.md](memory.md) Pending Features.

### Atomic tasks (open)

- [ ] Wire remaining `dashboard` endpoints (`at-risk`, `chronic-latecomers`, `faculty-performance`, `incomplete-records`) into `Dashboard.jsx` widgets, one endpoint/widget per PR.
- [ ] ECA (extra-curricular activity) tracking — US-12, GitHub issue #23. No backend model exists yet; scope the data model first (likely a new small app or extension of `attendance`) before UI.

## Phase 7 — Notifications (not started)

- **Objectives:** Email/SMS notifications for attendance thresholds, OTP reminders, or dashboard-triggered alerts.
- **Deliverables:** TBD — likely reuses the existing Brevo SMTP config for email; SMS provider not yet chosen.
- **Files affected:** New app (suggest `notifications/`) or extension of `dashboard`'s at-risk detection.
- **Dependencies:** Phase 6 (at-risk/chronic-latecomer detection already computes the trigger condition).
- **Complexity:** Medium.
- **Acceptance criteria:** TBD once scoped — do not start without a design note in [decisions.md](decisions.md) first (email vs. SMS, sync vs. async/queued sending).

## Phase 8 — Testing Hardening

**Status:** Ongoing baseline in place

- **Objectives:** Keep `manage.py test` coverage current as apps grow; keep migrations in sync (`makemigrations --check` in CI).
- **Deliverables:** `tests.py` per app (all 6 apps have one), `backend/integration_tests.py` for cross-app flows, GitLab CI `test` stage.
- **Files affected:** `backend/*/tests.py`, `backend/integration_tests.py`, `.gitlab-ci.yml`, `.github/workflows/ci.yml`.
- **Dependencies:** Runs against all prior phases.
- **Complexity:** Low per-test, ongoing.
- **Acceptance criteria:** CI green on `main`/`develop`/MRs. See [testing.md](testing.md) for strategy detail.

### Atomic tasks (ongoing discipline, not a one-time task)

- [ ] Any new view/serializer PR includes a test in the same PR — enforced by review, not currently by a coverage gate in CI.

## Phase 9 — Deployment & CI/CD

**Status:** Done

- **Objectives:** Automated test → build → deploy pipeline to Azure.
- **Deliverables:** `.gitlab-ci.yml` (test/build-frontend/deploy-backend/deploy-frontend), `.github/workflows/ci.yml` (test mirror), `backend/.deployment`/`.deployment` (Azure Oryx build config), `backend/postbuild.sh`, `backend/startup.sh`.
- **Files affected:** As above.
- **Dependencies:** All app phases (deploys everything).
- **Complexity:** Medium (async deploy handling for slow `dlib-bin`/`numpy` builds — see comment in `.gitlab-ci.yml`).
- **Acceptance criteria:** Push to `main` → tests pass → frontend built → both backend and frontend deployed to Azure without manual steps. See [deployment.md](deployment.md).

## Phase 10 — Engineering Hygiene (this effort)

**Status:** In progress (this document set)

- **Objectives:** Bring the repo up to the documentation/config standard described in this `docs/` set, without touching working application code.
- **Deliverables:** `docs/{prd,architecture,design,rules,phases,memory,api,testing,deployment,decisions}.md`, root config files (`.editorconfig`, `.prettierrc`, `.gitattributes`).
- **Files affected:** `docs/*`, repo-root config files only — no application code.
- **Dependencies:** None (documentation-only).
- **Complexity:** Low (content-authoring effort, not code risk).
- **Acceptance criteria:** All new docs cross-link correctly; no existing functionality touched; frontend/backend still build after the change (see [Validation checklist](#) in the PR description of this work).

### Atomic tasks (open, future)

- [ ] Add Prettier/ESLint format-on-save enforcement (`lint-staged` + a git hook) if the team wants it — deliberately not forced in this pass, see [rules.md](rules.md).
- [ ] Add a Python formatter/linter (`ruff` or `black`+`flake8`) to `backend/` and CI — none exists today.
- [ ] Retire or refresh `Guidelines/03_PROJECT_TRACKER.csv` (flagged stale since 2026-07-20 in `HANDOFF.md`).
