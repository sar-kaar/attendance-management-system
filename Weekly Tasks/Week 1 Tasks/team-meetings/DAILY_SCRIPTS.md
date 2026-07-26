# Meeting Notes — Week 1 (Sprint 0)

Team: Prizma (PM), Abhishek (Backend), Ekata (Frontend) · Jul 7–12, 2026

Use this as a template for standup notes each week — keep entries short: yesterday / today / blockers, not full transcripts.

---

## Day 1 (Tue Jul 7) — Setup
No standup. Trello, guide book, project tracker, sprint board, and Google Sheets were built and ready before Day 2.

---

## Day 2 (Wed Jul 8) — First Team Meeting

10:00 AM–12:00 PM, Discord/Google Meet, all 3 attended.

**Decisions:**
- Roles: Prizma = PM (docs, coordination), Abhishek = Backend (DB, API, face recognition), Ekata = Frontend (React UI)
- Standups: 9 AM daily, 10 min max
- Feature branches only, never push to `main` directly
- Trello for tasks, Google Drive for docs
- Blocked? Message Discord right away, don't wait for standup

**Tool check:** Trello fully set up (boards + sheets linked), guide book pinned in Discord. Ekata to set up Figma.

**11 user stories drafted** (see `docs/srs/03-functional-requirements.md` once written) covering: auth, attendance management, course management, dashboard/reports, student view.

**Sprint 0 split (by Sunday):**
- Prizma: SRS, Project Charter, meeting minutes
- Abhishek: GitHub repo, DB schema, architecture diagram, API design, face recognition research
- Ekata: wireframes, React init, base components

**Branch strategy (Abhishek):** `main` (protected) / `develop` (integration) / `feature/name` / `docs/name`. Commit format: `[type] description` — types: init, feat, fix, docs, chore, refactor.

**Action items for Day 3:**
- Abhishek → GitHub setup + `docs/database-schema`
- Ekata → `docs/wireframes`
- Prizma → `docs/srs-document`

---

## Day 3 (Thu Jul 9) — Standup

9:00 AM, 10 min.

- **Abhishek:** Yesterday — GitHub repo created (private, main+develop), both teammates invited, started DB schema on `docs/database-schema` (users, students, courses, attendance, face_data tables defined). Today — finish ER diagram + SQL migration.
- **Ekata:** Yesterday — Figma workspace set up, started login/register wireframes. Today — finish remaining wireframes (dashboard, students, attendance), start React project setup.
- **Prizma:** Yesterday — SRS outline + Section 1 (Introduction) written, Google Drive folder created. Today — Section 2 (Overall Description).
- Reminder: Ekata + Prizma still need to accept the GitHub invite.
- Blockers: none.

---

## Day 4 (Fri Jul 10) — Standup + Teacher Meeting + Google Sheets Analysis

**Morning cleanup (Abhishek):**
- Python 3.14.5 alpha uninstalled, PATH cleaned, project .venv (3.11.15) now resolves first
- `pip install -r requirements.txt` verified (all 11 packages)
- `python manage.py migrate` ran — applied courses.0002 Enrollment + 0003 backfill
- Enrollment model added to courses/models.py
- AttendanceSerializer.validate() added — rejects unenrolled students

**9:00 AM standup:**
- **Abhishek:** DB schema finished, Enrollment migration applied, Attendance validation added. Today — system architecture doc, Google Sheets data analysis.
- **Ekata:** Wireframes done, React scaffolded. Today — Material UI comparison, base components.
- **Prizma:** SRS Sections 1–2 done. Today — functional + non-functional requirements.

**Google Sheets analysis (~2 hours):**
Read all 4 Google Sheets via Composio:
1. Attendance — date grid + attendance key (P/L/E/U)
2. SUM I 2026 Dashboard — full analytics dashboard
3. Testing_Sheet_For_Dashboard — same layout
4. Student Master Dashboard — same layout

**10 features identified NOT in Django code:**
- US-06: Student Academic Dashboard API
- US-07: Attendance Statistics Overview
- US-08: Faculty Performance Dashboard
- US-09: At-Risk Student Detection
- US-10: Chronic Latecomers Detection
- US-11: Master Data Bulk Import
- US-12: ECA Tracking
- US-13: Incomplete Records Detection
- US-14: Attendance Key Configuration
- US-15: Enrollment REST Endpoint

All created as GitHub Issues (#17-#26) + Trello cards (86-95) in Product Backlog.

**11:00 AM teacher meeting (20 min):**
- Introduced project: face-recognition attendance system, currently in Sprint 0 (docs/design/setup).
- Stack confirmed: Django + DRF + SimpleJWT + SQLite (dev) / PostgreSQL (prod) + React.
- Timeline: 7 weeks total, Sprint 0 ends Sunday, MVP target Week 4, Weeks 5–7 for testing/deployment/docs.
- Teacher expects weekly GitHub activity — confirmed daily commits + feature-branch workflow already in place.

---

## Day 5 (Sat Jul 11) — Standup

9:00 AM.

- **Abhishek:** System architecture doc finished (tech stack, API list, folder structure), committed. Today — face recognition library research, backend project structure, OpenCV test.
- **Ekata:** Material UI chosen. Button/Input/Card/Table components + React Router done. Login page layout done. Today — more page components, refine wireframes based on build learnings.
- **Prizma:** Functional + non-functional requirements + use cases done. Today — start Project Charter, get SRS to reviewable state.
- Reminder: tomorrow is Week End Review — have everything committed and pushed by 5 PM.

---

## Day 6 (Sun Jul 12) — Week End Review

4:00 PM, 30 min.

**Completed:**
- Abhishek: GitHub repo + branches, DB schema + ER diagram + migration, architecture doc, face recognition library chosen, backend scaffolded, all pushed.
- Ekata: All wireframes, React init, Material UI + base components, router, login page, all pushed.
- Prizma: Meeting led, Google Drive set up, SRS v1 (Sections 1–4), Project Charter drafted, minutes logged, teacher meeting done.

**Sprint 0 goal check:** tooling ✅ · requirements (11 stories) ✅ · SRS draft ✅ · Charter ✅ · DB schema ✅ · architecture ✅ · wireframes ✅ · frontend scaffolded ✅

**Sprint 1 focus (starts Monday):** backend auth API + DB setup, frontend auth pages wired to API, face enrollment flow. Sprint 1 Trello board to be ready before Monday's standup.

---

## Daily sheet logging (everyone, every day — see `../TEAM_SYNC_PROTOCOL.md` for the full rule set)

1. Personal Log tab → https://docs.google.com/spreadsheets/d/1eXQK5cUmhQcFO2-vORI2bhKRxO1QXZ_PUo57qQxKqUY
2. Sprint Backlog tab (Day column) → https://docs.google.com/spreadsheets/d/1B2m9trSqt1Vl2SHmgeCLXnJxx1nJuS3GUKxXHmV-cKM

Skipping this loses burndown data for the whole team, not just you.

---

## Sprint 0 completion checklist (Verified Jul 10)
- [x] Tools set up, everyone has access
- [x] Roles confirmed
- [x] 11 original user stories + 10 new from Google Sheets (21 total)
- [x] Branch + commit conventions agreed
- [x] Standup rhythm running
- [x] Teacher meeting done
- [x] SRS v1 drafted (update needed with new FR-12 to FR-21)
- [x] Project Charter drafted
- [x] DB schema + architecture designed
- [x] Wireframes designed
- [x] Frontend scaffolded
- [x] Everything committed and pushed
- [x] **NEW — Google Sheets Data Analysis complete**
- [x] **NEW — Enrollment model + migration applied**
- [x] **NEW — Attendance validation (enforcement) added**
- [x] **NEW — 10 GitHub Issues created (#17-#26)**
- [x] **NEW — 10 Trello cards created (Cards 86-95)**
