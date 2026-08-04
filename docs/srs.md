# Software Requirements Specification (SRS) — Attendance Management System

> **Format:** IEEE 830-1998 structure, adapted for a course project.
> **Purpose:** The formal requirements deliverable for CSE 405 (GitHub issue #5 / Master Tracker FE-003). Distinct from [prd.md](prd.md): the PRD explains product intent and priorities for the team; this SRS is the structured, gradable requirements artifact, and is derived from the PRD, [architecture.md](architecture.md), and [database-schema.md](database-schema.md), which remain the source of truth for anything this document simplifies.
> **Status:** Written against the *as-built* system (2026-08-04), not a pre-implementation plan — the product already exists, so this SRS documents delivered behavior plus the few items still pending (see §2.3, §6).
> **Last updated:** 2026-08-04 · **Version:** 1.0

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [External Interface Requirements](#3-external-interface-requirements)
4. [System Features (Functional Requirements)](#4-system-features-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Other Requirements](#6-other-requirements)
7. [Appendix: Traceability](#7-appendix-traceability)

---

## 1. Introduction

### 1.1 Purpose

This document specifies the software requirements for the Attendance Management System (AMS), a web application that digitizes classroom attendance tracking for an academic institution. It is intended for the course instructor/evaluator, the three-person development team, and any future maintainer.

### 1.2 Scope

AMS covers: user authentication (including social login), student/course/enrollment management, four attendance-marking methods (manual, bulk, self-check-in code, face recognition), reporting/export, and role-scoped dashboards for admin, faculty, and student users. It does **not** currently cover: SMS/email notifications beyond OTP, extra-curricular activity (ECA) tracking, or a mobile app (planned separately — see [mobile-requirements.md](mobile-requirements.md)).

### 1.3 Definitions, Acronyms, Abbreviations

| Term | Meaning |
|---|---|
| AMS | Attendance Management System (this project) |
| OTP | One-Time Password (email-based identity verification) |
| DRF | Django REST Framework |
| JWT | JSON Web Token (access/refresh token auth) |
| RBAC | Role-Based Access Control |
| ECA | Extra-Curricular Activity |
| FR / NFR | Functional / Non-Functional Requirement |

### 1.4 References

- [prd.md](prd.md) — product requirements and priorities
- [architecture.md](architecture.md) — system design
- [database-schema.md](database-schema.md) — data model
- [api.md](api.md) — endpoint reference
- [security.md](security.md), [security-standards.md](security-standards.md)
- IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*

### 1.5 Overview

Section 2 describes the product context and constraints. Section 3 specifies external interfaces. Section 4 lists functional requirements grouped by feature. Section 5 lists non-functional requirements. Section 6 covers remaining items.

## 2. Overall Description

### 2.1 Product Perspective

AMS is a standalone web application, not an extension of an existing system. It is a Django/DRF backend (REST API) paired with a React/Vite single-page frontend, deployed on Azure. It integrates with three external services: Brevo (SMTP email for OTP), Google/Facebook OAuth (social login), and optionally Azure AI Face API (face recognition, alternative to the local `dlib` engine). Full topology: [architecture.md](architecture.md#deployment-architecture).

### 2.2 Product Functions (Summary)

- Register/authenticate users (email+OTP, or Google/Facebook)
- Manage students, courses, and enrollments (admin/faculty)
- Mark attendance: manually, in bulk, via a short-lived self-check-in code, or via face recognition
- Query and export attendance reports (CSV/PDF)
- View role-appropriate dashboards with attendance statistics, at-risk detection, chronic-latecomer detection, and faculty performance metrics
- Bulk-import master data (students/courses) as an admin

Full detail in §4.

### 2.3 User Classes and Characteristics

| Class | Technical proficiency | Frequency of use | Primary functions |
|---|---|---|---|
| **Admin** | Moderate–high | Regular | User/student/course management, system-wide reports, bulk import |
| **Faculty** | Low–moderate | Daily (during class) | Mark attendance, generate check-in codes, view own-course reports |
| **Student** | Low | Occasional | View own attendance history/percentage, register face |

### 2.4 Operating Environment

- **Server**: Azure App Service (Linux, Python 3.11), PostgreSQL (prod) or SQLite (dev)
- **Client**: any modern evergreen browser (Chrome, Edge, Firefox, Safari) with JavaScript enabled; face recognition and camera-based features additionally require browser camera/WebRTC permission
- **Network**: HTTPS required in production; internet connectivity required (no offline mode on web — offline support is mobile-only, see [mobile-architecture.md](mobile-architecture.md))

### 2.5 Design and Implementation Constraints

- Small team (3 people), fixed academic-term timeline — see [prd.md §Constraints](prd.md#constraints)
- Hosting budget limits the backend to Azure App Service's lower tiers, which cannot always build `dlib` from source natively — addressed by the pluggable `FACE_PROVIDER` (local dlib vs. Azure Face API), see [decisions.md](decisions.md) ADR-002/ADR-003
- Must run on SQLite (dev) and PostgreSQL (prod) without code changes (`DATABASE_URL`-driven)
- No native mobile app at this time (web-responsive only); mobile is planned but out of current scope

### 2.6 User Documentation

A formal end-user manual is not yet written (tracked as GitHub #32/T-032, unassigned/pending). This SRS and [api.md](api.md) currently serve technical readers; a plain-language user guide is a remaining deliverable.

### 2.7 Assumptions and Dependencies

- One face encoding per student is sufficient (no multi-angle enrollment) — see [prd.md §Assumptions](prd.md#assumptions)
- Availability of Brevo SMTP, Google/Facebook OAuth, and (optionally) Azure Face API as external dependencies; the system degrades (not crashes) if `FACE_PROVIDER=azure` is unconfigured, falling back to local dlib where installable

## 3. External Interface Requirements

### 3.1 User Interfaces

React SPA served from Azure Storage static hosting. Role-based navigation (admin/faculty/student see different menu items and dashboard widgets). UI conventions — spacing, color, feedback (toast/confirm system, never native `alert()`/`confirm()` per ADR-006) — are specified in [design.md](design.md).

### 3.2 Hardware Interfaces

None beyond the client device's camera (for face registration/recognition), accessed via the browser's WebRTC/`getUserMedia` API — no direct hardware integration.

### 3.3 Software Interfaces

| Interface | Direction | Purpose |
|---|---|---|
| Brevo SMTP | Outbound | OTP email delivery |
| Google OAuth 2.0 | Outbound/inbound | Social sign-in token verification |
| Facebook OAuth | Outbound/inbound | Social sign-in token verification |
| Azure AI Face API | Outbound (optional) | Face registration/recognition when `FACE_PROVIDER=azure` |
| Frontend ↔ Backend | REST/JSON over HTTPS | See [api.md](api.md) for the full endpoint list |

### 3.4 Communications Interfaces

REST API over HTTPS; JWT Bearer token in the `Authorization` header for authenticated requests; CORS restricted to configured `CORS_ALLOWED_ORIGINS`.

## 4. System Features (Functional Requirements)

Each feature below maps to one or more FR IDs from [prd.md](prd.md#functional-requirements) and a user story ID from the risk/dependency tracker (see [memory.md §External Trackers](memory.md#external-trackers)).

### 4.1 Authentication & Authorization (FR-1, FR-2 / US-01)

- **4.1.1** The system shall allow a new user to register with email, password, and role.
- **4.1.2** The system shall send a one-time password (OTP) to the user's email for verification before account activation, with a configurable expiry (`OTP_EXPIRY_MINUTES`) and resend cooldown (`OTP_RESEND_COOLDOWN_SECONDS`).
- **4.1.3** The system shall issue a JWT access token and refresh token on successful login.
- **4.1.4** The system shall allow sign-in via Google or Facebook OAuth as an alternative to password login.
- **4.1.5** The system shall enforce role-based access control (admin/faculty/student) on every protected endpoint.
- **4.1.6** The system shall throttle OTP-send, OTP-verify, and social-login endpoints per-IP to prevent abuse.

### 4.2 Student, Course, and Enrollment Management (FR-3 / US-02, US-03)

- **4.2.1** Admin/faculty shall be able to create, read, update, and delete Student records.
- **4.2.2** Admin/faculty shall be able to create, read, update, and delete Course records.
- **4.2.3** Admin shall be able to enroll a student in a course (Enrollment record) and remove an enrollment.
- **4.2.4** The system shall prevent duplicate enrollment of the same student in the same course.

### 4.3 Attendance Marking (FR-4, FR-5, FR-6 / US-04, US-07, US-08)

- **4.3.1** Faculty shall be able to mark attendance for a single student on a given course/date.
- **4.3.2** Faculty shall be able to mark attendance for an entire course roster in one bulk action.
- **4.3.3** The system shall reject an attendance-marking attempt for a student not enrolled in the target course.
- **4.3.4** Faculty shall be able to generate a short-lived attendance code; students shall be able to self-check-in by entering a valid, unexpired code.
- **4.3.5** A student shall be able to register a face image; the system shall store a face encoding, not the raw image, for matching.
- **4.3.6** The system shall recognize a registered student's face and mark attendance automatically, using either the local `dlib` engine or the Azure AI Face API depending on `FACE_PROVIDER` configuration.
- **4.3.7** The system shall never log or return raw face embeddings in any API response (privacy requirement, also NFR-7).

### 4.4 Reporting (FR-7, FR-8 / US-06, US-09)

- **4.4.1** Any authenticated user shall be able to query attendance records filtered by course, student, and/or date range, scoped to what their role is permitted to see.
- **4.4.2** The system shall compute and return total records, present count, absent count, and attendance percentage for a filtered query.
- **4.4.3** The system shall allow exporting a report as CSV or PDF.

### 4.5 Dashboard & Analytics (FR-9 / US-05, US-D1–D10)

- **4.5.1** The system shall provide role-scoped dashboard data: program/section breakdowns, per-student attendance breakdown, and aggregate attendance statistics.
- **4.5.2** The system shall identify "at-risk" students (attendance percentage below a threshold).
- **4.5.3** The system shall identify "chronic latecomer" students (repeated late marks).
- **4.5.4** The system shall detect incomplete attendance records (e.g., a session with no marks at all).
- **4.5.5** The system shall provide faculty-performance metrics (e.g., marking consistency) to admin users.

### 4.6 Bulk Data Import (FR-10 / US-D6)

- **4.6.1** Admin shall be able to bulk-import student/course/enrollment master data via CSV or JSON upload.
- **4.6.2** The system shall validate each row server-side and reject malformed rows individually rather than failing the whole batch.
- **4.6.3** The system shall support a dry-run mode that reports what would be imported without committing changes.

### 4.7 Not Yet Implemented (tracked, out of current delivered scope)

- Email/SMS notifications (US-11) — Phase 7, not started
- QR-code attendance (US-12) — open
- ECA tracking (US-D7) — open, no backend model yet
- Mobile app — planning complete, implementation not started (see [mobile-requirements.md](mobile-requirements.md))

## 5. Non-Functional Requirements

Numbered to align with [prd.md §Non-Functional Requirements](prd.md#non-functional-requirements) (NFR-1–6) plus two additions specific to this SRS:

- **NFR-1 Security**: No secrets committed to the repository; all configuration via environment variables. JWT-based auth on all non-public endpoints. See [security.md](security.md) for the current gap list (e.g., no dependency-vulnerability scanning yet).
- **NFR-2 Portability**: Must run on SQLite (dev) and PostgreSQL (prod) without code changes.
- **NFR-3 Degradability**: The app must remain functional where `dlib`/`face_recognition` cannot be installed; `FACE_PROVIDER=azure` is the fallback.
- **NFR-4 Rate Limiting**: Public side-effect endpoints (OTP email, social login) are throttled per-IP.
- **NFR-5 CI Enforcement**: Every push to `main`/`develop` and every merge/pull request runs migration checks, `manage.py check`, and the full backend test suite before merge/deploy.
- **NFR-6 Timezone Correctness**: Server runs in `Asia/Kathmandu`; all date-based attendance logic must respect this timezone.
- **NFR-7 Privacy** *(new in this SRS)*: Student face embeddings are biometric personally identifiable information (PII) and must never be logged or returned in any serializer/API response (see risk R-05 in the risk tracker).
- **NFR-8 Availability/Maintainability** *(new in this SRS)*: No formal uptime SLA (academic project), but the deployment must support rollback via redeploying a prior Azure deployment slot or reverting the offending commit — see [deployment.md §Rollback Plan](deployment.md#rollback-plan).

## 6. Other Requirements

### 6.1 Legal/Compliance

Student face data is biometric PII; no formal data-retention or consent policy is documented yet — flagged as an open item, not a resolved requirement. Any production use beyond the course context would need this addressed before go-live.

### 6.2 Database Requirements

See [database-schema.md](database-schema.md) for the authoritative, code-verified schema. Notable open data-integrity item: `Student` (students app) and `accounts.User` (role=`student`) are not foreign-key linked — see [database-schema.md](database-schema.md) and risk R-04.

## 7. Appendix: Traceability

| FR/NFR (this SRS) | PRD ID | User Story | Status |
|---|---|---|---|
| 4.1 | FR-1, FR-2 | US-01 | Done |
| 4.2 | FR-3 | US-02, US-03 | Done |
| 4.3.1–4.3.4 | FR-4, FR-5 | US-04 | Done |
| 4.3.5–4.3.7 | FR-6 | US-07, US-08 | Done |
| 4.4 | FR-7, FR-8 | US-06, US-09 | Done |
| 4.5 | FR-9 | US-05, US-D1–D10 | Done (backend); Dashboard UI frontend in progress |
| 4.6 | FR-10 | US-D6 | Done |
| 4.7 | — | US-11, US-12, US-D7, mobile | Not started / open |

This table should be kept in sync with [memory.md §Pending Features](memory.md#pending-features) and the risk tracker's user-story status matrix — if they disagree, `memory.md` wins per ADR-007.
