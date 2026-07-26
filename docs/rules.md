# Development Rules — Attendance Management System

> **Purpose:** Enforceable rules and conventions for anyone (human or AI agent) modifying this codebase.
> **Scope:** Whole repo. Violating these should be treated as a review blocker, not a style nit.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Security](#security)
- [Backend Rules (Django/DRF)](#backend-rules-djangodrf)
- [Frontend Rules (React)](#frontend-rules-react)
- [General Engineering Principles](#general-engineering-principles)
- [Git & Commits](#git--commits)
- [Documentation](#documentation)

## Security

1. **Never commit secrets.** `SECRET_KEY`, SMTP credentials, OAuth secrets, Azure Face keys — all via `.env` (backend) / `.env.local` (frontend), loaded through `python-decouple` / `import.meta.env`. Both `.env.example` files enumerate every variable a real `.env` needs; keep them in sync when adding a new setting.
2. **Never commit `.env`, `db.sqlite3`, or `media/`** — already covered by `.gitignore`; don't `git add -f` around it.
3. **Rate-limit any `AllowAny` endpoint that has a side effect** (sends email, calls an external API). Follow the existing `otp_send`/`otp_verify`/`social_login` DRF `ScopedRateThrottle` pattern in `config/settings.py`.
4. **Validate all user input server-side** — DRF serializers are the validation layer; never trust frontend-side validation alone. Enrollment gating (`AttendanceSerializer.validate()`) is the reference example: business rules belong in the serializer/view, not just the UI.
5. **Role checks belong in DRF permission classes**, not scattered `if request.user.role == ...` checks in view bodies where avoidable.

## Backend Rules (Django/DRF)

1. **One Django app per bounded domain concept.** Don't add unrelated models to an existing app (e.g., a new "notifications" feature gets its own app, not bolted onto `accounts`).
2. **Follow the existing per-app file shape**: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`, `tests.py`, `migrations/`. Don't invent a different structure for a new app.
3. **Use `DefaultRouter` + `ViewSet`** for anything that's genuinely resource CRUD; use plain `APIView`/function-based views for actions that aren't (auth, OTP, face recognition, dashboard aggregations) — matches current `accounts`/`face`/`dashboard` pattern.
4. **Business rules that span models (e.g., enrollment gating) live in serializer `validate()` or the view**, not in migrations or the admin.
5. **Face recognition must stay provider-pluggable.** Any change to `face/providers.py` must work through the existing `FACE_PROVIDER=local|azure` switch — don't hardcode a call to one provider from `views.py`.
6. **Lazy-import heavy/optional dependencies** (`dlib`, `face_recognition`) so the rest of the app runs on hosts where they aren't installed — this is why `dlib` isn't in `requirements.txt` today.
7. **Every new model needs a migration committed alongside it** — CI runs `manage.py makemigrations --check` and fails the build if one is missing.
8. **Write a test for new views/serializers.** CI runs `manage.py test` on every push to `main`/`develop` and every MR.

## Frontend Rules (React)

1. **All HTTP calls go through `services/api.js`.** Never call `axios`/`fetch` directly from a page/component — the centralized client handles the base URL and auth header injection.
2. **Keep business/API logic out of presentation components.** Fetch/transform data in the page component or a hook, keep JSX focused on rendering.
3. **Use the toast/confirm system (`NotificationContext`) for all user feedback and confirmations** — never native `alert()`/`confirm()`. (This was an explicit cleanup done 2026-07-20; don't regress it.)
4. **One page component per route** under `src/pages/`, registered in `App.jsx`. Shared chrome goes in `layouts/`, not duplicated per page.
5. **One stylesheet per feature area** under `src/styles/`, matching the existing naming (`<feature>.css`). Don't grow an unrelated file.
6. **Run `npm run lint` (ESLint) before committing** — flat-config rules (`eslint.config.js`) include `react-hooks` and `react-refresh` recommended sets; fix violations, don't disable rules inline without reason.
7. **Environment-specific values go through `import.meta.env.VITE_*`**, declared in `.env.example` — never hardcode an API URL or client ID.

## General Engineering Principles

Follow SOLID, DRY, KISS, YAGNI as defaults:

- **Single Responsibility** — a view/component/serializer does one thing. If a view is doing auth, validation, and business logic and formatting, consider splitting.
- **DRY, but not premature** — three similar lines beat a speculative abstraction; extract only once a third real use appears.
- **Avoid duplicated logic** — if the same validation/calculation appears in two serializers or two components, extract it (e.g., a shared serializer mixin, a shared util module).
- **Prefer composition over inheritance** — Django's class-based views already lean this way; don't build deep custom base-class hierarchies.
- **Avoid circular imports** — apps should depend downward (e.g., `attendance` imports from `students`/`courses`, not vice versa).
- **Keep functions and components small and focused** — if a view method or component exceeds ~50-70 lines of real logic, look for a natural split.
- **Handle exceptions explicitly; don't swallow them silently.** Log server-side errors; surface actionable messages to the client via the toast system.
- **Maintain backward compatibility on the API contract** where reasonably possible — changing a response shape breaks the frontend and any external consumer (Postman collection, mobile clients if added later).

## Git & Commits

1. **Branch naming**: `feature/US-NN-name`, `bugfix/name`, `chore/name`, `hotfix/name`, `docs/name` (see `Guidelines/REALITY_CHECK.md` "Branch Strategy").
2. **`main`** is production-ready (auto-deploys via GitLab CI); **`develop`** is the integration branch. Don't push directly to `main` outside the normal PR/MR flow.
3. **Write meaningful commit messages** — state the "why", not just "what changed" (the diff already shows what).
4. **PRs/MRs via `gh pr create`** (GitHub) — GitLab MRs mirror for CI/deploy purposes; keep both remotes in sync (see [deployment.md](deployment.md)).
5. Both GitHub and GitLab remotes are kept in sync intentionally — don't "clean up" by removing one without checking [deployment.md](deployment.md) first (GitLab drives the actual deploy pipeline).

## Documentation

1. **Update `docs/memory.md` after any major implementation** — it's the canonical, always-current status doc (see [memory.md](memory.md)). `HANDOFF.md`/`NEXT_STEPS.md` remain as dated session logs, not the primary source going forward.
2. **New env vars** → update both the relevant `.env.example` and, if it changes system behavior, [architecture.md](architecture.md) or [deployment.md](deployment.md).
3. **New/changed endpoints** → update [api.md](api.md).
4. **Non-trivial technical decisions** → add an entry to [decisions.md](decisions.md) (ADR format) instead of only explaining it in a commit message or PR description.
5. Document exported/public functions and classes where their purpose isn't obvious from the name — don't restate what the code already makes clear.
