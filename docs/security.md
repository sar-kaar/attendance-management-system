# Security — Attendance Management System

> **Purpose:** Security posture, secret handling, and known gaps — one place to check before adding an endpoint, a dependency, or a public-facing feature.
> **Scope:** Whole repo (backend, frontend, CI/CD, deployment).
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Secret Management](#secret-management)
- [AuthN / AuthZ](#authn--authz)
- [Data Protection](#data-protection)
- [Input Validation](#input-validation)
- [Rate Limiting](#rate-limiting)
- [Dependency Hygiene](#dependency-hygiene)
- [CI/CD Secrets](#cicd-secrets)
- [Known Gaps](#known-gaps)
- [Reporting a Vulnerability](#reporting-a-vulnerability)

## Secret Management

- All secrets (Django `SECRET_KEY`, SMTP credentials, OAuth client secrets, Azure Face API keys, JWT signing material) live in `.env` (backend) / `.env.local` (frontend), loaded via `python-decouple` and `import.meta.env` respectively. Both are gitignored.
- `backend/.env.example` and `frontend/.env.example` enumerate every variable a real `.env` needs, with no real values — keep them in sync when adding a new setting ([rules.md](rules.md)).
- **Never commit a real secret, key file, or credential dump to the repo**, even temporarily or in a scratch file at the repo root. If one lands there anyway (e.g., an exported OAuth client-secret JSON, a personal access token file, an API key dump), move it outside the repo immediately and add a `.gitignore` pattern for that filename shape — don't rely on remembering to `git rm` it before a commit.
- If a secret is ever committed to git history (not just present untracked), treat it as compromised: rotate the credential at the provider immediately. Removing it from a future commit does not remove it from history — `git log` still has it.
- Two remotes exist (GitHub `origin`, GitLab `gitlab`) and are kept in sync intentionally ([decisions.md](decisions.md) ADR-005) — a leaked secret is exposed on both.

## AuthN / AuthZ

- Authentication: JWT via SimpleJWT (access + refresh tokens), plus email OTP verification (Brevo SMTP) and Google/Facebook OAuth social sign-in.
- Authorization: role-gated (`accounts.User.role`) — DRF permission classes are the enforcement point. Per [rules.md](rules.md), role checks belong in permission classes, not scattered `if request.user.role == ...` checks inside view bodies.
- Enrollment-based access (e.g., a faculty member can only mark attendance for students enrolled in their own course) is enforced server-side in serializer `validate()`/view logic (`AttendanceSerializer.validate()`, `mark_bulk`) — this is a business rule, not just a permission class, and any new attendance-creation path must replicate it.
- Social login (`accounts/social.py`) exchanges a provider token server-side; never trust a client-supplied user identity without that server-side exchange.

## Data Protection

- Passwords: Django's default hasher (PBKDF2) — never logged, never returned in any serializer.
- PII in scope: student/faculty names, emails, attendance records, and (if `FACE_PROVIDER=local`/`azure` is enabled) face embeddings. Face data is biometric — treat it as more sensitive than ordinary PII: don't add logging that captures raw images or embeddings, don't return embeddings in any API response.
- Production database: PostgreSQL via `DATABASE_URL` (see [deployment.md](deployment.md)); local dev uses SQLite (`db.sqlite3`, gitignored, never commit a populated one).
- Media uploads (`media/`) are gitignored — don't rely on any test fixture that assumes uploaded files persist in the repo.

## Input Validation

- DRF serializers are the validation boundary — validate server-side always; frontend-side validation is UX only, never the source of truth ([rules.md](rules.md)).
- File uploads (face images, bulk-import CSVs) must be validated for type/size server-side before processing, not just via the `<input accept>` attribute on the frontend.
- CSV/bulk-import paths (`dashboard` master-data import) are a common injection/malformed-data surface — validate row shape and reject rather than best-effort-parse malformed rows.

## Rate Limiting

- Any `AllowAny` endpoint with a side effect (sends email, calls an external API, creates a resource) must be rate-limited. Existing pattern: DRF `ScopedRateThrottle` on `otp_send`/`otp_verify`/`social_login`, configured in `backend/config/settings.py` (`OTP_RESEND_COOLDOWN_SECONDS`, `THROTTLE_OTP_*`). Follow this pattern for any new unauthenticated endpoint.

## Dependency Hygiene

- No automated dependency-vulnerability scanning (`pip-audit`, `npm audit` in CI, Dependabot) is configured yet — this is a known gap, not a hidden one.
- Heavy/optional dependencies (`dlib`, `face_recognition`) are deliberately absent from `requirements.txt` and lazy-imported so the app runs on hosts without them ([decisions.md](decisions.md) ADR-003) — don't add them back to `requirements.txt` without re-reading that ADR, since it was a deliberate deploy-reliability tradeoff, not an oversight.

## CI/CD Secrets

- GitLab CI/CD masked variables hold production secrets (SMTP credentials, Azure deploy credentials) and are synced into Azure App Service settings at deploy time, guarded on the relevant variable being present so an unset/unavailable Protected variable never overwrites a live setting with an empty string ([deployment.md](deployment.md)).
- GitHub Actions (`develop` test mirror) does not have deploy credentials and should never be given them — it only needs enough to run `manage.py test` against an ephemeral SQLite DB.
- `backend/scripts/push_gitlab_vars.py` / `stage_gitlab_vars.py` write to GitLab's CI/CD variables API — the personal access token they need must never be committed; keep it in a local, gitignored file or an environment variable when running these scripts.

## Known Gaps

These are documented, not hidden — flag before treating the system as production-hardened:

- No dependency vulnerability scanning in CI.
- No dedicated APM/log aggregation beyond Azure's default App Service log stream ([deployment.md](deployment.md)).
- `FACE_PROVIDER=azure` has not been exercised end-to-end against a real Azure Face resource ([memory.md](memory.md)).
- No automated secret-scanning pre-commit hook (e.g., `gitleaks`, `git-secrets`) — the incident that prompted this doc (several credential files sitting untracked at the repo root) was caught manually, not by tooling. Adding a pre-commit secret scan is a reasonable next step (see [phases.md](phases.md)).
- No formal CSP / security headers audit has been done on the deployed frontend.

## Reporting a Vulnerability

This is a student/course project, not a public product with a formal disclosure program. If you find a security issue, report it directly to the current maintainers (see `README.md` / `docs/decisions.md` for team contacts) rather than filing a public GitHub issue with exploit details.
