# Sprint Retrospective & Feasibility Study — Attendance Management System

**Prepared:** July 21, 2026
**Covers:** Project kickoff (Jul 7) through current day (Jul 21) — Week 1 (Initiation), Week 2 (Sprint 0: Design), and the first two days of Week 3 (Sprint 1: Auth, per the original plan)
**Team:** Prizma Subedi (PM), Abhishek Rokaya (Backend/Admin, GitHub `sar-kaar`), Ekata Rimal (Frontend, GitHub `ekatarimal`)
**Sources used:** `git log` (69 commits on `develop`), GitHub issue tracker (26 issues), `HANDOFF.md`, `Guidelines/REALITY_CHECK.md`, `Cost Estimation (AMS).md`, `.gitlab-ci.yml`, `backend/config/settings.py`

> **Note on scope:** By the calendar plan in `Guidelines/01_WEEKLY_ROADMAP.md`, "Sprint 1" only started July 20 — we're two days into it. But the team asked for a retrospective on "sprint 1 to till now," so this covers everything shipped since Day 1, because on the engineering side the project has already blown past the Sprint 1 scope (see below). This document supersedes nothing — it sits alongside `HANDOFF.md` and `REALITY_CHECK.md` as the source of truth for how the project has actually gone, not how it was planned to go.

---

## 1. Executive Summary

The technical build is running **far ahead of schedule** — what the roadmap scopes as five sprints of backend work (auth, CRUD, face recognition, dashboards, reports, deployment) is already built, tested in CI, and live at `https://ams-backend.azurewebsites.net` in what the plan still calls "Sprint 1." At the same time, the project is running **behind on everything that isn't code**, though less flatly than first thought: of the PM's four assigned Week 1-2 documents, the Project Charter is genuinely done (written by Jul 15, a real PMBOK-style document), Requirements Gathering is marked done on Trello with no file found to back it up, SRS is actively being worked on, and Team Norms has not been started. The frontend owner's two open items (Dashboard UI, ECA Tracking) remain outstanding. See the addendum in section 4.2 for the full correction and how it was found. The single biggest risk carried out of these two weeks is not technical — it's that **one person (Abhishek) has produced effectively 100% of the commits, closed issues, and deployed infrastructure**, while the PM and frontend roles show close to zero tracked output so far. That imbalance, not face recognition accuracy or hosting cost, is the thing most likely to hurt this project by Week 7.

---

## 2. Reality Check: Planned vs. Actual

| | Planned (per `01_WEEKLY_ROADMAP.md`) | Actual, as of Jul 21 |
|---|---|---|
| Week 1 (Jul 7–12) | Kickoff, requirements, SRS draft — no code | All 4 Django apps scaffolded with models, JWT auth, working CRUD (initial commit Jul 9) |
| Week 2 / Sprint 0 (Jul 13–19) | Design docs only: ER diagram, wireframes, architecture, charter | Enrollment table + CRUD, dashboard stats API, face recognition module + tests, CSV/PDF export, unit tests, Postman collection, CI pipeline, backend/frontend split, first Azure deploy |
| Week 3 / Sprint 1 (Jul 20–26, in progress) | Goal: verify/secure existing auth, connect frontend | OTP email verification (Brevo), Google/Facebook social sign-in, Azure Face API as a second face-recognition provider, faculty data scoping, CRUD UX polish (toasts/confirms), CSRF/CORS hardening |
| Sprint 2–5 scope (Aug) | Student/course UI, face recognition, reports, dashboards, deployment | **Already shipped** in Sprint 0–1: dashboard analytics (US-06–US-13), attendance codes (US-14), bulk import groundwork, CSV/PDF export, live Azure deployment with CI/CD |

The gap runs in both directions at once: engineering is roughly 3–4 sprints ahead of the plan, while two of three role-tracks (PM docs, dedicated frontend features) are behind where Week 1–2 deadlines put them. `HANDOFF.md` already flags this and explicitly tells readers to stop trusting `Guidelines/03_PROJECT_TRACKER.csv` and `01_WEEKLY_ROADMAP.md` as current status — that's the right call, and this document treats them the same way (as the original plan to measure against, not as current fact).

---

## 3. What Went Well

- **Backend velocity and scope.** 69 commits landed on `develop` in under two weeks, covering everything the roadmap allotted five sprints for: auth + JWT + RBAC, full CRUD across students/courses/attendance/enrollment, face recognition (with a **second, swappable provider** — Azure AI Face API — added specifically to work around `dlib` not building on constrained Azure App Service plans), CSV/PDF export, a full analytics dashboard (US-06 through US-13), attendance codes, OTP email verification, and social sign-in.
- **Security risk closed early, not deferred.** The roadmap's own risk register flagged "hardcoded `SECRET_KEY` / open CORS" as a risk to fix "before Week 7 deploy, not after." Checked directly in `backend/config/settings.py`: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS` are all environment-configured via `python-decouple`, with safe non-production defaults. This was fixed in Week 2, not left for Week 7.
- **The Enrollment-table risk was resolved deliberately, not by accident.** The original roadmap flagged "no Enrollment table — any student markable in any course" as a Medium risk to decide by Week 2–3. It was added Jul 9 (Day 3) with a documented rationale in `REALITY_CHECK.md`: adding it after Ekata's UI work started would break the API contract, so it went in immediately as one migration, with `AttendanceSerializer.validate()` and `mark_bulk` enforcement, and a backfill migration. This is a real example of the "decide early, before it's expensive to change" principle working.
- **CI/CD exists and runs on every push.** `.gitlab-ci.yml` runs `makemigrations --check`, `manage.py check`, and the full test suite on every push to `main`/`develop` and on merge requests, with a separate frontend build stage and an automated Azure deploy stage. 986 lines of backend test code exist across the `accounts` and `attendance` apps.
- **Self-correcting documentation.** Rather than let the stale roadmap/tracker mislead the team, `HANDOFF.md` and `REALITY_CHECK.md` were introduced specifically to hold current, accurate state and explicitly say "don't trust the CSV." That's good practice under a fast-moving solo push — most teams don't catch this drift until a demo goes wrong.
- **Real production debugging, resolved.** The Azure deploy pipeline hit and fixed a string of genuine issues rather than papering over them: CSRF trusted-origin misconfiguration behind the Azure proxy, a startup script that couldn't find the virtualenv, gunicorn bind settings misaligned with the `Procfile`, and a bug where the app was silently swallowing real `dlib`/`face_recognition` install errors instead of surfacing them. All are fixed and merged.

## 4. What Went Wrong

### 4.1 Contribution imbalance — the real risk

This is the headline finding, and it's unambiguous from the data, not a guess:

| Signal | Finding |
|---|---|
| Commits on `develop` (69 total) | **100% authored by Abhishek** (`sar-kaar`/`Sarkar`). Zero commits from `Prizma515` or `ekatarimal`. |
| Frontend-directory commits | 9 of 9 authored by Abhishek — including the commit that added the entire React frontend (`fadaf01: feat: React frontend with full backend integration`). |
| GitHub issues closed (9 total) | All 9 are Abhishek's work (backend features, ER diagram, architecture doc). |
| GitHub issues assigned to Prizma (T-002 Requirements, T-003 SRS, T-007 Charter, T-008 Team Norms) | **All 4 still OPEN**, 0% complete, all overdue against the Week 1–2 deadlines in `04_DELIVERABLES_CHECKLIST.md`. |
| GitHub issues owned by Ekata (#1 US-10 Dashboard UI, #23 US-12 ECA Tracking) | Both still open — and the dashboard UI that exists so far was built by Abhishek, not by the person nominally assigned the frontend track. |

The practical effect: the project currently has a **bus factor of one**. If Abhishek is unavailable for even a few days, nothing else moves — there's no second person who has touched the codebase, and the PM-track deliverables that would normally provide project structure (SRS, charter, requirements) don't exist to fall back on either. This also means the "code review" and "peer review" processes described in `GIT_WORKFLOW.md` and `00_COMPLETE_PROJECT_GUIDE_BOOK.md` can't be functioning as designed — a PR reviewed and approved by someone who hasn't written any of the code they're reviewing is a rubber stamp, not a review.

### 4.2 Documentation and planning debt

- Zero of the four PM-owned Week 1–2 documents (SRS, Project Charter, Requirements Gathering writeup, Team Norms/Comms Plan) exist yet, despite being marked "Done" with fabricated-looking dates in `03_PROJECT_TRACKER.csv` (that CSV shows Sprint 0 100% complete, which is not true for the PM's share of it).

**Addendum (2026-07-21, later same day):** this claim was checked against GitHub issues only. The team's real Trello board (`trello.com/b/ecB6ppQa`, not the abandoned `tf3ceNmA` board this project's own `05_TRELLO_WORKFLOW_GUIDE.md` used to point to) tells a different, more accurate story:

| Doc | Trello status | What actually exists |
|---|---|---|
| T-007 Project Charter | Done, card moved 2026-07-21 | Real. `Project Charter (AMS).gdoc`, a full PMBOK-style document (PACT analysis, SWOT, stakeholder register, team roles), owned by Prizma's school account, last edited 2026-07-15. The document was finished six days before the Trello card caught up to it. |
| T-002 Requirements Gathering | Done, 2026-07-18 | Not found. No standalone requirements document exists in the repo or Google Drive. The card is marked done with no visible deliverable behind it. |
| T-003 SRS Document | Doing, card moved 2026-07-21 | Genuinely in progress today. No SRS file exists yet, consistent with the card status. |
| T-008 Team Norms and Comms Plan | To Do, not started | Consistent, nothing exists. |

So the PM track is not the flat zero this document originally reported. One real deliverable exists, one Trello "done" has no artifact behind it, one is actively being worked on, and one has not started. Also worth flagging: the Project Charter's stated tech stack (React, Node.js/Express, MySQL) does not match what was actually built (Django/DRF, SQLite), a real mismatch between the planning document and the shipped system.
- `03_PROJECT_TRACKER.csv` and `01_WEEKLY_ROADMAP.md` are both stale and, per `HANDOFF.md`, actively risk misleading anyone who reads them as current — they still show "Sprint 1 in progress" for basic register/login that's been done since Week 1.
- Wireframes (T-005) are unassigned and open — there's no design artifact backing the UI that already shipped.

### 4.3 Issue-tracker hygiene

- PR #30 ("Dashboard API — US-06 to US-13," merged Jul 18) implemented the backend for six issues (#17, #18, #19, #20, #21, #22) but none were closed — the tracker currently understates how much backend work is actually done.
- Two open issues are both titled "US-10" (#1 "Dashboard UI," frontend, genuinely open; #24 "Chronic Latecomers Detection," backend, already covered by PR #30) — a numbering collision from reused labels that risks confusing anyone triaging by ID.
- Issue #6 and #13 are both "T-001: GitHub Repo Setup," a leftover from the repo being deleted and recreated early on to fix branch-protection settings.

### 4.4 Deploy pipeline churn

The commit log shows real trial-and-error on deployment, not a clean first pass: GitHub Actions deploy workflow added, then removed twice in favor of Azure Deployment Center, then replaced again with GitLab CI; `az webapp deploy` flipped between synchronous and asynchronous modes twice in two days (Jul 19–20) chasing false-failure timeouts; the startup script was rewritten three times (dynamic venv discovery, then simplified to just activate `antenv`, then hardened again). None of this is unusual for a first-time Azure deployment, but it represents real time spent on infrastructure thrashing rather than features, and it's worth not repeating blind in Sprint 5 crunch.

### 4.5 Known unresolved technical risk

- **Azure Face API is implemented but unverified end-to-end.** `backend/face/providers.py` (added Jul 20) has only been exercised locally — it has not yet been tested against a real Azure Face resource in production, and `FACE_PROVIDER` still defaults to `local` (`dlib`), which is documented as unable to build on constrained App Service plans. This is a real gap between "code exists" and "feature works in production."
- **`dlib` build friction** was significant enough to need dedicated setup instructions (CMake + Visual Studio Build Tools on Windows) and a fallback provider — a real cost that the original roadmap didn't anticipate when it scoped face recognition as a single sprint's worth of "OpenCV integration."

---

## 5. Feasibility Study

### 5.1 Technical feasibility — **Confirmed, low risk**
The hardest part of the original scope (face recognition) is proven end-to-end locally and has a cloud fallback path for hosting constraints that weren't visible at planning time. Auth, RBAC, CRUD, reporting, and analytics are live in production, not prototypes. The stack (Django/DRF, SimpleJWT, React/Vite, SQLite, OpenCV/dlib or Azure Face API) has no open technical blocker. Residual risk is narrow and specific: verifying the Azure Face API path in production, and deciding whether SQLite is acceptable for the final deployed database or needs to move to a managed Postgres instance before grading/demo day.

### 5.2 Schedule feasibility — **Mixed; genuinely at risk, but not for the reason the roadmap assumed**
The roadmap treated face recognition (Sprint 3) as the highest schedule risk. In practice that's the one part of the plan running comfortably ahead. The actual schedule risk is on the **documentation and frontend-completeness side**: SRS, Charter, Requirements, Team Norms, Dashboard UI, and ECA Tracking are all still open with three-plus weeks left. None of these are individually hard, but they've had zero visible progress for two weeks against Week 1–2 deadlines, and a project graded on PMBOK-style deliverables (per the course's own guide book) can't submit code alone.

### 5.3 Resource / team feasibility — **At risk**
Nominal team size is three, but effective delivery capacity right now is one person across both backend and frontend, plus whatever PM/documentation work someone eventually does. This is the most important number in this whole document: **376 planned hours across the team (per `Cost Estimation (AMS).md`) assumed roughly even three-way effort (146/132/98 backend/frontend/PM hours); actual git and issue-tracker evidence shows one person carrying effectively all of it so far.** If that doesn't rebalance, either scope has to shrink, or the workload concentrates further on one person through Week 7 — a real burnout and single-point-of-failure risk the project's own Risk Register (R: "Team member unavailable") already anticipated, just aimed at the wrong person.

### 5.4 Economic feasibility — **Confirmed, favorable**
Per `Cost Estimation (AMS).md`: total mandatory tangible cost is NPR 157,740 (opportunity-cost labor NPR 138,900 + NPR 4,500 mandatory non-labor + 10% contingency), all software and tooling is free/open-source, and hosting is near-free (Azure App Service + free-tier storage, ~NPR 700 mandatory). Nothing about proven costs threatens the project. The only economic note worth adding post-hoc: the labor split assumed in that estimate (146/132/98 hours) doesn't match actual effort distribution — worth a quick reconciliation pass against the Personal Log sheet the guide book asks the team to maintain, if that's actually being filled in.

### 5.5 Operational feasibility — **Confirmed for what's built, with one open gap**
Role-based access (admin/faculty/student) is implemented and enforced at the API layer, not just the UI. Faculty data scoping (added Jul 19) means faculty only see their own assigned courses/students — a real access-control feature, not a placeholder. The system is reachable at a live URL today, which is more than most student projects can say two weeks in. The one open operational gap: nobody has run a full admin → faculty → student walkthrough against the *deployed* Azure instance with the Azure Face provider active — everything verified so far is either local or partial-production.

---

## 6. Risk Register — Original vs. Current Status

| Original risk (`01_WEEKLY_ROADMAP.md`) | Status now |
|---|---|
| Face recognition accuracy low | Mitigated — manual fallback still available; dual-provider design (local/Azure) is a stronger mitigation than the original plan called for |
| No Enrollment table | **Closed** — added Jul 9, enforced in serializer + bulk-mark logic |
| Hardcoded `SECRET_KEY` / open CORS | **Closed** — verified in `settings.py`, all env-configurable with safe defaults |
| Frontend framework undecided | Closed — React + Vite, in production |
| Team member unavailable | **Open, and understated** — the real exposure isn't "one person gets sick," it's that two of three people have near-zero tracked contribution right now |
| *(not in original register)* PM/documentation deliverables incomplete | **New, should be added** — 1 of 4 PM Week 1–2 docs genuinely done (Charter), 1 marked done with no artifact found (Requirements), 1 in progress (SRS), 1 not started (Team Norms). See section 4.2 addendum. |
| *(not in original register)* Azure Face API unverified in production | **New, should be added** — code complete, production path untested |
| *(not in original register)* Issue-tracker/tracker-doc drift | **New, low severity, should be added** — stale CSV/roadmap risk misleading anyone using them as status |

---

## 7. Recommendations / Action Items

| # | Action | Owner | Priority |
|---|---|---|---|
| 1 | Get Prizma unblocked on Requirements/SRS/Charter/Team Norms this week — even draft versions close the biggest schedule gap that actually exists | Prizma, PM-supported by team | Critical |
| 2 | Get Ekata committing directly — pair on the two open frontend issues (#1 Dashboard UI, #23 ECA Tracking) rather than letting Abhishek continue absorbing frontend scope | Ekata + Abhishek | Critical |
| 3 | Verify the Azure Face API provider end-to-end against a real Azure Face resource before treating it as production-ready | Abhishek | High |
| 4 | Close the six dashboard issues (#17, #18, #19, #20, #21, #22) already implemented by PR #30, after a quick sanity check against `/api/dashboard/*` | Abhishek | Medium |
| 5 | Retire or refresh `03_PROJECT_TRACKER.csv` and `01_WEEKLY_ROADMAP.md` so they stop contradicting `HANDOFF.md`/`REALITY_CHECK.md` | Prizma | Medium |
| 6 | Reconcile actual hours against `Cost Estimation (AMS).md`'s planned 146/132/98 split using the Personal Log sheet, and flag the imbalance to the teacher proactively rather than have it surface at final review | Prizma | Medium |
| 7 | Decide now whether the deployed database stays SQLite or moves to managed Postgres before final submission — don't leave it for Week 7 | Abhishek + team | Medium |
| 8 | Fix the duplicate/ambiguous issue numbering (#1 vs #24, both "US-10"; #6 vs #13, both "T-001") so tracker triage isn't confusing | Prizma | Low |

---

## 8. Bottom Line

Judged purely on shipped code, this project is ahead — arguably the strongest technical position it could be in two weeks into a seven-week academic project. Judged as a *team* project against the standards the team set for itself (PMBOK docs, shared ownership, peer review, balanced velocity), it's carrying real risk that has nothing to do with the technology. The fix is not more backend work — it's getting the other two-thirds of the team producing visible, tracked output before Sprint 2 planning, and treating the documentation debt as seriously as the team's own guide book says it should be treated.
