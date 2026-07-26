# Testing Strategy — Attendance Management System

> **Purpose:** Documents how AMS is tested today and the goals for extending coverage.
> **Scope:** Backend (Django test suite, CI-enforced) and frontend (currently untested — see gaps below).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Current State](#current-state)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Integration Tests](#integration-tests)
- [CI Enforcement](#ci-enforcement)
- [Mocking Strategy](#mocking-strategy)
- [Coverage Goals](#coverage-goals)
- [Test Structure](#test-structure)

## Current State

- **Backend**: every Django app has a `tests.py`, plus `backend/integration_tests.py` for cross-app flows. Run via `python manage.py test`. Enforced in both CI pipelines on every push to `main`/`develop` and every MR/PR.
- **Frontend**: no automated test suite exists yet (no Jest/Vitest/RTL/Cypress in `frontend/package.json`). Manual verification is the current practice. This is a known gap — see [phases.md](phases.md) Phase 8 and the Atomic Tasks below.

## Backend Testing

- **Framework**: Django's built-in `TestCase` (unittest-based, DB-backed with transactional rollback per test).
- **Location**: `backend/<app>/tests.py` — one file per app (`accounts`, `students`, `courses`, `attendance`, `face`, `dashboard`).
- **Face app tests**: patch the provider seam (`face/providers.py`) rather than calling real `dlib`/Azure — CI installs `face-recognition==1.3.0` with `--no-deps` specifically so the face app's imports resolve without needing a full `dlib` build (see `.gitlab-ci.yml` `before_script`). Tests should not assume a specific `FACE_PROVIDER` is live-callable.
- **Run locally**:
  ```bash
  cd backend
  python manage.py test --verbosity=2
  ```
- **Run a single app/test**:
  ```bash
  python manage.py test attendance
  python manage.py test attendance.tests.AttendanceBulkTests.test_skips_non_enrolled
  ```

## Frontend Testing

Not yet set up. When adding it, prefer:

- **Vitest** (pairs naturally with the existing Vite setup) over Jest, to avoid a second bundler config.
- **React Testing Library** for component tests — test behavior (what the user sees/does), not implementation details.
- Start with the highest-value untested surfaces: `services/api.js` (auth header injection, error handling), `AuthContext`, and any component with non-trivial conditional rendering (role-based dashboard widgets).

## Integration Tests

`backend/integration_tests.py` covers flows spanning multiple apps (e.g., register → enroll → mark attendance → report) that a single app's `tests.py` can't exercise in isolation. Add new cross-app scenarios here, not by importing one app's test case into another's `tests.py`.

## CI Enforcement

Both pipelines run the same gate on every relevant push/MR:

1. `python manage.py makemigrations --check` — fails if a model change wasn't captured in a migration.
2. `python manage.py check` — Django system check framework.
3. `python manage.py test --verbosity=2` — full suite.

See `.gitlab-ci.yml` (`test` stage, gates `build-frontend`/`deploy-backend` via `needs`) and `.github/workflows/ci.yml` (test-only, targets `develop`). No test step currently runs for the frontend in either pipeline — `build-frontend` in GitLab CI only runs `npm run build` (a build check, not a test run) and only on `main`.

## Mocking Strategy

- **External services** (Brevo SMTP, Google/Facebook OAuth, Azure AI Face API) should be mocked/stubbed in tests — never let a test suite make a real network call. `accounts/services.py`/`accounts/social.py` and `face/providers.py` are the seams to patch.
- **`dlib`/`face_recognition`**: since these are optional/lazy-imported, face app tests must not assume they're importable in every environment — patch at the provider boundary (`face/providers.py`), not deep inside `dlib` calls.

## Coverage Goals

No coverage percentage is currently tracked/enforced (no `coverage.py` gate in CI). Recommended direction, not yet mandated:

- Every new serializer `validate()` method gets at least one positive and one negative test.
- Every new view gets at least one test per permission tier it exposes (e.g., admin can, faculty can, student cannot).
- Bulk/aggregate endpoints (`mark_bulk`, `dashboard/*`) get a test with a mixed valid/invalid input set, not just the happy path.

## Test Structure

```
backend/
├── accounts/tests.py
├── students/tests.py
├── courses/tests.py
├── attendance/tests.py
├── face/tests.py        # patches provider seam, doesn't hit real dlib/Azure
├── dashboard/tests.py
└── integration_tests.py  # cross-app flows
```

### Atomic tasks (open)

- [ ] Stand up a Vitest + React Testing Library baseline for the frontend (config + one smoke test), before adding component-level tests.
- [ ] Add a frontend test/build step to CI once a test command exists (currently only `npm run build` runs, and only on `main`).
