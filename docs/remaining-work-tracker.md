# Remaining Work Tracker

> Created: 2026-08-06 · Owner of this doc: Abhishek (backend)
> Companion to [docs/memory.md](memory.md) (canonical status per ADR-007), [HANDOFF.md](../HANDOFF.md), and the
> [GitHub Project board](https://github.com/users/sar-kaar/projects/5). Where those disagree, `memory.md` wins.
> Mirror as a Google Sheet: <https://docs.google.com/spreadsheets/d/1cXRmDkhBEzE6pf1wPndSA4IIGpdKBvMED1yTXEA1bwU/edit>
> (a *new* sheet — the existing external tracker sheet can't be edited via API; keep this repo doc canonical).
>
> **Purpose:** single view of what is *not done*, who owns it, and how work moves through the board.
> This exists because the GitHub board (Todo/In Progress/Done + Sprint field) and the external Google Sheet
> can drift; this file is version-controlled and reviewed in PRs.

---

## Board lifecycle (how we move items)

The board Status field has **Todo / In Progress / Done** (there is no separate "Backlog" column), plus a
**Sprint** iteration field. The requested backlog→sprint→doing→done flow maps to:

| Requested stage | Board action |
|---|---|
| Backlog | Status = **Todo**, no Sprint set |
| Pulled into sprint | Status = **Todo** + **Sprint** = current iteration |
| Processing / doing | Status = **In Progress** |
| Done | Status = **Done** (and close the issue) |

Moving items requires a `gh` token with the **`project`** write scope. As of 2026-08-06 the local token has only
`read:project`, so board moves are done via `scripts/board-move.sh` **after** running `gh auth refresh -s project`.

---

## Remaining work inventory (open issues: 15)

### Frontend — owner: **Ekata Rimal** (`ekatarimal`)

| # | Item | Status | Notes |
|---|---|---|---|
| 23 | US-12 ECA (Extra-Curricular Activity) Tracking — **frontend UI** | In Progress (backend done) | Backend model `ECAActivity` + `Attendance.eca_activity` shipped & migrated (commit d4f365d, migration 0004/0005). Frontend list/assign UI remains. |
| 48 | Master Data Bulk Import **UI** | In Progress | Backend bulk-import (US-11 / #21) is Done. This is the remaining web UI. |

### PM / Process — owner: **Prizma Subedi** (`Prizma515`)

| Item | Status | Notes |
|---|---|---|
| Push `develop` → GitLab | Open | `develop` is ahead of `gitlab/develop`; GitLab drives the Azure deploy. Coordinate before pushing (triggers prod deploy). |
| Board hygiene | Open | Confirm #36/#38 "In Progress" accuracy; ensure Sprint 2 items are pulled correctly on 2026-08-09. |
| Charter tech-stack fix | Open | `Project Charter (AMS).gdoc` lists Node/Express/MySQL; actual stack is Django/DRF/PostgreSQL. |

### Backend / Infra — owner: **Abhishek Rokaya** (`sar-kaar`)

The coherent, interrelated backend set below (the **10-item mobile-readiness plan**) is what backend is actively
driving to unblock **Sprint 2 "Mobile Core" (starts 2026-08-09)**.

### Mobile app (React Native) — Epic #34

Sub-issues #35, #37–#41, #43, #44 are mobile **frontend** (owner TBD, Sprint 2). #36 and #42 have **backend**
halves owned by Abhishek (see plan below). #45/#46 are build-pipeline/QA.

---

## The 10-item backend mobile-readiness plan (Abhishek)

Decomposition of **#36 Backend Readiness for Mobile** + **#42 Push Notifications (backend)**. These are
interrelated (auth → session lifecycle → device → push) and independently shippable & testable.

| # | Deliverable | Maps to | Board stage |
|---|---|---|---|
| B1 | Refresh-token **rotation** (`ROTATE_REFRESH_TOKENS`) | #36 | ✅ Done |
| B2 | Token **blacklist** app + migration (secure invalidation) | #36 | ✅ Done |
| B3 | **Logout** endpoint (blacklist refresh token) — `POST /api/auth/logout/` | #36 | ✅ Done |
| B4 | **Device registration** model (user, token, platform, active) | #42 | ✅ Done |
| B5 | Device **register / unregister / list** — `/api/devices/`, `/register/`, `/unregister/` | #42 | ✅ Done |
| B6 | **Push-send service** abstraction (`PUSH_PROVIDER` = console/expo) | #42 | ✅ Done |
| B7 | Push on **absence** marking (`AttendanceViewSet.perform_create`) | #42 | ✅ Done |
| B8 | **API versioning** / stable mobile contract (`/api/` namespace doc) | #36 | Todo |
| B9 | **CORS / allowed origins** review for mobile clients | #36 | Todo |
| B10 | **Contract doc** for mobile (auth flow, endpoints, error shapes) | #36 | Todo |

New endpoints shipped this session: `POST /api/auth/logout/`, `GET /api/devices/`,
`POST /api/devices/register/`, `POST /api/devices/unregister/`. New app: `notifications`
(`Device` model + `services.send_to_user`). New settings: `PUSH_PROVIDER` (default `console`),
`ROTATE_REFRESH_TOKENS` + `BLACKLIST_AFTER_ROTATION`. Migrations: `token_blacklist` (built-in),
`notifications/0001`. Tests: `accounts.LogoutBlacklistTest`, `notifications` (10), `attendance.AbsenceNotificationTest` — full suite **111 passing**.

Current backend baseline (already done, do **not** rebuild): SimpleJWT login/refresh, OTP (Brevo),
Google/Facebook OAuth, CORS middleware, DRF pagination.

---

## Status log

- **2026-08-06** — Tracker created. Backend baseline audited; frontend (#23, #48) flagged + assigned to Ekata;
  PM/process items flagged to Prizma (#34 comment). Board moves blocked on `project` token scope (see lifecycle note).
- **2026-08-06** — **B1–B7 shipped** (JWT rotation + blacklist + logout; `notifications` app with Device model,
  register/unregister/list endpoints, provider-gated push service; absence-push hook). Full suite 111 passing.
  Remaining backend: B8 (API versioning), B9 (CORS review), B10 (mobile contract doc).
