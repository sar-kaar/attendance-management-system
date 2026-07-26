# Abhishek — Week 1 (Sprint 0)

**Role:** Backend Developer
**Branch prefix:** `docs/` (Sprint 0 = no app code yet, docs only)
**Full rules:** see `../TEAM_SYNC_PROTOCOL.md` — do the "before you start" and "end of day" steps every day below, not repeated per-day here.

### Your scope
- Backend code, database, auth, face recognition
- GitHub admin: repo, branches, PR reviews
- Deployment / developer / API docs

### Trello cards you own
T-001, T-002, T-004, T-005, T-008 · US-03, US-05, US-07, US-08, US-09, US-11, US-14 · Face Recognition Research · Deployment Guide, Developer Guide, API Documentation

---

## Day 1 (Tue Jul 7) — Setup — DONE
- Trello workspace + boards built
- Guide book written, pinned in Discord
- Project tracker + sprint board loaded
- Google Sheets tracker created
No git work this day.

## Day 2 (Wed Jul 8) — GitHub setup — DONE (meeting did NOT happen)

**Correction: the "team meeting" that was logged here never actually happened. Only the git/repo work below is real. The actual kickoff meeting is TODAY (Jul 9) — run it first using `Guidelines/06_TOMORROW_MEETING_GUIDE.md` before doing anything else today.**

```powershell
cd D:\CSE Project
git clone https://github.com/sar-kaar/attendance-management-system.git
cd attendance-management-system
git add .
git commit -m "[init] Project initialization with README and .gitignore"
git branch -M main
git remote add origin https://github.com/sar-kaar/attendance-management-system.git
git push -u origin main
git checkout -b develop
git push -u origin develop
```
Then: GitHub → Settings → Collaborators → add Prizma + Ekata.

---

## Day 3 (Thu Jul 9) — Verify Real Schema (NOT build from scratch)

**Before you start:** check `../TEAM_SYNC_PROTOCOL.md` step 1-3. Confirm no one else touched `develop` since last night.

```powershell
git checkout develop
git pull origin develop
git checkout -b docs/database-schema
```

**Task 1 — Confirm real tables.** Run and check output matches:
```powershell
python manage.py inspectdb
```
Real tables: `User` (custom, role field: admin/faculty/student), `Student`, `Course`, `Attendance`. Face data is stored directly on `Student` (no separate `face_data` table). **There is no `Enrollment` table** — any student can currently be marked present in any course. Decide today: add one, or accept the gap for now and note it.

**Task 2 — Write `docs/database-schema.md`** documenting the 4 REAL tables above (columns, FKs, role field values), not the old 6-table UUID design. Update `docs/er-diagram.md` (already in repo) if it's out of date instead of replacing it.

**Task 3 — Two real security gaps to fix today (before anyone builds on top):**
- `SECRET_KEY` in `config/settings.py` is hardcoded — move it to `.env`, load with `python-decouple` or `os.environ`.
- CORS is wide open — restrict `CORS_ALLOWED_ORIGINS` to `http://localhost:3000` (Ekata's dev server).

**Task 4 — commit and tell the team**
```powershell
git add .
git commit -m "[docs] Document real Django schema, flag Enrollment gap, harden SECRET_KEY+CORS"
git push -u origin docs/database-schema
```
Post in Discord: "Real schema is 4 tables, not 6 — no Enrollment table exists yet, any student can be marked in any course right now. Ekata + Prizma, this is what your API/wireframes map to."

**Running behind today?** Fix the SECRET_KEY + CORS first — those are actual open holes. The schema doc can slip to tomorrow morning without blocking anyone.

---

## Day 4 (Fri Jul 10) — Google Sheets Analysis + System Architecture + Week 1 Complete

**Before you start: Cleanup already done** — Python 3.14.5 alpha was uninstalled, PATH was cleaned, and `python` resolves to the project `.venv` (3.11.15). All 11 requirements are installed in `.venv`.

**New task: Google Sheets Data Analysis**
*This task was added to Week 1 — analyze existing Google Sheets dashboards to identify features not yet in the Django code, create user stories as GitHub Issues + Trello cards.*

```powershell
python -c "import decouple, django; print('ok')"  # confirm .venv works
```

**Task 1 — Read Google Sheets, compare to Django code, create user stories**
Read 4 sheets via Composio/API, identify missing features, create GitHub Issues + Trello cards.

Sheets analyzed:
- `Attendance` — Class 1 grid (dates × students) + Attendance key (P/L/E/U)
- `SUM I 2026 Dashboard` — Dashboard, Master Data, Stats, Faculty, At-Risk, Latecomers
- `Testing_Sheet_For_Dashboard` — Same dashboard layout
- `Student Master Dashboard` — Same layout, rokayaabi123 account

**Findings — 10 features NOT in Django code:**
| Feature | GitHub Issue | Trello Card |
|---------|-------------|-------------|
| Student Academic Dashboard API | #19 | Card 86 |
| Attendance Statistics Overview | #17 | Card 87 |
| Faculty Performance Dashboard | #18 | Card 88 |
| At-Risk Student Detection | #20 | Card 89 |
| Chronic Latecomers Detection | #24 | Card 90 |
| Master Data Bulk Import | #21 | Card 91 |
| ECA Tracking | #23 | Card 92 |
| Incomplete Records Detection | #22 | Card 93 |
| Attendance Key Configuration | #26 | Card 94 |
| Enrollment REST Endpoint | #25 | Card 95 |

All created as GitHub Issues on `sar-kaar/attendance-management-system` (#17-#26) + Trello cards in Product Backlog (86-95).

Teacher meeting 11 AM — have a 2-line status ready.

**ALREADY DONE (previous session):** `docs/system-architecture.md`, `docs/database-schema.md`, SECRET_KEY → .env, CORS restricted, requirements all installed in .venv.

**Week 1 checklist — DONE:**
- [x] GitHub repo + main/develop branches + collaborators added
- [x] Database schema doc + ER diagram documented
- [x] System architecture doc (Django/DRF/SQLite) + API endpoint list
- [x] 10 user stories created from Google Sheets analysis (US-06 to US-15)
- [x] Backend hardened (SECRET_KEY in .env, CORS locked down)
- [x] Google Sheets data analyzed, 10 new features identified and tracked
- [x] GitHub Issues #17-#26 created + Trello cards 86-95 in Product Backlog
- [x] Enrollment model added, migrations 0002/0003 applied
- [x] AttendanceSerializer.validate() added for enrollment enforcement
- [x] AGENTS.md + SKILL.md created, opencode.json configured
