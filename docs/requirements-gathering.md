# Requirements Gathering — Attendance Management System

> **Purpose:** Documents *how* AMS's requirements were gathered and validated — the process artifact for CSE 405 (GitHub issue #7 / Master Tracker FE-002), distinct from [srs.md](srs.md) (the *what*, formally specified) and [prd.md](prd.md) (product intent/priorities).
> **Last updated:** 2026-08-04 · **Version:** 1.0

## Table of Contents

- [1. Methodology](#1-methodology)
- [2. Stakeholders](#2-stakeholders)
- [3. Elicitation Techniques Used](#3-elicitation-techniques-used)
- [4. Requirements Sources](#4-requirements-sources)
- [5. Prioritization](#5-prioritization)
- [6. Validation](#6-validation)
- [7. Change Management](#7-change-management)
- [8. Traceability](#8-traceability)

## 1. Methodology

AMS requirements were gathered iteratively rather than in a single up-front phase, consistent with the team's Agile Scrum approach ([TEAM_SYNC_PROTOCOL.md](../Weekly%20Tasks/TEAM_SYNC_PROTOCOL.md)). The starting point was the course brief (attendance tracking with a differentiator feature) and the team's own experience as students frustrated by manual attendance. From there:

1. **Problem framing** — identify the core pain point (manual, error-prone attendance; no queryable history) — captured in [prd.md §Problem Statement](prd.md#problem-statement).
2. **Persona-driven elicitation** — define admin/faculty/student personas and ask "what does each need to do?" — see §2 below.
3. **User story writing** — convert needs into US-NN stories with acceptance criteria, tracked in the risk/dependency tracker (see [memory.md §External Trackers](memory.md#external-trackers)) and GitHub issues.
4. **Backlog grooming per sprint** — requirements were refined and re-prioritized at each sprint boundary (see [phases.md](phases.md)) as the team learned more about implementation constraints (e.g., discovering `dlib` wouldn't build on Azure's B1 tier reshaped the face-recognition requirement into a pluggable-provider requirement, ADR-002).
5. **Requirements verification against the built system** — because documentation work happened partly *after* substantial implementation (an engineering-hygiene pass on 2026-07-26), requirements in [prd.md](prd.md) and [srs.md](srs.md) were cross-checked against actual code (`backend/*/models.py`, `backend/*/views.py`) rather than taken purely from planning documents — this is why [database-schema.md](database-schema.md) is explicitly labeled "verified against actual models.py files," not a design doc.

## 2. Stakeholders

| Stakeholder | Interest | Consulted via |
|---|---|---|
| Faculty Supervisor / Course Instructor | Grading criteria, academic deliverable requirements | Course syllabus (`Guidelines/Course Syllabus CSE 405.pdf`), verbal guidance |
| Project Manager (Prizma Subedi) | Scope, timeline, documentation completeness | Team standups, PACT/SWOT analysis in Project Charter |
| Backend Developer (Abhishek Rokaya) | Technical feasibility, hosting constraints | Direct implementation experience (e.g., dlib build failure on Azure B1) |
| Frontend Developer (Ekata Rimal) | UI/UX feasibility, component design | Wireframes (`wireframes/*.html`), design conventions ([design.md](design.md)) |
| End users (proxy: team's own experience as students/would-be faculty) | Usability, real-world workflow fit | No formal user interviews conducted — see §3 gap note |

## 3. Elicitation Techniques Used

| Technique | Used? | Notes |
|---|---|---|
| Stakeholder interviews | Partial | Informal team discussion; no external faculty/student interviews were conducted — the team self-identified as proxies for faculty/student personas, a known limitation for an academic project of this size |
| Persona/PACT analysis | Yes | See Project Charter (Google Doc, linked from repo root as `Project Charter (AMS).gdoc`) — People/Activities/Context/Technologies breakdown |
| SWOT analysis | Yes | Same Project Charter document |
| User story writing | Yes | US-01 through US-15 (core) and US-D1–D10 (dashboard analytics), tracked in the risk/dependency sheet |
| Wireframing | Yes | Static HTML mockups in `wireframes/` (login, dashboard, students) — used to validate UI-facing requirements before build |
| Competitive/prior-art review | Implicit | Team's own experience with manual/spreadsheet attendance systems informed the problem statement; no formal competitor analysis document exists |
| Technical spike / feasibility check | Yes | Face recognition requirement was validated against real hosting constraints mid-implementation (dlib build failure), which changed the requirement from "local face recognition" to "pluggable local-or-cloud face recognition" — documented as ADR-002/ADR-003 |

**Gap, stated plainly**: this project did not conduct formal interviews or surveys with actual faculty/students who would use the system. Requirements were derived from the course brief, the team's own experience, and iterative technical discovery. This is an accepted limitation for a 3-person academic team project (see Project Charter SWOT "Weaknesses": small team, limited time), not an oversight to silently paper over.

## 4. Requirements Sources

1. **Course syllabus** (`Guidelines/Course Syllabus CSE 405.pdf`) — grading rubric and deliverable checklist, which shaped which PM artifacts (SRS, Charter, this document) were required regardless of product need.
2. **Team-authored PRD** ([prd.md](prd.md)) — the primary functional/non-functional requirements source.
3. **Architecture constraints discovered during build** — e.g., Azure App Service B1 tier's inability to build `dlib` from source reshaped FR-6 (face recognition) into a provider-pluggable requirement.
4. **Risk/dependency analysis** (Google Sheet "AMS - User Story Dependencies & Risks") — surfaced implicit requirements like "student face embeddings must never be logged" (now NFR-7 in [srs.md](srs.md)) that weren't in the original brief but emerged from a security-lens review.

## 5. Prioritization

Requirements were prioritized P0–P3 (see [prd.md §Features & Priorities](prd.md#features--priorities)):

- **P0** — auth, student/course/enrollment CRUD, manual+bulk attendance, reporting — the minimum viable product without which the system has no value.
- **P1** — attendance codes, face recognition, dashboard (backend), dashboard UI (frontend) — the differentiating features that justify building a new system instead of using a spreadsheet.
- **P2** — ECA tracking — adjacent but non-core.
- **P3** — notifications — nice-to-have, explicitly deferred (see risk W-05, scope-creep risk against a 3-person team).

This prioritization was revisited, not fixed once — e.g., mobile app work was originally implied by early course-tracker templates (see the stale "Attendance Management System - Project Tracker" sheet) but was explicitly demoted to "stretch goal, not commitment" once the team recognized web-app completion should come first (risk M-12/W-05).

## 6. Validation

Requirements were validated primarily through **implementation and testing**, not a separate sign-off step:

- Each functional requirement in [srs.md](srs.md) §4 is only marked "Done" if there is corresponding passing test coverage (`backend/*/tests.py`, 75+ tests as of the 2026-07-26 ruff/hygiene pass) and, where applicable, working frontend UI.
- The `docs/database-schema.md` file was explicitly re-verified against live `models.py` files rather than trusted from an earlier design doc — a deliberate validation step after discovering earlier planning docs (`Guidelines/REALITY_CHECK.md`) had drifted from reality.
- No formal user-acceptance testing (UAT) with real faculty/students has been conducted — flagged as a gap, consistent with the elicitation gap noted in §3.

## 7. Change Management

Requirement changes are tracked as:

1. A GitHub issue (feature request or bug) referencing the affected user story ID.
2. If the change affects architecture or a hard trade-off, an ADR entry in [decisions.md](decisions.md) (e.g., ADR-002 for the face-provider pluggability change).
3. An update to [memory.md](memory.md) — the canonical status doc — reflecting the new state, per ADR-007.

There is no formal change-control board; for a 3-person team, changes are agreed informally in standup/Discord (per [TEAM_SYNC_PROTOCOL.md](../Weekly%20Tasks/TEAM_SYNC_PROTOCOL.md)) and then documented after the fact. This is appropriate for the team's scale, but is itself a documented process risk (W-02 in the risk tracker: no formal code-review/change-control gate before merge).

## 8. Traceability

Requirement → user story → implementation → test traceability is maintained in three places, which should agree (if they don't, [memory.md](memory.md) is authoritative per ADR-007):

1. [srs.md §7 Appendix: Traceability](srs.md#7-appendix-traceability) — FR/NFR to user story to status.
2. [memory.md §Pending Features](memory.md#pending-features) — what remains, who owns it, which GitHub issue tracks it.
3. The "AMS - User Story Dependencies & Risks" Google Sheet — user-story status matrix plus dependency chains between stories (e.g., Auth → Attendance → Dashboard → Analytics is the highest-risk cascading chain).
