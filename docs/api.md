# API Reference — Attendance Management System

> **Purpose:** Documents every backend endpoint — auth, request/response shape, errors, rate limits.
> **Scope:** `backend/*/urls.py` as of 2026-07-26. Base URL: `http://localhost:8000/api` (dev) — see [deployment.md](deployment.md) for prod.
> **Last updated:** 2026-07-26 · **Version:** 1.0
>
> A Postman collection is also kept at [`backend/postman_collection.json`](../backend/postman_collection.json) — prefer it for interactive exploration; this doc is the canonical written reference.

## Table of Contents

- [Authentication](#authentication)
- [Auth & Users — `/api/auth/`](#auth--users--apiauth)
- [Students — `/api/students/`](#students--apistudents)
- [Courses & Enrollments — `/api/`](#courses--enrollments--api)
- [Attendance — `/api/attendance/`](#attendance--apiattendance)
- [Face Recognition — `/api/face/`](#face-recognition--apiface)
- [Dashboard — `/api/dashboard/`](#dashboard--apidashboard)
- [Error Format](#error-format)
- [Rate Limits](#rate-limits)
- [Future Endpoints](#future-endpoints)

## Authentication

All endpoints except `register/`, `login/`, `token/refresh/`, `otp/*`, `google/`, `facebook/` require:

```
Authorization: Bearer <access_token>
```

Access tokens expire in 1 day, refresh tokens in 7 days (`SIMPLE_JWT` in `config/settings.py`). Some endpoints additionally require `role` to be `admin` and/or `faculty` (noted per-row below).

## Auth & Users — `/api/auth/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `register/` | AllowAny | Register a new user |
| POST | `login/` | AllowAny | JWT obtain (SimpleJWT `TokenObtainPairView`) — returns `access`/`refresh` |
| POST | `token/refresh/` | AllowAny | Exchange `refresh` for a new `access` token |
| GET | `me/` | Authenticated | Current user profile |
| POST | `otp/send/` | AllowAny (throttled: `otp_send`) | Send email OTP for verification |
| POST | `otp/verify/` | AllowAny (throttled: `otp_verify`) | Verify OTP code |
| POST | `google/` | AllowAny (throttled: `social_login`) | Google ID-token sign-in |
| POST | `facebook/` | AllowAny (throttled: `social_login`) | Facebook token sign-in |
| GET/POST/PUT/DELETE | `users/`, `users/:id/` | Admin | Admin user management (DRF router, `AdminUserViewSet`) |

## Students — `/api/students/`

DRF `DefaultRouter` — standard CRUD.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `students/` | Authenticated | List students |
| POST | `students/` | Admin, Faculty | Create student |
| GET | `students/:id/` | Authenticated | Student detail |
| PUT/PATCH | `students/:id/` | Admin, Faculty | Update student |
| DELETE | `students/:id/` | Admin, Faculty | Delete student |

## Courses & Enrollments — `/api/`

Mounted directly under `/api/` (not `/api/courses/`) — see `config/urls.py`.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `courses/` | Authenticated | List courses |
| POST | `courses/` | Admin, Faculty | Create course |
| GET | `courses/:id/` | Authenticated | Course detail |
| PUT/PATCH | `courses/:id/` | Admin, Faculty | Update course |
| DELETE | `courses/:id/` | Admin, Faculty | Delete course |
| GET/POST/PUT/DELETE | `enrollments/` | Admin, Faculty | Enrollment CRUD (US-15) |

## Attendance — `/api/attendance/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `attendance/` | Authenticated | List attendance records |
| POST | `attendance/` | Admin, Faculty | Create a record — rejected if student not enrolled in course |
| GET | `attendance/:id/` | Authenticated | Detail |
| PUT/PATCH | `attendance/:id/` | Admin, Faculty | Update |
| DELETE | `attendance/:id/` | Admin, Faculty | Delete |
| POST | `attendance/bulk/` | Admin, Faculty | Bulk mark; non-enrolled students are **skipped** (returned in a `skipped` list with reason), not a hard failure |
| GET | `attendance/report/` | Admin, Faculty | Query params: `course`, `student`, `start_date`, `end_date` — returns stats |
| GET | `attendance/export/csv/` | Admin, Faculty | CSV export of a report |
| GET | `attendance/export/pdf/` | Admin, Faculty | PDF export (reportlab) |
| GET/POST/PUT/DELETE | `attendance/codes/` | Admin, Faculty | `AttendanceCodeViewSet` — generate/manage self-check-in codes |

## Face Recognition — `/api/face/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `face/register/` | Authenticated | Register a student's face (image upload) |
| POST | `face/recognize/` | Authenticated | Identify a face against registered students |
| POST | `face/mark-attendance/` | Authenticated | Recognize + mark attendance in one call |
| GET | `face/registered/` | Authenticated | List students with a registered face |

Behavior depends on `FACE_PROVIDER` (`local` or `azure`) — see [architecture.md](architecture.md#face-recognition-flow). Errors differ by provider (e.g., Azure network/quota errors vs. local no-match); check `backend/face/views.py` for the exact error payloads if building a new client against this.

## Dashboard — `/api/dashboard/`

All read-only aggregation endpoints; each returns computed data over Student/Course/Enrollment/Attendance.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `dashboard/programs/` | Authenticated | Distinct program list |
| GET | `dashboard/sections/` | Authenticated | Distinct section list |
| GET | `dashboard/students/` | Authenticated | Student search |
| GET | `dashboard/students/:id/attendance/` | Authenticated | Per-student attendance breakdown |
| GET | `dashboard/attendance-stats/` | Authenticated | Aggregate attendance stats |
| GET | `dashboard/at-risk/` | Admin, Faculty | Students below an attendance threshold |
| GET | `dashboard/faculty-performance/` | Admin | Faculty-level attendance/marking stats |
| GET | `dashboard/chronic-latecomers/` | Admin, Faculty | Students frequently marked `late` |
| GET | `dashboard/incomplete-records/` | Admin, Faculty | Sessions with missing/incomplete attendance |
| POST | `dashboard/master-data/import/` | Admin | Bulk import students/courses |

Exact permission classes per view are enforced in `backend/dashboard/views.py` — the table above reflects intent from `HANDOFF.md`; verify against the view's `permission_classes` before building a client that depends on a specific role gate.

## Error Format

DRF's default error shape — field-level validation errors:

```json
{ "field_name": ["error message"] }
```

or non-field errors:

```json
{ "detail": "error message" }
```

`401` — missing/invalid/expired JWT. `403` — authenticated but role-forbidden. `400` — validation failure (e.g., marking attendance for a non-enrolled student on the single-create path). `429` — throttled (OTP/social-login endpoints).

## Rate Limits

Configured via `THROTTLE_OTP_SEND`, `THROTTLE_OTP_VERIFY`, `THROTTLE_SOCIAL_LOGIN` env vars (DRF `ScopedRateThrottle`, per-client-IP):

| Scope | Default |
|---|---|
| `otp_send` | 5/hour |
| `otp_verify` | 20/hour |
| `social_login` | 30/hour |

## Future Endpoints

- Notifications (Phase 7 — not started, see [phases.md](phases.md)).
- ECA tracking (US-12, open).
