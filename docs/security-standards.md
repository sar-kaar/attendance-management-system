# Security Standards — Attendance Management System

> **Purpose:** OWASP-aligned engineering standards for authn/authz, data protection, and secure coding — the rules to follow when writing code. For current posture, known gaps, and incident-response notes, see [security.md](security.md); this doc is the standard, that doc is the status report.
> **Scope:** Backend, Web, Mobile (planned).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Authentication](#authentication)
- [JWT & Refresh Tokens](#jwt--refresh-tokens)
- [Password Hashing](#password-hashing)
- [Authorization / RBAC](#authorization--rbac)
- [Input Validation](#input-validation)
- [Rate Limiting](#rate-limiting)
- [CSRF](#csrf)
- [XSS](#xss)
- [SQL Injection](#sql-injection)
- [Secrets Management](#secrets-management)
- [Encryption](#encryption)
- [Audit Logs](#audit-logs)
- [OWASP Top 10 Mapping](#owasp-top-10-mapping)
- [Security Headers](#security-headers)
- [File Upload Security](#file-upload-security)

## Authentication

- Every new authenticated surface (web route, mobile screen, API endpoint) must resolve identity from a verified JWT — never from a client-supplied user ID/role in a request body.
- Social login (Google/Facebook) must exchange the provider token server-side before issuing an AMS JWT — never accept a client's self-reported "I am user X" claim from a social provider without that server-side verification step (existing pattern in `accounts/social.py`).
- Mobile (planned): the same JWT contract as web — no separate, weaker mobile-only auth path.

## JWT & Refresh Tokens

- Access tokens: short-lived (currently 1 day — see [tech-stack.md](tech-stack.md) for the tradeoff). Refresh tokens: longer-lived (7 days).
- Store tokens appropriately per platform: web — memory/httpOnly-cookie preferred over `localStorage` where feasible (current implementation detail: check `frontend/src/context/AuthContext` before assuming this is already true, and treat moving off raw `localStorage` as a hardening task if it isn't); mobile (planned) — `expo-secure-store`, never `AsyncStorage` in plaintext.
- No server-side token revocation list exists today ([security.md](security.md) Known Gaps) — a leaked refresh token is valid until natural expiry. Until a revocation mechanism exists, keep refresh-token lifetime as short as the UX can tolerate, and treat "log out everywhere" as unsupported (document this limitation to users if it becomes user-facing).
- Never log a token (access or refresh), even at debug level.

## Password Hashing

- Django's default PBKDF2 hasher — do not weaken (no MD5/SHA1-only schemes, no reduced iteration counts) and do not roll a custom hasher without a documented reason in [decisions.md](decisions.md).
- Never log, return in a serializer, or include in an error message a user's password (plaintext or hash) — DRF serializers already exclude `password` from read by default; don't override that.

## Authorization / RBAC

- Three roles today: `admin`, `faculty`, `student` (`accounts.User.role`). Every view declares its allowed role(s) explicitly via a DRF permission class — see [api-standards.md](api-standards.md).
- Object-level checks (a faculty member acting only on their own course) are as important as role checks — a role check alone ("is faculty") is insufficient if the action should be scoped to "faculty who owns this specific course." Follow the `AttendanceSerializer.validate()` enrollment-gating pattern.
- `packages/permissions` (planned, see [package-guidelines.md](package-guidelines.md)) will centralize role-based UI gating for web/mobile — client-side permission checks are always UX-only; the server-side check is the actual boundary.

## Input Validation

- Server-side validation via DRF serializers is the only trusted validation layer ([api-standards.md](api-standards.md)).
- File uploads (face images, bulk CSVs, profile photos): validate content-type and size server-side before processing; never trust the client-declared MIME type alone — sniff/validate actual file content where the library supports it (e.g., Pillow's image verification for uploaded photos).
- Reject rather than best-effort-sanitize malformed bulk-import data — a silently "fixed" bad row in an attendance import is worse than a rejected one.

## Rate Limiting

DRF `ScopedRateThrottle` on every `AllowAny` endpoint with a side effect — existing pattern (`otp_send`/`otp_verify`/`social_login`) is the template for any new public endpoint (password reset, if added; any future public webhook receiver).

## CSRF

- The API is token-authenticated (JWT via `Authorization` header), which is inherently not CSRF-vulnerable the way cookie-session auth is — no CSRF token is needed for JWT-authenticated API calls.
- `CSRF_TRUSTED_ORIGINS` is still configured ([deployment.md](deployment.md)) for the Django admin panel, which does use session auth — don't remove this thinking it's dead config; it protects the one remaining session-authenticated surface.

## XSS

- React escapes rendered content by default — never use `dangerouslySetInnerHTML` with user-supplied content (student names, course titles, etc.) without sanitization (e.g., DOMPurify) if a genuine rich-text need ever arises. No current usage of `dangerouslySetInnerHTML` exists — keep it that way unless there's a specific, reviewed need.
- Mobile (planned): React Native doesn't render HTML by default, so classic XSS is largely N/A there — but any `WebView` usage (if ever added) would reintroduce the same class of risk and needs the same scrutiny.

## SQL Injection

- Django ORM parameterizes queries by default — never build a query with raw string interpolation (`.raw()`, `.extra()`, or a manually-formatted SQL string). If raw SQL is ever genuinely needed, use parameterized placeholders (`cursor.execute(sql, [params])`), never f-string/`.format()` interpolation of user input into SQL text.

## Secrets Management

See [security.md](security.md) Secret Management for the operational rules (`.env`, gitignore, what to do if one leaks). Standard: every secret is an environment variable, loaded via `python-decouple`/`import.meta.env`, with a placeholder entry in the relevant `.env.example` — no secret is ever a literal in source code, a test fixture, or a comment ("temporarily hardcoded, will fix later" is not an acceptable exception).

## Encryption

- In transit: TLS terminates at Azure's edge for both App Service and Storage static website — confirm `ALLOWED_HOSTS`/HTTPS redirect settings stay correct after any hosting change ([deployment.md](deployment.md)).
- At rest: relies on Azure's platform-level disk/storage encryption for the database and media files — no application-level field encryption is implemented today. **Recommendation**: if face-embedding data (biometric, higher sensitivity than ordinary PII) is scaled up, evaluate application-level encryption for that field specifically rather than encrypting everything — targeted encryption on the most sensitive field avoids unnecessary complexity elsewhere.

## Audit Logs

See [database-standards.md](database-standards.md) Audit Tables — not yet implemented; standard once it exists: every write to `User`, `Attendance`, `Enrollment` records actor + action + timestamp, queryable per-record.

## OWASP Top 10 Mapping

Quick-reference for where each OWASP Top 10 (2021) category is addressed in this repo's standards:

| OWASP Category | Where addressed |
|---|---|
| A01 Broken Access Control | [Authorization / RBAC](#authorization--rbac), [api-standards.md](api-standards.md) |
| A02 Cryptographic Failures | [Password Hashing](#password-hashing), [Encryption](#encryption) |
| A03 Injection | [SQL Injection](#sql-injection), [Input Validation](#input-validation) |
| A04 Insecure Design | [decisions.md](decisions.md) ADR process — security-relevant design choices are recorded, not ad hoc |
| A05 Security Misconfiguration | [deployment.md](deployment.md) env var checklist, [Security Headers](#security-headers) |
| A06 Vulnerable/Outdated Components | [security.md](security.md) Dependency Hygiene (known gap: no automated scanning yet) |
| A07 Identification/Authentication Failures | [Authentication](#authentication), [JWT & Refresh Tokens](#jwt--refresh-tokens) |
| A08 Software/Data Integrity Failures | [cicd.md](cicd.md) — no unsigned/unverified deploy artifacts; migrations reviewed before merge |
| A09 Security Logging/Monitoring Failures | [Audit Logs](#audit-logs), [security.md](security.md) Known Gaps (no APM/log aggregation yet) |
| A10 Server-Side Request Forgery | Not currently a large surface (no user-supplied-URL fetch feature exists) — re-evaluate if one is added (e.g., a future "import from URL" feature) |

## Security Headers

- **Not yet audited.** No explicit CSP, `X-Frame-Options`, `X-Content-Type-Options`, or `Strict-Transport-Security` configuration has been confirmed on the deployed frontend/backend ([security.md](security.md) Known Gaps).
- **Recommendation**: `django-csp` or manual middleware for the backend's HTML-serving surfaces (mainly the admin panel); confirm Azure Storage static website hosting's default headers for the frontend and add a CSP meta tag or headers config if the platform allows it.

## File Upload Security

- Size limits: enforce server-side (DRF `FileField`/`ImageField` with `max_length`/validators), not just a frontend `<input>` hint.
- Type validation: verify actual file content (e.g., Pillow-based image verification), not just the extension or client-declared MIME type.
- Storage: uploaded files go to `media/` (gitignored, not in source control) — never accept a file path or storage key directly from the client that could be used for path traversal; let Django's storage backend generate the final path.
- Face images specifically: treated as biometric data — see [Encryption](#encryption) and [security.md](security.md) Data Protection.
