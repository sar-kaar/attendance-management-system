# HANDOFF — Attendance Management System

> Last updated: 2026-08-04
> **Canonical status doc is [docs/memory.md](docs/memory.md) per ADR-007** — this file is a human-facing session handoff, kept in sync with it but memory.md wins on any disagreement.

---

## Project Overview

| Field | Value |
|---|---|
| Course | CSE 405 Software Project Management |
| GitHub repo | https://github.com/sar-kaar/attendance-management-system |
| GitHub Project board | https://github.com/users/sar-kaar/projects/5 ("Attendance Management System", 23 items) |
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

## Status: backend + frontend both substantially built and deployed; mobile is planned, not started

Web app (backend + frontend) is feature-complete for the core scope (see [docs/prd.md](docs/prd.md#features--priorities)). Mobile app is fully planned (12-issue epic on the project board) but has zero code — Sprint 2 "Mobile Core" is scheduled to start **2026-08-09**.

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
| Attendance Report | `/api/attendance/report/` | Done — `course`/`student`/`date` filters all verified working (see Corrections below) |
| Attendance Export (CSV/PDF) | `/api/attendance/export/csv/`, `/export/pdf/` | Done |
| Attendance Codes | `/api/attendance/codes/` | Done (US-14) |
| Face Recognition | `/api/face/` | Done — provider-selectable: local `dlib` or Azure AI Face API (`FACE_PROVIDER` env var). **Azure path still unverified end-to-end against a real Azure resource** (open risk R-11/W-08). |
| Dashboard | `/api/dashboard/*` (US-06 to US-13, PR #30) | Done, backend-complete. Frontend Dashboard UI is the main open gap — see #1 and #48 below. |

### Recent work (this session, 2026-08-04)

- **Fixed `docs/memory.md`**: it had unresolved git merge-conflict markers (`<<<<<<<`/`=======`/`>>>>>>>`) committed into the file since `bcd18cc`, which had caused it to tell two contradictory stories about whether the attendance-report filter was a real bug. Re-verified against code: it is **not** a bug — `AttendanceViewSet.report()` calls `get_queryset()`, which already applies `course`/`student`/`date` filtering — resolved and documented.
- **Wrote `docs/srs.md`** (SRS, IEEE 830 format) and **`docs/requirements-gathering.md`** — these did not exist as artifacts before today, despite GitHub issues #5/#7 being marked closed since 2026-07-30 (see Corrections below).
- **Added a Credential Inventory & Deployment Continuity section to `docs/deployment.md`** — addresses risk P-01/P-02 (Abhishek as sole holder of all Azure/CI credentials) with a documented backup-access runbook.
- **Reviewed all three external Google Sheets trackers** and cross-linked them from `docs/memory.md` (see External Trackers section there). The most current/detailed is **"AMS - User Story Dependencies & Risks"**: https://docs.google.com/spreadsheets/d/1BRHCixRfskt6hvGgwYHx0g14h1ZX58ru2uIgd7bozn8 — dependency chains, a 33-item technical risk register (R-01–R-33), a full user-story status matrix, and a team/process risk register (P-01–P-10, W-01–W-12). It was created 2026-07-27, the same day GitHub issue **#51 "Risk Management"** was opened — #51 is the course-assignment prompt that produced this sheet.
- Commit: `609e475` — `docs: add SRS and requirements-gathering docs, fix memory.md conflict markers` (pushed to GitHub `origin`; **not yet pushed to GitLab**, see Corrections below).

### Corrections found this session (documentation vs. reality had drifted)

1. **PM deliverables status was wrong everywhere** (this file, `NEXT_STEPS.md`, `docs/memory.md` all previously said overdue/not-started): GitHub issues **#5 (SRS), #7 (Requirements Gathering), #8 (Charter), #9 (DB Schema), #10 (System Architecture), #11 (Wireframes), #12 (Team Norms), #6 (Repo Setup)** are all **CLOSED**, and all show **"Done"** on the GitHub Project board under "Sprint 1 - Planning" — closed 2026-07-30, in a single batch, with **zero comments and no linked PR** on any of them. Cross-checking each:
   - **Charter** — genuinely exists: `Project Charter (AMS).gdoc` at repo root, a real Google Doc with PACT/SWOT/PESTLE analysis. Its Technologies section is stale (lists Node.js/Express/MySQL; actual stack is Django/DRF/PostgreSQL) — needs a content fix, not a rewrite.
   - **Team Norms** — genuinely exists: `Weekly Tasks/TEAM_SYNC_PROTOCOL.md` + `Weekly Tasks/GIT_WORKFLOW.md`.
   - **Wireframes** — genuinely exists: `wireframes/*.html`.
   - **DB Schema / System Architecture** — genuinely exists: `docs/database-schema.md`, `docs/architecture.md`, `docs/er-diagram.md`.
   - **SRS and Requirements Gathering** — **did not exist as artifacts** anywhere (repo or Drive) until written this session (2026-08-04), five days after the issues were closed. These two were likely closed prematurely/administratively without an attached deliverable. They're covered now (`docs/srs.md`, `docs/requirements-gathering.md`), but flag this pattern to Prizma — closing an issue isn't the same as completing the deliverable.
2. **`develop` vs `origin/develop` (GitHub)**: in sync as of this session (0 commits either direction after this session's push).
3. **`develop` vs `gitlab/develop`**: **`develop` is 7 commits ahead of GitLab**, unpushed. GitLab is what actually drives the deploy pipeline (see `docs/deployment.md`) — production is running code from before those 7 commits. Recommend pushing to `gitlab` deliberately (it triggers a real Azure deploy), not as a routine git-hygiene step.
4. **Project board "In Progress" mismatch**: issues #36 (Backend Readiness for Mobile) and #38 (Mobile Attendance Marking) show status **"In Progress"** on the board, but the actual repo has **zero mobile code** — only planning docs (`docs/mobile-*.md`). Either the board status is stale, or work has started outside this repo/branch — worth confirming with whoever owns those cards before Sprint 2 starts (2026-08-09).

---

## Deployment

- **Host**: Azure App Service `ams-backend` (resource group `ams-rg`), frontend static assets to storage account `amsfrontendweb`.
- **CI/CD**: GitLab CI (`.gitlab-ci.yml`) — tests run on `main`, `develop`, and merge requests; frontend build + backend deploy run only on `main`. See `docs/deployment.md` for the full pipeline and, as of this session, a credential-inventory/continuity runbook.
- **GitHub** (`origin`) is used for team visibility, issues, and PRs; **GitLab** (`gitlab`) drives the actual deploy pipeline. Both remotes are meant to be kept in sync manually — currently 7 commits out of sync (see Corrections above).
- Mail/OTP secrets are synced from GitLab CI/CD masked variables into Azure App Service settings at deploy time — nothing secret is committed.

### Test status

Backend test suite runs in GitLab CI on every push to `main`/`develop` and on MRs (`python manage.py test`). 75+ tests passing as of the 2026-07-26 ruff/hygiene pass — check the latest GitLab pipeline for the current count rather than trusting a cached number here.

---

## Pending work

### Prizma (PM) — see Corrections above; GitHub says Done, verify for real

| Issue | Title | GitHub state | Reality |
|---|---|---|---|
| #7 | T-002: Requirements Gathering | Closed (board: Done) | Now has a real artifact (`docs/requirements-gathering.md`, written 2026-08-04) |
| #5 | T-003: SRS Document (IEEE 830) | Closed (board: Done) | Now has a real artifact (`docs/srs.md`, written 2026-08-04) |
| #11 | T-005: Wireframes and Mockups | Closed (board: Done) | Real: `wireframes/*.html` |
| #8 | T-007: Project Charter | Closed (board: Done) | Real, but tech-stack section is stale — needs a content fix |
| #12 | T-008: Team Norms and Comms Plan | Closed (board: Done) | Real: `Weekly Tasks/TEAM_SYNC_PROTOCOL.md` + `GIT_WORKFLOW.md` |
| #51 | Risk Management | **Open** | Produced the risk Google Sheet (see External Trackers link above) — issue itself is still open even though the deliverable behind it exists |

### Ekata (Frontend) — still incomplete

| Issue | Title | Notes |
|---|---|---|
| #1 | US-10: Dashboard UI | Open. Overlaps with #48 (RBAC-aware dashboard UI/UX, board status "In Progress", Sprint 5) — confirm these two aren't duplicate/conflicting scope before both are worked. |
| #23 | US-12: ECA Tracking | Open. No backend model exists yet either (risk R-20/US-D7) — this is blocked on backend work, not purely a frontend task. |

### GitHub issue hygiene (long-standing, still not acted on)

- PR #30 (*"Dashboard API — US-06 to US-13"*, merged 2026-07-18) implemented the backend for issues **#19 (US-06), #17 (US-07), #18 (US-08), #20 (US-09), #21 (US-11), #22 (US-13)** but none were closed — still open as of 2026-08-04. Recommend closing once confirmed working against live `/api/dashboard/*`.
- Two open issues both titled "US-10": **#1** (Dashboard UI, frontend, genuinely open) and **#24** (Chronic Latecomers Detection, backend, actually done via PR #30, not yet closed). Numbering collision, not urgent, but confusing in triage.

### Mobile epic (GitHub #34, 12 sub-issues, project board)

Planning is complete (`docs/mobile-requirements.md`, `docs/mobile-architecture.md`, `docs/feature-matrix.md`, `docs/gap-analysis.md`, ADR-008). Sprint 2 "Mobile Core" starts 2026-08-09. No mobile code exists yet in this repo — see the board-status mismatch flagged in Corrections above before assuming #36/#38 are actually underway.

---

## Architecture notes

- **Database**: SQLite (local dev) / PostgreSQL (production, via `DATABASE_URL`).
- **Auth**: SimpleJWT (access + refresh) + email OTP verification (Brevo SMTP) + Google/Facebook social sign-in.
- **User model**: custom `accounts.User` with roles: `admin`, `faculty`, `student`.
- **Face recognition**: `FACE_PROVIDER` env var selects `local` (dlib/face_recognition, no network call) or `azure` (Azure AI Face API, needs `AZURE_FACE_ENDPOINT` / `AZURE_FACE_KEY` / `AZURE_FACE_PERSON_GROUP`). Local is the default; Azure path not yet verified end-to-end (see Corrections above and risk R-11).
- **Seed data**: `python manage.py seed_data`.
- **Static files**: WhiteNoise (backend) / Azure storage (frontend build).

---

## Next steps

1. **Decide on and execute a GitLab push** — `develop` is 7 commits ahead of `gitlab/develop`; pushing triggers a real Azure deploy on `main`, so do this deliberately, not blindly.
2. Verify #36/#38 board "In Progress" status against actual work — either update the board or confirm work is genuinely underway somewhere not reflected in this repo.
3. Close the stale-but-implemented dashboard issues (#19, #17, #18, #20, #21, #22, #24) after a sanity check against `/api/dashboard/*`.
4. Reconcile #1 (Dashboard UI) and #48 (RBAC-aware dashboard UI/UX) — confirm they're not overlapping/duplicate scope before Ekata works either.
5. Chase Ekata on US-12 (ECA Tracking, #23) — also needs a backend model first (currently no owner for that half).
6. Fix the Project Charter's stale tech-stack section (Node/MySQL → Django/DRF/PostgreSQL).
7. Verify `FACE_PROVIDER=azure` end-to-end against a real Azure Face resource (risk R-11/W-08, still open).
8. Retire or refresh `Guidelines/03_PROJECT_TRACKER.csv` and the "Attendance Management System - Project Tracker" Google Sheet — both stale, unmaintained since day 2 of the project (see `docs/memory.md` External Trackers).
9. Update the "AMS - User Story Dependencies & Risks" sheet: R-07/W-08 (report filter) should move from "Open" to "Mitigated" now that it's confirmed not a bug.

---

## Prior session log

Earlier session-by-session debug notes (dlib install, `.gitignore` fix, file-location fix, Google Sheets → GitHub issue generation, architecture diagrams) have been trimmed from this file now that all of that work is long resolved and merged. See git history (`git log -- HANDOFF.md`) for the full archive if needed.
