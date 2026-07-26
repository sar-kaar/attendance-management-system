# Technology Stack — Attendance Management System

> **Purpose:** The final, decided technology stack for AMS as an enterprise-grade monorepo — what's chosen, why, what was considered, and how to upgrade it. This is a decision record, not a tutorial; see [architecture.md](architecture.md) for how the pieces fit together.
> **Scope:** Backend, Web, Mobile (planned), shared packages, infra.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [How to Read This Document](#how-to-read-this-document)
- [Backend](#backend)
- [Database & ORM](#database--orm)
- [Web Frontend](#web-frontend)
- [Mobile (Planned)](#mobile-planned)
- [Shared Packages](#shared-packages)
- [Cross-Cutting Concerns](#cross-cutting-concerns)
- [Infrastructure & Deployment](#infrastructure--deployment)
- [Tooling](#tooling)
- [Upgrade Strategy (Summary)](#upgrade-strategy-summary)

## How to Read This Document

Each entry: **Choice** (what's used today, or planned), **Why**, **Alternatives considered**, **Pros**, **Cons**, **Upgrade strategy**. Entries marked **(planned)** describe a decision for future work (mobile, shared packages) that has not been implemented yet — per [rules.md](rules.md), do not implement application features as a side effect of reading this doc; it's a blueprint, not a task list.

## Backend

### Framework: Django 5.x + Django REST Framework

- **Why**: Batteries-included ORM, migrations, and admin panel let a small team ship CRUD-heavy features (students, courses, attendance) fast without reinventing auth/admin tooling. DRF's ViewSets/routers map cleanly onto REST resources.
- **Alternatives considered**: FastAPI (faster, async-native, but no built-in admin/ORM — would mean building admin tooling and a migration system from scratch for a small team); Flask (more manual wiring for the same batteries).
- **Pros**: mature ecosystem, built-in admin panel (used for user management), strong ORM, huge library surface (SimpleJWT, WhiteNoise, reportlab all exist as drop-in Django-aware packages).
- **Cons**: heavier than a minimal API framework; synchronous by default (no async views in use today); ORM migrations must be reviewed carefully for destructive changes ([database-standards.md](database-standards.md)).
- **Upgrade strategy**: Django LTS releases roughly every 2 years — track the LTS line, upgrade minor versions promptly (low risk), treat major version bumps as their own reviewed change with the release notes' deprecation list checked against every app.

### Auth: `djangorestframework-simplejwt`

- **Why**: Stateless JWT integrates directly with DRF permission classes; no server-side session store needed, which matters for a horizontally-simple single-instance Azure App Service deployment.
- **Alternatives considered**: Django session auth (stateful, awkward for a decoupled SPA + future mobile client); `django-oauth-toolkit` (full OAuth2 provider — more machinery than a single first-party frontend/mobile client needs).
- **Pros**: works identically for web and future mobile clients (same bearer-token contract); short-lived access tokens limit blast radius of a leaked token.
- **Cons**: no built-in token revocation (a stolen refresh token is valid until expiry unless a blocklist is added); requires the client to handle refresh-token rotation correctly.
- **Upgrade strategy**: pin to the latest SimpleJWT minor compatible with the installed DRF/Django versions; re-test token refresh and the `me/` endpoint after any bump.

### API Framework: DRF ViewSets/Routers + APIView

- **Why/Pros/Cons/Alternatives**: see [api-standards.md](api-standards.md) — this is a convention decision, not a separate library choice.

## Database & ORM

### Database: SQLite (dev) → PostgreSQL (prod)

- **Why**: SQLite needs zero setup for local dev and CI; PostgreSQL is the production target because it scales, supports proper concurrent writes, and is what Azure's managed database offerings provide.
- **Alternatives considered**: MySQL (comparable, but Postgres has stronger JSON/constraint support and is the team's existing operational familiarity); SQLite in production (rejected — no safe concurrent-write story for a multi-user attendance system).
- **Pros**: `DATABASE_URL`-driven switch means the same Django settings module works in all three environments with no code branching.
- **Cons**: dev/CI running SQLite means some Postgres-specific behavior (constraint timing, certain field types) isn't caught until a real Postgres run — mitigate by testing against Postgres before a schema-heavy release.
- **Upgrade strategy**: track the Postgres major version the Azure managed offering supports; run `pg_dump`-based backups before any major-version upgrade ([database-standards.md](database-standards.md) Backups).

### ORM: Django ORM

- **Why**: Ships with Django; no reason to add a second ORM layer for a single-service backend.
- **Alternatives considered**: SQLAlchemy (better suited to multi-framework or async codebases — not this one).
- **Upgrade strategy**: tied to the Django version.

## Web Frontend

### Framework: React 19 + Vite

- **Why**: SPA architecture calling the DRF API directly — no SSR/SEO requirement (this is an authenticated internal tool, not a public content site), so Next.js's extra complexity buys nothing. Vite gives a fast dev server and simple, standard build output (static files uploaded to Azure Storage).
- **Alternatives considered**: Next.js (SSR/routing conventions unneeded here); Create React App (deprecated, slower dev server); Vue/Svelte (would mean a second framework to teach the team, no functional advantage for this app's needs).
- **Pros**: fast HMR, minimal config, plain static build output that deploys trivially to Azure Storage static website hosting.
- **Cons**: no SSR (fine for an authenticated dashboard app); routing/state management are "bring your own" (see below).
- **Upgrade strategy**: React major versions are typically low-risk for a codebase using function components + hooks only (no legacy class-component patterns); re-run `npm run lint`/`npm run build` and manually smoke-test auth + attendance flows after any major bump.

### Routing: `react-router-dom`

- **Why**: De facto standard for SPA routing in React; route table lives in `App.jsx`.
- **Alternatives considered**: file-based routing frameworks (TanStack Router, Next.js routing) — unnecessary indirection for a route table with a fixed, small page count.

### State Management: React Context + local state

- **Why**: `AuthContext` (session/JWT) and `NotificationContext` (toasts) are the only cross-cutting state; everything else is local `useState`/`useReducer` in the owning page. A global store (Redux/Zustand) would be solving a problem this app doesn't have.
- **Alternatives considered**: Redux Toolkit, Zustand, Jotai — all rejected as premature for the current state surface. **Reconsider only if** a third cross-cutting concern emerges that Context can't handle cleanly (e.g., complex derived/cached server state) — at that point, prefer a server-state library (TanStack Query) over a general store, since most of this app's state *is* server state.
- **Upgrade strategy**: N/A (no external dependency to upgrade beyond React itself).

### UI Framework / Component Library: none (plain CSS)

- **Why**: Early planning docs mention MUI, but the shipped frontend uses plain CSS per feature area (`src/styles/<feature>.css`) — no component library was adopted. This is documented here so the gap between planning docs and reality doesn't cause confusion (see [decisions.md](decisions.md)).
- **Current state**: acceptable for the app's current size; **recommendation** if the frontend grows substantially: adopt a headless component library (Radix UI, Headless UI) rather than a fully-styled one (MUI, Ant), to preserve the existing plain-CSS design language instead of an abrupt visual rewrite — see [design.md](design.md).

### Styling: Plain CSS, one file per feature area

- **Why**: matches current codebase; no CSS-in-JS runtime cost, no build-step dependency beyond Vite's native CSS handling.
- **Alternatives considered**: Tailwind (would mean rewriting every existing stylesheet — not justified without a broader design-system initiative); CSS Modules / styled-components (extra tooling for marginal benefit at this scale).

### Icons: inline SVG sprite (`icons.svg`)

- **Why**: matches current `public/icons.svg` approach — zero extra dependency, no icon-font FOUC.

### Charts: Chart.js + `react-chartjs-2`

- **Why**: dashboard visualizations (attendance trends, at-risk breakdowns) — Chart.js is lightweight and covers the chart types needed (line, bar, pie) without a heavier library like D3.
- **Alternatives considered**: D3 (far more power than needed, steep learning curve for marginal gain on standard chart types); Recharts (comparable — Chart.js was already in place, no reason to churn it).

### Forms & Validation (Frontend)

- **Current state**: manual controlled-component forms + inline validation, no form library.
- **Recommendation (planned)**: if form complexity grows (multi-step wizards, complex cross-field validation), adopt `react-hook-form` + a schema validator shared with the backend's validation rules where possible (see [Shared Packages](#shared-packages) `validation`/`schemas`) — don't duplicate validation logic between a new form library and hand-rolled checks.

### Networking: axios (`services/api.js`)

- **Why**: centralized instance with base URL + auth-header injection in one place — every page/component goes through it (enforced in [rules.md](rules.md)).
- **Alternatives considered**: native `fetch` (axios's interceptor support for auth-header injection and refresh-token retry logic is worth the small dependency).

## Mobile (Planned)

### Framework: React Native + Expo **(planned)**

- **Why**: maximizes code sharing with the existing React/TypeScript-capable web codebase — API client, validation, types, and business-rule logic can live in `packages/` and be consumed by both web and mobile (see [Shared Packages](#shared-packages)). Expo specifically reduces native-build/signing overhead for a small team without dedicated mobile-release infrastructure.
- **Alternatives considered**: Flutter (excellent cross-platform performance, but Dart cannot consume the JS/TS shared packages — would mean duplicating types/validation/business rules in a second language); native Kotlin/Swift (best per-platform experience, but doubles the mobile codebase and the team size needed to maintain it — not justified for this project's scale).
- **Pros**: single codebase for iOS/Android, shares `packages/api-client`, `packages/types`, `packages/validation` directly with web.
- **Cons**: Expo's managed workflow limits some native-module access until you eject/use a dev client — acceptable given the mobile feature set planned (QR attendance, push notifications, camera access for face capture — all supported by standard Expo modules).
- **Upgrade strategy**: track Expo SDK releases (roughly quarterly); Expo's upgrade tooling (`expo upgrade`) handles most of the native-dependency churn automatically.

### Mobile Navigation: React Navigation **(planned)**

- **Why**: the standard for React Native, well-integrated with Expo.

### Mobile State/Offline: TanStack Query + a local persistence layer (e.g. WatermelonDB or Expo SQLite) **(planned)**

- **Why**: offline attendance marking + sync is a stated requirement (see [prd.md](prd.md)) — this needs a real local-first data layer, not just in-memory Context. Decision on the specific local DB is deferred to the mobile-foundation phase ([phases.md](phases.md)); documented here as a placeholder so it isn't forgotten.

## Shared Packages

See [package-guidelines.md](package-guidelines.md) for the full package-by-package design. Summary of stack choices that affect them:

- **Language**: TypeScript for all shared packages (`packages/*`), even though the current web frontend is plain JS (`.jsx`) — new shared code should be written in TS from the start so both a future TS-migrated web app and the planned React Native/Expo app (also TS) get type safety, and so `packages/types` has one canonical source instead of being re-derived per consumer.
- **Validation**: a single schema library (recommend `zod`) shared between `packages/validation` (frontend/mobile) and, where practical, mirrored in DRF serializers on the backend — see [api-standards.md](api-standards.md) on keeping the two in sync without one literally importing the other (Python/TS can't share a runtime schema object directly).
- **Build**: each package builds independently (recommend a lightweight bundler like `tsup` per package, or a monorepo tool like Turborepo/Nx once package count justifies the overhead — not needed yet at 0 packages implemented).

## Cross-Cutting Concerns

| Concern | Choice | Notes |
|---|---|---|
| Logging (backend) | Python stdlib `logging`, Django's default config | No structured/aggregated logging yet — known gap, see [security.md](security.md) and [deployment.md](deployment.md) |
| Logging (frontend) | `console.*` + toast system for user-facing errors | No client-side error tracking (Sentry, etc.) configured yet |
| Monitoring | Azure App Service log stream | No APM configured — documented gap, not silently missing |
| Analytics | none | No product analytics configured; add only with a clear purpose and a privacy review given student PII is in scope |
| File Storage | Django `media/` (local disk on App Service) | Not yet on a durable blob store — see [Known Gaps](#known-gaps-summary) below; Azure Blob Storage is the natural choice if this needs to survive App Service restarts/scaling |
| Notifications | Brevo SMTP (email only) | SMS/push not yet implemented (planned, see [phases.md](phases.md) Phase 7 / mobile push) |
| Documentation | Markdown in `docs/`, Mermaid diagrams | This doc set itself |

## Infrastructure & Deployment

See [deployment.md](deployment.md) and [cicd.md](cicd.md) for full detail.

| Concern | Choice | Why |
|---|---|---|
| Backend hosting | Azure App Service | Team's existing Azure familiarity; Oryx build pipeline handles Python builds without a custom Docker image |
| Frontend hosting | Azure Storage static website | Cheapest correct option for a static SPA build; no server needed |
| Containerization | None currently | App Service's Oryx build is used instead of Docker — **reconsider** if a second deploy target (e.g., a container-based host, local Docker dev parity) becomes a real need; don't add Docker speculatively |
| CI | GitLab CI (deploy) + GitHub Actions (test mirror) | See [deployment.md](deployment.md) "Why Two CI Configs" — deliberate, not redundant |
| Package manager (backend) | `pip` + `requirements.txt` | Simple, matches Oryx's expectations; **not** Poetry/PDM — those complicate the Oryx build path for marginal benefit at this dependency count |
| Package manager (frontend/monorepo) | `npm` | `package-lock.json` is the tracked lockfile; a stray `bun.lock` was found and removed — **npm is the single source of truth**, do not introduce a second package manager's lockfile |

## Tooling

| Tool | Purpose | Status |
|---|---|---|
| ESLint (flat config) | Frontend linting | Configured, enforced via `npm run lint` |
| Prettier | Formatting (JS/TS/JSON/MD) | Configured (`.prettierrc`/`.prettierignore`), not yet wired into CI as a check — see [cicd.md](cicd.md) |
| `ruff` | Backend linting/formatting | **Not yet configured** — recommended in [rules.md](rules.md)/[phases.md](phases.md), single fast tool covers both lint and format |
| EditorConfig | Cross-editor whitespace/indent consistency | Configured (`.editorconfig`) |
| `.gitattributes` | Line-ending normalization, binary file marking | Configured |

## Upgrade Strategy (Summary)

1. **Patch/minor versions**: upgrade routinely, no special process beyond CI passing.
2. **Major versions** (Django, React, DRF, SimpleJWT): dedicated PR, read the release's breaking-changes list against every app/page that touches the changed surface, run the full test suite + a manual smoke test of auth/attendance/face flows before merge.
3. **New dependency**: must be justified in a [decisions.md](decisions.md) ADR before merge — "why this and not the alternative" is not optional for anything beyond a trivial utility.
4. **Removing a dependency**: confirm nothing in `packages/` (once implemented) or either app silently relies on a transitive behavior of it; update this doc in the same PR.
