# Mobile API Contract

> Created: 2026-08-07 · Owner: Abhishek (backend) · Audience: mobile team (Ekata, Prizma)
> Companion to [remaining-work-tracker.md](remaining-work-tracker.md). This is the **B8–B10** deliverable of the
> mobile-readiness plan (#36). It describes the stable backend contract the React Native (Expo) app builds against.

## Base URL & versioning (B8)

- **Production:** `https://ams-backend.azurewebsites.net`
- **Local dev:** `http://<your-LAN-IP>:8000` (not `localhost` — the phone/emulator can't reach the host's localhost;
  use the machine's LAN IP, or an Expo tunnel).
- **Pin mobile to the versioned prefix:** `**/api/v1/**`. The unversioned `/api/` still works (the web app uses it)
  and currently resolves to the same views, but `/api/v1/` is the contract the mobile app should depend on so a
  future `/api/v2/` can change web behavior without breaking shipped mobile builds.

All paths below are relative to `<base>/api/v1/`.

## Auth & headers

- Auth is **JWT Bearer**. Send `Authorization: Bearer <access>` on every protected request.
- Content type: `application/json`.
- Token lifetimes: **access = 1 day**, **refresh = 7 days**.
- **Refresh rotation is ON**: calling refresh returns a **new** refresh token and **blacklists the old one**.
  The client must persist the newest refresh token each time and discard the previous one. Reusing an old refresh
  token returns `401`.

### Auth endpoints

| Method | Path | Body | Response | Notes |
|---|---|---|---|---|
| POST | `auth/register/` | `{username, email, password, role, first_name, last_name, phone?}` | `201` user | `role` ∈ `student\|faculty\|admin` |
| POST | `auth/login/` | `{username, password}` | `200 {access, refresh}` | |
| POST | `auth/token/refresh/` | `{refresh}` | `200 {access, refresh}` | rotates; store the new `refresh` |
| POST | `auth/logout/` | `{refresh}` | `205` (no body) | blacklists the refresh token; call on sign-out |
| GET | `auth/me/` | — | `200 {id, username, email, role, phone, first_name, last_name, is_active, student_id}` | current user |
| POST | `auth/otp/send/` | `{email, purpose}` | `200` | rate-limited 5/hour per IP |
| POST | `auth/otp/verify/` | `{email, code, purpose}` | `200` | |
| POST | `auth/google/` | `{token}` (Google ID token) | `200 {access, refresh}` | throttled 30/hour |
| POST | `auth/facebook/` | `{token}` (FB access token) | `200 {access, refresh}` | throttled 30/hour |

### Recommended client token flow

1. `login/` → store `access` + `refresh` in secure storage (e.g. `expo-secure-store`).
2. Attach `access` to requests. On `401`, call `token/refresh/`, **replace both stored tokens**, retry once.
3. If refresh returns `401`, the session is dead → route to login.
4. On logout, call `auth/logout/` with the current `refresh`, then clear storage and unregister the push device.

## Push notifications (device registration)

Register the device's push token after login; unregister on logout.

| Method | Path | Body | Response | Notes |
|---|---|---|---|---|
| POST | `devices/register/` | `{token, platform}` | `200` device | `platform` ∈ `ios\|android\|web`. Idempotent: re-registering the same `token` re-points it to the current user. |
| POST | `devices/unregister/` | `{token}` | `204` | only the owner can unregister; unknown token → `404` |
| GET | `devices/` | — | `200` `[{id, token, platform, is_active, created_at, updated_at}]` | caller's devices only |

**Server-side push behavior:** when a student is marked **absent**, the backend pushes to that student's registered
devices (best-effort). Backend provider is env-gated (`PUSH_PROVIDER` = `console` in dev/CI = logs only, `expo` in
prod). Payload `data`: `{type: "attendance", course_id, date}`.

## Core resources (all require Bearer, role-gated)

| Area | Endpoint(s) | Notes |
|---|---|---|
| Students | `students/` (CRUD) | admin/faculty write; list is paginated |
| Courses | `courses/` (CRUD) | |
| Enrollments | `enrollments/` (CRUD) | |
| Attendance | `attendance/` (CRUD) | |
| Attendance — bulk mark | `POST attendance/mark_bulk/` | `{course, date, records:[{student, status}]}`; enrollment-enforced |
| Attendance — my records | `GET attendance/my_attendance/` | for the logged-in student |
| Attendance — report | `GET attendance/report/?course=&student=&date=` | |
| Attendance — export | `GET attendance/export_csv/`, `attendance/export_pdf/` | file download |
| Attendance codes | `attendance/codes/` (CRUD) | self-check-in codes |
| ECA activities | `attendance/eca-activities/` (CRUD) | for `status="eca"` records |
| Face | `POST face/register/`, `face/recognize/`, `face/mark-attendance/`, `GET face/registered/` | multipart image upload |
| Dashboard | `dashboard/attendance-stats/`, `at-risk/`, `faculty-performance/`, `chronic-latecomers/`, `incomplete-records/`, `programs/`, `sections/`, `students/`, `students/<id>/attendance/`, `eca/` | read-only analytics |

Attendance `status` values: `present`, `absent`, `late`, `lp` (late present), `eca`.

## Pagination

List endpoints use page-number pagination (`PAGE_SIZE = 20`):

```json
{ "count": 57, "next": "…?page=2", "previous": null, "results": [ … ] }
```

Always read `results`; don't assume the array is at the top level.

## Error format

DRF standard. Validation errors are field-keyed; auth/permission errors use `detail`:

```json
// 400 validation
{ "email": ["This field is required."], "student_id": ["Enter a valid ID."] }
// 401 / 403 / 404
{ "detail": "Authentication credentials were not provided." }
```

Status codes: `200/201/204/205` success · `400` validation · `401` unauthenticated/expired ·
`403` wrong role · `404` not found · `429` throttled (OTP/social).

## CORS (B9)

Native React Native / Expo Go sends no browser `Origin`, so CORS never applies to it. CORS only gates browser
contexts (Expo **web**). Dev defaults allow Vite (`5173`), Expo web (`19006`), and Metro (`8081`) on
`localhost`/`127.0.0.1`; in `DEBUG` all origins are allowed. Production origins come from the
`CORS_ALLOWED_ORIGINS` env var.

## Changelog

- **2026-08-07** — Initial contract. Covers auth (rotation/blacklist/logout), device/push, core resources,
  pagination, errors, versioning (`/api/v1/`), CORS. Backend items B1–B10 complete.
