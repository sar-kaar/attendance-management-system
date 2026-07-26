# Feature Matrix — Web vs. Mobile

> **Purpose:** For every existing (or planned) feature, states whether it's in scope for the mobile app, and why. Prevents scope-creep debates mid-implementation.
> **Scope:** Mobile Application epic (GitHub #34). Source list is the web feature set in [architecture.md](architecture.md) / [api.md](api.md).
> **Last updated:** 2026-07-26 · **Version:** 1.0

| Feature | Web | Mobile v1 | Notes |
|---|---|---|---|
| Register / login (email, Google, Facebook) | Yes | **In scope** | Native OAuth SDKs, not the web redirect flow — see [mobile-architecture.md](mobile-architecture.md) |
| Email OTP verification | Yes | **In scope** | Same `/api/auth/otp/*` endpoints |
| Manual attendance marking (single) | Yes | **In scope** | Faculty only |
| Bulk attendance marking | Yes | **In scope**, offline-queueable | See [mobile-architecture.md](mobile-architecture.md) Offline Queue |
| Attendance codes (self-check-in) | Yes | **In scope** | Both roles |
| Face recognition attendance | Yes | **In scope**, online-only | Reuses `FACE_PROVIDER` backend as-is |
| Attendance report (query/filter) | Yes | **In scope**, read-only | |
| CSV/PDF export | Yes | **Out of scope** | On-device file generation adds real complexity (share-sheet plumbing, storage permissions) for a feature students/faculty rarely need on a phone; export from web when needed. Revisit only if user feedback demands it. |
| Student/Course CRUD | Yes (Admin/Faculty) | **Out of scope** | Data-entry-heavy forms are a poor mobile fit; this is an admin/faculty desk workflow, not a mobile one |
| Enrollment management | Yes (Admin/Faculty) | **Out of scope** | Same reasoning as above |
| Dashboard (stats, at-risk, chronic-latecomers, faculty performance) | Yes | **In scope**, read-only | Faculty/student views only — `faculty-performance` (admin-only on web) stays out |
| Master-data bulk import | Yes (Admin) | **Out of scope** | Admin-only, desk workflow, large-file upload is a poor mobile fit |
| Django admin panel | Yes (staff) | **Out of scope** | Web-only by nature |
| ECA (extra-curricular activity) tracking | No — not built anywhere yet | **Out of scope** | Blocked upstream: no backend model exists (see [phases.md](phases.md) Phase 6 open item, GitHub #23). Not a mobile-specific gap — do not scope mobile ECA work before the backend model exists. |
| Push notifications | No | **In scope (mobile-only)** | No web equivalent exists yet; piggybacks on the same at-risk detection logic once [phases.md](phases.md) Phase 7 (web notifications) lands |
| Offline attendance queue | No | **In scope (mobile-only)** | No web equivalent — connectivity is assumed on web |
| Profile view/edit | Yes (`/api/auth/me/`) | **In scope** | |
| Social login admin management (`/api/auth/users/`) | Yes (Admin) | **Out of scope** | Admin-only |

## Summary

**In scope for v1**: auth (incl. OTP + native social login), attendance marking (manual, bulk, code, face) with offline queueing for manual/bulk, attendance reports (read-only), dashboard (read-only, role-scoped), push notifications, profile.

**Explicitly out of scope for v1**: anything admin-only, anything requiring on-device file generation/export, anything requiring large-form data entry (CRUD on students/courses/enrollments/master-data), ECA tracking (blocked on a pre-existing backend gap, unrelated to mobile).
