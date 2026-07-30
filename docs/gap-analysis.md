# Gap Analysis — Backend Readiness for Mobile

> **Purpose:** What the current backend is missing to support the mobile app in [mobile-requirements.md](mobile-requirements.md). This is the concrete task list behind GitHub #36 ("Backend Readiness for Mobile") and [phases.md](phases.md) Phases 13–14.
> **Scope:** `backend/` changes only. No mobile client code.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Method](#method)
- [Gap 1 — Mobile-native OAuth token exchange](#gap-1--mobile-native-oauth-token-exchange)
- [Gap 2 — Push notification device registration](#gap-2--push-notification-device-registration)
- [Gap 3 — CORS / host allowlist for a mobile client](#gap-3--cors--host-allowlist-for-a-mobile-client)
- [Gap 4 — API contract confirmation](#gap-4--api-contract-confirmation)
- [Not a gap](#not-a-gap)

## Method

Walked every mobile functional requirement (MR-01 through MR-12 in [mobile-requirements.md](mobile-requirements.md)) against the current endpoint list in [api.md](api.md) and `backend/*/views.py`. Anything the mobile client needs that the backend doesn't already expose is listed below with a proposed shape — **design only, no implementation in this pass** (per GitHub #34's "planning-only expansion" scope).

## Gap 1 — Mobile-native OAuth token exchange

**Requirement**: MR-01, native Google/Facebook SDKs on-device (see [mobile-architecture.md](mobile-architecture.md) Auth & Token Storage).

**Current state**: `POST /api/auth/google/` and `/facebook/` (`backend/accounts/social.py`) accept whatever the web `SocialLogin.jsx` flow sends them — verify the exact payload shape before assuming it's reusable as-is.

**Gap**: A native mobile SDK produces a **device-issued ID token** (Google) or **access token** (Facebook), not necessarily the same shape as the web's browser-redirect flow produces. The existing views may already accept a bare ID token (worth checking first, cheapest fix if so) or may need a mobile-specific variant.

**Proposed approach**: Confirm `backend/accounts/social.py`'s token verification path against Google/Facebook's server-side SDKs — both are capable of verifying either a web or mobile-issued token as long as the *client ID* used to request the token is registered correctly (mobile needs its own OAuth client ID per platform in the Google/Facebook consoles, separate from the web client ID, but can hit the same backend endpoint). Likely **no new endpoint needed**, just new client ID configuration (`GOOGLE_CLIENT_ID_MOBILE` / equivalent env vars) and a verification-path check. Confirm during Phase 14 before assuming an endpoint change is required.

## Gap 2 — Push notification device registration

**Requirement**: MR-09.

**Current state**: No endpoint exists. No `Device`/push-token model exists anywhere in `backend/`.

**Gap**: Need somewhere to store `(user, expo_push_token, platform, last_seen)` and a way for the at-risk/chronic-latecomer detection logic (`backend/dashboard/views.py`) to trigger a send.

**Proposed approach**:
- New model, likely in a new small app (`notifications/`, matching [phases.md](phases.md) Phase 7's suggestion for the web-side notification work — **one app should serve both**, not two parallel notification systems) or `accounts` if kept minimal.
- `POST /api/notifications/devices/` (Authenticated) — register/update a push token for the current user.
- `DELETE /api/notifications/devices/:id/` — unregister (e.g. on logout).
- Sending itself is a Phase 7 dependency, not solely a mobile concern — do not build a mobile-only send path; wire both web (email) and mobile (push) off the same trigger condition once Phase 7 is scoped.

**Blocked on**: [phases.md](phases.md) Phase 7 (web notifications) should be scoped *before* or *alongside* this, not after — building push in isolation risks the exact two-parallel-systems problem called out above.

## Gap 3 — CORS / host allowlist for a mobile client

**Requirement**: All mobile requests hitting the deployed backend.

**Current state**: `django-cors-headers` (or equivalent) is configured for the web frontend's origin(s) — check `backend/config/settings.py` `CORS_ALLOWED_ORIGINS`/`CSRF_TRUSTED_ORIGINS`.

**Gap**: Native mobile HTTP requests don't send an `Origin` header the way a browser does, so **CORS itself is not the blocker** — but `CSRF_TRUSTED_ORIGINS` and any host-header validation (`ALLOWED_HOSTS`) should be re-checked to confirm they don't implicitly assume a browser client. JWT auth (Bearer header, not cookies) means CSRF protection largely doesn't apply to the mobile client's requests in the first place — confirm this is true for every endpoint the mobile app calls (in particular, double-check no endpoint relies on session-cookie auth as a fallback).

**Proposed approach**: Audit pass in Phase 14, not a code change unless the audit finds a real assumption to fix.

## Gap 4 — API contract confirmation

**Requirement**: [mobile-architecture.md](mobile-architecture.md) states the mobile app is "another client of the same `/api/*` surface" — this needs to be true in practice, not just in principle.

**Current state**: [api.md](api.md) documents the intended contract; a Postman collection exists (`backend/postman_collection.json`).

**Gap**: [api.md](api.md) itself flags several endpoints (`dashboard/*`) where documented permission classes should be "verified against the view's `permission_classes`" rather than taken as confirmed. A mobile client hitting a permission mismatch mid-development is a worse debugging experience than catching it now.

**Proposed approach**: Phase 13 — walk every endpoint the mobile app needs (MR-01 through MR-12) against its actual `permission_classes` in code, fix [api.md](api.md) if it's wrong, file a follow-up if the *code* is wrong (e.g., an endpoint that should be student-readable but isn't). This is a documentation/verification pass, not new code, unless it uncovers a genuine bug.

## Not a gap

- **Face recognition**: works as-is for any HTTP client, mobile included — see [mobile-architecture.md](mobile-architecture.md) Face Recognition on Mobile.
- **Attendance/dashboard/reports read endpoints**: no changes needed, mobile consumes them exactly as the web does.
- **Rate limiting**: existing `THROTTLE_OTP_SEND`/`THROTTLE_OTP_VERIFY`/`THROTTLE_SOCIAL_LOGIN` scopes (see [api.md](api.md) Rate Limits) apply per-client-IP already and need no mobile-specific change.
