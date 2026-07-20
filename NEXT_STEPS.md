# NEXT_STEPS.md

> Last updated: 2026-07-20 — see `HANDOFF.md` for full current status.

The migration/dashboard-build steps this file used to track (Student
`program`/`section` fields, Attendance `LP`/`ECA` statuses, the GitHub Actions CI
pipeline, lazy `face_recognition` imports, and all 10 dashboard endpoints US-06
through US-15) are done and merged.

## What's actually next

1. **Push `develop`** to both `origin` (GitHub) and `gitlab` — local branch is ahead
   of both.
2. **Close stale GitHub issues** for dashboard features already shipped in PR #30:
   #17 (US-07), #18 (US-08), #19 (US-06), #20 (US-09), #21 (US-11), #22 (US-13).
3. **PM deliverables (Prizma)** — SRS, Project Charter, Wireframes, Team Norms,
   Requirements doc (issues #2, #3, #5, #7, #8) are all still open and overdue
   against the Week 1–2 checklist in `Guidelines/04_DELIVERABLES_CHECKLIST.md`.
4. **Frontend gaps (Ekata)** — Dashboard UI (#1, US-10) and ECA Tracking (#23,
   US-12) still open.
5. **Azure Face API provider** (`backend/face/providers.py`, added 2026-07-20) is
   implemented but only exercised locally so far — verify an end-to-end registration
   + match against a real Azure Face resource before relying on it in production,
   and decide whether `FACE_PROVIDER=azure` should become the deployed default given
   `dlib` can't build on constrained App Service plans.
6. **Guidelines/03_PROJECT_TRACKER.csv** is stale (still shows Sprint 1 in progress)
   — refresh it or stop treating it as authoritative; `HANDOFF.md` and
   `Guidelines/REALITY_CHECK.md` reflect real status.

## Where things run

- Backend dev: `cd backend && python manage.py runserver` (see `backend/.env.example`)
- Frontend dev: `cd frontend && npm run dev`
- CI/tests: GitLab CI (`.gitlab-ci.yml`) on push to `main`/`develop` and on MRs
- Deploy: GitLab CI, `main` branch only → Azure App Service `ams-backend`
