# Project Workflow Instructions

You are an autonomous software engineering agent. These instructions apply EVERY session — do not skip them.

## Startup Workflow (MANDATORY — every new session)

### Phase 1 — Read HANDOFF.md
Read `HANDOFF.md` at project root. It is the current source of truth: completed work, pending work, known issues, architecture decisions.

### Phase 2 — Review Git History
Run: `git log --oneline -10`, `git status`, `git diff --stat`, `git branch`. Understand recent commits, active branch, unfinished work.

### Phase 3 — Inspect File Activity
Check which files were recently modified. Identify ongoing work before making changes.

### Phase 4 — Review Guidelines
Read everything in `Guidelines/`. Some docs may be outdated — compare against newer documents and HANDOFF.md. Update or flag stale docs.

### Phase 5 — Review Weekly Tasks
Read `Weekly Tasks/` to understand completed, in-progress, and upcoming priorities.

### Phase 6 — Check Logs
Read `debug.log` if it exists. Look for recurring errors, warnings, crashes.

### Phase 7 — Read Implementation Files
Only after Phases 1-6. Read only files relevant to the task. Avoid unnecessary scanning.

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
- If you discover outdated docs, update them or record in HANDOFF.md as documentation debt.
- Never leave documentation inconsistent with code.
- Update HANDOFF.md with session outcomes, pending items, and known issues.

## General Principles
- Verify before modifying. Never assume project state.
- Preserve existing architecture unless improvement is justified.
- Maintain consistency with existing coding style.
- Avoid duplicate implementations.
- Minimize unnecessary file reads.
- Prefer targeted changes over large refactors.
- Keep documentation synchronized with code.
