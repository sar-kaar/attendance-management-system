# Deployment — Attendance Management System

> **Purpose:** How AMS is built, tested, and deployed — dev, CI, and production.
> **Scope:** `.gitlab-ci.yml`, `.github/workflows/ci.yml`, Azure config (`.deployment`, `backend/.deployment`, `backend/postbuild.sh`, `backend/startup.sh`).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Environments](#environments)
- [Development Environment](#development-environment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Why Two CI Configs](#why-two-ci-configs)
- [Environment Variables](#environment-variables)
- [Production Deployment](#production-deployment)
- [Deployment Checklist](#deployment-checklist)
- [Rollback Plan](#rollback-plan)
- [Monitoring & Logging](#monitoring--logging)

## Environments

| Environment | Backend | Frontend | Database |
|---|---|---|---|
| Local dev | `python manage.py runserver` → `localhost:8000` | `npm run dev` → `localhost:5173` | SQLite |
| CI (test) | Ephemeral container, `python:3.11` | `node:20` (build check only) | SQLite (in-container) |
| Production | Azure App Service `ams-backend` | Azure Storage static website `amsfrontendweb` | PostgreSQL via `DATABASE_URL` (falls back to SQLite if unset) |

## Development Environment

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

Or from the repo root: `npm run dev` (runs both concurrently via the root `package.json`, which assumes a `.venv-win` virtualenv — adjust `backend` script if your venv is named differently).

## CI/CD Pipeline

**GitLab CI** (`.gitlab-ci.yml`) — the pipeline that actually deploys:

```mermaid
flowchart LR
    Push[push/MR] --> Test[test: migrations-check, check, manage.py test]
    Test -->|main only| BuildFE[build-frontend: npm ci && npm run build]
    Test -->|main only| DeployBE[deploy-backend: az webapp deploy --async]
    BuildFE --> DeployFE[deploy-frontend: az storage blob upload-batch]
```

- `test` stage runs on `main`, `develop`, and every merge request.
- `build-frontend`, `deploy-backend`, `deploy-frontend` only run on `main`, gated on `test` passing (`needs: [test]`).
- Backend deploy zips `backend/` and uploads via `az webapp deploy --async true` — async specifically because a synchronous deploy holds the HTTP request open while Oryx rebuilds `numpy`/`dlib-bin` (often >230s on the B1 plan), and Azure's front door cuts the request off, false-failing the job even when the deploy succeeds.
- Mail/OTP settings are synced from GitLab CI/CD masked variables into Azure App Service settings at deploy time, guarded on `EMAIL_HOST_PASSWORD` being set — if it's missing (e.g., a Protected variable unavailable on this branch), the sync is skipped rather than overwriting live settings with empty strings.

## Why Two CI Configs

`.github/workflows/ci.yml` runs the same backend test steps (migrations-check, check, test) on push/PR to `develop`, on GitHub Actions. This is intentional, not redundant config to delete: per `HANDOFF.md`, **GitHub is used for team visibility, issues, and PRs**, while **GitLab drives the actual deploy pipeline**. Both remotes (`origin` = GitHub, `gitlab` = GitLab) are kept in sync manually. Do not remove either pipeline without updating this doc and confirming with the team — GitHub Actions is the only CI signal visible to anyone only watching the GitHub repo.

## Environment Variables

See `backend/.env.example` and `frontend/.env.example` for the full, current list. Key ones:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key — required, no default in production |
| `DEBUG` | Must be `False` in production |
| `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` | Host/origin allowlists |
| `DATABASE_URL` | If set and starts with `postgres`, switches DB engine to Postgres; otherwise SQLite |
| `EMAIL_*` | Brevo SMTP for OTP email |
| `OTP_EXPIRY_MINUTES`, `OTP_RESEND_COOLDOWN_SECONDS`, `THROTTLE_OTP_*` | OTP behavior/rate limits |
| `GOOGLE_CLIENT_ID`/`SECRET`, `FACEBOOK_APP_ID`/`SECRET` | Social sign-in |
| `FACE_PROVIDER`, `AZURE_FACE_*` | Face recognition provider selection |
| `VITE_API_URL`, `VITE_GOOGLE_CLIENT_ID`, `VITE_FACEBOOK_APP_ID` (frontend) | Frontend build-time config |

## Production Deployment

- **Host**: Azure App Service `ams-backend` (resource group `ams-rg`); Oryx builds the Python app on deploy per `.deployment`/`backend/.deployment` (`SCM_DO_BUILD_DURING_DEPLOYMENT = true`), with `backend/postbuild.sh`/`backend/startup.sh` as custom hooks.
- **Frontend**: static build uploaded to Azure Storage static website `amsfrontendweb`.
- **Static files**: WhiteNoise serves Django static assets from within the App Service; frontend assets are served directly from Azure Storage, not through Django.

## Deployment Checklist

1. Confirm `main` has a passing `test` stage before merging (CI blocks build/deploy on it already, but verify locally if bypassing is ever considered — it shouldn't be).
2. If new env vars were added, confirm they're set in Azure App Service settings (or added to the GitLab CI/CD sync block in `.gitlab-ci.yml` if they're mail/OTP-related).
3. If a new migration was added, confirm it applies cleanly (`makemigrations --check` already gates this in CI, but a manual `migrate --plan` check against prod-like data is wise for destructive schema changes).
4. After deploy, smoke-test `GET /api/auth/me/` (with a token) and `GET /` (redirects to `FRONTEND_URL`) against the live App Service URL.

## Rollback Plan

No automated rollback is configured. To roll back:

1. Azure App Service keeps prior deployment slots/history under "Deployment Center" — redeploy a prior successful zip, or
2. Revert the offending commit on `main`, push, and let the pipeline redeploy the previous good state.
3. For a bad migration, `python manage.py migrate <app> <previous_migration_name>` against the production DB (requires DB access — coordinate before running against shared Postgres).

## Monitoring & Logging

No dedicated APM/log-aggregation is configured. Azure App Service's built-in log stream (`az webapp log tail`) and Application Insights (if enabled on the resource) are the available tools today. This is a documented gap, not a hidden one — add structured logging/monitoring as a future task if the team decides it's worth the operational overhead (see [phases.md](phases.md) for where to slot it).
