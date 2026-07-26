# Contributing — Attendance Management System

> **Purpose:** How to get a local environment running and submit a change.
> **Scope:** Whole repo (backend, frontend).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Making a Change](#making-a-change)
- [Branch & Commit Conventions](#branch--commit-conventions)
- [Before Opening a PR](#before-opening-a-pr)
- [Code Review Expectations](#code-review-expectations)
- [Where Things Live](#where-things-live)

## Prerequisites

- Python 3.11 (backend)
- Node 20 (frontend)
- A GitHub account (PRs/issues) — GitLab access if you need to touch deploy config ([deployment.md](deployment.md))

## Local Setup

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # fill in SECRET_KEY at minimum
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
copy .env.example .env        # points VITE_API_URL at the backend
npm run dev
```

Or from the repo root: `npm run dev` runs both concurrently (assumes a `.venv-win` virtualenv — adjust the root `package.json`'s `backend` script if yours is named differently). Full detail in [deployment.md](deployment.md).

## Making a Change

1. Read [rules.md](rules.md) first — it's the enforceable convention set (backend app shape, frontend HTTP-client rule, no native `alert()`/`confirm()`, etc.). PRs that violate it are a review blocker, not a nit.
2. Check [docs/memory.md](memory.md) for current status/priorities and [phases.md](phases.md) for where a feature is meant to land, so new work doesn't collide with something in flight.
3. For anything touching the DB schema, read [database-schema.md](database-schema.md) first — note the known gap that `Student` (in `students`) and `accounts.User` (role=`student`) are not FK-linked; don't assume they are.
4. For a non-trivial technical decision (new dependency, new pattern, a tradeoff), add an ADR entry to [decisions.md](decisions.md) instead of only explaining it in the PR description — PR descriptions don't survive a `git blame` five months later, ADRs do.

## Branch & Commit Conventions

- Branch naming: `feature/US-NN-name`, `bugfix/name`, `chore/name`, `hotfix/name`, `docs/name` (see `Guidelines/REALITY_CHECK.md` "Branch Strategy").
- `main` is production and auto-deploys via GitLab CI on every merge — never push directly to it outside the normal PR/MR flow.
- `develop` is the integration branch; branch new work from it.
- Commit messages should explain *why*, not just *what* — the diff already shows what changed.

## Before Opening a PR

- [ ] Backend: `python manage.py makemigrations --check` (CI fails the build if a migration is missing) and `python manage.py test`.
- [ ] Frontend: `npm run lint` (ESLint flat config — fix violations rather than disabling a rule inline without reason) and `npm run build` (catches build-time errors CI will also catch).
- [ ] New env var? Update the relevant `.env.example` and, if it changes system behavior, [architecture.md](architecture.md) or [deployment.md](deployment.md).
- [ ] New/changed endpoint? Update [api.md](api.md).
- [ ] Touched something security-relevant (auth, rate limiting, a new `AllowAny` endpoint, a new external API call)? Check [security.md](security.md).

## Code Review Expectations

- PRs go through GitHub (`gh pr create`); GitLab MRs mirror for CI/deploy purposes — see [deployment.md](deployment.md) for why both exist. Don't consolidate to one remote without updating that doc first.
- Both GitHub Actions (test-only, `develop`) and GitLab CI (test → build → deploy, `main`) must pass before merge to `main`.
- A migration touching a table with production data should call that out explicitly in the PR description — reviewers should ask for a `migrate --plan` check against prod-like data on anything destructive.

## Where Things Live

| Kind of work | Location |
|---|---|
| API endpoint / business logic | `backend/<app>/` (one Django app per bounded domain — see [architecture.md](architecture.md)) |
| UI page | `frontend/src/pages/`, registered in `App.jsx` |
| Shared UI chrome | `frontend/src/layouts/` |
| HTTP client | `frontend/src/services/api.js` — all HTTP calls go through it, never direct `axios`/`fetch` from a component |
| Design/style change | `frontend/src/styles/<feature>.css` — one stylesheet per feature area, see [design.md](design.md) |
| Deploy/CI config | `.gitlab-ci.yml` (deploy), `.github/workflows/ci.yml` (test mirror) — see [deployment.md](deployment.md) before editing either |
| Architecture decision | [decisions.md](decisions.md) (ADR) |
| Status/priorities | [memory.md](memory.md) — update after any major implementation |
