# Release Process — Attendance Management System

> **Purpose:** How a change goes from merged code to a live deployment, and what code-quality tooling gates it. Complements [versioning.md](versioning.md) (how things are numbered) and [cicd.md](cicd.md) (pipeline mechanics).
> **Scope:** Whole repo.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Current Release Model](#current-release-model)
- [Release Checklist](#release-checklist)
- [Code Quality Gates](#code-quality-gates)
- [Recommended Tooling (Not Yet Adopted)](#recommended-tooling-not-yet-adopted)
- [Hotfix Process](#hotfix-process)

## Current Release Model

Continuous deployment on `main`: every merged PR/MR to `main` that passes the `test` stage deploys automatically ([deployment.md](deployment.md)). There is no separate "release" event distinct from "merge to main" today — this doc's checklist is what should happen around that merge, not a separate ceremony to add.

## Release Checklist

Before merging to `main` (extends [deployment.md](deployment.md) Deployment Checklist with the broader engineering-standards lens):

1. CI passing (`test` stage — migrations check, `manage.py check`, full test suite).
2. New env vars documented in `.env.example` and, if behavior-affecting, in [architecture.md](architecture.md)/[deployment.md](deployment.md).
3. New/changed endpoints documented in [api.md](api.md), following [api-standards.md](api-standards.md).
4. New/changed schema documented in [database-schema.md](database-schema.md), following [database-standards.md](database-standards.md); destructive migrations flagged explicitly in the PR.
5. Security-relevant change (auth, rate limiting, new public endpoint, new external API call) reviewed against [security-standards.md](security-standards.md).
6. Non-trivial technical decision recorded in [decisions.md](decisions.md) as an ADR.
7. [memory.md](memory.md) updated if this is a major implementation (per its own stated update policy).

## Code Quality Gates

Current vs target — see [cicd.md](cicd.md) for the pipeline-stage detail:

| Gate | Current | Target |
|---|---|---|
| Backend lint/format | None | `ruff` in CI |
| Frontend lint | Configured, not CI-enforced | `npm run lint` in CI |
| Frontend format | Configured (Prettier), not enforced | `prettier --check` in CI |
| Backend tests | Enforced | Enforced (no change) |
| Frontend tests | None (no suite) | Vitest suite, CI-enforced once it exists |
| Migration check | Enforced | Enforced (no change) |
| Dependency audit | None | `pip-audit`/`npm audit`, non-blocking report first |
| Secret scanning | Manual only (see [security.md](security.md) incident) | Pre-commit hook (`gitleaks` or similar) — recommended next step |
| Dead code / duplicate code detection | None | Not currently recommended to add — revisit if the codebase grows enough that this becomes a real navigation problem; premature for current size |
| Complexity analysis | None | Not currently recommended — same reasoning |
| License checking | None | Add if/when a dependency with a restrictive license could become a real concern (e.g., before any closed-source commercial use) — not relevant to a course/student project today |

## Recommended Tooling (Not Yet Adopted)

In priority order (highest-value-first, matching the phased "visibility before enforcement" pattern used throughout these standards docs):

1. `ruff` (backend lint/format) — single tool, immediate value, low setup cost.
2. Frontend lint/build in CI on every PR (not just `main`) — catches issues before merge instead of after.
3. `pip-audit` / `npm audit` as a non-blocking CI report.
4. Pre-commit secret-scanning hook.
5. Vitest baseline + CI test step for frontend.
6. `drf-spectacular` (OpenAPI generation, see [api-standards.md](api-standards.md)) — unlocks contract testing and typed client generation as follow-on value.

Don't adopt all six at once — each is a separate, reviewable PR per [rules.md](rules.md)/[phases.md](phases.md) phasing philosophy.

## Hotfix Process

For a production bug needing an urgent fix outside the normal `develop → main` flow:

1. Branch `hotfix/<name>` from `main` (not `develop`) — matches [rules.md](rules.md) Git & Commits branch naming.
2. Fix + test locally; CI still gates the merge to `main` (no skipping the `test` stage, even for a hotfix — see [rules.md](rules.md), never bypass CI/hooks).
3. Merge to `main` → auto-deploys via GitLab CI ([deployment.md](deployment.md)).
4. Merge/cherry-pick the same fix into `develop` immediately after, so the next regular release doesn't reintroduce the bug.
5. Record the incident and root cause in [decisions.md](decisions.md) if it reveals a gap in the standards/process (not required for a routine bug fix — use judgment on whether it's a "this could recur" class of issue).
