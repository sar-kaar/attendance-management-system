# Versioning — Attendance Management System

> **Purpose:** How the app, its API, and (once they exist) shared packages are versioned.
> **Scope:** Whole repo.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Current State](#current-state)
- [Application Versioning](#application-versioning)
- [API Versioning](#api-versioning)
- [Shared Package Versioning (Planned)](#shared-package-versioning-planned)
- [Mobile App Versioning (Planned)](#mobile-app-versioning-planned)
- [Dependency Version Pinning](#dependency-version-pinning)

## Current State

No version scheme is applied today — `main` deploys continuously on merge, with no version number attached to a deploy ([cicd.md](cicd.md) Version Tagging). This doc defines the target scheme to adopt incrementally, not a retroactive requirement.

## Application Versioning

Adopt Semantic Versioning (`MAJOR.MINOR.PATCH`) for the overall AMS product once versioning starts:

- **MAJOR**: breaking API change ([api-standards.md](api-standards.md) versioning), or a change requiring coordinated migration across web+mobile.
- **MINOR**: new feature, backward compatible.
- **PATCH**: bug fix, no behavior/contract change.

Apply as a git tag on `main` (`vX.Y.Z`) at meaningful points — not required on every merge given the current continuous-deploy model; useful specifically for "what was live when" traceability ([cicd.md](cicd.md)).

## API Versioning

See [api-standards.md](api-standards.md) Versioning — `/api/` today is implicit v1; a new `/api/v1/` prefix is reserved for when the first genuinely breaking change needs to ship without breaking the deployed frontend. API version and application version are independent — a PATCH app release doesn't imply an API version bump, and vice versa.

## Shared Package Versioning (Planned)

Once `packages/*` exist ([package-guidelines.md](package-guidelines.md)):

- Independent semver per package, not a single monorepo-wide version — a `utils` patch shouldn't force a version bump on `ui`.
- Internal packages (consumed only by `apps/web`/`apps/mobile` in this monorepo, never published externally) can use a simpler scheme: version bumps tracked via the monorepo's own commit history rather than published to a registry — don't add npm-registry publishing machinery for packages with no external consumer.
- If a package boundary later needs to be consumed outside this monorepo, that's the trigger to add real publishing/versioning tooling (e.g., Changesets) — not before.

## Mobile App Versioning (Planned)

- Follow the platform stores' version conventions: a user-facing version string (semver-like, e.g. `1.2.0`) plus a monotonically increasing build number per platform (`versionCode` Android, `CFBundleVersion`/build number iOS) — Expo's `app.json`/EAS handles this; don't hand-roll it.
- App version bumps are independent of backend API version bumps, but a mobile release that requires a specific minimum backend API version should declare that dependency (e.g., in [decisions.md](decisions.md) or a compatibility table in this doc once mobile ships) so an old mobile build against a newer backend fails predictably rather than silently.

## Dependency Version Pinning

- Backend: `requirements.txt` pins exact versions (current practice) — keeps Oryx builds reproducible. Upgrade deliberately, not via a floating range.
- Frontend: `package-lock.json` is the lockfile of record ([tech-stack.md](tech-stack.md) — `npm` is the single package manager; the stray `bun.lock` found during cleanup was removed). `package.json` ranges follow npm convention (`^` for minor/patch flexibility); the lockfile pins the actual resolved versions used in CI/prod.
- Shared packages (planned): pin their own dependencies the same way; a monorepo tool (Turborepo/Nx, see [tech-stack.md](tech-stack.md)) is not needed until package count/build-time coordination actually requires it.
