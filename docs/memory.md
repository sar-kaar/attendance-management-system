# Project Memory — Attendance Management System

> **Purpose:** Persistent, living project status for both humans and AI coding agents. **Update this file after every major implementation.**
> **Scope:** Current state only — historical narrative belongs in `HANDOFF.md` (session logs) or [decisions.md](decisions.md) (why a decision was made), not here.
> **Last updated:** 2026-08-06 · **Version:** 2.0 (see [decisions.md](decisions.md) ADR-007 for why this file exists and supersedes older status docs)

## Table of Contents

- [Project Status](#project-status)
- [Completed Features](#completed-features)
- [Pending Features](#pending-features)
- [Known Bugs / Open Issues](#known-bugs--open-issues)
- [Technical Debt](#technical-debt)
- [Recent Decisions](#recent-decisions)
- [Files Modified / Created This Effort](#files-modified--created-this-effort)
- [Current Branch Status](#current-branch-status)
- [Current Priorities](#current-priorities)
- [Next Recommended Tasks](#next-recommended-tasks)
- [Important Implementation Notes](#important-implementation-notes)
- [External Trackers](#external-trackers)

## Project Status

Backend and frontend are **both substantially built and deployed** (Azure App Service + Azure Storage static site). This is ahead of the original course week-by-week plan (`Guidelines/01_WEEKLY_ROADMAP.md`, `Guidelines/03_PROJECT_TRACKER.csv` — both stale, do not treat as current). As of 2026-07-26, the engineering-hygiene pass (this `docs/` set + root config files) is the active work.

## Completed Features

- Auth: register, JWT login/refresh, email OTP verification (Brevo SMTP), Google/Facebook social sign-in, admin user management.
- **Mobile-readiness backend (2026-08-06, #36/#42)**: refresh-token rotation + blacklist + `POST /api/auth/logout/`; new `notifications` app — `Device` model, `POST /api/devices/register/`, `/unregister/`, `GET /api/devices/`, provider-gated push service (`PUSH_PROVIDER=console|expo`), and an absence-push hook in `AttendanceViewSet`. 111 tests passing. Remaining B8–B10 (API versioning, CORS review, mobile contract doc) tracked in [remaining-work-tracker.md](remaining-work-tracker.md).
- **Default model ordering (2026-08-06)**: added `Meta.ordering` to `Student`/`Course`/`Enrollment`/`Attendance` (migrations `students/0007`, `courses/0004`, `attendance/0005`) to fix `UnorderedObjectListWarning` and make pagination deterministic.
- Students, Courses, Enrollments: full CRUD, role-gated.
- Attendance: manual + bulk marking (enrollment-enforced), attendance codes (self-check-in), report query + CSV/PDF export.
- Face recognition: register/recognize/mark-attendance, pluggable `FACE_PROVIDER` (`local` dlib or `azure` Azure AI Face API).
- Dashboard (backend): programs, sections, student search, per-student breakdown, attendance stats, at-risk detection, faculty performance, chronic-latecomer detection, incomplete-record detection, master-data bulk import.
- CI/CD: GitLab CI (test → build → deploy to Azure on `main`), GitHub Actions (test mirror on `develop`).
- This documentation set: `docs/{prd,architecture,design,rules,phases,memory,api,testing,deployment,decisions,security,contributing,tech-stack,package-guidelines,coding-standards,api-standards,database-standards,testing-strategy,security-standards,cicd,versioning,release-process,development-guide}.md` — the full 22-doc engineering foundation, per [rules.md](rules.md) Documentation policy.
- Repo hygiene: removed committed-nowhere secret files and cache/log noise from the working tree (see Files Modified/Created below).
- **Phase 1 — Repository Stabilization (2026-07-26)**: audited backend (`manage.py check` clean, `makemigrations --check --dry-run` clean — no schema drift) and frontend (`vite build` succeeds; only a non-blocking >500kB chunk-size advisory, not an error). Removed genuine dead code flagged by ESLint `no-unused-vars`: unused `enrolledStudents` state (setter was called but the value was never read), unused `studentAPI`/`FaDownload` imports in `frontend/src/pages/Attendance.jsx`, and unused `FaUserCircle` import in `frontend/src/pages/StudentDashboard.jsx`. Lint errors dropped from 15 to 11.
- **Phase 1 follow-up — lint error suppression (2026-07-26)**: resolved the remaining 11 ESLint errors (`react-hooks/set-state-in-effect` x8, `react-refresh/only-export-components` x3) with targeted `eslint-disable-next-line` comments, each carrying a short reason, at every flagged line — user's explicit decision, chosen over restructuring the effect/export patterns (would touch behavior-adjacent code across 8+ files) or disabling the rules globally (would silence the rules for genuinely new bugs too). Zero behavior change; verified via `eslint .` (0 errors, 2 pre-existing unrelated `exhaustive-deps` warnings remain, untouched) and `vite build` (still succeeds). Lint errors now at 0.
- **Backend `ruff` added (2026-07-26)**: `backend/pyproject.toml` (config: line-length 100, `E`/`F`/`W`/`I` rules, `E501` ignored, `migrations/` excluded) + `backend/requirements-dev.txt` (dev-only, `ruff` pinned). Initial run found 71 issues; auto-fixed 67 safe ones (`I001` unsorted imports, `F401` unused imports, `W292` missing EOF newline). Manually cleaned 3 more dead-code `F841` unused-variable findings (`accounts/tests.py`, `attendance/tests.py` — unused test-fixture assignments, values only needed for their side effect) and renamed an `E741` ambiguous variable `l`→`line` in `backend/scripts/inventory_sources.py`. `ruff check .` now runs in both `.gitlab-ci.yml` and `.github/workflows/ci.yml` (pip cache keys updated to also hash `requirements-dev.txt`). Verified with `manage.py check`, `makemigrations --check --dry-run`, and the full test suite (75 tests, all passing).
- **Admin User Management + role-aware Dashboard (2026-08-04)**: `frontend/src/pages/Users.jsx` (new) consumes the previously-frontend-orphaned `AdminUserViewSet` (`/api/auth/users/`) — list/filter by role, create, edit, delete, reset password (via a local modal, not `window.prompt`, per ADR-06). Wired to a new admin-only `/dashboard/users` route and a role-filtered `DashboardLayout` nav (`navItems[].roles`). `Dashboard.jsx` now relabels stat cards/title based on `user.role` ("My Students"/"My Courses"/"My Dashboard" for faculty) and surfaces the previously-unused Faculty Performance endpoint (#18) as a panel. Verified end-to-end in a real browser (admin + faculty test logins, create/delete flow, route-guard redirect). Addresses most of #48's concrete gaps except Master Data Bulk Import UI (#21), left as a follow-up.
- **`AttendanceViewSet.report` filter dead-code resolved (2026-07-26)**: the 2 `F841` findings from the ruff pass (`course_id`, `student_id` local vars in `report()`) were initially suspected to be a real filtering bug, but tracing the call showed `report()` calls `self.get_queryset()`, which already reads and applies the same `course`/`student`/`date` query params (`backend/attendance/views.py` `get_queryset()`). So the two local vars were genuinely dead — redundant reads, not a bug. Removed them and added a one-line comment explaining why, plus two regression tests (`test_report_filters_by_course`, `test_report_filters_by_student` in `backend/attendance/tests.py`) that lock in the already-correct filtering behavior so it can't silently regress.
- **Mobile auth flow (Phase 16, 2026-08-06, commit `106c262`)**: mobile/ now has working login, register, and email-OTP verification screens. JWT access/refresh tokens persist in `expo-secure-store`; a 401 response interceptor auto-refreshes the token; `AuthContext` restores the session silently on boot and `RootNavigator` renders the role-appropriate tab shell (student/faculty). API contracts verified live against the backend: `register` (student role), `login` (SimpleJWT pair), `me` (role field), `otp/send` + `otp/verify` (`email_verification` purpose). Typecheck (`tsc --noEmit`) and lint (`eslint .`) both clean. Note: OTP email delivery itself needs the Brevo SMTP creds (present in `backend/.env`); without them the register→verify flow still proceeds and surfaces a resend option, mirroring the web frontend.

## Pending Features

| Feature | Owner | Tracking |
|---|---|---|
| Master Data Bulk Import UI (file upload + dry-run preview) | Ekata | GitHub #1 **closed 2026-08-05** (acceptance criteria satisfied by current `Dashboard.jsx`); remaining scope now tracked as **#48**, re-scoped down to just this one gap. Backend (`POST /api/dashboard/master-data/import/`) already done. |
| ECA (extra-curricular activity) tracking | Ekata (frontend) | GitHub #23 (US-12) — **backend done & migrated 2026-08-06** (`ECAActivity` model + `Attendance.eca_activity`, migrations 0004/0005); remaining is the frontend list/assign UI, assigned to Ekata. On board (In Progress). |
| Notifications — mobile push | sar-kaar (backend done) / mobile client pending | GitHub #42 — **backend shipped 2026-08-06**: `notifications` app (Device model, register/unregister/list endpoints, provider-gated push service), absence-push hook. Mobile client remains. See [remaining-work-tracker.md](remaining-work-tracker.md). |
| Notifications (email/SMS) | Unassigned | Phase 7, not started, see [phases.md](phases.md) |
| SRS Document (IEEE 830) | Prizma | GitHub #5 (T-003) — **closed on GitHub since 2026-07-30** (board: Done), but no artifact existed until **drafted 2026-08-04**, see [srs.md](srs.md); needs Prizma/team review |
| Requirements Gathering doc | Prizma | GitHub #7 (T-002) — **closed on GitHub since 2026-07-30** (board: Done), but no artifact existed until **drafted 2026-08-04**, see [requirements-gathering.md](requirements-gathering.md); needs Prizma/team review |
| Wireframes and Mockups (formal) | Prizma | GitHub #11 (T-005) — closed, board: Done; genuinely exists as `wireframes/*.html` |
| Project Charter | Prizma | GitHub #8 (T-007) — closed, board: Done; **already exists** as a Google Doc (`Project Charter (AMS).gdoc` shortcut at repo root, PACT/SWOT/PESTLE analysis complete), but its Technologies section is stale (lists Node.js/Express/MySQL; actual stack is Django/DRF/PostgreSQL per [tech-stack.md](tech-stack.md)) — needs a content update, not a rewrite |
| Team Norms and Comms Plan | Prizma | GitHub #12 (T-008) — closed, board: Done; **already substantially covered** by `Weekly Tasks/TEAM_SYNC_PROTOCOL.md` (daily standup format, escalation process, EOD logging) and `Weekly Tasks/GIT_WORKFLOW.md` (branch/PR/commit conventions) |
| Risk Management writeup | Prizma | GitHub **#51 — still open** (left open deliberately, it's a PM/course deliverable), opened 2026-07-27, the same day the "AMS - User Story Dependencies & Risks" sheet (see External Trackers below) was created — that sheet is the deliverable behind this issue |

> **Note (2026-08-04):** #5, #7, #8, #11, #12 were all closed on GitHub in a single batch on 2026-07-30 with zero comments and no linked PR on any of them. For #8/#11/#12 a real artifact genuinely exists elsewhere (verified above). For #5/#7, no artifact existed anywhere until this session wrote them — those two issues were likely closed administratively without an attached deliverable. Don't trust "issue closed" as proof of "deliverable exists" without checking, going forward.

## Known Bugs / Open Issues

- **Social login buttons missing on the live site (found 2026-08-04)**: `SocialLogin.jsx` renders nothing (`if (!configured) return null`) unless `VITE_GOOGLE_CLIENT_ID`/`VITE_FACEBOOK_APP_ID` are set at `npm run build` time. `.gitlab-ci.yml`'s `build-frontend` job never set them, and `backend/scripts/push_gitlab_vars.py`/`stage_gitlab_vars.py` never pushed them to GitLab CI/CD variables in the first place — only the backend-side `GOOGLE_CLIENT_ID`/`FACEBOOK_APP_ID` were ever created. Fixed: both scripts now also emit `VITE_GOOGLE_CLIENT_ID`/`VITE_FACEBOOK_APP_ID` (same public values, duplicated under the Vite-prefixed name), and `.gitlab-ci.yml`'s `build-frontend` job now passes them through explicitly with a build-time warning if unset. **Action still needed**: run `python backend/scripts/push_gitlab_vars.py` (requires `GITLAB_TOKEN` and the local credential source files) to actually create the two new GitLab CI/CD variables, or add them manually in GitLab → Settings → CI/CD → Variables using the same values already in `GOOGLE_CLIENT_ID`/`FACEBOOK_APP_ID`. Until that's done, the next frontend deploy will still ship without social login.

- **Issue title/AC-body mismatch bug (found + fixed 2026-08-05)**: issues #17, #18, #19, #20, #21, #22, #23, #24 all had a correct title matching shipped code, but an Acceptance-Criteria body copied from a *different* issue — a bulk-import artifact from the original Google-Sheets → GitHub issue generation. All 7 implemented ones (#17–#22, #24) closed with a comment explaining the mismatch (verified against `backend/dashboard/urls.py`, not the stale AC text); #23 (ECA Tracking) left open since it's genuinely unimplemented. If anyone reads an AC body on one of these issues going forward, don't trust it literally — check the title against real code instead.
- **Azure Face provider unverified end-to-end**: `FACE_PROVIDER=azure` is implemented (`backend/face/providers.py`) but only exercised locally, not against a real Azure Face resource in an end-to-end run.
- **`Guidelines/REALITY_CHECK.md` and `Guidelines/03_PROJECT_TRACKER.csv` are stale** — the former claims no frontend exists (false); the latter still shows Sprint 1 in progress. Both are kept for historical/course-deliverable purposes but must not be treated as current status. `HANDOFF.md` also flags this.
- **`docs/system-architecture.md`** predates the `face` and `dashboard` apps and the working CI/CD — `docs/architecture.md` (this effort) is now the current reference; `system-architecture.md`'s Mermaid diagrams/SVGs are kept for the parts still accurate (core auth/attendance flow) but the app/endpoint lists there are outdated.

## Technical Debt

- ~~No Python linter configured for `backend/`~~ — resolved 2026-07-26: `ruff` added and CI-enforced in both `.gitlab-ci.yml` and `.github/workflows/ci.yml` (see Completed Features and Files Modified/Created).
- ~~Bug found by the ruff pass~~ — re-investigated 2026-07-26 and reclassified: not a bug. `report()`'s `qs = self.get_queryset()` call already applies `course`/`student` filtering (via `get_queryset()`'s own query-param handling), so the two local vars were dead code, not a missing filter. Resolved — see Completed Features. (This superseded an earlier draft of this note that called it an unfixed bug; that draft was committed by mistake alongside unresolved merge-conflict markers and cleaned up 2026-08-04. The risk register's R-07 was updated to "Mitigated" on 2026-08-05.)
- No frontend automated test suite (Vitest/RTL not set up) — see [testing.md](testing.md).
- No coverage gate in CI (backend tests run, but no minimum-coverage enforcement).
- `Student` (in `students` app) and `accounts.User` (role=`student`) are not FK-linked — a design gap noted in `docs/database-schema.md`, not yet resolved.
- No centralized design tokens/color palette/breakpoint scale on the frontend (see [design.md](design.md)) — each stylesheet is independent.
- No monitoring/structured logging beyond Azure's default App Service log stream (see [deployment.md](deployment.md)).
- **2 `react-hooks/exhaustive-deps` warnings remain** (`Attendance.jsx`, `Students.jsx`) — pre-existing, missing-dependency warnings on fetch-on-mount effects, not addressed by the lint-error suppression pass below (warnings, not errors; out of that task's scope).
- ~~11 ESLint errors (`react-hooks/set-state-in-effect`, `react-refresh/only-export-components`)~~ — resolved 2026-07-26 via targeted `eslint-disable-next-line` comments (see Files Modified/Created and Completed Features). If `eslint-plugin-react-hooks`/`eslint-plugin-react-refresh` are upgraded later and these rules' behavior changes, re-check whether the suppressions are still the right call.

## Recent Decisions

See [decisions.md](decisions.md) for full ADRs. Most recent: ADR-007 (this memory doc supersedes `HANDOFF.md`/tracker docs as the status source of truth, 2026-07-26).

## Files Modified / Created This Effort

**Created** (all additive, no existing files deleted or application code touched):

- `docs/prd.md`, `docs/architecture.md`, `docs/design.md`, `docs/rules.md`, `docs/phases.md`, `docs/memory.md` (this file), `docs/api.md`, `docs/testing.md`, `docs/deployment.md`, `docs/decisions.md`
- `docs/security.md`, `docs/contributing.md` — closed the two gaps this file's own audit flagged.
- `docs/tech-stack.md`, `docs/package-guidelines.md`, `docs/coding-standards.md`, `docs/api-standards.md`, `docs/database-standards.md`, `docs/testing-strategy.md`, `docs/security-standards.md`, `docs/cicd.md`, `docs/versioning.md`, `docs/release-process.md`, `docs/development-guide.md` — enterprise engineering-foundation pass (2026-07-26, second session): final tech stack with rationale, planned `packages/` boundaries (design only, not implemented), and standards for coding/API/DB/testing/security/CI-CD/versioning/release/workflow. Each cross-references rather than duplicates the operational docs above (e.g. `security-standards.md` is the rule set, `security.md` stays the status/gap report).
- `.editorconfig`, `.prettierrc`, `.prettierignore`, `.gitattributes` (root)

**2026-08-06 session — Drive consolidation + cleanup**:

- Consolidated project docs + Google Sheets into a single Drive folder on the MIT account and
  recorded the URL in the External Trackers section below. Added the "AMS - Resource Labeling
  Register" sheet (resource/cost register, 33 rows, from `Cost Estimation (AMS).md`, total
  157,740 NPR).
- **Drive policy set by the team (2026-08-06): the folder holds only word/google-doc + Google Sheet
  deliverables — no `.md` files** (they live in GitHub/local). Applied it fully: converted
  `Cost Estimation (AMS).md` → native Google Doc `Cost Estimation (AMS)` in the folder, then moved
  **all 75 remaining `.md` files to Drive Trash** (root README/AGENTS/HANDOFF/Cost Estimation +
  all 33 in `docs/` + 10 in `Guidelines/` + 25 in `Weekly Tasks/` + `frontend/README.md` +
  `mobile/AGENTS.md`/`README.md`) and trashed the now-empty `docs/`, `Weekly Tasks/`, `frontend/`,
  `mobile/` folders. Everything is recoverable from Drive Trash and remains in git locally.
  Kept in the folder: `Problem statement (AMS).docx`, `Cost Estimation (AMS)` (Google Doc),
  5 sheets (Master Tracker, Risk & Dependencies, Resource Register, Project Tracker, SWOT), and
  `Guidelines/` (`Sample of Last session_Project.xlsx`, `Course Syllabus CSE 405.pdf`,
  `03_PROJECT_TRACKER.csv`).
- Also trashed (team-confirmed 2026-08-06): "Attendance" (literal app test data), "Attendance
  Management System" (early agile planning, superseded by the Master Tracker), "AMS Project Prompt
  and Planning" (AI-prompt scratch), and "Attendance Management System - Project Tracker.xlsx"
  (duplicate export of the Project Tracker Google Sheet). The early "Attendance Management System -
  Project Tracker" **Google Sheet** (11 tabs) itself was kept as a historical deliverable.

**Modified (2026-08-05 session — cross-system doc/sheet completeness pass)**:

- `AGENTS.md` — rewrote the Startup Workflow: fixed the stale "HANDOFF.md is source of truth" claim (it's `docs/memory.md`, per ADR-007), added explicit phases for checking GitHub Issues/Project board and both Google Sheets, added a "Golden rule" (trust code over docs). Updated Documentation Rules to cover `memory.md` and the sheets, not just `HANDOFF.md`.
- Master Tracker Google Sheet — updated tabs: "1. Project Overview" (progress/sprint/phase), "34. Progress Dashboard" (real sprint completion, added a note that the sprint model is mobile-centric and doesn't capture the already-complete web MVP), "3. Functional Requirements" (corrected 4 rows from stale "Planned" to "Completed", added 2 missing rows), "20. Bug Tracker" (replaced 3 unverifiable placeholder bugs with a note + added 3 real, verified entries), "26. Dependencies" (was Flutter/Firebase from an abandoned plan — replaced with the real Django/DRF + React + Expo dependency list, corrected to match ADR-008), "9. GitHub Issues" (was empty — added a live snapshot), "31. AI Task Tracker" (was one stale row — added real completed-work history), "33. Agent Instructions" (was a 4-row generic placeholder — rewritten as the canonical cross-system onboarding doc, see External Trackers below).
- Risk Google Sheet, "Risk Mitigation Plan" tab — R-07 status corrected from "Open" to "Mitigated" (this tab hadn't been updated even though the sibling "Risk Analysis" tab had been); added new row R-34 for the social-login-missing-in-production bug.

**Created (2026-08-04 session — overdue PM deliverables + risk/docs cleanup)**:

- `docs/srs.md` — Software Requirements Specification, IEEE 830 format, derived from `prd.md`/`architecture.md`/`database-schema.md` and cross-checked against actual code.
- `docs/requirements-gathering.md` — requirements elicitation methodology, stakeholder list, and traceability; documents an honest gap (no formal faculty/student interviews were conducted).
- Fixed unresolved git merge-conflict markers (`<<<<<<<`/`=======`/`>>>>>>>`) that had been committed into this file since `bcd18cc` — resolved in favor of the accurate content (the `AttendanceViewSet.report` filter "bug" was re-verified as already fixed, not open).
- Added the "External Trackers" section below, cross-referencing the three project-tracking Google Sheets found in Drive.
- Added a "Credential Inventory & Deployment Continuity" section to `docs/deployment.md`, addressing risk P-01/P-02 (single point of failure on Azure/CI credentials).

**Modified**:

- `frontend/src/pages/Attendance.jsx` — removed unused `enrolledStudents` state/setter and unused `studentAPI`/`FaDownload` imports (Phase 1, 2026-07-26); added `eslint-disable-next-line react-hooks/set-state-in-effect` on the fetch-on-filter-change effect (Phase 1 follow-up, 2026-07-26).
- `frontend/src/pages/StudentDashboard.jsx` — removed unused `FaUserCircle` import (Phase 1, 2026-07-26).
- `frontend/src/context/AuthContext.jsx` — added `eslint-disable-next-line react-hooks/set-state-in-effect` (initial auth-check effect) and `eslint-disable-next-line react-refresh/only-export-components` (on `useAuth` export) (Phase 1 follow-up, 2026-07-26).
- `frontend/src/context/NotificationContext.jsx` — added `eslint-disable-next-line react-refresh/only-export-components` on the `formatApiError` and `useNotify` exports (Phase 1 follow-up, 2026-07-26).
- `frontend/src/layouts/DashboardLayout.jsx` — added `eslint-disable-next-line react-hooks/set-state-in-effect` on the route-change drawer-close effect (Phase 1 follow-up, 2026-07-26).
- `frontend/src/pages/AttendanceCodes.jsx`, `Courses.jsx`, `Students.jsx` — added `eslint-disable-next-line react-hooks/set-state-in-effect` on each fetch-on-mount effect (Phase 1 follow-up, 2026-07-26).
- `frontend/src/pages/Enrollments.jsx` — added `eslint-disable-next-line react-hooks/set-state-in-effect` on the fetch-on-filter-change effect, alongside the pre-existing `exhaustive-deps` disable (Phase 1 follow-up, 2026-07-26).
- `frontend/src/pages/FaceRecognition.jsx` — added `eslint-disable-next-line react-hooks/set-state-in-effect` on the search-results-clear effect (Phase 1 follow-up, 2026-07-26).
- `backend/accounts/tests.py`, `backend/attendance/tests.py` — dropped unused variable assignments on side-effect-only test fixture calls (ruff `F841`, 2026-07-26).
- `backend/scripts/inventory_sources.py` — renamed ambiguous variable `l` to `line` (ruff `E741`, 2026-07-26).
- 13 backend files across `accounts/`, `attendance/`, `courses/`, `dashboard/`, `face/`, `students/`, `config/` — ruff `--fix` applied: import sorting/grouping and removal of unused imports, no logic changes (2026-07-26).

**Created** (backend tooling, 2026-07-26): `backend/pyproject.toml`, `backend/requirements-dev.txt`.

(Prior to Phase 1, application code was untouched by the docs/hygiene effort.)

**Deleted** (repo-hygiene cleanup, same session): `.playwright-mcp/`, `.devswarm-temp/`, all `__pycache__` dirs, `debug.log`, `sqlite_mcp_server.db` (0 bytes), `azure.js` (0 bytes), `facebookOauth.js` (unreferenced FB SDK snippet), `mermaid.md` (unrelated tooling note), `bun.lock` (stray — npm is the tracked package manager), and the unused 228MB `.venv/` (root `package.json` uses `.venv-win`). Also: moved several untracked secret-bearing files (`client_secret_*.json`, `gitlab.api`, `gitlab-variables-*.txt`, `gitlabpat.txt`, `brevo.txt`, `brevo-authorized-ips.txt`) out of the repo entirely — none were ever committed to git history — and added matching `.gitignore` patterns.

## Current Branch Status

Branch: `develop` (active work) and `main` (deploy branch), both fully synced to `origin` (GitHub) and `gitlab` (GitLab) as of 2026-08-06. Pushing `main` to GitLab triggers the real Azure production deploy. GitLab CI **pipeline #29** (2026-08-06) deployed the first batch — mobile auth (`106c262`), ECA backend model (`d4f365d`), admin User Management — to production; the subsequent batch (mobile-readiness backend #36/#42, board-move tooling) was merged to `main` (`3f4f61d`) and pushed this same day. GitLab push credentials are now configured: `credential.https://gitlab.com.helper store` with the PAT in `~/.git-credentials` (mode 600) on Linux, same store-helper setup documented for Windows — GitHub auth (via `gh`) is untouched. Backend suite: **111 tests passing**. The one remaining production gap: `VITE_GOOGLE_CLIENT_ID`/`VITE_FACEBOOK_APP_ID` GitLab CI/CD variables still need creating (see Known Bugs, R-34) or the next frontend deploy ships without social login.

## Current Priorities

1. Master Data Bulk Import UI (#48's remaining scope) — file upload + dry-run preview against `POST /api/dashboard/master-data/import/`.
2. ECA Tracking frontend UI (#23's remaining scope) — backend model shipped in `d4f365d`; only the list/assign UI remains.
3. Project Charter tech-stack fix (#8) — blocked on Prizma directly, no API edit/comment access to her doc.
4. Confirm remaining mobile board cards (#35, #37–#41, #43, #44) before Sprint 2 starts 2026-08-09 — #36/#42 (mobile auth + push-notification backend) now have code (`106c262`, `2e30528`); the rest are still scaffold-only.

## Next Recommended Tasks

1. Verify `FACE_PROVIDER=azure` end-to-end against a real Azure Face resource (see [decisions.md](decisions.md) ADR-002 consequences).
2. Stand up a minimal Vitest smoke test for the frontend so a test step can be added to CI.
3. Retire or refresh `Guidelines/03_PROJECT_TRACKER.csv`.
4. Create the two missing `VITE_GOOGLE_CLIENT_ID`/`VITE_FACEBOOK_APP_ID` GitLab CI/CD variables (via `backend/scripts/push_gitlab_vars.py` or GitLab UI) — the code fix (`646bed4`) is merged, but production still ships without social login until these exist (R-34).

## Important Implementation Notes

- `dlib`/`face_recognition` are deliberately absent from `requirements.txt` and lazy-imported — don't "fix" this by adding them back without re-reading [decisions.md](decisions.md) ADR-003.
- Enrollment is enforced in `AttendanceSerializer.validate()` and `mark_bulk`, not via a hard DB foreign-key constraint from `attendance` to `enrollment` — any new attendance-creation path must replicate this check.
- Both GitHub and GitLab remotes are intentionally kept in sync — see [decisions.md](decisions.md) ADR-005 before consolidating CI.
- Use the toast/confirm system for all new UI feedback — never native `alert()`/`confirm()` (ADR-006).

## External Trackers

> **Any agent starting work here should also read `AGENTS.md`'s Startup Workflow** — it now walks
> through checking GitHub Issues/Project board and both sheets below before making changes, and the
> Master Tracker's own **"33. Agent Instructions"** tab is the canonical cross-system onboarding doc
> (rewritten 2026-08-05 after stale sheets/issues caused real merge conflicts between concurrent
> agent sessions).

Project status also lives in team-managed Google Sheets (not in this repo, so they can drift — this file remains the code-verified source of truth per ADR-007):

- **In-repo remaining-work tracker**: [remaining-work-tracker.md](remaining-work-tracker.md) (canonical, version-controlled). **Assignments** are recorded in the Master Tracker tab **"7. Feature Backlog"** (Assignee column, kept in sync via Composio `GOOGLESHEETS_UPDATE_VALUES_BATCH`) and on GitHub issue assignees. **Policy (2026-08-07):** do **not** create standalone mirror sheets — edit the existing team sheets only (two created 2026-08-06 were trashed).

- **Consolidated Google Drive folder (MIT account)** — https://drive.google.com/drive/folders/1Ntq3s7vrMrwNzAYcUl_oxsbyLCW53Mfm — **holds only word/google-doc + Google Sheet deliverables** (team policy, 2026-08-06): `Problem statement (AMS).docx`, `Cost Estimation (AMS)` (Google Doc), the 5 sheets listed below plus the Project Tracker + SWOT sheets, and the `Guidelines/` folder (a `.xlsx`, `.pdf`, `.csv`). **No `.md` files** — all trashed (recoverable), all still in GitHub/local. The "AMS - Resource Labeling Register" sheet (ID `1d7WVIOHCi5_23CWILuwHVb2DYG-Ys0jEKmcqj2y-x14`) is the resource/cost register generated from `Cost Estimation (AMS).md`.
- **"Attendance Management System – Master Tracker"** (https://docs.google.com/spreadsheets/d/1Tr8JOwc4HTXpyPvXP2LaV0pTpCRSuePEjo4AURUln2Y) — 34 tabs: project overview, requirements, sprint board, feature backlog, GitHub issues/PRs snapshots, bug tracker, dependencies, risks, and the **"33. Agent Instructions"** onboarding tab. Most tabs were stale placeholders ("Planned" for things that were actually done) as of 2026-08-04; corrected 2026-08-05 for Project Overview, Progress Dashboard, Functional Requirements, Bug Tracker, Dependencies, GitHub Issues, AI Task Tracker, and Agent Instructions — the remaining tabs (Non-Functional Requirements, Sprint Board, Feature Backlog, Web/Mobile Development, UI Components, Design System, Testing, Security Checklist, Release Planning, Documentation Tracker, Changelog, API Inventory, Architecture Decisions, Database Schema, DevOps, Dependencies-chain-adjacent tabs) were **not** touched in that pass and may still be stale — verify before trusting.
- **"AMS - User Story Dependencies & Risks"** (https://docs.google.com/spreadsheets/d/1BRHCixRfskt6hvGgwYHx0g14h1ZX58ru2uIgd7bozn8) — user-story dependency chains, technical risk register (R-01–R-33) on the "Risk Analysis" tab, user-story status matrix, a team/process risk register (P-01–P-10, W-01–W-12) on the "Personal & Work Risks" tab, and a combined action-item view on the **"Risk Mitigation Plan"** tab. Created 2026-07-27, the same day as GitHub issue #51 ("Risk Management") — that issue is the assignment prompt this sheet answers; **#51 is now closed** (was previously incorrectly noted here as still open). Most current and detailed risk source. **R-07 (report filter) is "Mitigated" as of 2026-08-05 on both the Risk Analysis and Risk Mitigation Plan tabs** — note it is a distinct risk from **W-08** (Azure Face verification), which is still genuinely open. **New row R-34 added 2026-08-05** on the Risk Mitigation Plan tab for the social-login-missing-in-production bug (see Known Bugs above) — code fixed, GitLab CI/CD variable creation still a pending manual step.
- **"Attendance Management System - Project Tracker"** — an early (2026-07-07/08) sprint-planning template, stale and unmaintained since day 2 of the project; do not treat as current (same caveat as `Guidelines/03_PROJECT_TRACKER.csv`).
