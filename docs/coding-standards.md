# Coding Standards — Attendance Management System

> **Purpose:** How to organize and name things. For *enforceable, review-blocking* rules (security musts, "never do X"), see [rules.md](rules.md) — this doc is the broader reference for structure and naming that rules.md assumes but doesn't spell out in full.
> **Scope:** Backend, Web, Mobile (planned), shared packages (planned).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Folder Structure](#folder-structure)
- [Naming Conventions](#naming-conventions)
- [Component Organization (Frontend)](#component-organization-frontend)
- [Feature Organization](#feature-organization)
- [API Organization](#api-organization)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Environment Variables & Configuration](#environment-variables--configuration)
- [Documentation in Code](#documentation-in-code)

## Folder Structure

Current (see [architecture.md](architecture.md) Folder Structure for the authoritative current tree): `backend/<app>/`, `frontend/src/{pages,layouts,context,components,services,styles}/`. Target future shape (see [package-guidelines.md](package-guidelines.md) for the full design): `apps/{web,mobile,backend}/` + `packages/*` — not implemented yet, don't restructure as a side effect of unrelated work.

## Naming Conventions

| Kind | Convention | Example |
|---|---|---|
| Python files/modules | `snake_case` | `serializers.py` |
| Python classes | `PascalCase` | `AttendanceSerializer` |
| Python functions/variables | `snake_case` | `mark_bulk()` |
| Django app names | `snake_case`, singular-or-plural matching domain concept | `students`, `attendance` |
| JS/TS files (components) | `PascalCase.jsx`/`.tsx` | `AttendanceCodes.jsx` |
| JS/TS files (non-component) | `camelCase.js`/`.ts` | `api.js` |
| JS/TS variables/functions | `camelCase` | `markAttendance()` |
| React components | `PascalCase` | `DashboardLayout` |
| CSS files | `kebab-case`, matching feature area | `attendance-codes.css` |
| Constants (any language) | `UPPER_SNAKE_CASE` for true constants | `OTP_EXPIRY_MINUTES` |
| Environment variables | `UPPER_SNAKE_CASE`, prefixed `VITE_` for frontend build-time vars | `VITE_API_URL` |
| Shared package names (planned) | `kebab-case`, matching the directory | `packages/api-client` |

## Component Organization (Frontend)

- One page component per route, under `src/pages/`, registered in `App.jsx` — existing rule ([rules.md](rules.md)).
- Shared chrome (nav, header) in `src/layouts/` — not duplicated per page.
- Genuinely reusable, presentation-focused pieces (not tied to one page) go in `src/components/` (e.g., `SocialLogin`) — a component used by exactly one page stays colocated conceptually with that page (same file or a page-local subfolder), promote to `components/` only once a second consumer exists (same "earns its existence" principle as [package-guidelines.md](package-guidelines.md)).
- Keep business/API logic out of presentation components — fetch/transform in the page component or a hook; JSX stays focused on rendering ([rules.md](rules.md)).

## Feature Organization

- Backend: one Django app per bounded domain concept — don't bolt a new feature onto an unrelated existing app ([rules.md](rules.md)).
- Frontend: currently page-per-route, not a feature-folder structure (no `features/attendance/{components,hooks,api}` nesting) — this is acceptable at current app size; **reconsider** a feature-folder restructure only if `src/pages/` and `src/components/` both grow large enough that flat organization becomes hard to navigate, not preemptively.

## API Organization

See [api-standards.md](api-standards.md) for the full standard (naming, versioning, request/response shape). Backend view organization: `DefaultRouter`+`ViewSet` for resource CRUD, `APIView`/function-based views for actions — existing pattern, see [architecture.md](architecture.md) Backend Architecture.

## Error Handling

- **Backend**: DRF's default exception handling returns a structured error response for `ValidationError`/`PermissionDenied`/etc. Custom business-logic errors should raise a DRF exception subclass (not a bare `Exception`) so the response shape stays consistent ([api-standards.md](api-standards.md) Error Responses). Never let an unhandled exception leak a stack trace to the client in production (`DEBUG=False` already prevents Django's debug page; confirm any custom exception handler doesn't reintroduce detail leakage).
- **Frontend**: every `services/api.js` call site handles the error case explicitly (via try/catch or a query library's error state) and surfaces it through the toast/confirm system ([rules.md](rules.md)) — never a silent `catch {}` that swallows the error with no user feedback and no log.
- **Mobile (planned)**: same principle — surface errors via the platform's native feedback pattern (not a native `Alert` used as a blanket catch-all; prefer inline/toast-equivalent feedback matching the design system, see [design.md](design.md)).

## Logging

- **Backend**: Python stdlib `logging` (Django's default config) — log at the point where an error is handled/swallowed, include enough context (user id, resource id, action) to debug without needing to reproduce. Never log a secret, token, or password (see [security-standards.md](security-standards.md)).
- **Frontend**: `console.error`/`console.warn` for developer-facing diagnostics; the toast system for user-facing messages — these are two different audiences, don't conflate them (a `console.log` is not user feedback).
- No structured/centralized logging exists yet ([tech-stack.md](tech-stack.md) Cross-Cutting Concerns) — plain stdlib logging is the standard until that changes.

## Environment Variables & Configuration

- Every environment-specific value goes through `python-decouple` (backend) or `import.meta.env.VITE_*` (frontend) — never hardcoded ([rules.md](rules.md)).
- New env var → add to the relevant `.env.example` with a comment describing its purpose, in the same PR that introduces it ([rules.md](rules.md) Documentation, [release-process.md](release-process.md) checklist).
- `packages/config` (planned, see [package-guidelines.md](package-guidelines.md)) will provide a typed accessor contract for shared config once it exists — not a place to put actual secret values.

## Documentation in Code

- Document exported/public functions and classes where their purpose isn't obvious from the name — don't restate what the code already makes clear ([rules.md](rules.md)).
- Prefer a docstring/comment explaining *why* (a non-obvious constraint, a workaround, an invariant) over *what* (the code already shows what).
- Non-trivial technical decisions belong in [decisions.md](decisions.md) as an ADR, not only as an inline comment — a comment explains local context; an ADR explains a decision's reasoning for the whole team/future contributors.
