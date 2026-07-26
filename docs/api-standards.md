# API Standards — Attendance Management System

> **Purpose:** Conventions for every REST endpoint going forward. For the actual current endpoint list, see [api.md](api.md) — that doc describes *what exists*; this doc defines *what new/changed endpoints must follow*.
> **Scope:** `backend/*/urls.py`, `views.py`, `serializers.py`.
> **Last updated:** 2026-07-26 · **Version:** 1.0
>
> **Honesty note**: the current API (documented in [api.md](api.md)) does not fully conform to every rule below — it has no version prefix and no standard pagination/error envelope on most endpoints. That's an existing-code reality, not something to silently "fix" by breaking clients. New endpoints must follow this doc; retrofitting old ones is a deliberate, tracked migration (see [Migrating Existing Endpoints](#migrating-existing-endpoints)), not a side effect of an unrelated change.

## Table of Contents

- [Resource Naming](#resource-naming)
- [Versioning](#versioning)
- [Request Format](#request-format)
- [Response Format](#response-format)
- [Pagination](#pagination)
- [Filtering & Sorting](#filtering--sorting)
- [Authentication & Authorization](#authentication--authorization)
- [Validation](#validation)
- [Error Responses & Status Codes](#error-responses--status-codes)
- [Rate Limiting](#rate-limiting)
- [Logging & Audit Trails](#logging--audit-trails)
- [OpenAPI / Swagger](#openapi--swagger)
- [Migrating Existing Endpoints](#migrating-existing-endpoints)

## Resource Naming

- Plural, lowercase, hyphenated for multi-word resources: `/students/`, `/attendance-codes/` (not `/attendanceCodes/` or `/attendance_code/`).
- Nested resources reflect real ownership: `/courses/:id/enrollments/` is acceptable for course-scoped enrollment listing; don't nest more than one level deep — use query params instead (`/attendance/?course=:id&date=...`).
- Actions that aren't CRUD (OTP send/verify, face recognize, bulk mark) are verbs on a sub-path: `/attendance/mark-bulk/`, `/face/recognize/` — matches the existing pattern in [api.md](api.md).

## Versioning

New API surfaces should be mounted under `/api/v1/`. The current unversioned `/api/` prefix stays as-is (breaking it would break the deployed frontend with no benefit) — treat `/api/` as an implicit `v1` for now. **Do not** introduce a second version until there's a real breaking change to ship; version bumps are for breaking changes only, not routine additions (a new optional field or a new endpoint is not a breaking change and doesn't need a new version).

## Request Format

- `Content-Type: application/json` for all non-file-upload endpoints; `multipart/form-data` for file uploads (student photos, face images, bulk-import CSVs).
- Request bodies use `snake_case` keys, matching Django/DRF convention and the existing serializers — don't introduce `camelCase` request bodies inconsistently with the rest of the API.
- Dates: ISO 8601 (`YYYY-MM-DD` for dates, `YYYY-MM-DDTHH:MM:SSZ` for datetimes) — matches DRF's default serialization.

## Response Format

- Single resource: the resource object directly (matches current behavior) — `{ "id": 1, "name": "...", ... }`.
- Collection (new endpoints): a paginated envelope (see [Pagination](#pagination)) — `{ "count": N, "next": "...", "previous": "...", "results": [...] }`, which is DRF's default `PageNumberPagination`/`LimitOffsetPagination` shape. Prefer this over inventing a custom envelope.
- Field naming: `snake_case`, matching request format.
- Never return a raw Python exception message or stack trace in a response body — see [Error Responses](#error-responses--status-codes).

## Pagination

- New list endpoints must paginate using DRF's built-in `PageNumberPagination` (default) — don't return an unbounded list from a new endpoint that could grow large (attendance records, students).
- Existing unpaginated list endpoints (see [api.md](api.md)) should gain pagination before their result sets become large enough to matter — track this as a deliberate migration in [phases.md](phases.md), not urgent today given current data volume.
- Default page size: 20–50, configurable via `?page_size=`. Cap `page_size` server-side (e.g., max 200) to prevent an unbounded request.

## Filtering & Sorting

- Filtering: query params matching the field name (`?role=faculty`, `?course=3&date=2026-07-20`) — use `django-filter`'s `FilterSet` for any endpoint with more than one or two filter fields, rather than hand-rolling `request.query_params` parsing in the view.
- Sorting: `?ordering=field` / `?ordering=-field` (DRF `OrderingFilter` convention) — don't invent a different query param name.
- Full-text search (student/course name lookups): `?search=` (DRF `SearchFilter` convention).

## Authentication & Authorization

- Every endpoint declares its permission class explicitly — no endpoint should silently default to `AllowAny` by omission. If it's meant to be public, that's a one-line explicit `permission_classes = [AllowAny]` with a comment-worthy reason (registration, login, OTP, social auth — the existing public set).
- Role checks live in DRF permission classes (`IsAdminUser`-style custom classes keyed on `request.user.role`), not scattered in view bodies — see [rules.md](rules.md).
- Object-level authorization (e.g., a faculty member can only act on their own course's enrollments) is enforced in the view/serializer `validate()`, following the existing `AttendanceSerializer.validate()` pattern — document any new such rule in the endpoint's docstring and in [api.md](api.md).

## Validation

- All validation lives in the DRF serializer (`validate_<field>`, `validate()`) — never trust client-side validation as the source of truth ([rules.md](rules.md), [security.md](security.md)).
- Cross-field/business-rule validation (e.g., enrollment gating) belongs in `validate()`, not in the view or a signal, so it's testable in isolation and visible in one place.
- Bulk-operation endpoints (`mark-bulk`) validate every row and report per-row success/failure rather than failing the entire batch on one bad row, unless the operation is explicitly atomic-or-nothing — document which behavior a given bulk endpoint uses.

## Error Responses & Status Codes

Standard status codes:

| Code | Meaning | When |
|---|---|---|
| 200 | OK | Successful GET/PUT/PATCH, or POST that doesn't create a resource |
| 201 | Created | Successful POST creating a resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation failure (serializer `is_valid()` false) |
| 401 | Unauthorized | Missing/invalid/expired token |
| 403 | Forbidden | Valid token, insufficient role/permission |
| 404 | Not Found | Resource doesn't exist or isn't visible to this user |
| 409 | Conflict | Uniqueness violation (e.g., duplicate `(student, course, date)` attendance record) |
| 429 | Too Many Requests | Throttled endpoint (OTP, social login) |
| 500 | Internal Server Error | Unhandled exception — must be logged server-side; body must never leak internals |

Error body shape (new endpoints; matches DRF's default serializer-error shape, which is already what's returned today):

```json
{ "field_name": ["Error message."], "non_field_errors": ["Error message."] }
```

For non-validation errors (404, 403, 429), DRF's default `{"detail": "..."}` shape is acceptable and already in use — don't invent a third shape.

## Rate Limiting

Any `AllowAny` endpoint with a side effect must use DRF's `ScopedRateThrottle`, following the existing `otp_send`/`otp_verify`/`social_login` pattern in `config/settings.py` — see [security.md](security.md) for the full rule.

## Logging & Audit Trails

- Every write operation (create/update/delete) on a sensitive resource (`User`, `Attendance`, `Enrollment`) should be attributable to the acting user in server logs at minimum (`request.user.id` + action + object id).
- **Not yet implemented**: a dedicated audit-log table recording who changed what and when. This is a known gap — recommended before AMS is used in a setting where after-the-fact dispute resolution (e.g., "who marked me absent") matters. See [database-standards.md](database-standards.md) Audit Tables and [phases.md](phases.md) for where to slot this.

## OpenAPI / Swagger

**Not yet implemented.** [api.md](api.md) and the Postman collection (`backend/postman_collection.json`) are the current source of truth. Recommended next step: `drf-spectacular` to generate an OpenAPI schema from the existing DRF serializers/views with minimal annotation overhead, then serve a Swagger UI in dev. This would also let `packages/types` (see [package-guidelines.md](package-guidelines.md)) be generated from the schema instead of hand-maintained once the shared-packages work starts — worth sequencing OpenAPI adoption before that point.

## Migrating Existing Endpoints

When an existing endpoint needs a breaking change (new required field, changed response shape, removed field):

1. Prefer additive/non-breaking changes (new optional field, new endpoint) over breaking ones.
2. If a breaking change is unavoidable, add it under `/api/v1/` addressing only that resource, keep the old endpoint working, and track the deprecation in [decisions.md](decisions.md) with a removal target.
3. Update [api.md](api.md), the Postman collection, and any consuming frontend code in the same PR — an API change with a stale doc is worse than no doc.
