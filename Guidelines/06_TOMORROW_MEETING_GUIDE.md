# Today's Team Meeting Guide (Jul 9) — Real Kickoff, Not Jul 8

**This meeting did NOT happen on Jul 8 like the file used to say. Jul 8 was git/repo setup only (real, already done). This is the actual first team meeting — run it today, before anything else.**

## Meeting Details

| Item | Info |
|------|------|
| **Date** | July 9, 2026 |
| **Time** | 9:00 AM standup slot (suggested, use up to 2 hrs) |
| **Platform** | Google Meet / Discord / In-person |
| **Attendees** | Prizma (PM), Abhishek (Backend), Ekata (Frontend) |
| **Goal** | Align roles, plan Week 1, draft requirements |

---

## Meeting Agenda (2 Hours)

### 1. Opening & Role Confirmation (10 min) — LEAD: Prizma
```
Prizma says:
"Welcome team! Today is our first real working day. 
Quick confirm:
- I'm Prizma — Project Manager — I handle planning, docs, client comms
- Abhishek — Backend Developer — APIs, database, face recognition
- Ekata — Frontend Developer — UI/UX, dashboards, user-facing features
Any questions about roles?"
```
**Checklist:**
- [ ] Everyone agrees on their role
- [ ] Teacher's role clarified (guides weekly)
- [ ] Decision-making: PM decides after team input

---

### 2. Tool Setup Verification (15 min) — LEAD: Prizma

Go around the table. Each person says YES/NO:

| Tool | Who Needs It | Check Command |
|------|-------------|---------------|
| VS Code | All | `code --version` |
| Git | All | `git --version` |
| Python 3.10+ | All | `python --version` |
| Python 3.10+ | Abhishek | `python --version` |
| Trello access | All | Check board links |
| GitHub account | All | Username ready |

**OUTCOME:** All tools verified. If anyone is missing something, note it and fix after meeting.

---

### 3. Requirements Brainstorming (30 min) — LEAD: Prizma

**Step 1: Silent brainstorming (5 min)**
Everyone writes down features they think the system needs. Use paper/phone.

**Step 2: Share & group (15 min)**
Go around, each person shares one feature at a time. Group into categories:

```
CATEGORIES:
[Auth] - Login, Register, Roles
[Students] - Add, Edit, Delete, List
[Courses] - Add, Edit, Delete, List
[Attendance] - Manual Mark, Face Recognition, View, Edit
[Reports] - Dashboard, Charts, Export CSV/PDF
[Other] - Notifications, Audit Log
```

**Step 3: Prioritize (10 min)**
Label each: **M** = Must-have, **S** = Should-have, **N** = Nice-to-have

**OUTCOME:** Prioritized feature list on Trello (📝 Requirements list)

---

### 4. User Stories Drafting (25 min) — LEAD: Prizma

Using the feature list, write user stories in format:
> **As a** [role], **I want** [feature] **so that** [benefit]

**Abhishek** — Read out the first few from the guide book for examples:
```
US-01: As an admin, I want to register users so they can access the system
US-02: As a user, I want to log in so I can access my dashboard
...
```

**Everyone** — Write 3-5 stories each. Then read them out.

**Prizma** — Records all stories on Trello (📝 Requirements → User Stories card)

**OUTCOME:** 10-15 user stories written and on Trello

---

### 5. Sprint 0 Planning (20 min) — LEAD: Prizma

Look at the Week 1 Plan card on the Trello board.

Assign tasks for rest of Week 1:

| Task | Who | Deadline |
|------|-----|----------|
| SRS Document (draft) | Prizma | Jul 11 |
| GitHub Repo Setup | Abhishek | Jul 8 (today!) |
| Database Schema Design | Abhishek | Jul 14 (next week) |
| Architecture Design | Abhishek | Jul 14 |
| Wireframes & Mockups | Ekata | Jul 15 |
| Project Charter | Prizma | Jul 17 |
| Tech Stack Finalization | All (decide together) | Jul 9 |

**Checklist:**
- [ ] Each person knows what they're doing
- [ ] Deadlines set
- [ ] Blockers identified

---

### 6. Communication Rules (10 min) — LEAD: Prizma

Decide as a team:

| Decision | Options | Our Choice |
|----------|---------|------------|
| Daily standup time | 9 AM / 10 AM / Other | _______ |
| Chat platform | WhatsApp / Discord / Telegram | _______ |
| Teacher meeting day | Friday / Monday / Other | _______ |
| Document sharing | Google Drive folder created | _______ |
| Code repo | GitHub (private) | ✓ |

**OUTCOME:** Written agreement. Prizma updates the "Team Norms" card.

---

### 7. GitHub Setup (10 min) — LEAD: Abhishek

```
Abhishek says:
"I'll create the GitHub repo right now.
- Name: attendance-management-system
- Private repo
- I'll add both of you as collaborators
- Branch rule: main is protected, work in feature branches
- Branch naming: feature/US-01-add-students
```

**Tech stack — already decided, confirm out loud, don't re-vote:**
```
Backend: Django + Django REST Framework (already built)
Frontend: React
Database: SQLite (dev), PostgreSQL later if deployed
Face recognition: OpenCV + face_recognition (planned, Week 5)
```

**OUTCOME:** GitHub repo already exists (real, done Jul 8), team already has collaborator access. Confirm this out loud, then move to today's real Day 3 work.

---

### 8. Wrap-up & Action Items (5 min) — LEAD: Prizma

```
Prizma says:
"Let's quickly summarize what everyone does next:

Abhishek — [confirm next action]
Ekata — [confirm next action]
I'll — [confirm next action]

Same time tomorrow for standup? Great. Meeting adjourned!"
```

---

## After Today's Meeting — What Each Person Does

### Abhishek (Backend):
1. Confirm GitHub repo access, branch protection, collaborators (already real, done Jul 8)
2. Move straight to real Day 3 task: verify Django schema, fix SECRET_KEY + CORS — see `Weekly Tasks/Week 1 Tasks/Abhishek/DAY_BY_DAY.md`

### Prizma (PM):
1. Save today's meeting minutes to Trello (Meeting Notes → "Kickoff Meeting" card)
2. Create Google Drive folder → share with team
3. Start SRS document (IEEE 830 outline) — real stack is Django + SQLite, not FastAPI/PostgreSQL
4. Send teacher a summary email

### Ekata (Frontend):
1. Start wireframes (Figma)
2. Tomorrow standup: show wireframe drafts

---

## Links for Tomorrow

| Resource | Link |
|----------|------|
| Main Trello Board | https://trello.com/b/tf3ceNmA |
| Week 1 Sprint Board | https://trello.com/b/MprhfVuh/ams-week-1-sprint |
| Project Tracker Sheet | https://docs.google.com/spreadsheets/d/1B2m9trSqt1Vl2SHmgeCLXnJxx1nJuS3GUKxXHmV-cKM/edit |
| Progress Tracker Sheet | https://docs.google.com/spreadsheets/d/1eXQK5cUmhQcFO2-vORI2bhKRxO1QXZ_PUo57qQxKqUY/edit |
| Guide Book | 00_COMPLETE_PROJECT_GUIDE_BOOK.md |
| Meeting Scripts | 02_MEETING_SCRUM_GUIDE.md |
| Deliverables Checklist | 04_DELIVERABLES_CHECKLIST.md |
