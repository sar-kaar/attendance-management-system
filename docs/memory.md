# Project Memory — Attendance Management System

> **Purpose:** Persistent, living project status for both humans and AI coding agents. **Update this file after every major implementation.**
> **Scope:** Current state only — historical narrative belongs in `HANDOFF.md` (session logs) or [decisions.md](decisions.md) (why a decision was made), not here.
> **Last updated:** 2026-07-26 · **Version:** 1.3 (see [decisions.md](decisions.md) ADR-007 for why this file exists and supersedes older status docs)

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

## Project Status

Backend and frontend are **both substantially built and deployed** (Azure App Service + Azure Storage static site). This is ahead of the original course week-by-week plan (`Guidelines/01_WEEKLY_ROADMAP.md`, `Guidelines/03_PROJECT_TRACKER.csv` — both stale, do not treat as current). As of 2026-07-26, the engineering-hygiene pass (this `docs/` set + root config files) is the active work.

## Completed Features

- Auth: register, JWT login/refresh, email OTP verification (Brevo SMTP), Google/Facebook social sign-in, admin user management.
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
- **`AttendanceViewSet.report` filter dead-code resolved (2026-07-26)**: the 2 `F841` findings from the ruff pass (`course_id`, `student_id` local vars in `report()`) were initially suspected to be a real filtering bug, but tracing the call showed `report()` calls `self.get_queryset()`, which already reads and applies the same `course`/`student`/`date` query params (`backend/attendance/views.py` `get_queryset()`). So the two local vars were genuinely dead — redundant reads, not a bug. Removed them and added a one-line comment explaining why, plus two regression tests (`test_report_filters_by_course`, `test_report_filters_by_student` in `backend/attendance/tests.py`) that lock in the already-correct filtering behavior so it can't silently regress.

## Pending Features

| Feature | Owner | Tracking |
|---|---|---|
| Dashboard UI (frontend widgets for the backend-complete dashboard endpoints) | Ekata | GitHub #1 (US-10) |
| ECA (extra-curricular activity) tracking | Ekata | GitHub #23 (US-12) |
| Notifications (email/SMS) | Unassigned | Phase 7, not started, see [phases.md](phases.md) |
| SRS Document (IEEE 830) | Prizma | GitHub #5 (T-003) |
| Requirements Gathering doc | Prizma | GitHub #7 (T-002) |
| Wireframes and Mockups (formal) | Prizma | GitHub #11 (T-005) — note: `wireframes/*.html` already exist as static mockups; unclear if this issue means something further |
| Project Charter | Prizma | GitHub #8 (T-007) |
| Team Norms and Comms Plan | Prizma | GitHub #12 (T-008) |

## Known Bugs / Open Issues

- **Issue numbering collision**: two open GitHub issues both titled "US-10" — #1 (Dashboard UI, frontend, genuinely open) and #24 (Chronic Latecomers Detection, backend, actually done via PR #30). Not urgent, but confusing in triage — flagged in `HANDOFF.md`.
- **Stale-but-done issues not closed**: PR #30 ("Dashboard API — US-06 to US-13", merged 2026-07-18) implemented #19, #17, #18, #20, #21, #22 but none were closed. Recommend closing after a sanity check against the live `/api/dashboard/*` endpoints.
- **Azure Face provider unverified end-to-end**: `FACE_PROVIDER=azure` is implemented (`backend/face/providers.py`) but only exercised locally, not against a real Azure Face resource in an end-to-end run.
- **`Guidelines/REALITY_CHECK.md` and `Guidelines/03_PROJECT_TRACKER.csv` are stale** — the former claims no frontend exists (false); the latter still shows Sprint 1 in progress. Both are kept for historical/course-deliverable purposes but must not be treated as current status. `HANDOFF.md` also flags this.
- **`docs/system-architecture.md`** predates the `face` and `dashboard` apps and the working CI/CD — `docs/architecture.md` (this effort) is now the current reference; `system-architecture.md`'s Mermaid diagrams/SVGs are kept for the parts still accurate (core auth/attendance flow) but the app/endpoint lists there are outdated.

## Technical Debt

- ~~No Python linter configured for `backend/`~~ — resolved 2026-07-26: `ruff` added and CI-enforced in both `.gitlab-ci.yml` and `.github/workflows/ci.yml` (see Completed Features and Files Modified/Created).
- ~~Bug found by the ruff pass~~ — re-investigated 2026-07-26 and reclassified: not a bug. `report()`'s `qs = self.get_queryset()` call already applies `course`/`student` filtering (via `get_queryset()`'s own query-param handling), so the two local vars were dead code, not a missing filter. Resolved — see Completed Features.
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

Branch: `ams`. Prior session's `HANDOFF.md` (2026-07-20) noted `develop` was ahead of both `origin` and `gitlab` remotes and needed pushing — verify current remote sync state with `git log --oneline --graph --all` before assuming this is still accurate, since it may have been resolved since.

## Current Priorities

1. Verify this documentation effort didn't break anything (`Validation` section — run frontend build, backend `manage.py check`).
2. Close the stale-but-implemented dashboard issues (#19, #17, #18, #20, #21, #22) after confirming against `/api/dashboard/*`.
3. Finish Dashboard UI (#1) and ECA Tracking (#23) on the frontend.
4. Chase PM deliverables (#7, #5, #11, #8, #12) — all overdue against the original Week 1–2 checklist.

## Next Recommended Tasks

1. Merge `fix/attendance-report-filter` (ruff + CI wiring + report dead-code cleanup + regression tests) into `develop`/`main` via PR — currently pushed but not merged.
2. Verify `FACE_PROVIDER=azure` end-to-end against a real Azure Face resource (see [decisions.md](decisions.md) ADR-002 consequences).
4. Stand up a minimal Vitest smoke test for the frontend so a test step can be added to CI.
5. Retire or refresh `Guidelines/03_PROJECT_TRACKER.csv`.

## Important Implementation Notes

- `dlib`/`face_recognition` are deliberately absent from `requirements.txt` and lazy-imported — don't "fix" this by adding them back without re-reading [decisions.md](decisions.md) ADR-003.
- Enrollment is enforced in `AttendanceSerializer.validate()` and `mark_bulk`, not via a hard DB foreign-key constraint from `attendance` to `enrollment` — any new attendance-creation path must replicate this check.
- Both GitHub and GitLab remotes are intentionally kept in sync — see [decisions.md](decisions.md) ADR-005 before consolidating CI.
- Use the toast/confirm system for all new UI feedback — never native `alert()`/`confirm()` (ADR-006).
