# HANDOFF — Attendance Management System

> Last updated: 2026-08-06
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
| Google Drive (MIT account, consolidated) | https://drive.google.com/drive/folders/1Ntq3s7vrMrwNzAYcUl_oxsbyLCW53Mfm |
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

## Status: backend + frontend deployed; mobile foundation + auth built (Sprint 2 in progress)

Web app (backend + frontend) is feature-complete for the core scope (see [docs/prd.md](docs/prd.md#features--priorities)). Mobile app now has a working foundation and auth — Expo scaffold (PR #52, merged 2026-07-28), mobile auth screens (`106c262`), and the mobile-readiness backend (#36/#42, `2e30528`) — with attendance marking still pending for Sprint 2 "Mobile Core" (starts **2026-08-09**).

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
- **GitHub** (`origin`) is used for team visibility, issues, and PRs; **GitLab** (`gitlab`) drives the actual deploy pipeline. Both remotes are synced as of 2026-08-06 (`main` + `develop` on both; `main` push deploys to production).
- Mail/OTP secrets are synced from GitLab CI/CD masked variables into Azure App Service settings at deploy time — nothing secret is committed.

### Test status

Backend test suite runs in GitLab CI on every push to `main`/`develop` and on MRs (`python manage.py test`). **111 tests passing** as of 2026-08-06 — check the latest GitLab pipeline for the current count rather than trusting a cached number here.

---

## Pending work

### Session update — 2026-08-06

- **Merged `develop` → `main` and synced both remotes** (`7d22830`, `3f4f61d`). Committed the concurrent in-tree work (default model ordering + migrations, modal backdrop UX fixes, `run.sh` Linux launcher) as `f8f8313` and doc updates as `da3bee9`. Pushed `main` + `develop` to `origin` (GitHub) and `main` to `gitlab` — GitLab CI **pipeline #29** deployed the first batch to production; the mobile-readiness batch (#36/#42) landed via `2e30528` + merge `3f4f61d` and was pushed the same day. 111 backend tests, frontend lint/build, and mobile typecheck/lint all green before merge.
- **GitLab push credentials configured**: `credential.https://gitlab.com.helper store` + PAT in `~/.git-credentials` (mode 600) on Linux; same store-helper commands documented for the Windows machine. GitHub auth via `gh` untouched. **Rotate the PAT if it ever leaks** (it was shared in chat).
- **Google Sheets synced** (Master Tracker): `9. GitHub Issues` (#23 ECA → Done; #36/#42 → Done with code refs; #34/#35-46 updated), `34. Progress Dashboard` (Sprint 2 → 50%, auth done), `8. Sprint Board` (Sprint 2 50%), `21. Changelog` (added v0.2.0), `10. GitHub Pull Requests` (PR #52 + both develop→main merges). `docs/remaining-work-tracker.md` GitLab row → Done.

- **Mobile auth flow committed (`106c262`, `feat: add mobile auth flow (login, register, email OTP verification)`)**: completed + verified the in-progress mobile auth work. New `mobile/src/screens/auth/RegisterScreen.tsx` + `VerifyOtpScreen.tsx`; `LoginScreen.tsx`, `AuthContext.tsx`, `AuthNavigator.tsx`, `services/api.ts` extended. JWT tokens in SecureStore with auto-refresh interceptor; silent session restore on boot; role-based routing in `RootNavigator`. Typecheck + lint clean; contracts verified live against the running backend (register→login→me). Committed **only** the 6 mobile files — the concurrent uncommitted backend-model/`Meta.options` + migrations + frontend page changes in the tree were left untouched (another agent's work in progress).

- **Drive consolidation + cleanup completed**: all deliverables now live in one Google Drive folder on the MIT account (URL in the overview table above), including the new **"AMS - Resource Labeling Register"** sheet (33 resource rows, 10 columns, cost total 157,740 NPR from `Cost Estimation (AMS).md`). Team policy: the folder holds only word/google-doc + Google Sheet deliverables — no
  `.md`** (those live in GitHub/local). Converted `Cost Estimation (AMS).md` → native Google Doc
  `Cost Estimation (AMS)`, then moved **all 75 `.md` files** in the folder to Drive Trash
  (recoverable) and trashed the now-empty `docs/`, `Weekly Tasks/`, `frontend/`, `mobile/` folders.
  Kept: `Problem statement (AMS).docx`, `Cost Estimation (AMS)` (Google Doc), 5 sheets (Master
  Tracker, Risk & Dependencies, Resource Register, Project Tracker, SWOT), and `Guidelines/`
  (`.xlsx`, `.pdf`, `.csv`).
- **Google Sheets audit**: Master Tracker (34 tabs), Risk & Dependencies (6 tabs), and Resource
  Register are the live trackers; SWOT Analysis and the early Project Tracker sheet (11 tabs) are
  kept as deliverables. **Trashed**: "Attendance" (literal app test data), "Attendance Management
  System" (early agile planning, superseded by Master Tracker), "AMS Project Prompt and Planning"
  (AI-prompt scratch), and "Attendance Management System - Project Tracker.xlsx" (duplicate export
  of the Project Tracker sheet).

### Session update — 2026-08-05

- **Resolved a stuck `git merge` of `origin/develop` into `develop`** (9 files, `UU` conflicts) that was blocking all further work — every hunk resolved by keeping the side that was actually referenced/used elsewhere in the codebase (verified via grep, not guessed). 88 backend tests pass post-merge. Merge commit `f94029e`, pushed to `origin/develop` and `gitlab/develop` (the latter only runs tests on `develop`, no deploy — see CI/CD note below).
- **Found a systemic issue-data bug**: issues #17, #18, #19, #20, #21, #22, #24 all have a title that correctly matches shipped code, but an **Acceptance-Criteria body that belongs to a different issue** (looks like a shuffle from the original Google-Sheets → GitHub bulk import). Verified each real endpoint against `backend/dashboard/urls.py` and closed all 7 as backend-done (PR #30, covered by the 88-test suite) — comments on each issue explain the mismatch so nobody chases the stale AC text later. **#23 (ECA Tracking) has the same title/body mismatch but is genuinely unimplemented** (no model, no endpoint) — left open, comment added correcting it's assigned to `sar-kaar` (not Ekata as previously written here).
- **Closed #1** (Dashboard UI) — its 3 acceptance criteria (layout, widgets, charts) are all satisfied by the current `Dashboard.jsx`. **#48 stays open**, re-scoped down to its one remaining real gap: Master Data Bulk Import UI (backend done, no frontend yet).
- **#51 (Risk Management)** — left open (PM/course deliverable, not mine to close), but commented linking the risk sheet and noting R-07 was updated.
- **Updated the "AMS - User Story Dependencies & Risks" Google Sheet**: R-07 (`Risk Analysis` tab) moved Open → Mitigated with a corrected description. Note: W-08 in the `Personal & Work Risks` tab is a *different* risk (Azure Face verification) — this file previously conflated "R-07/W-08" as the same thing; they aren't. W-08 is still genuinely open.
- **Project Charter tech-stack fix — blocked, not done.** The doc (`Project Charter (AMS).gdoc`) is owned by Prizma with only public read access; no edit or comment permission available via API. Needs a direct ask to Prizma, not something an agent can action.
- **Verified #36/#38 mobile board-status mismatch is real** (via `gh project item-list 5 --owner sar-kaar`): both show "In Progress" for Sprint 2 (starts 2026-08-09) despite zero mobile code in the repo. Commented on #34 flagging it rather than silently changing the board — didn't want to guess whether work is happening outside this repo.
- **Did not touch**: `FACE_PROVIDER=azure` end-to-end verification (needs a real Azure resource, out of scope for a doc/issue-hygiene pass), retiring `Guidelines/03_PROJECT_TRACKER.csv` / the stale "Project Tracker" sheet (deferred, no strong reason to prioritize this session).

### Prizma (PM) — see Corrections above; GitHub says Done, verify for real

| Issue | Title | GitHub state | Reality |
|---|---|---|---|
| #7 | T-002: Requirements Gathering | Closed (board: Done) | Now has a real artifact (`docs/requirements-gathering.md`, written 2026-08-04) |
| #5 | T-003: SRS Document (IEEE 830) | Closed (board: Done) | Now has a real artifact (`docs/srs.md`, written 2026-08-04) |
| #11 | T-005: Wireframes and Mockups | Closed (board: Done) | Real: `wireframes/*.html` |
| #8 | T-007: Project Charter | Closed (board: Done) | Real, but tech-stack section is stale — needs a content fix. **Blocked**: no edit/comment access to the doc, needs Prizma directly (see session update above). |
| #12 | T-008: Team Norms and Comms Plan | Closed (board: Done) | Real: `Weekly Tasks/TEAM_SYNC_PROTOCOL.md` + `GIT_WORKFLOW.md` |
| #51 | Risk Management | **Open** | Produced the risk Google Sheet (see External Trackers link above) — left open, it's a PM/course deliverable, not mine to close |

### Frontend — still incomplete

| Issue | Title | Notes |
|---|---|---|
| #48 | RBAC-aware dashboard UI/UX (re-scoped 2026-08-05) | Open, narrowed to its one remaining gap: Master Data Bulk Import UI. #1 closed as satisfied/subsumed. |
| #23 | US-12: ECA Tracking | Open, assigned to `sar-kaar` (not Ekata). No backend model exists yet either (risk R-20/US-D7) — blocked on backend work first. |

### Mobile epic (GitHub #34, 12 sub-issues, project board)

Planning is complete (`docs/mobile-requirements.md`, `docs/mobile-architecture.md`, `docs/feature-matrix.md`, `docs/gap-analysis.md`, ADR-008). Sprint 2 "Mobile Core" starts 2026-08-09. No mobile code exists yet in this repo — #36/#38 board status flagged as likely stale, see session update above; not changed unilaterally.

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

1. **Fix the Project Charter's stale tech-stack section** (Node/MySQL → Django/DRF/PostgreSQL) — blocked on Prizma directly, no API access to her doc (see session update above).
2. Confirm with whoever's actually doing it whether #36/#38 (mobile) are genuinely underway before Sprint 2 starts 2026-08-09, or move the board status back to Todo.
3. Build the Master Data Bulk Import UI (#48's remaining scope) — file upload + dry-run preview against `POST /api/dashboard/master-data/import/`.
4. Design the ECA Tracking backend model (#23) — currently blocks any frontend work on that story.
5. Verify `FACE_PROVIDER=azure` end-to-end against a real Azure Face resource (risk R-11/W-08, still open).
6. Retire or refresh `Guidelines/03_PROJECT_TRACKER.csv` and the "Attendance Management System - Project Tracker" Google Sheet — both stale, unmaintained since day 2 of the project (see `docs/memory.md` External Trackers).
7. Decide on a `gitlab main` push/merge — this is the one that triggers a real Azure production deploy, needs an explicit deliberate go-ahead (unlike `develop`, which was pushed this session and only runs tests).

---

## Prior session log

Earlier session-by-session debug notes (dlib install, `.gitignore` fix, file-location fix, Google Sheets → GitHub issue generation, architecture diagrams) have been trimmed from this file now that all of that work is long resolved and merged. See git history (`git log -- HANDOFF.md`) for the full archive if needed.
