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
- [Phase 11 — Mobile Platform Decision & Requirements](#phase-11--mobile-platform-decision--requirements)
- [Phase 12 — Mobile Architecture Design](#phase-12--mobile-architecture-design)
- [Phase 13 — Shared API Layer Confirmation](#phase-13--shared-api-layer-confirmation)
- [Phase 14 — Backend Readiness for Mobile](#phase-14--backend-readiness-for-mobile)
- [Phase 15 — Mobile App Foundation & Scaffold](#phase-15--mobile-app-foundation--scaffold)
- [Phase 16 — Mobile Authentication](#phase-16--mobile-authentication)
- [Phase 17 — Mobile Attendance Marking](#phase-17--mobile-attendance-marking)
- [Phase 18 — Mobile Face Recognition](#phase-18--mobile-face-recognition)
- [Phase 19 — Mobile Reports & Results](#phase-19--mobile-reports--results)
- [Phase 20 — Mobile Dashboard](#phase-20--mobile-dashboard)
- [Phase 21 — Mobile Push Notifications](#phase-21--mobile-push-notifications)
- [Phase 22 — Mobile Offline Mode (Hardening)](#phase-22--mobile-offline-mode-hardening)
- [Phase 23 — Mobile Profile, Build & Release, Testing](#phase-23--mobile-profile-build--release-testing)

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

## Phase 11 — Mobile Platform Decision & Requirements

**Status:** Done (this effort, 2026-07-26)

- **Objectives:** Decide the mobile tech stack and write down what the mobile app actually needs to do, before any scaffold code exists.
- **Deliverables:** [mobile-requirements.md](mobile-requirements.md), [decisions.md](decisions.md) ADR-008 (React Native/Expo).
- **Files affected:** `docs/mobile-requirements.md`, `docs/decisions.md`.
- **Dependencies:** None.
- **Complexity:** Low (writing/decision effort, no code).
- **Acceptance criteria:** Every mobile story in GitHub #34 traces to at least one functional requirement in `mobile-requirements.md`; ADR-008 states a decision with alternatives and rationale, not just a conclusion.

## Phase 12 — Mobile Architecture Design

**Status:** Done (this effort, 2026-07-26)

- **Objectives:** Define the mobile project's stack, layout, navigation, offline strategy, and integration points with the existing backend.
- **Deliverables:** [mobile-architecture.md](mobile-architecture.md).
- **Files affected:** `docs/mobile-architecture.md`.
- **Dependencies:** Phase 11 (requirements inform architecture choices, e.g. offline queue scope).
- **Complexity:** Low–Medium (design effort, no code).
- **Acceptance criteria:** Every functional requirement in Phase 11 has a corresponding architectural answer (which layer/module handles it); no requirement is left architecturally unaddressed.

## Phase 13 — Shared API Layer Confirmation

**Status:** Done (this effort, 2026-07-26) — documentation pass; code-level permission verification still open, see atomic tasks

- **Objectives:** Confirm [api.md](api.md) is an accurate, mobile-consumable contract — not just a description written for the web client.
- **Deliverables:** [gap-analysis.md](gap-analysis.md) Gap 4 (API contract confirmation) captures the verification method and known soft spots (`dashboard/*` permission classes flagged as unverified in `api.md` itself).
- **Files affected:** `docs/gap-analysis.md`; `docs/api.md` if the verification pass below finds and fixes a documentation error.
- **Dependencies:** Phase 11 (need the mobile functional requirements to know which endpoints matter).
- **Complexity:** Low (verification), Medium if it uncovers a real permission bug.
- **Acceptance criteria:** Every endpoint referenced by an MR-* requirement in [mobile-requirements.md](mobile-requirements.md) has a confirmed (not assumed) permission class.

### Atomic tasks (open)

- [ ] Walk `backend/dashboard/views.py`'s actual `permission_classes` against the table in [api.md](api.md) Dashboard section and correct any mismatch — flagged but not yet done (see [gap-analysis.md](gap-analysis.md) Gap 4).

## Phase 14 — Backend Readiness for Mobile

**Status:** Planning done (this effort, 2026-07-26); implementation not started

- **Objectives:** Identify and design (not yet implement) every backend change the mobile app needs beyond what already exists — GitHub #36.
- **Deliverables:** [gap-analysis.md](gap-analysis.md) (Gaps 1–3: mobile-native OAuth token exchange, push device registration, CORS/host allowlist audit).
- **Files affected:** `docs/gap-analysis.md` (planning); future `backend/` changes land here once implemented.
- **Dependencies:** Phase 13.
- **Complexity:** Medium (OAuth token verification nuance, new notification model design).
- **Acceptance criteria (for this planning pass):** Each gap has a proposed approach and is explicitly marked blocked/not-blocked on other phases. **Acceptance criteria (for eventual implementation, not yet started):** mobile client can complete Google/Facebook login end-to-end; a device can register a push token; a full backend audit confirms no browser-session assumption blocks a mobile client.

### Atomic tasks (open, blocks Phase 16/21)

- [ ] Implement Gap 1 (mobile OAuth token exchange) — confirm first whether existing `backend/accounts/social.py` views already accept a bare mobile-issued token before assuming a new endpoint is needed.
- [ ] Implement Gap 2 (push device registration model + endpoints) — coordinate with Phase 7 (web notifications) so both channels share one trigger, not two.
- [ ] Complete Gap 3 audit (CORS/CSRF/`ALLOWED_HOSTS` assumptions) — audit only, code change if it finds a real issue.

## Phase 15 — Mobile App Foundation & Scaffold

**Status:** Not started (GitHub #35)

- **Objectives:** Stand up the `mobile/` project skeleton — no features, just a booting shell.
- **Deliverables:** `mobile/` Expo managed-workflow project, `mobile/.env.example`, role-based navigator shells (empty), lint/typecheck CI stage (additive to GitHub Actions, not `.gitlab-ci.yml`).
- **Files affected:** New `mobile/` directory tree (see [mobile-architecture.md](mobile-architecture.md) Project Layout), `.github/workflows/` (new mobile lint job).
- **Dependencies:** Phase 12 (architecture), Phase 13 (shared API layer confirmed — referenced directly in GitHub #35).
- **Complexity:** Medium.
- **Acceptance criteria:** App boots to an empty auth/unauth shell on both iOS and Android simulators; no hardcoded URLs (env-driven per NFR-05 in [mobile-requirements.md](mobile-requirements.md)).

## Phase 16 — Mobile Authentication

**Status:** Not started (GitHub #37)

- **Objectives:** Implement MR-01/02/03/12 from [mobile-requirements.md](mobile-requirements.md) — login, OTP, session persistence, logout.
- **Deliverables:** Auth screens, `AuthContext` port, token storage via `expo-secure-store`.
- **Files affected:** `mobile/src/screens/{Login,Register,VerifyOtp}.tsx`, `mobile/src/context/AuthContext.tsx`, `mobile/src/services/api.ts`.
- **Dependencies:** Phase 15 (scaffold), Phase 14 (mobile OAuth token exchange, for Google/Facebook login specifically).
- **Complexity:** Medium.
- **Acceptance criteria:** A user can register, verify via OTP, log in (incl. Google/Facebook), and reach a role-gated screen; session survives an app restart.

## Phase 17 — Mobile Attendance Marking

**Status:** Not started (GitHub #38)

- **Objectives:** MR-04/06/10 — manual marking, self-check-in codes, offline queue MVP (manual marking only, per [mobile-requirements.md](mobile-requirements.md) Open Questions).
- **Deliverables:** Attendance marking screens, `offlineQueue.ts` (SQLite-backed), sync-on-reconnect logic.
- **Files affected:** `mobile/src/screens/Attendance*.tsx`, `mobile/src/services/offlineQueue.ts`.
- **Dependencies:** Phase 16 (auth).
- **Complexity:** High (offline queue correctness, conflict surfacing).
- **Acceptance criteria:** Marking attendance offline queues locally and syncs correctly on reconnect; a conflicting record surfaces the existing `400` validation error rather than silently failing or double-marking.

## Phase 18 — Mobile Face Recognition

**Status:** Not started (GitHub #39)

- **Objectives:** MR-05 — face-based attendance marking via device camera.
- **Deliverables:** Camera capture screen (`expo-camera`), calls to `/api/face/recognize/` and `/mark-attendance/`.
- **Files affected:** `mobile/src/screens/FaceRecognition.tsx`.
- **Dependencies:** Phase 17 (attendance marking foundation), Phase 16 (auth).
- **Complexity:** Medium (camera permission UX, matches NFR-04).
- **Acceptance criteria:** End-to-end register→recognize→mark-attendance works against whichever `FACE_PROVIDER` the backend is configured with, same as the web flow.

## Phase 19 — Mobile Reports & Results

**Status:** Not started (GitHub #40)

- **Objectives:** MR-07 — student attendance history/stats, read-only.
- **Deliverables:** Reports screen consuming `attendance/report/` and `dashboard/students/:id/attendance/`.
- **Files affected:** `mobile/src/screens/Reports.tsx`.
- **Dependencies:** Phase 16.
- **Complexity:** Low–Medium.
- **Acceptance criteria:** A student can see their own attendance history and computed stats; a faculty member cannot see another faculty's students' data they aren't scoped to (mirrors existing backend role scoping — no new permission logic needed).

## Phase 20 — Mobile Dashboard

**Status:** Not started (GitHub #41)

- **Objectives:** MR-08 — faculty roster/at-risk/chronic-latecomer views, read-only.
- **Deliverables:** Dashboard screen(s) consuming `dashboard/*` endpoints scoped to faculty (not the admin-only `faculty-performance` endpoint — see [feature-matrix.md](feature-matrix.md)).
- **Files affected:** `mobile/src/screens/Dashboard.tsx`.
- **Dependencies:** Phase 13 (confirmed permission classes), Phase 16.
- **Complexity:** Medium (chart/visualization choice for React Native — likely `victory-native` or `react-native-svg`-based, not chart.js which is web-only).
- **Acceptance criteria:** Faculty sees roster/at-risk/chronic-latecomer data scoped correctly to their own courses.

## Phase 21 — Mobile Push Notifications

**Status:** Not started (GitHub #42)

- **Objectives:** MR-09 — push on at-risk/threshold events.
- **Deliverables:** Device token registration (client side of [gap-analysis.md](gap-analysis.md) Gap 2), `expo-notifications` integration.
- **Files affected:** `mobile/src/services/push.ts`.
- **Dependencies:** Phase 14 (backend push device endpoint must exist first), Phase 7 (web notifications — shared trigger logic, see Gap 2 note on not building two parallel systems).
- **Complexity:** Medium.
- **Acceptance criteria:** A registered device receives a push notification when the same condition that would trigger a web notification (Phase 7) fires.

## Phase 22 — Mobile Offline Mode (Hardening)

**Status:** Not started (GitHub #43)

- **Objectives:** Harden the Phase 17 offline queue MVP — retry/backoff, partial-batch failure UX, queue size limits, and re-evaluate whether face recognition or other online-only flows can get any offline affordance (see [mobile-requirements.md](mobile-requirements.md) Open Questions).
- **Deliverables:** TBD, scoped once Phase 17 ships and real usage patterns are known — do not over-design this speculatively.
- **Files affected:** `mobile/src/services/offlineQueue.ts` and callers.
- **Dependencies:** Phase 17.
- **Complexity:** Medium–High.
- **Acceptance criteria:** TBD at scoping time.

## Phase 23 — Mobile Profile, Build & Release, Testing

**Status:** Not started (GitHub #44, #45, #46 — bundled here the same way Phase 8/9 bundle testing/deployment for the web app rather than splitting per-feature)

- **Objectives:** MR-11 (profile view/edit), Expo EAS Build pipeline for iOS/Android, and a mobile test baseline.
- **Deliverables:** Profile screen; EAS Build config + store submission process; a `mobile/` test setup (framework TBD — likely Jest + React Native Testing Library, mirroring the web's not-yet-implemented Vitest plan in [testing.md](testing.md)).
- **Files affected:** `mobile/src/screens/Profile.tsx`, `mobile/eas.json`, `mobile/**/*.test.tsx`, `.github/workflows/` (mobile CI additions).
- **Dependencies:** Phase 16 (profile needs auth); build/release realistically wants most other phases substantially done first, but the *pipeline setup itself* can start as soon as Phase 15's scaffold exists.
- **Complexity:** Medium (store submission process, signing credentials) for build/release; Low for profile screen; Medium for establishing the test baseline from zero.
- **Acceptance criteria:** A signed build can be produced via EAS for both platforms; profile view/edit round-trips against `/api/auth/me/`; at least a smoke-test suite runs in CI for `mobile/`.
