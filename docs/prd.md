# Product Requirements Document (PRD) — Attendance Management System

> **Purpose:** Defines *what* the Attendance Management System (AMS) is, *why* it exists, and the scope of features it must support.
> **Scope:** Product-level requirements only — see [architecture.md](architecture.md) for *how* it's built.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Vision](#vision)
- [Goals](#goals)
- [Target Audience & Personas](#target-audience--personas)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Features & Priorities](#features--priorities)
- [User Stories](#user-stories)
- [Success Metrics](#success-metrics)
- [Constraints](#constraints)
- [Assumptions](#assumptions)
- [Risks](#risks)
- [Future Roadmap](#future-roadmap)

## Overview

AMS is a web application for tracking student attendance across courses, built as the term project for CSE 405 (Software Project Management). It replaces manual roll-calls and spreadsheets with a Django/DRF API and a React web client, and adds facial-recognition-based attendance marking as a differentiator over a plain CRUD system.

## Problem Statement

Manual attendance tracking (paper sheets, ad-hoc spreadsheets) is slow, error-prone, and produces no queryable history — faculty can't easily answer "who is at risk of falling below the attendance threshold this semester?" without manual tallying. Students have no self-service way to check their own record.

## Vision

A single system where: faculty mark attendance in seconds (manually, in bulk, or via face recognition), administrators manage the student/course/enrollment master data, and everyone — admin, faculty, student — gets a dashboard suited to their role, backed by exportable reports (CSV/PDF).

## Goals

1. Eliminate manual tallying — attendance percentage, at-risk lists, and chronic-latecomer detection are computed by the system.
2. Support multiple attendance-marking methods (manual, bulk, code-based, face recognition) so faculty can pick what fits their classroom.
3. Give every role (admin/faculty/student) a dashboard relevant to their permissions.
4. Keep the system deployable on low-cost infrastructure (Azure App Service B1 tier, SQLite/Postgres).

## Target Audience & Personas

| Persona | Role | Needs |
|---|---|---|
| **Admin** (e.g., department staff) | `admin` | Manage users, students, courses, view system-wide reports, import master data in bulk. |
| **Faculty** | `faculty` | Mark attendance for their courses, view their own course's stats, generate attendance codes for self-check-in, export reports. |
| **Student** | `student` | View personal attendance history and percentage, verify identity via face registration. |

## Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | Users can register, verify email via OTP, and log in with JWT (access + refresh tokens). |
| FR-2 | Users can sign in via Google or Facebook OAuth. |
| FR-3 | Admin/faculty can perform CRUD on Students, Courses, and Enrollments. |
| FR-4 | Faculty can mark attendance individually or in bulk for a course/date. |
| FR-5 | Faculty can generate short-lived attendance codes students can self-check-in against. |
| FR-6 | Students can register a face (image) and be recognized/marked present via face recognition. |
| FR-7 | Any authenticated user can view attendance reports filtered by course/student/date range. |
| FR-8 | Reports can be exported as CSV or PDF. |
| FR-9 | Dashboard exposes program/section breakdowns, attendance stats, at-risk students, chronic latecomers, faculty performance, and incomplete-record detection. |
| FR-10 | Admin can bulk-import master data (students/courses) via the dashboard import endpoint. |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | **Security** — no secrets committed to the repo; all config via environment variables (`python-decouple`). JWT-based auth on all non-public endpoints. |
| NFR-2 | **Portability** — must run on SQLite for local dev and Postgres in production without code changes (env-driven `DATABASE_URL`). |
| NFR-3 | **Degradability** — the app must run even where `dlib`/`face_recognition` can't be installed (constrained hosting); `FACE_PROVIDER=azure` is a fallback to a cloud API. |
| NFR-4 | **Rate limiting** — public-facing endpoints that trigger side effects (OTP email, social login) are throttled per-IP. |
| NFR-5 | **CI** — every push to `main`/`develop` and every MR runs migrations-check, `manage.py check`, and the full test suite before merge/deploy. |
| NFR-6 | **Timezone correctness** — server runs in `Asia/Kathmandu` time; all date-based attendance logic must respect this. |

## Features & Priorities

| Feature | Priority | Status |
|---|---|---|
| Auth (register/login/JWT/OTP/social) | P0 | Done |
| Student/Course/Enrollment CRUD | P0 | Done |
| Manual + bulk attendance marking | P0 | Done |
| Attendance report + CSV/PDF export | P0 | Done |
| Attendance codes (self-check-in) | P1 | Done |
| Face registration & recognition attendance | P1 | Done |
| Dashboard (stats, at-risk, latecomers, faculty performance) | P1 | Done, backend-complete |
| Dashboard UI (frontend) | P1 | In progress (see [phases.md](phases.md)) |
| ECA (extra-curricular activity) tracking | P2 | Open |
| Notifications (email/SMS) | P3 | Not started |

## User Stories

See [`docs/phases.md`](phases.md) for the phase-by-phase breakdown and `Guidelines/REALITY_CHECK.md`'s US-01…US-15 table for the original numbering. Representative stories:

- **US-04**: As faculty, I can mark attendance for my course roster in one bulk action so I don't submit one request per student.
- **US-07**: As a student, I can register my face so the system can recognize me for attendance without me touching a device.
- **US-09**: As faculty/admin, I can pull a report of a student's/course's attendance over a date range and export it.
- **US-10**: As any authenticated user, I see a dashboard suited to my role when I log in.
- **US-14**: As faculty, I can generate a time-limited code students enter to self-mark attendance.

## Success Metrics

- Attendance marking for a full class takes under 1 minute (bulk or face-recognition path) vs. minutes of manual tally.
- Zero attendance records created for non-enrolled students (enforced server-side, not just UI-side).
- CI test suite passes on every merge to `main`/`develop` — no untested code ships.

## Constraints

- Small team (3 people — see [`docs/memory.md`](memory.md) for current assignments), academic-term timeline.
- Hosting budget constrains the backend to Azure App Service's lower tiers, which cannot always build `dlib` from source — hence the pluggable `FACE_PROVIDER`.
- SQLite in local/dev; Postgres only when `DATABASE_URL` is set (no separate dev/prod code paths).

## Assumptions

- One face encoding per student is sufficient for recognition (no multi-angle enrollment).
- A student's app-login account and their `Student` record are logically related but not FK-linked in the current schema (see [architecture.md](architecture.md#data-model)) — treated as acceptable for the current scope.

## Risks

| Risk | Mitigation |
|---|---|
| `dlib` fails to build on constrained hosts | `FACE_PROVIDER=azure` fallback to Azure AI Face API |
| OTP/social-login endpoints abused (spam, quota burn) | Per-IP DRF throttling (`THROTTLE_OTP_SEND`, `THROTTLE_OTP_VERIFY`, `THROTTLE_SOCIAL_LOGIN`) |
| Stale planning docs mislead contributors | `docs/memory.md` is the canonical status doc; superseded docs are marked accordingly |

## Future Roadmap

See [`docs/phases.md`](phases.md) Phase 7 (Notifications) and Phase 9+ for planned work: SMS/email notifications, ECA tracking, and expanded reporting/analytics.
