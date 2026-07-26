# Development Guide — Workflows

> **Purpose:** Step-by-step workflow for each kind of change — what to do, what must pass, who reviews it. For environment setup and the PR checklist, see [contributing.md](contributing.md); this doc is the workflow-by-change-type reference that sits above it.
> **Scope:** Whole repo.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [New Feature](#new-feature)
- [Bug Fix](#bug-fix)
- [Hotfix](#hotfix)
- [Release](#release)
- [Refactor](#refactor)
- [Documentation Update](#documentation-update)
- [Dependency Upgrade](#dependency-upgrade)
- [Security Patch](#security-patch)

Every workflow below assumes the base setup in [contributing.md](contributing.md) and the branch/commit conventions in [rules.md](rules.md).

## New Feature

**Steps:**
1. Check [memory.md](memory.md) and [phases.md](phases.md) — confirm the feature isn't already in flight and see where it's meant to land architecturally.
2. Branch `feature/US-NN-name` from `develop`.
3. Implement, following [coding-standards.md](coding-standards.md) and [rules.md](rules.md); new endpoints follow [api-standards.md](api-standards.md), new schema follows [database-standards.md](database-standards.md).
4. Add tests per [testing-strategy.md](testing-strategy.md) coverage expectations for the layer touched.
5. Update docs per the [release-process.md](release-process.md) checklist (api.md, .env.example, decisions.md if a non-trivial choice was made).

**Required checks:** CI `test` stage (migrations check, `manage.py check`, full suite); frontend lint/build once CI-enforced ([cicd.md](cicd.md)).
**Review process:** PR via `gh pr create` against `develop`; at least one reviewer confirms the checklist above, not just "tests pass."
**Merge requirements:** CI green, checklist items addressed or explicitly deferred with a reason in the PR description.

## Bug Fix

**Steps:**
1. Branch `bugfix/name` from `develop`.
2. Add a test that reproduces the bug *before* fixing it (confirms the test would have caught it), then fix.
3. If the bug reveals a gap in [rules.md](rules.md)/[coding-standards.md](coding-standards.md) (a pattern that should have prevented this class of bug), note it — doesn't have to be fixed in the same PR, but should be recorded ([memory.md](memory.md) Known Bugs / Technical Debt or a new [decisions.md](decisions.md) entry if it's a real pattern gap).

**Required checks / review / merge:** same as New Feature, scaled to the size of the fix — a one-line fix doesn't need the full checklist ceremony, use judgment.

## Hotfix

See [release-process.md](release-process.md) Hotfix Process for the full procedure (branches from `main`, not `develop`; must still pass CI; gets cherry-picked back to `develop`).

## Release

Continuous deployment on `main` merge — there's no separate "cut a release" step today ([release-process.md](release-process.md) Current Release Model). When [versioning.md](versioning.md) tagging is adopted: tag `main` at the merge point, following semver.

## Refactor

**Steps:**
1. State the reason in the PR description — a refactor with no stated problem it solves is scope creep, not a refactor ([rules.md](rules.md) "don't add features/refactor beyond what's needed").
2. No behavior change — the existing test suite passing (or being updated to reflect an intentionally-changed *implementation* while asserting the same *behavior*) is the acceptance bar, not "looks cleaner."
3. Keep refactor PRs separate from feature/bugfix PRs — mixing "I refactored this while fixing the bug" makes the actual fix harder to review; refactor first (separate PR) if the fix genuinely needs it, or after.

**Required checks:** full CI, same as any change — a refactor is not exempt from tests.

## Documentation Update

**Steps:**
1. Update the specific doc(s) affected — cross-reference [memory.md](memory.md) if it's a status change, or the specific standards doc (api.md, database-schema.md, etc.) if it's a factual/architecture change.
2. Verify cross-links still resolve (a renamed doc/section breaks every doc that links to it — grep for the old name before renaming).
3. No CI gate applies beyond normal PR review for a docs-only change — but per [rules.md](rules.md), keep docs synchronized with implementation; a docs PR that contradicts the actual code is worse than no docs PR.

## Dependency Upgrade

**Steps:**
1. Patch/minor: routine, CI passing is sufficient signal ([tech-stack.md](tech-stack.md) Upgrade Strategy).
2. Major: dedicated PR, read the changelog/breaking-changes list against every consuming app, full test suite + manual smoke test of the core flows (auth, attendance, face) before merge.
3. New dependency (not an upgrade): requires a [decisions.md](decisions.md) ADR justifying it over alternatives, per [tech-stack.md](tech-stack.md).
4. Security-driven dependency bump: see [Security Patch](#security-patch) below instead — different urgency profile.

**Required checks:** full CI; major upgrades additionally get a manual smoke test recorded in the PR description.

## Security Patch

**Steps:**
1. Assess severity/exploitability before deciding urgency — not every security advisory needs a hotfix-speed response; use judgment, but never silently defer a genuinely exploitable issue.
2. If urgent: follow the [Hotfix](#hotfix) workflow (branch from `main`).
3. If not urgent (e.g., a transitive dev-dependency advisory with no production exposure): normal `develop` flow is fine, but don't let it silently age indefinitely — track it if deferred.
4. Never disclose exploit details in a public commit message/PR description for an unpatched vulnerability — patch first, describe the fix in terms of "what," not "here's exactly how it was exploitable," until it's live ([security.md](security.md) Reporting a Vulnerability).
5. After patching, confirm the fix in [security.md](security.md) Known Gaps if it closes a documented gap, or [decisions.md](decisions.md) if it changes a prior security-relevant decision.

**Required checks:** full CI, plus the specific regression test proving the vulnerability is closed.
