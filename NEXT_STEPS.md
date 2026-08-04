# NEXT_STEPS.md

> Last updated: 2026-08-04 — see `HANDOFF.md` (session handoff) and `docs/memory.md`
> (canonical status per ADR-007) for full current status. This file is kept brief
> and points there rather than duplicating; correct it here if it drifts again.

## What's actually next (2026-08-04)

1. **Push `develop` to GitLab** — 7 commits ahead of `gitlab/develop`, unpushed.
   GitLab drives the real deploy pipeline, so do this deliberately (see
   `docs/deployment.md`). GitHub (`origin`) is already in sync.
2. **Close stale GitHub issues** for dashboard features shipped in PR #30 but never
   closed: #17, #18, #19, #20, #21, #22, #24.
3. **PM deliverables (Prizma)** — GitHub says #5/#7/#8/#11/#12 are Done, but #5
   (SRS) and #7 (Requirements Gathering) had no actual artifact until this session
   wrote `docs/srs.md`/`docs/requirements-gathering.md` — see `HANDOFF.md`
   Corrections for the full picture. Issue #51 (Risk Management) is still open.
4. **Frontend gaps (Ekata)** — Dashboard UI (#1) overlaps with #48 (RBAC-aware
   dashboard UI/UX, board says "In Progress") — reconcile scope before starting
   either. ECA Tracking (#23) is also blocked on a missing backend model.
5. **Azure Face API provider** — implemented but still unverified end-to-end
   against a real Azure Face resource (risk R-11/W-08).
6. **Mobile epic** (#34, 12 sub-issues) — planning complete, zero code. Sprint 2
   "Mobile Core" starts 2026-08-09. Board shows #36/#38 as "In Progress" —
   confirm that's accurate before trusting it.

## Where things run

- Backend dev: `cd backend && python manage.py runserver` (see `backend/.env.example`)
- Frontend dev: `cd frontend && npm run dev`
- CI/tests: GitLab CI (`.gitlab-ci.yml`) on push to `main`/`develop` and on MRs
- Deploy: GitLab CI, `main` branch only → Azure App Service `ams-backend`
