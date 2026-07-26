# Prizma — Week 1 (Sprint 0)

**Role:** Project Manager / Team Lead
**Branch prefix:** `docs/`
**Full rules:** see `../TEAM_SYNC_PROTOCOL.md` — you run standup, so also enforce it: ask each person the 3 questions, write down blockers, chase them same day.

### Your scope
- Docs: SRS, Project Charter, Risk Register, Final Report
- Meetings: standups, minutes, teacher meetings
- Trello + Sheets admin
- Team coordination

### Trello cards you own
Project Resources, Product Vision, Charter, Stakeholders, Requirements, Meeting Notes, Reports, Sprint Planning, Risks, Issues, Change Requests, Documentation, Closure, Archive, Competitor Analysis

---

## Day 1 (Tue Jul 7) — DONE
Reviewed Abhishek's Trello/tracker/sheets setup, prepped for first team meeting. No git work.

## Day 2 (Wed Jul 8) — SRS start — partial (meeting did NOT happen)

**Correction: no team meeting happened Jul 8, so nothing below was actually agreed — it never got confirmed with the team. The real kickoff meeting is TODAY (Jul 9), run it first using `Guidelines/06_TOMORROW_MEETING_GUIDE.md`. Treat the branch strategy / task split below as your proposal to bring to today's meeting, not settled fact.**

**Proposed agenda (bring to today's meeting):**
1. Roles confirmed
2. Tool setup check
3. Requirements brainstorm → draft user stories
4. Sprint 0 tasks split (self: SRS+Charter, Abhishek: repo+schema+architecture, Ekata: wireframes+React)
5. Branch strategy: `main` protected, `develop` integration, `feature/`, `docs/` prefixes, commit style `[type] description`

**Google Drive folder:**
```
AMS - CSE 405/
├── Meeting Minutes/
├── SRS Document/
├── Project Charter/
├── Design Assets/
└── Reports/
```

```powershell
git checkout develop
git pull origin develop
git checkout -b docs/srs-document
mkdir docs\srs
```

`docs/srs/01-introduction.md` — purpose, scope (face-recognition attendance system), audience, references (IEEE 830-1998).

```powershell
git add .
git commit -m "[docs] Create SRS document outline"
git push -u origin docs/srs-document
```

---

## Day 3 (Thu Jul 9) — SRS Part 1

Standup 9 AM — come with yesterday's progress + today's plan already in your head, don't figure it out live.

**Before you start:** pull `docs/srs-document`, re-read yesterday's Section 1 so today's Section 2 doesn't contradict it.

```powershell
git checkout docs/srs-document
git pull origin docs/srs-document
```

Write `docs/srs/02-overall-description.md`:

- **Product perspective:** new system, replaces manual attendance. Parts: Django backend + DRF + SQLite (dev) / PostgreSQL (prod), camera integration.
- **Product functions:** register/login, face enrollment, automatic + manual attendance, course management, reports, dashboard.
- **User types:**

| Type | Tech level | Access | Frequency |
|---|---|---|---|
| Faculty | Basic–intermediate | Full system | Daily |
| Student | Basic | View own attendance | Weekly |
| Admin | Intermediate | Everything | As needed |

- **Operating environment:** Chrome/Firefox/Edge 90+, Python 3.10+ server, SQLite (dev) / PostgreSQL 14+ (prod), webcam 720p+.
- **Constraints:** face data encrypted at rest, 40 students processed in under 30 sec, privacy compliance for biometric data.
- **Assumptions:** decent classroom lighting, teacher has camera access, students cooperate with enrollment.

**Commit + tell the team:**
```powershell
git add .
git commit -m "[docs] Add SRS sections 1 and 2"
git push origin docs/srs-document
```
Post in Discord: "SRS Section 2 pushed. If the user types or scope look wrong to either of you, flag it before I build Section 3 on top of it."

**Running behind today?** Get the product-functions list and constraints written — those are the parts Abhishek and Ekata actually reference. User-type table and assumptions can be tightened tomorrow.

---

## Day 4 (Fri Jul 10) — SRS Part 2 + User Stories from Google Sheets

Standup 9 AM. Teacher meeting 11 AM — prep a 2-minute status update (project name, team, what Sprint 0 covers).

**New data available:** Google Sheets dashboards were analyzed. 10 new features identified, all created as GitHub Issues (#17-#26) + Trello cards (86-95) in Product Backlog. Update SRS to include these dashboard/analytics requirements.

**New functional requirements to add to SRS:**
- **FR-12:** Student Academic Dashboard — search, per-subject breakdown, color-coded status
- **FR-13:** Attendance Statistics Overview — per-subject stats (Classes Run, Enrolled, Marked, Avg Headcount, %)
- **FR-14:** Faculty Performance Dashboard — per-faculty analytics, worst subject identification
- **FR-15:** At-Risk Student Detection — flag students with <60% attendance
- **FR-16:** Chronic Latecomers Detection — flag students with 3+ late marks
- **FR-17:** ECA Tracking — extra-curricular activity marks
- **FR-18:** Master Data Import — bulk import from Google Sheets format
- **FR-19:** Incomplete Records Detection — flag subjects with missing data
- **FR-20:** Attendance Key Configuration — configurable P/L/E/U codes
- **FR-21:** Enrollment REST API — expose enrollment CRUD

**SRS Sections 3-5 from original Day 4 plan still valid, incorporate the new FRs.**

```powershell
git checkout docs/srs-document
git pull origin docs/srs-document
```

---

## Day 5 (Sat Jul 11) — Project Charter

Standup 9 AM.

```powershell
git checkout develop
git pull origin develop
git checkout -b docs/project-charter
```

`docs/project-charter.md` — keep each section to a few lines:

- **Team:** Prizma (PM), Abhishek (Backend), Ekata (Frontend)
- **Business case:** manual attendance is slow and error-prone; face recognition cuts marking time from ~5-10 min to under 30 sec
- **In scope:** web attendance app, face enrollment, course management, reports, auth
- **Out of scope (this project):** native mobile apps, SMS/email alerts, LMS integration, ML analytics
- **Milestones:** Sprint 0 (Jul 12) → Sprint 1 (Jul 19) → Sprint 2 (Jul 26) → Sprint 3 (Aug 2) → Sprint 4 (Aug 9) → Final (Aug 16)
- **Risks:**

| Risk | Impact | Mitigation |
|---|---|---|
| Face recognition inaccuracy | High | manual override always available |
| Team availability | Medium | daily standups catch it early |
| Camera hardware issues | Medium | manual marking fallback |
| Scope creep | High | PM gates all new feature requests |

```powershell
git add .
git commit -m "[docs] Add Project Charter draft"
git push -u origin docs/project-charter
```

---

## Day 6 (Sun Jul 12) — Review + Submit

Week End Review 4 PM — you lead it.

`docs/srs/index.md` — links to all 5 sections + a short revision history table.

```powershell
git checkout develop
git pull origin develop
git merge docs/srs-document
git merge docs/project-charter
git push origin develop
git push origin --all
```

Trello card "Sprint 0 Review — Jul 12": what got done, what's carrying into Sprint 1.

```powershell
git add .
git commit -m "[docs] Complete Sprint 0 - SRS v1 and Project Charter"
git push origin develop
```

**In the review meeting, check these against goals, out loud, one by one:** tooling setup, requirements gathered, SRS draft, Project Charter, DB schema, system architecture, wireframes, frontend scaffolded. If any are red, decide now whether they roll into Sprint 1 Day 1 or get cut.

---

## Week 1 checklist
- [ ] Team meeting led, roles confirmed
- [ ] Google Drive structure created
- [ ] SRS v1 — all 5 sections
- [ ] Project Charter drafted
- [ ] Meeting minutes logged on Trello, every day
- [ ] Teacher meeting completed
- [ ] Sprint 1 goals ready to present Monday
