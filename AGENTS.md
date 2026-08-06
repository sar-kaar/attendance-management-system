# Project Workflow Instructions

You are an autonomous software engineering agent. These instructions apply EVERY session — do not skip them.

## ⚠️ CI/CD lives on GitLab, not GitHub

The **real CI/CD pipeline runs on GitLab** (`.gitlab-ci.yml`, remote `gitlab` →
https://gitlab.com/rokayaabi123/attendance-management-system). It runs tests on every push to
`main`/`develop`/MRs, and on `main` it deploys the backend to Azure App Service
(`ams-backend`) and the frontend to Azure Storage — see `docs/deployment.md` and `docs/cicd.md`
for the full pipeline shape and current gaps.

**GitHub** (remote `origin` → https://github.com/sar-kaar/attendance-management-system) mirrors
only the `test` stage via GitHub Actions, for team visibility. It does **not** deploy anything.
GitHub is used for issues, PRs, and the project board — not for CI/CD.

Practical implications for any agent working here:
- Pushing to `gitlab`/`main` triggers a real production deploy — don't do it casually.
- The two remotes drift out of sync (git history, not CI config, tracks this) — check
  `git log gitlab/develop..develop` before assuming GitLab is caught up with local work.
- If asked to "check the pipeline" or "check CI," check GitLab, not GitHub Actions status.

## Startup Workflow (MANDATORY — every new session)

> Full detail and rationale for every step below lives in the **"33. Agent Instructions"** tab of the
> Master Tracker sheet (https://docs.google.com/spreadsheets/d/1Tr8JOwc4HTXpyPvXP2LaV0pTpCRSuePEjo4AURUln2Y),
> rewritten 2026-08-05 to be the canonical onboarding entry point for any agent (human or AI). This
> section is the condensed, code-side mirror of it — keep both in sync if you change either.

### Phase 1 — Read `docs/memory.md` (canonical status, NOT `HANDOFF.md`)
`docs/memory.md` supersedes `HANDOFF.md` as the source of truth for project status — see `docs/decisions.md`
ADR-007. Read it first: Completed Features, Pending Features, Known Bugs, Technical Debt, Current
Priorities. `HANDOFF.md` is still useful as a human-facing session log, but if the two disagree,
`docs/memory.md` wins.

### Phase 2 — Review Git History
Run: `git log --oneline -10`, `git status`, `git branch -a`, `git fetch --all`. Understand recent
commits, active branch, unfinished work. **Check for a stuck merge** (`test -f .git/MERGE_HEAD`) and
divergence from `origin`/`gitlab` before assuming a clean starting point — multiple agents/sessions
can work on this repo concurrently, and a stuck, half-resolved merge sat unresolved for over a week
in July 2026 because no one checked this.

### Phase 3 — Check GitHub Issues and the Project board
- Issues: https://github.com/sar-kaar/attendance-management-system/issues — a closed issue does
  **not** guarantee a real deliverable exists (a few were closed administratively without linked
  work in the past). Verify against actual code, not issue state alone.
- Project board: https://github.com/users/sar-kaar/projects/5 — board status can lag real code
  state (seen with the mobile-scaffold cards). Cross-check before trusting a card.

### Phase 4 — Check the two team-managed Google Sheets
- **Master Tracker** (34 tabs — requirements, sprints, backlog, risks, bugs, dependencies, etc.):
  https://docs.google.com/spreadsheets/d/1Tr8JOwc4HTXpyPvXP2LaV0pTpCRSuePEjo4AURUln2Y — start with
  the "33. Agent Instructions" tab.
- **Risk & Dependencies** (6 tabs — Dependency Chain, Risk Analysis, User Story Dependencies,
  Personal & Work Risks, Risks, Risk Mitigation Plan):
  https://docs.google.com/spreadsheets/d/1BRHCixRfskt6hvGgwYHx0g14h1ZX58ru2uIgd7bozn8 — check the
  "Risk Mitigation Plan" tab's Status column before treating any R-/M-/P-/W- risk ID as still open.
- **Consolidated Google Drive folder (MIT account)**:
  https://drive.google.com/drive/folders/1Ntq3s7vrMrwNzAYcUl_oxsbyLCW53Mfm — **holds only
  word/google-doc + Google Sheet deliverables** (team policy, 2026-08-06): `Problem statement (AMS).docx`,
  `Cost Estimation (AMS)` (Google Doc), the 5 project sheets (Master Tracker, Risk & Dependencies,
  Resource Labeling Register, Project Tracker, SWOT), and the `Guidelines/` folder (a `.xlsx`, `.pdf`,
  `.csv`). **No `.md` files live here** — they were all moved to Drive Trash (recoverable) and exist
  in GitHub/local only. The "AMS - Resource Labeling Register" sheet (ID `1d7WVIOHCi5_23CWILuwHVb2DYG-Ys0jEKmcqj2y-x14`)
  is the resource/cost register generated from `Cost Estimation (AMS).md`.

Both sheets (and the Drive folder) are team-managed, not in git, and can drift from code reality —
treat them the same way as `docs/memory.md`'s "External Trackers" section describes: useful, but
verify against code.

### Phase 5 — Inspect File Activity
Check which files were recently modified. Identify ongoing work before making changes.

### Phase 6 — Review Guidelines
Read everything in `Guidelines/`. Some docs are **explicitly stale**: `Guidelines/REALITY_CHECK.md`
and `Guidelines/03_PROJECT_TRACKER.csv` — `docs/memory.md` flags these, do not treat as current.

### Phase 7 — Review Weekly Tasks
Read `Weekly Tasks/` to understand completed, in-progress, and upcoming priorities.

### Phase 8 — Check Logs
Read `debug.log` if it exists. Look for recurring errors, warnings, crashes.

### Phase 9 — Read Implementation Files
Only after Phases 1-8. Read only files relevant to the task. Avoid unnecessary scanning.

### Golden rule
When docs disagree with each other or with what you observe, **trust the code and git history**,
not any doc/sheet/issue status. Verify, then update the doc to match reality — never the other way
around. Every stale-doc incident in this project happened because someone trusted a document instead
of checking the repo.

## Before Making Changes
Summarize your understanding of:
- The project state
- What the requested task is
- Risks, affected modules
- Your implementation plan

Get confirmation before proceeding.

## After Completing Work
Provide:
- What changed and why
- Files modified
- Documentation updated
- Tests run and status
- Remaining work / TODOs

## Documentation Rules
- If you discover outdated docs, update them or record in `docs/memory.md` as documentation debt.
- Never leave documentation inconsistent with code.
- Update **both** `docs/memory.md` (canonical) and `HANDOFF.md` (session log) with session outcomes,
  pending items, and known issues.
- If your session touched anything reflected in the Master Tracker or Risk & Dependencies Google
  Sheets (Phase 4 above), update the relevant tab(s) too — don't leave the sheets stale while git is
  current, that gap is exactly what caused conflicts and duplicate work before 2026-08-05.

## General Principles
- Verify before modifying. Never assume project state.
- Preserve existing architecture unless improvement is justified.
- Maintain consistency with existing coding style.
- Avoid duplicate implementations.
- Minimize unnecessary file reads.
- Prefer targeted changes over large refactors.
- Keep documentation synchronized with code.
