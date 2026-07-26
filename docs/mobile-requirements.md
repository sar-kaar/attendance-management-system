# Mobile Requirements — Attendance Management System

> **Purpose:** Defines *what* the mobile app must do — functional and non-functional requirements, target roles, and platforms. Companion to [mobile-architecture.md](mobile-architecture.md) (*how*) and [feature-matrix.md](feature-matrix.md) (*what's in/out of scope*).
> **Scope:** Mobile Application epic (GitHub #34) only. Web requirements are unchanged — see [prd.md](prd.md).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Goal](#goal)
- [Target Roles & Platforms](#target-roles--platforms)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Explicit Non-Goals](#explicit-non-goals)
- [Open Questions](#open-questions)

## Goal

Give students and faculty a native mobile client for the parts of AMS they use most day-to-day (marking/viewing attendance, checking results, getting notified), consuming the **same** Django/DRF backend as the web app — no parallel backend, no data model changes beyond what [gap-analysis.md](gap-analysis.md) identifies as required.

## Target Roles & Platforms

| Role | Mobile need |
|---|---|
| Student | View own attendance/reports, self-check-in via attendance code, receive at-risk/notification alerts, manage profile |
| Faculty | Mark attendance (manual + face recognition), view course rosters and dashboard stats, manage own courses |
| Admin | **Not a mobile target for v1** — admin/master-data workflows stay web-only (see [feature-matrix.md](feature-matrix.md)) |

Platforms: iOS and Android from a single codebase (React Native/Expo — see [decisions.md](decisions.md) ADR-008). No tablet-specific layout in v1; phone-first, responsive enough not to break on tablets.

## Functional Requirements

| ID | Requirement | Maps to web equivalent |
|---|---|---|
| MR-01 | Register/log in with email+password, Google, or Facebook | `POST /api/auth/register/`, `/google/`, `/facebook/` |
| MR-02 | Email OTP verification flow | `POST /api/auth/otp/send/`, `/verify/` |
| MR-03 | Session persists across app restarts (stored refresh token, silent re-auth) | `AuthContext.jsx` equivalent |
| MR-04 | Faculty: mark attendance manually for a course/date | `POST /api/attendance/`, `/attendance/bulk/` |
| MR-05 | Faculty: mark attendance via face recognition (device camera) | `POST /api/face/recognize/`, `/face/mark-attendance/` |
| MR-06 | Faculty/Student: self-check-in via attendance code | `POST /api/attendance/codes/` flow |
| MR-07 | Student: view own attendance history and stats | `GET /api/attendance/report/`, `/dashboard/students/:id/attendance/` |
| MR-08 | Faculty: view course roster, at-risk/chronic-latecomer lists | `GET /api/dashboard/*` |
| MR-09 | Push notification on attendance-threshold/at-risk events (once Phase 7 web notifications exist) | New — see [gap-analysis.md](gap-analysis.md) |
| MR-10 | Attendance marking queues locally and syncs when connectivity returns (offline queue MVP) | New — no web equivalent, mobile-specific |
| MR-11 | View/edit own profile (name, phone, profile picture) | `GET/PUT /api/auth/me/` |
| MR-12 | Log out (revoke local session, clear stored tokens) | Client-side only |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | Cold start to usable auth/unauth shell in under 3s on a mid-range device |
| NFR-02 | Works on a flaky/offline connection for attendance marking (MR-10); read-only screens degrade to a cached/last-known-good state, not a crash |
| NFR-03 | No secrets or long-lived tokens in plaintext storage — use platform secure storage (Keychain/Keystore via `expo-secure-store`) |
| NFR-04 | Face capture requests camera permission with a clear rationale prompt; app remains usable (minus that feature) if denied |
| NFR-05 | API base URL and all environment-specific config come from `mobile/.env.example`-documented vars — no hardcoded hosts (mirrors [rules.md](rules.md) for the web app) |
| NFR-06 | Accessibility: minimum tappable target size, readable contrast — not a v1 blocking requirement but tracked as debt if skipped |

## Explicit Non-Goals

See [feature-matrix.md](feature-matrix.md) for the full breakdown. Summary: no admin/master-data workflows, no on-device CSV/PDF generation, no ECA tracking (blocked upstream on a backend model gap, not mobile-specific), no offline face recognition (requires network round-trip to the configured `FACE_PROVIDER` either way).

## Open Questions

- Should faculty be able to mark attendance fully offline (queue + sync), or only self-check-in codes queue offline while manual/face marking requires connectivity? Current lean: queue applies to **manual marking only** for v1 (MR-10); face recognition needs a live provider call regardless of provider (`local` or `azure`), so it isn't queueable without also caching student face data on-device — deferred, see [phases.md](phases.md) Phase 22.
- Native Google/Facebook SDKs (mobile-native OAuth) vs. reusing the existing web OAuth redirect flow in an in-app browser — resolved in [gap-analysis.md](gap-analysis.md) (native SDKs, backend contract must accept a device-issued ID token instead of a web redirect code).
