# Architecture Decision Records (ADR) — Attendance Management System

> **Purpose:** Log of significant technical decisions — context, alternatives, rationale, consequences.
> **Scope:** Whole project. Add a new entry (don't edit past ones except to update `Status`) whenever a decision would otherwise only live in a commit message or someone's memory.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [ADR format](#adr-format)
- [ADR-001: Enrollment as an explicit model, added early](#adr-001-enrollment-as-an-explicit-model-added-early)
- [ADR-002: Pluggable face recognition provider (local dlib vs. Azure AI Face API)](#adr-002-pluggable-face-recognition-provider-local-dlib-vs-azure-ai-face-api)
- [ADR-003: `dlib` excluded from `requirements.txt`, lazy-imported](#adr-003-dlib-excluded-from-requirementstxt-lazy-imported)
- [ADR-004: Async Azure backend deploy (`--async true`)](#adr-004-async-azure-backend-deploy---async-true)
- [ADR-005: Dual CI — GitLab (deploy) + GitHub Actions (visibility)](#adr-005-dual-ci--gitlab-deploy--github-actions-visibility)
- [ADR-006: Toast/confirm system replaces native `alert()`/`confirm()`](#adr-006-toastconfirm-system-replaces-native-alertconfirm)
- [ADR-007: `docs/memory.md` supersedes `HANDOFF.md`/tracker docs as status source of truth](#adr-007-docsmemorymd-supersedes-handoffmdtracker-docs-as-status-source-of-truth)

## ADR format

Each entry: **Decision**, **Context**, **Alternatives considered**, **Rationale**, **Consequences**, **Date**, **Status** (Proposed / Accepted / Superseded).

---

## ADR-001: Enrollment as an explicit model, added early

- **Date**: 2026-07-09 (Day 3)
- **Status**: Accepted
- **Decision**: Add a `courses.Enrollment` model (student↔course, unique together, `is_active`) before frontend UI work started, rather than deferring it.
- **Context**: Attendance needs to know which students belong to which course. Without an explicit table, this would be inferred implicitly (e.g., "has an attendance record") which is circular.
- **Alternatives considered**: Defer to a later week per the original roadmap; infer enrollment from attendance history.
- **Rationale**: Adding it later would break the `attendance` API contract once frontend work started building against it. One migration + one model now is cheaper than a breaking change later, and no UI code existed yet to be affected.
- **Consequences**: `AttendanceSerializer.validate()` and `mark_bulk` both had to add enrollment checks (done same effort — see `docs/database-schema.md` "Resolved: Enrollment table added"). A backfill migration (`0003_backfill_enrollment`) populated rows from existing attendance history.

## ADR-002: Pluggable face recognition provider (local dlib vs. Azure AI Face API)

- **Date**: 2026-07-20
- **Status**: Accepted
- **Decision**: Introduce `FACE_PROVIDER` env var (`local` | `azure`) and `backend/face/providers.py` as the abstraction boundary, rather than hard-coding one face recognition backend.
- **Context**: `dlib` (required by `face_recognition`) compiles from C++ source and has no guaranteed prebuilt wheel for every host; Azure App Service's constrained plans (e.g., B1) can fail or time out building it.
- **Alternatives considered**: Require `dlib-bin` everywhere and accept deploy failures on constrained plans; drop face recognition from the deployed product entirely.
- **Rationale**: A provider abstraction keeps local dev fast/offline/free while giving production a working fallback (Azure AI Face API) without maintaining two separate feature sets.
- **Consequences**: Two code paths to keep behaviorally consistent; `AZURE_FACE_ENDPOINT`/`AZURE_FACE_KEY`/`AZURE_FACE_PERSON_GROUP` become required config when `azure` is selected. As of this writing, the Azure path is implemented but not yet verified end-to-end against a real Azure Face resource (open item, see [phases.md](phases.md) Phase 5).

## ADR-003: `dlib` excluded from `requirements.txt`, lazy-imported

- **Date**: 2026-07-10 (Day 4), reaffirmed 2026-07-19
- **Status**: Accepted
- **Decision**: `dlib`/`face_recognition` are not in `backend/requirements.txt`; `face/views.py` imports them lazily so the rest of the app runs without them installed. CI installs `face-recognition==1.3.0 --no-deps` separately alongside `dlib-bin` from `requirements.txt`.
- **Context**: Plain `pip install dlib` builds from source and fails without CMake/a C++ toolchain; `dlib-bin` provides a prebuilt wheel under the same import name but pulling in plain `face-recognition` via normal `pip install -r requirements.txt` would still try to build `dlib` from source as a declared dependency.
- **Alternatives considered**: Require all contributors to install build tools locally; drop face recognition tests from CI entirely.
- **Rationale**: Keeps `pip install -r requirements.txt` fast and reliable for contributors who don't touch face recognition, while still exercising the face app in CI via the `--no-deps` install trick.
- **Consequences**: Anyone working on `face/` locally needs the extra manual install step documented in `Guidelines/REALITY_CHECK.md` ("Build Requirements — dlib"). New face-app code must not assume `dlib`/`face_recognition` are importable at module load time.

## ADR-004: Async Azure backend deploy (`--async true`)

- **Date**: pre-2026-07-20 (exact date not recorded prior to this ADR log)
- **Status**: Accepted
- **Decision**: `az webapp deploy` in `.gitlab-ci.yml` uses `--async true` rather than the default synchronous deploy.
- **Context**: A synchronous deploy holds one HTTP request open while Oryx rebuilds `numpy`/`dlib-bin` (often >230s on the B1 App Service plan); Azure's front door cuts the request off, which false-fails the CI job even when the deploy actually succeeds.
- **Alternatives considered**: Upgrade the App Service plan to avoid the slow rebuild; pre-build a Docker image instead of Oryx source-build deploy.
- **Rationale**: `--async true` uploads the zip and lets the Azure CLI poll ARM deployment status directly, which isn't subject to the same front-door timeout, and exits 0/1 based on the real final status.
- **Consequences**: Slightly more complex deploy step; deploy status is only as reliable as the CLI's polling, not a single request/response.

## ADR-005: Dual CI — GitLab (deploy) + GitHub Actions (visibility)

- **Date**: ongoing (both configs coexist since early in the project)
- **Status**: Accepted
- **Decision**: Keep both `.gitlab-ci.yml` (full test→build→deploy) and `.github/workflows/ci.yml` (test-only, `develop` branch) rather than consolidating to one CI provider.
- **Context**: GitHub (`origin`) is used by the team for issues, PRs, and general visibility; GitLab (`gitlab`) is the CI/CD provider actually wired to Azure credentials and deploy targets.
- **Alternatives considered**: Move deploy to GitHub Actions and drop GitLab entirely; drop the GitHub Actions test mirror and rely on GitLab CI status checks alone (would require everyone to check GitLab, not just GitHub).
- **Rationale**: Splitting concerns — team collaboration stays on the tool the team actually uses daily (GitHub), while deploy secrets/credentials stay in GitLab, without duplicating deploy logic in two places.
- **Consequences**: Two pipeline configs to keep in sync for the `test` stage specifically (they run near-identical steps); a change to test setup (e.g., a new required env var) must be mirrored in both files.

## ADR-006: Toast/confirm system replaces native `alert()`/`confirm()`

- **Date**: 2026-07-20
- **Status**: Accepted
- **Decision**: Replace native browser `alert()`/`confirm()` dialogs with the app's own toast/confirm dialog system (`NotificationContext`) across `Attendance`, `AttendanceCodes`, `Courses`, `Enrollments`, and `Students` pages.
- **Context**: Native dialogs are blocking, inconsistent in styling, and (per Claude Code's own browser-automation guidance) can hang automated testing/interaction tools since they block all further page events.
- **Alternatives considered**: Keep native dialogs for destructive-action confirmations only; adopt a third-party dialog library.
- **Rationale**: A single in-house system gives consistent styling/UX and avoids the automation/accessibility pitfalls of native dialogs, without adding a new dependency.
- **Consequences**: All new destructive/confirmation UI must use `NotificationContext`, not native dialogs (enforced going forward — see [rules.md](rules.md)).

## ADR-007: `docs/memory.md` supersedes `HANDOFF.md`/tracker docs as status source of truth

- **Date**: 2026-07-26
- **Status**: Accepted
- **Decision**: `docs/memory.md` (this documentation effort) becomes the canonical, living project-status document going forward. `HANDOFF.md` and `NEXT_STEPS.md` remain as dated session logs (useful history, not to be edited retroactively); `Guidelines/REALITY_CHECK.md` and `Guidelines/03_PROJECT_TRACKER.csv` remain explicitly flagged as stale/historical, per `HANDOFF.md`'s own note.
- **Context**: Prior to this, project status was scattered across `HANDOFF.md`, `NEXT_STEPS.md`, and `Guidelines/REALITY_CHECK.md`, with the latter actively wrong (claims "no frontend code exists" when a full React app is shipped) and no single doc mandated to be kept current.
- **Alternatives considered**: Keep `HANDOFF.md` as the living doc (rejected — its own content flags itself as a snapshot, not a continuously-updated doc); delete stale docs outright (rejected — task constraints require preserving existing content, and they retain historical value).
- **Rationale**: A single, explicitly-designated "update this after every major change" doc avoids the drift that produced the current stale-docs problem in the first place.
- **Consequences**: Anyone (human or AI agent) finishing a non-trivial change should update `docs/memory.md` — see [rules.md](rules.md) Documentation section.
