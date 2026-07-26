# CSE 405 — Attendance Management System
## Complete Project Guide Book

**Course:** CSE 405 — Software Project Management
**Project:** Attendance Management System (Facial Recognition + Manual Attendance)
**Team:** Prizma Subedi (PM), Abhishek Rokaya (Backend), Ekata Rimal (Frontend)
**Timeline:** 7 Weeks — July 7 to August 25, 2026
**Methodology:** Agile Scrum + Kanban (Scrumban) + PMBOK practices
**Board:** https://trello.com/b/tf3ceNmA
**GitHub:** https://github.com/sar-kaar/attendance-management-system

---

**How to use this book:** This is your team's manual for the entire project. Read the **Role Matrix** below first — it tells every person exactly what they own. Then use Parts 3-7 as a day-by-day reference. When you need to write a document or run a meeting, jump to the specific template in Part 8. If you're ever confused about what to do next, start with the Daily Standup (Section 4.1) and check the Trello board.

**Before anything else, read `REALITY_CHECK.md` in this same folder.** The real stack is Django + DRF + SimpleJWT + SQLite, roles are admin/faculty/student (not teacher), and backend auth + CRUD are already built as of Week 1. That file is the source of truth whenever it disagrees with this book — this book gets updated to match it, not the other way around.

---

## 👑 WHO DOES WHAT — TEAM ROLE MATRIX

Every card on Trello has a member assigned. If you see your avatar on a card, it is YOUR responsibility.

### Prizma Subedi — Project Manager (PM)
**Trello:** @prizmasubedi | **Goal:** Keep project on track, documents complete, team unblocked

| What You Own | Where (Trello List / Cards) |
|-------------|----------------------------|
| All planning docs | Project Charter, Business Case, Scope Statement, Product Vision cards |
| Requirements | SRS, Functional/Non-Functional Req, User Stories, Use Cases, Actors, Acceptance Criteria cards |
| Stakeholder mgmt | Stakeholder Register, Stakeholder Analysis, Communication Plan cards |
| All risk & change | Risk Register, Change Request, Issue Tracking cards |
| All meetings & reports | Kickoff + Daily Scrum + Status Reports + Sprint Reports cards |
| All closure docs | Final Report, Presentation, Lessons Learned, Project Handover, Closing Report cards |
| Project Resources | Project Brief, Tech Stack, Team Norms, Useful Links cards |
| Sprint planning | Sprint 0–6 goal cards in Sprint Planning list |

**Your daily checklist:**
- [ ] 9:00 AM — Lead standup (15 min max)
- [ ] After standup — Update Trello (move cards, check assignments)
- [ ] After standup — Update Google Sheet progress
- [ ] End of day — Write meeting minutes if there was a meeting
- [ ] End of day — Check for blockers, tag devs if needed

---

### Abhishek Rokaya — Backend Developer
**Trello:** @abhishekrokaya | **Goal:** Build all backend — APIs, database, auth, face recognition

| What You Own | Where (Trello List / Cards) |
|-------------|----------------------------|
| All user stories with "Backend" label | Product Backlog (US-03, US-05, US-07, US-08, US-09, US-11, US-14) |
| All Sprint 0 setup tasks | To Do (T-001, T-002, T-004, T-005, T-008) |
| Face recognition research | Ideas & Research → Face Recognition API Research card |
| Deployment & code docs | Documentation → Deployment Guide, Developer Guide, API Documentation |
| GitHub admin | Create repo, manage branches, review PRs, CI/CD |
| All backend code | Every file in `server/` directory — models, routes, controllers, middleware, config |

**Your daily checklist:**
- [ ] 9:00 AM — Attend standup (say what you did yesterday, what you do today, blockers)
- [ ] Morning — Check Trello "In Progress" for your cards
- [ ] Work — Code, commit (git add → commit → push), create PR when feature is done
- [ ] Afternoon — Review Ekata's PR if she has one
- [ ] End of day — Move your Trello cards to correct list (In Progress → Review → Done)

---

### Ekata Rimal — Frontend Developer
**Trello:** @ekatarimal | **Goal:** Build all frontend — UI, wireframes, React components, dashboards

| What You Own | Where (Trello List / Cards) |
|-------------|----------------------------|
| All user stories with "Frontend" label | Product Backlog (US-01, US-02, US-04, US-06, US-10, US-12, US-13, US-15) |
| All Sprint 0 setup tasks | To Do (T-003, T-006) |
| UI/UX research | Ideas & Research → UI/UX Design Research card |
| User docs | Documentation → User Manual |
| All frontend code | Every file in `client/` directory — pages, components, styles, routes |

**Your daily checklist:**
- [ ] 9:00 AM — Attend standup
- [ ] Morning — Check Trello "In Progress" for your cards
- [ ] Work — Code, commit, PR
- [ ] Afternoon — Review Abhishek's PR if he has one
- [ ] End of day — Move your Trello cards to correct list

---

### 🔑 Golden Rules
1. **Your face on a card = your job.** Pick it up, work it, move it across the board.
2. **No card moves to "Done" without PM approval.** Prizma moves cards.
3. **Blocked?** Move card to "Blocked" list and tag Prizma on Trello.
4. **Code review?** Respond within 12 hours. If you can't, say so.
5. **Commit every day.** Even if it's one line. You should have 5+ commits per week.

---

## 📊 GOOGLE SHEET TRACKER GUIDE — Where To Log Everything

We have **2 Google Sheets** with **16 tabs total**. Here is exactly what goes where:

### Sheet 1: Project Tracker (Main)
**Link:** https://docs.google.com/spreadsheets/d/1B2m9trSqt1Vl2SHmgeCLXnJxx1nJuS3GUKxXHmV-cKM

| Tab | Who Updates | What Goes There | When |
|-----|------------|----------------|------|
| **Task Tracker** (Sheet1) | Prizma | All 42 tasks with status, dates, story points | Weekly (sprint start) |
| **Sprint Summary** | Prizma | Sprint totals: tasks done/in progress/not started | End of each sprint |
| **User Stories** | Prizma | All 15 US with Feature ID, Priority, Role, Action, Goal | Created now, update as needed |
| **Release Plan** | Prizma | Sprint schedule: dates, story points, status | Created now, update each sprint |
| **Sprint 1-5 Backlog** | Abhishek + Ekata | **Log your daily hours** in Day 1-5 columns — this creates the burndown! | Every day during sprint |
| **Sprint Review & Retro** | Prizma | What worked, what didn't, action items | End of each sprint |
| **BDD Scenarios** | Prizma + Devs | Test scenarios for each feature | Before/during each sprint |

### Sheet 2: Personal & Project Progress
**Link:** https://docs.google.com/spreadsheets/d/1eXQK5cUmhQcFO2-vORI2bhKRxO1QXZ_PUo57qQxKqUY

| Tab | Who Updates | What Goes There | When |
|-----|------------|----------------|------|
| **Personal Log** | **Everyone** | Your daily hours per task | Every day after work! |
| **Project Progress** | Prizma | Task completion % per sprint | Weekly |
| **Weekly Summary** | Prizma | Week-by-week goal tracking | Weekly |
| **Git Cheat Sheet** | Reference | Git commands (read only) | No updates needed |
| **Daily Checklist** | **Everyone** | Check off your daily tasks | Every day during standup |

### IMPORTANT: Daily Hour Logging Rule
**Every team member must fill their hours in 2 places each day:**
1. **Personal Log** tab (Sheet 2) — log Date, Task, Hours Spent, Status
2. **Sprint [N] Backlog** tab (Sheet 1) — log hours in Day 1-5 columns

This is how we track velocity and create burndown charts. Takes 2 minutes.

---

## PART 1: UNDERSTANDING THE APPROACH (Why We Do Things This Way)

### 1.1 Single Board Philosophy

**A Trello board = your project.** Lists are phases or states. Cards are tasks.

Think of the board as a factory assembly line. Each card is a product moving through stations: raw materials arrive (Product Backlog), get processed (In Progress), inspected (Code Review), tested (Testing), and shipped (Done). You can stand at one end and see the entire workflow at a glance.

For a 7-week, 3-person project, a **single board** keeps everything visible. Multiple boards would mean switching between them, losing context, and wasting time. Professional teams use this approach all the time:

- **Spotify Squads** use a single board per squad to track all work.
- **Startup teams** use one board because everyone needs to see everything.
- **University project teams** use one board because the project is small enough.

Our board has **25 lists** representing the complete Software Development Life Cycle (SDLC), from idea to completion. Each list has a specific purpose (see Part 7 for the full list).

### 1.2 Scrum + Kanban = Scrumban

We are using a hybrid approach called **Scrumban**. Here is what that means:

| Methodology | Core Idea | What We Use |
|---|---|---|
| **Scrum** | Fixed timeboxes (sprints), roles (PM, Dev), ceremonies (standup, planning, review, retro) | Sprint planning, 1-week sprints, daily standups, reviews |
| **Kanban** | Visual workflow, Work-in-Progress (WIP) limits, continuous flow | 25-list board, WIP limit of 2 tasks per person, cards flow left to right |
| **PMBOK** | Industry-standard best practices for documentation | Project charter, risk register, stakeholder register, change requests |

**How it works in practice:**

1. We use **Scrum for planning** — every week is a sprint with a goal.
2. We use **Kanban for tracking** — cards move through visual lists.
3. We use **PMBOK for documentation** — we write proper project artifacts.

This gives us the best of all worlds: the structure of Scrum, the visibility of Kanban, and the professionalism of PMBOK.

### 1.3 Sprints in a Single Board

You might wonder: "If we have one board, how do we manage multiple sprints?"

Here is how:

- Each sprint is represented as a **card** in the "Sprint Planning" list (not a separate board).
- When a sprint starts, the PM moves the sprint card to "Sprint Backlog" and pulls individual tasks from the Product Backlog into "To Do".
- When a sprint finishes, the completed sprint card moves to "Completed Sprints".

**Real-world analogy:** Professional tools like **Jira** work exactly this way. An "Epic" (like a sprint card) contains multiple "Stories" (tasks). You plan the epic once and track its stories through the workflow.

### 1.4 Why 7 Weeks? Why 5 Sprints?

Our timeline is:

| Period | What |
|---|---|
| Week 1 (Jul 7-12) | Initiation & Requirements (no sprint — just planning) |
| Week 2 (Jul 13-19) | Sprint 0 — Design & Planning |
| Week 3 (Jul 20-26) | Sprint 1 — Foundation & Auth |
| Week 4 (Jul 27-Aug 2) | Sprint 2 — Core Attendance |
| Week 5 (Aug 3-9) | Sprint 3 — Face Recognition |
| Week 6 (Aug 10-16) | Sprint 4 — Reports & Testing |
| Week 7 (Aug 17-25) | Sprint 5 — Finalization & Submission |

Week 1 is setup (no sprint). Sprints 0-5 are each 1 week (except Sprint 5 which is ~9 days to allow for final submission). This is standard for a 7-week academic project.

---

## PART 2: TEAM ROLES & RESPONSIBILITIES

### 2.1 Project Manager — Prizma Subedi

**You are the glue that holds the project together.** Your job is not to code — it is to make sure the coders can code effectively.

**Specific responsibilities:**

| Area | What You Do |
|---|---|
| **Sprint Planning** | Lead the planning meeting, set sprint goals, prioritize backlog |
| **Client Communication** | Talk to the teacher, report progress, ask for feedback |
| **Risk Management** | Maintain the risk register, watch for problems, plan mitigations |
| **Progress Tracking** | Update Trello daily, track burndown, measure velocity |
| **Documentation** | Write the Project Charter, SRS lead, Status Reports, Final Report |
| **Meetings** | Schedule and run all ceremonies, take minutes |

**Your daily routine:**

1. 8:45 AM — Review Trello board, check what moved
2. 9:00 AM — Run daily standup (15 min)
3. 9:15 AM — Update Trello: move cards, update checklists, add comments
4. 9:30 AM — Check risks, update risk register if needed
5. 10:00 AM — Your own work (documentation, planning)
6. End of day — Review what was completed, prepare for tomorrow

**Documents you own:**

| Document | Due | Template Location |
|---|---|---|
| Project Charter | End of Week 2 | See Part 8 |
| SRS (lead) | End of Week 2 | See Trello checklist |
| Risk Register | Start of Week 2, update weekly | See Trello checklist |
| Weekly Status Reports | Every Friday | See Part 8 |
| Meeting Minutes | After every meeting | See Part 8 |
| Final Report (lead) | Week 7 | See Trello checklist |

### 2.2 Backend Developer — Abhishek Rokaya

**You build the engine.** Every feature the user sees on screen depends on APIs and database work you do behind the scenes.

**Specific responsibilities:**

| Area | What You Do |
|---|---|
| **Database Design** | Design tables (users, students, courses, attendance, face_data), write migrations |
| **API Development** | Build REST endpoints for auth, CRUD, attendance, reports |
| **Face Recognition** | Integrate OpenCV/dlib, train recognition model, build API |
| **Authentication** | JWT-based login, role-based access control (RBAC) middleware |
| **Deployment** | Set up server, deploy backend, configure environment |
| **API Documentation** | Document every endpoint with examples |

**Your daily routine:**

1. 9:00 AM — Daily standup (report what you did, what you will do, blockers)
2. 9:15 AM — Update your Trello cards (move to In Progress, update checklist)
3. 9:30 AM-12:30 PM — Coding block
4. 12:30-1:30 PM — Lunch
5. 1:30-5:00 PM — Coding block (end with git commit + push)
6. End of day — Update Trello cards with progress notes

**Technology stack (actual — already implemented):**

| Layer | Technology |
|---|---|
| Backend | Django + Django REST Framework (DRF) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Face Rec | OpenCV + dlib + face_recognition (Python) |
| Auth | SimpleJWT (djangorestframework-simplejwt) |
| Hosting | Railway / Render / Heroku (free tier) |

**Key tip:** Start the face recognition research in Week 1 itself. It is the hardest part of the project and you will need the full week to get it right.

### 2.3 Frontend Developer — Ekata Rimal

**You build what users see and touch.** The backend could be perfect, but if the UI is confusing, users will hate it.

**Specific responsibilities:**

| Area | What You Do |
|---|---|
| **UI/UX Design** | Wireframes, mockups, color scheme, typography |
| **Frontend Dev** | Build all pages (login, dashboard, students, courses, attendance) |
| **API Integration** | Connect frontend to backend APIs (axios/fetch) |
| **Camera Component** | Build the camera UI for face recognition |
| **Responsive Design** | Make sure everything works on mobile + desktop |
| **User Manual** | Write the guide for end users |

**Your daily routine:**

Same as backend developer but focused on frontend work.

**Technology stack you will use (suggested):**

| Layer | Technology |
|---|---|
| Framework | React (Vite) |
| Styling | Tailwind CSS or Bootstrap 5 |
| HTTP Client | Axios |
| Charts | Chart.js or Recharts |
| Camera | react-webcam or getUserMedia API |
| Hosting | Vercel / Netlify (free tier) |

**Key tip:** Start building the login page as soon as the backend auth API is ready (end of Week 3). Do not wait for the perfect design — build a working version first, then improve it.

### 2.4 Teacher (Guide)

Your teacher is not on Trello and does not attend daily standups. They check in weekly to guide you.

**When to approach the teacher:**

1. **After sprint reviews** — Demo what you built, get feedback.
2. **When blocked** — If you are stuck on a decision (e.g., which face API to use), ask the teacher.
3. **For scope decisions** — If you need to cut features or add scope, get approval first.

**Teacher meeting script (for PM):**

> "Hello teacher! This week we worked on [summary of work]. Abhishek completed [X], Ekata completed [Y]. Our blockers are [Z]. For next week, we plan to [goals]. Do you have any feedback or guidance?"

---

## PART 3: COMPLETE 7-WEEK TIMELINE

### Week 1 (Jul 7-12) — Project Initiation & Requirements

**Theme:** Set everything up. No coding yet.

| Day | Date | What Happens | Who Leads |
|---|---|---|---|
| Tue | Jul 7 | Kickoff meeting. Team introductions. Set up Trello, GitHub, dev environments. | PM |
| Wed | Jul 8 | Team norms. Communication plan (WhatsApp/Discord). Create GitHub repo. | PM |
| Thu | Jul 9 | Requirements gathering. Brainstorm features. Draft user stories. | All |
| Fri | Jul 10 | Create Product Backlog on Trello. Prioritize stories. | PM + All |
| Sat | Jul 11 | Optional work day. Start SRS draft. | All |
| Sun | Jul 12 | Complete SRS draft v1. Share with team for review. | PM |

**Deliverable by Sunday:** SRS Document v1 draft, GitHub repo initialized, Trello board with Product Backlog populated.

**Abhishek's focus this week:** Install dev environment (Python, Django, IDE). Research face recognition options (OpenCV vs API services). Write findings in Trello Ideas list.

**Ekata's focus this week:** Install dev environment (React, Node.js). Research UI design inspiration. Create a Figma or pen-paper wireframe sketches. Write findings in Trello Ideas list.

**PM's focus this week:** Write Project Brief card. Create all Trello lists and cards. Draft SRS. Schedule teacher meeting for end of week.

### Week 2 (Jul 13-19) — Sprint 0: Design & Planning

**Theme:** Plan before building. All design documents finalized.

**Sprint Goal:** Complete all design documents and plan Sprint 1.

| Day | Activity | Details |
|---|---|---|
| Mon Jul 13 | Sprint Planning for Sprint 0 | Set goal, assign tasks |
| Tue Jul 14 | Wireframes (Ekata) + ER Diagram (Abhishek) | First draft |
| Wed Jul 15 | DFD, System Architecture | Second draft |
| Thu Jul 16 | Finalize all design docs | Incorporate feedback |
| Fri Jul 17 | Sprint Review + Retro | Demo wireframes, ERD, DFD, architecture |
| Sat Jul 18 | Sprint Planning for Sprint 1 | Select stories, estimate, assign |
| Sun Jul 19 | Buffer / catch-up day | Complete any pending docs |

**Documents to complete in Sprint 0:**

| Document | Owner | Format |
|---|---|---|
| Project Charter (signed) | PM | Word/PDF |
| Stakeholder Register | PM | Trello card |
| Risk Register | PM | Trello card |
| Wireframes (all pages) | Ekata | Figma/images |
| ER Diagram | Abhishek | draw.io/PDF |
| DFD (Level 0, 1) | Abhishek | draw.io/PDF |
| System Architecture | Abhishek | draw.io/PDF |
| Technology Stack Decision | All | Trello card |

**Sprint 0 Story Points:** ~13 points (all documentation, no code).

### Week 3 (Jul 20-26) — Sprint 1: Foundation & Auth

**Sprint Goal:** Users can register, log in, and see a dashboard based on their role.

**Backend tasks (Abhishek):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Set up Django project structure | 2 | 1 |
| Create User model with role field | 3 | 2 |
| Build register endpoint (POST /api/auth/register) | 4 | 2 |
| Build login endpoint (POST /api/auth/login) | 3 | 2 |
| Implement JWT token generation | 3 | 1 |
| Create RBAC middleware (admin/faculty/student) | 4 | 3 |
| Create basic user CRUD endpoints | 4 | 2 |
| Set up database and run migrations | 2 | 1 |
| **Total** | **25** | **14** |

**Frontend tasks (Ekata):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Set up React project | 2 | 1 |
| Build registration page | 4 | 2 |
| Build login page | 3 | 2 |
| Create dashboard shell (sidebar + header) | 4 | 2 |
| Implement role-based routing | 4 | 2 |
| Create reusable components (table, form, button) | 4 | 2 |
| Connect login/register to backend API | 3 | 2 |
| **Total** | **24** | **13** |

**PM tasks:**

- Update Trello daily
- Track sprint burndown
- Prepare for Sprint Review (Fri Jul 24)
- Write Weekly Status Report
- Schedule teacher meeting

**Testing focus:** Auth flow (register -> login -> get token -> access protected route).

**Sprint 1 Story Points total:** ~27 points.

### Week 4 (Jul 27-Aug 2) — Sprint 2: Core Attendance

**Sprint Goal:** Admin can manage students and courses. Faculty can mark attendance manually.

**Backend tasks (Abhishek):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Create Student model + CRUD API | 6 | 3 |
| Create Course model + CRUD API | 4 | 2 |
| Create Attendance model + marking API | 6 | 3 |
| Create attendance retrieval API (by student, course, date) | 4 | 2 |
| Add validation and error handling | 3 | 2 |
| Write API tests | 3 | 2 |
| **Total** | **26** | **14** |

**Frontend tasks (Ekata):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Build student management page (list + add + edit) | 6 | 3 |
| Build course management page (list + add + edit) | 5 | 3 |
| Build manual attendance marking UI (date, course, student list, present/absent) | 8 | 5 |
| Build attendance view page (student view) | 4 | 2 |
| Connect all pages to backend APIs | 3 | 2 |
| **Total** | **26** | **15** |

**PM tasks:**

- Mid-sprint backlog refinement (Wed Jul 29)
- Sprint Review + Retro (Fri Jul 31)
- Sprint Planning for Sprint 3 (Sat Aug 1)
- Weekly Status Report

**Testing focus:** Full CRUD flows, attendance marking, data persistence.

**Integration point:** Ekata needs the API endpoints from Abhishek by Tuesday. If Abhishek is late, Ekata should use mock data (JSON files) to build the UI in parallel.

### Week 5 (Aug 3-9) — Sprint 3: Face Recognition

**Sprint Goal:** Students can register their face. Faculty can mark attendance using facial recognition.

**Backend tasks (Abhishek):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Research and select face recognition approach | 4 | 2 |
| Set up face detection (OpenCV) | 6 | 3 |
| Build face registration endpoint (receive image, extract encoding, store) | 8 | 5 |
| Build face recognition attendance endpoint (receive image, match, mark) | 8 | 5 |
| Handle edge cases (no face, multiple faces, low light) | 4 | 3 |
| Write face recognition tests | 4 | 2 |
| **Total** | **34** | **20** |

**Frontend tasks (Ekata):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Build camera component (react-webcam / getUserMedia) | 4 | 2 |
| Build face registration UI (capture photo -> preview -> submit) | 5 | 3 |
| Build face recognition attendance UI (camera -> submit -> result) | 6 | 3 |
| Add loading states and error feedback | 3 | 2 |
| Connect camera components to backend APIs | 3 | 2 |
| **Total** | **21** | **12** |

**PM tasks:**

- This is the highest-risk sprint. Check progress daily.
- Ensure Abhishek starts face recognition research on Day 1 (Monday).
- Schedule mid-sprint check-in with teacher (Wednesday).
- Sprint Review + Retro (Fri Aug 7)
- Weekly Status Report

**Risk mitigation:**

- If face recognition is too complex by Wednesday, have a backup plan: manual attendance with photo verification (teacher shows photo, marks present).
- Start with a simple approach (OpenCV face detection + face_recognition library) and improve later.

**Integration point:** Abhishek should provide a simple test endpoint by Tuesday so Ekata can test the camera-to-API flow.

### Week 6 (Aug 10-16) — Sprint 4: Reports & Testing

**Sprint Goal:** Admin can view dashboards, generate reports, and export data. Full system test done.

**Backend tasks (Abhishek):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Build report generation API (attendance by student, course, date range) | 5 | 3 |
| Build CSV export endpoint | 3 | 2 |
| Build PDF export endpoint | 4 | 2 |
| Build dashboard stats API (total students, present %, trends) | 4 | 2 |
| Bug fixes from integration testing | 4 | 2 |
| **Total** | **20** | **11** |

**Frontend tasks (Ekata):**

| Task | Est. Hours | Story Points |
|---|---|---|
| Build admin dashboard with charts (Chart.js/Recharts) | 6 | 3 |
| Build student dashboard (attendance %, history) | 4 | 2 |
| Build report view page with filters | 5 | 3 |
| Add export buttons (CSV, PDF) | 3 | 2 |
| System-wide responsive design polish | 4 | 2 |
| **Total** | **22** | **12** |

**Testing (both developers):**

| Test Type | What | Who |
|---|---|---|
| Unit tests | Test individual functions | Each dev for their code |
| Integration tests | Test API + database together | Abhishek |
| System tests | Full flow: UI -> API -> DB -> UI | Ekata |
| UAT | Try with real user scenarios | PM + team |

**PM tasks:**

- User Manual draft (assign to Ekata)
- Start Final Report outline
- Sprint Review + Retro (Fri Aug 14)
- Sprint Planning for Sprint 5
- Weekly Status Report

### Week 7 (Aug 17-25) — Sprint 5: Finalization & Submission

**Sprint Goal:** Everything ready for submission. No new features. Only polish.

**Tasks (all team):**

| Task | Owner | Est. Hours |
|---|---|---|
| Final bug fixes | Both devs | 8 |
| Deployment to hosting (both frontend + backend) | Abhishek | 6 |
| Complete all pending tests | Both devs | 6 |
| Complete User Manual | Ekata | 4 |
| Complete Final Report | PM (all contribute) | 10 |
| Prepare presentation slides | PM (all contribute) | 6 |
| Practice presentation | All | 3 |
| Record demo video (if required) | All | 3 |
| Code freeze (no more changes after Aug 22) | All | — |
| Submit project | PM | 1 |

**Key dates:**

| Date | Milestone |
|---|---|
| Aug 17 (Mon) | Sprint 5 begins. Code freeze for minor fixes only. |
| Aug 20 (Thu) | User Manual + Final Report first draft complete |
| Aug 22 (Sat) | Code freeze. No code changes after today. |
| Aug 23 (Sun) | Presentation slides complete. Practice. |
| Aug 24 (Mon) | Final review. Record demo. |
| Aug 25 (Tue) | SUBMISSION DAY |

**Final submission checklist (see Part 10 for details).**

---

## PART 4: SCRUM CEREMONIES GUIDE

### 4.1 Daily Standup (15 min) — Every Day Including Weekends

**Purpose:** Align the team, identify blockers, plan the day.

**Time:** 9:00 AM (agree and stick to it).

**Format:** Each person answers three questions:

1. **What did I do yesterday?** — Be specific. "I built the login endpoint" not "I worked on auth."
2. **What will I do today?** — Again, specific. "I will add JWT token verification middleware."
3. **Any blockers?** — Something stopping you? Need help? Need a decision?

**Example standup:**

> **PM:** Let's start. Abhishek?
>
> **Abhishek:** Yesterday I set up the Django project and created the User model with role field. Today I'll work on the register API endpoint. No blockers.
>
> **Ekata:** Yesterday I created the login page wireframe in Figma. Today I'll code the login page in React. I need the API endpoint URL from Abhishek so I can connect it.
>
> **PM:** Noted. I updated the risk register and prepared the Sprint Planning agenda. Today I'll refine user stories with teacher feedback. Abhishek and Ekata, please coordinate on the API URL after standup. No blockers from my side.

**PM's job after standup:**

1. Update Trello board (move cards, update checklists)
2. Note any blockers and follow up
3. Update the daily standup card in Trello

### 4.2 Sprint Planning (2 hours) — Start of Each Sprint

**Purpose:** Decide what will be done in the upcoming sprint.

**Who:** PM + Developers (teacher optional).

**Agenda:**

| Time | Activity |
|---|---|
| 0:00-0:10 | Review sprint goal. What do we want to achieve? |
| 0:10-0:40 | Review Product Backlog. Which stories are candidates? |
| 0:40-1:10 | Estimate story points (t-shirt sizes). Discuss complexity. |
| 1:10-1:30 | Assign tasks to developers. |
| 1:30-1:40 | Set sprint goal checkbox in Trello. |
| 1:40-2:00 | Create Sprint [N] card, move to Sprint Backlog. |

**After the meeting, PM should:**

1. Create the Sprint [N] card in Sprint Planning list
2. Move selected stories to Sprint Backlog list
3. Move the sprint goal card to Sprint Backlog
4. Assign story point custom fields
5. Update the Sprint Planning card with minutes

### 4.3 Sprint Review (1 hour) — End of Each Sprint

**Purpose:** Demo completed work to the team and teacher.

**Who:** PM + Developers + Teacher.

**Agenda:**

| Time | Activity |
|---|---|
| 0:00-0:05 | PM reviews sprint goal (did we achieve it?) |
| 0:05-0:35 | Each developer demos their work (share screen, show features) |
| 0:35-0:50 | Teacher feedback and questions |
| 0:50-1:00 | PM moves Done cards, updates backlog |

**What to demo:**

- Show the feature working in real time
- Show the code if relevant
- Show error handling ("what happens if...")
- Do NOT show TODO code or incomplete features

**After the meeting:**

- Move all "Ready for Demo" cards to "Done"
- Create a Sprint Review notes card in Meeting Notes
- Create a Sprint Report card in Project Reports

### 4.4 Sprint Retrospective (1 hour) — After Sprint Review

**Purpose:** Improve how we work. No teacher present.

**Who:** Team only.

**Format:** Start-Stop-Continue

| Column | Question |
|---|---|
| **Start doing** | What should we start doing that we are not doing now? |
| **Stop doing** | What should we stop doing because it is not helping? |
| **Continue doing** | What is working well that we should keep doing? |

**Example retrospective outcomes:**

| Start | Stop | Continue |
|---|---|---|
| Write unit tests before merging | Working on multiple tasks at once | Daily standups at 9 AM |
| Update Trello cards immediately | Skipping code review | Good communication on WhatsApp |
| Pair program on difficult features | Forgetting to update task hours | Friday demos |

**After the meeting:**

1. PM writes the Sprint Retro card in Meeting Notes
2. Identify 1-2 actionable improvements for the next sprint
3. Add those improvements to the next Sprint Planning agenda

---

## PART 5: MEETING GUIDES WITH SCRIPTS

### 5.1 First Team Kickoff Meeting Script

**When:** Day 1 (Jul 7, Tuesday)
**Duration:** 1 hour
**Attendees:** Entire team

**PM says:**

> "Welcome everyone! This is our Attendance Management System project for CSE 405. We have 7 weeks starting today. Let me go over the roles quickly: I am Prizma, the Project Manager. Abhishek is our Backend Developer handling database, APIs, and face recognition. Ekata is our Frontend Developer handling UI/UX and all user-facing screens. Our teacher will guide us weekly.
>
> Today we need to:
> 1. Introduce ourselves and our background
> 2. Set up Trello and invite everyone to the board
> 3. Create the GitHub repository
> 4. Agree on our communication channel and meeting times
> 5. Review the 7-week timeline
> 6. Plan Week 1 tasks
>
> Let me share my screen and walk us through the Trello board..."

**Decision log to create during this meeting:**

| Decision | Options | Chosen |
|---|---|---|
| Communication app | WhatsApp / Discord / Slack | |
| Daily standup time | 9 AM / 10 AM / other | |
| Code hosting | GitHub / GitLab | GitHub |
| Branch strategy | main-dev-feature / gitflow | |
| Dev environment | Local / Cloud (CodeSandbox) | |

### 5.2 Weekly Teacher Meeting Script

**When:** After Sprint Review (or as scheduled)
**Duration:** 20-30 min
**Attendees:** PM + Teacher (developers optional)

**PM says:**

> "Hello teacher, thank you for meeting with us. Here is our progress this week:
>
> **What we planned:** [sprint goal]
>
> **What we completed:** [list completed items]
> - Abhishek built [X] and [Y]
> - Ekata built [A] and [B]
>
> **What we did NOT complete:** [if anything was missed]
>
> **Blockers:** [list any blockers]
>
> **Next week plan:** [next sprint goal]
>
> Do you have any feedback on our progress? Are we on the right track? Is the scope appropriate?"

**What to show the teacher:**

1. Trello board (share screen) — walk through the lists
2. Working features (live demo if available)
3. Documents completed (SRS, charter, etc.)

**Questions to always ask:**

- "Is our scope correct for the remaining time?"
- "Are we on track for a good grade?"
- "Any changes you recommend?"

### 5.3 Daily Standup Script Example

**PM:** "Good morning! Let's do our standup. Abhishek, you start."

**Abhishek:** "Yesterday I finished the user model and register endpoint. I also wrote unit tests for the register flow. Today I will work on the login endpoint with JWT. I have no blockers, but I might need Ekata to test the login endpoint once it is up."

**Ekata:** "Yesterday I completed the login page wireframe and started coding the HTML/CSS. Today I will finish the login page and set up React Router for navigation. My blocker: I need the API base URL from Abhishek to connect the login form. Can you share that today, Abhishek?"

**PM:** "Thanks both. Yesterday I updated the risk register (added a risk about face recognition complexity) and refined the Product Backlog with teacher feedback. Today I will prepare the Sprint 1 plan and update the timeline document. No blockers. Abhishek, please share the API URL with Ekata after this call. Meeting over!"

### 5.4 Sprint Planning Script Example

**PM:** "Welcome to Sprint Planning for Sprint 1. Our sprint goal is: Users can register, log in, and see a role-based dashboard. Let us review the Product Backlog."

[PM shares screen and scrolls through Product Backlog]

**PM:** "Which stories support this goal?"

**Abhishek:** "We need US-01 (Register), US-02 (Login), and US-03 (RBAC)."

**Ekata:** "Plus the dashboard setup and the UI pages."

**PM:** "Great. Let us estimate. Abhishek, for the register endpoint — S, M, L, or XL?"

**Abhishek:** "M (2 points). It is straightforward but needs validation and error handling."

**PM:** "Agreed. Ekata, login page?"

**Ekata:** "S (1 point). Simple form, no complex logic."

And so on until all stories are estimated and assigned.

---

## PART 6: USER STORIES & REQUIREMENTS GUIDE

### 6.1 How to Write User Stories

A user story describes a feature from the end user's perspective. The format is always:

> **As a** [type of user], **I want** [action or feature] **so that** [benefit or value].

**Examples for our Attendance System:**

| Story | Role | Action | Benefit |
|---|---|---|---|
| US-01 | Admin | Add students | They can be tracked in the system |
| US-02 | Faculty | Mark attendance | Record student presence |
| US-03 | Faculty | Use face recognition | Contactless, fast attendance |
| US-04 | Student | View attendance | Know my attendance status |
| US-05 | Admin | Generate reports | Monitor attendance trends |

**Why this format works:**

- "As a [role]" — Forces you to think about who needs this.
- "I want [feature]" — Describes WHAT, not HOW.
- "So that [benefit]" — Explains WHY, which helps prioritize.

### 6.2 Acceptance Criteria (Definition of Done)

Every user story must have acceptance criteria — a checklist of conditions that must be true for the story to be considered done.

**Example for US-01 (Admin adds students):**

> **Acceptance Criteria:**
> - [ ] Admin can navigate to "Students" page from dashboard
> - [ ] Admin sees a list of all registered students with name, email, ID
> - [ ] Admin can click "Add Student" and see a form with fields: name, email, student ID, course
> - [ ] Form validates: email format, required fields, duplicate ID check
> - [ ] On submit, student appears in the list without page refresh
> - [ ] Error message shown if API fails
> - [ ] Mobile responsive

### 6.3 Story Points Estimation

We use **t-shirt sizes** mapped to points:

| Size | Points | Meaning | Example |
|---|---|---|---|
| XS | 0.5 | Typo fix, CSS tweak | Fix button color |
| S | 1 | Simple UI change, minor fix | Add a new input field |
| M | 2 | New page, simple endpoint | Login page, register API |
| L | 3 | Complex feature with DB changes | Student CRUD with validations |
| XL | 5 | Multiple components, new tech | Face registration UI + API |
| XXL | 8 | Major feature, risky | Full face recognition attendance |

**How to estimate as a team:**

1. PM reads the story description and acceptance criteria
2. Each developer thinks about complexity (not time)
3. Everyone holds up fingers (1-5) or says their size
4. If estimates differ significantly, discuss why
5. Agree on a final number

**Important:** Story points measure complexity, not hours. A 5-point task might take 4 hours or 10 hours, depending on the developer and unknowns.

### 6.4 Complete User Story Catalog

| ID | Story | Points | Backend | Frontend | Sprint |
|---|---|---|---|---|---|
| US-01 | As an admin, I want to register new users so that they can access the system. | 2 | Yes | Yes | 1 |
| US-02 | As a user, I want to log in so that I can access my dashboard. | 2 | Yes | Yes | 1 |
| US-03 | As an admin, I want role-based access so that data is secure. | 3 | Yes | Yes | 1 |
| US-04 | As an admin, I want to manage students (CRUD) so that records are up to date. | 3 | Yes | Yes | 2 |
| US-05 | As an admin, I want to manage courses (CRUD) so that attendance can be tracked per course. | 3 | Yes | Yes | 2 |
| US-06 | As a faculty member, I want to mark attendance manually so that I can record student presence. | 5 | Yes | Yes | 2 |
| US-07 | As a student, I want to register my face so that I can use facial recognition attendance. | 5 | Yes | Yes | 3 |
| US-08 | As a faculty member, I want face recognition attendance so that marking is contactless. | 8 | Yes | Yes | 3 |
| US-09 | As an admin, I want attendance reports so that I can monitor trends. | 3 | Yes | Yes | 4 |
| US-10 | As a faculty member, I want CSV/PDF export so that I can submit reports. | 3 | Yes | Yes | 4 |
| US-11 | As an admin, I want a dashboard with charts so that I can see attendance at a glance. | 3 | No | Yes | 4 |
| US-12 | As a student, I want a dashboard so that I can see my attendance percentage. | 2 | No | Yes | 4 |
| US-13 | As a faculty member, I want to edit attendance so that I can correct errors. | 2 | Yes | Yes | 2 |
| US-14 | As a student, I want email notifications so that I know when attendance is marked. | 3 | Yes | No | 4 |
| US-15 | As an admin, I want an audit log so that I can track all changes. | 2 | Yes | No | 2 |

**Total story points:** 47 points across 15 stories.

### 6.5 Non-Functional Requirements

These are not user stories, but system requirements about performance, security, etc.

| NFR ID | Requirement | Target |
|---|---|---|
| NFR-01 | Page load time | Under 2 seconds |
| NFR-02 | Face recognition time | Under 3 seconds |
| NFR-03 | Uptime | 99.9% |
| NFR-04 | Concurrent users | Support 50+ |
| NFR-05 | Password encryption | bcrypt or argon2 |
| NFR-06 | Data encryption | AES-256 at rest, TLS in transit |
| NFR-07 | Browser support | Chrome, Firefox, Edge, Safari |
| NFR-08 | Mobile responsive | Works on 320px+ screens |

---

## PART 7: TRELLO WORKFLOW GUIDE

### 7.1 The 25 Lists — What Goes Where

| # | List Name | Purpose | Who Uses |
|---|---|---|---|
| 1 | Project Resources | Reference materials, templates, guidelines | All (read-only) |
| 2 | Ideas & Research | Raw ideas, tech research, exploration | All |
| 3 | Product Vision | Vision statement, elevator pitch, KPIs | PM |
| 4 | Project Charter | Formal project authorization documents | PM |
| 5 | Stakeholders | Stakeholder register, analysis, communication plan | PM |
| 6 | Requirements | All requirement artifacts (FR, NFR, user stories, use cases) | All |
| 7 | Product Backlog | ALL work to be done (prioritized) | PM |
| 8 | Sprint Planning | Future sprint goal cards | PM |
| 9 | Sprint Backlog | Current sprint goal + committed stories | All |
| 10 | To Do | Tasks ready to work on (this sprint) | All |
| 11 | In Progress | Currently being worked on (WIP limit: 2 per person) | Devs |
| 12 | Code Review | Awaiting peer review | Devs |
| 13 | Testing | Being tested | Devs |
| 14 | Blocked | Cannot proceed (reason noted on card) | All |
| 15 | Ready for Demo | Completed, awaiting sprint review | All |
| 16 | Done | Completed and accepted | All |
| 17 | Documentation | All project documents (SRS, reports, manuals) | PM |
| 18 | Meeting Notes | Meeting minutes and action items | PM |
| 19 | Risks | Risk register | PM |
| 20 | Issues | Bug tracking | All |
| 21 | Change Requests | Scope changes | PM |
| 22 | Project Reports | Status reports, velocity, burndown | PM |
| 23 | Completed Sprints | Sprint retrospective cards | PM |
| 24 | Project Closure | Final deliverables, lessons learned | PM |
| 25 | Archive | Historical reference | PM |

### 7.2 Daily Trello Workflow

**Morning (after standup):**

1. Check the "Sprint Backlog" list — review the sprint goal
2. Find your tasks in "To Do" that are assigned to you
3. Move ONE task to "In Progress" (WIP limit: 2 max)
4. Update the card: add a comment with what you plan to do today

**During the day:**

- Keep the card updated as you make progress
- Check off checklist items as you complete them
- If blocked, move the card to "Blocked" and add a comment explaining why

**End of day:**

1. If the task is done: move to "Code Review" and assign a teammate as reviewer
2. If the task is partially done: add a comment summarizing progress
3. Move any new completed items to the appropriate list

### 7.3 Card Movement Rules

```
To Do -> In Progress (when you start working)
In Progress -> Code Review (when code is ready for peer review)
Code Review -> Testing (when peer has approved)
Testing -> Ready for Demo (when tests pass)
Testing -> Blocked (if test fails and you cannot fix immediately)
Ready for Demo -> Done (during sprint review, after demo accepted)
Any list -> Blocked (if something blocks progress)
Blocked -> In Progress (blocker resolved, resume work)
```

### 7.4 Label Usage

Every card should have at least one priority label and one type label.

**Priority labels:**

| Label | Color | When to Use |
|---|---|---|
| Priority: Critical | Red | Must do NOW. Server down, data loss, security issue. |
| Priority: High | Orange | Important for sprint goal. Missing feature. |
| Priority: Medium | Yellow | Normal feature work. Standard priority. |
| Priority: Low | Green | Nice-to-have. Will do if time permits. |

**Type labels:**

| Label | Color | When to Use |
|---|---|---|
| Bug | Red | Defect found in testing or production |
| Feature | Lime | New functionality being built |
| Enhancement | Lime | Improving existing feature |
| Research | Black | Investigation or learning task |
| Backend | Blue | Server-side task |
| Frontend | Purple | Client-side task |
| Database | Blue | Database schema or query work |
| Testing | Pink | Writing or running tests |
| Documentation | Sky | Writing documents |
| Blocked | Red | Card is stuck |
| PM Task | Sky | Administrative task for PM |
| Sprint Goal | Lime | The main goal card for the sprint |
| Risk | Red | Risk management card |

### 7.5 WIP Limits

Work-In-Progress limits prevent you from starting too many tasks at once. Research shows that multitasking slows everyone down.

| List | WIP Limit | Why |
|---|---|---|
| In Progress | 2 per person | Focus on 1-2 tasks, finish them, then start more |
| Code Review | 3 total | Do not let reviews pile up — review quickly |
| Testing | 3 total | Test promptly so work does not bottleneck |

**If you are blocked:**

1. Move the card to "Blocked"
2. Add a comment: what is the blocker? who can resolve it?
3. Pick the next task from "To Do" and start working
4. Do NOT wait around — switch to another task

---

## PART 8: PROJECT MANAGEMENT TEMPLATES

### 8.1 Meeting Minutes Template

```markdown
# Meeting Minutes

**Project:** Attendance Management System
**Date:** [Date]
**Time:** [Start] - [End]
**Location:** [Physical/Virtual link]
**Attendees:** [Names]
**Facilitator:** Prizma Subedi
**Note Taker:** [Name]

## Agenda

1. [Item 1]
2. [Item 2]
3. [Item 3]

## Discussion

### [Item 1]
- Key point discussed
- Decision made

### [Item 2]
- Key point discussed
- Decision made

## Decisions Made

| Decision | Details |
|---|---|
| [Decision 1] | [Details] |

## Action Items

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | [Action] | [Name] | [Date] |
| 2 | [Action] | [Name] | [Date] |

## Next Meeting

**Date:** [Date]
**Time:** [Time]
**Location:** [Link]
```

### 8.2 Weekly Status Report Template

```markdown
# Weekly Status Report — Week [N]

**Period:** [Start Date] to [End Date]
**Reported by:** Prizma Subedi
**Status:** [On Track / At Risk / Behind]

## Progress Summary

[2-3 sentences summarizing the week]

## Completed This Week

- [Task 1] (Owner)
- [Task 2] (Owner)
- [Task 3] (Owner)

## In Progress

| Task | Owner | Est. Completion |
|---|---|---|
| [Task] | [Name] | [Date] |

## Planned for Next Week

- [Task 1]
- [Task 2]
- [Task 3]

## Risks & Issues

| ID | Description | Status | Mitigation |
|---|---|---|---|
| R-001 | [Risk] | [Open/Mitigated] | [Plan] |

## Metrics

- Sprint velocity this week: [X] points
- Total completed: [X] points
- Burn rate: [X] points/day

## Notes

[Any additional information]
```

### 8.3 Risk Register Entry Template

Each risk in the Risk Register follows this format:

```markdown
## Risk R-00X: [Risk Title]

**Description:** [Detailed description of the risk]
**Category:** [Technical / Schedule / Resource / External]
**Probability:** [1 (rare) to 5 (almost certain)]
**Impact:** [1 (negligible) to 5 (catastrophic)]
**Risk Score:** [Probability x Impact]
**Owner:** [Name]
**Trigger:** [What event would activate this risk?]

### Mitigation Strategy
[What will we do to reduce the probability or impact?]

### Contingency Plan
[What will we do if the risk actually happens?]

### Status
[Open / Mitigated / Closed]
**Last Reviewed:** [Date]
```

**Example:**

```markdown
## Risk R-003: Face Recognition Accuracy Below 90%

**Description:** The face recognition model may not be accurate enough for reliable attendance marking, especially in varied lighting conditions or with different camera qualities.
**Category:** Technical
**Probability:** 4 (likely)
**Impact:** 4 (major — core feature failure)
**Risk Score:** 16
**Owner:** Abhishek Rokaya
**Trigger:** Accuracy drops below 85% during testing

### Mitigation Strategy
- Start research early (Week 1-2)
- Test with multiple face recognition libraries (OpenCV, dlib, face_recognition, DeepFace)
- Use ensemble approach (multiple models vote)

### Contingency Plan
- Fallback to manual attendance with photo verification
- Teacher manually confirms identity via photo display

### Status
Open
**Last Reviewed:** Jul 7, 2026
```

### 8.4 Change Request Template

```markdown
# Change Request

**CR ID:** CR-00X
**Date:** [Date]
**Requested by:** [Name]
**Category:** [Scope / Schedule / Resource / Technology]

## Description of Change

[What is being changed?]

## Justification

[Why is this change needed?]

## Impact Analysis

### Scope Impact
[What features are affected?]

### Schedule Impact
[Will this delay the project? How many days?]

### Resource Impact
[Do we need additional tools, people, or skills?]

## Approval

| Role | Decision | Date |
|---|---|---|
| Project Manager | [Approve / Reject / Defer] | |
| Team | [Agree / Disagree] | |

## Implementation Notes

[If approved, how will this be implemented?]
```

### 8.5 Sprint Review Notes Template

```markdown
# Sprint Review — Sprint [N]

**Date:** [Date]
**Attendees:** [Names]

## Sprint Goal

[Original sprint goal]

## Completed Stories

| Story | Points | Owner | Demo Notes |
|---|---|---|---|
| US-0X | X | [Name] | [What was shown] |
| US-0Y | Y | [Name] | [What was shown] |

## Not Completed

| Story | Reason | Carry Over? |
|---|---|---|
| US-0Z | [Reason] | [Yes/No] |

## Feedback

### Teacher Feedback
[Notes from teacher]

### Team Feedback
[Notes from team]

## Actions

| Action | Owner |
|---|---|
| [Action] | [Name] |
```

### 8.6 Retrospective Notes Template

```markdown
# Sprint Retrospective — Sprint [N]

**Date:** [Date]
**Attendees:** [Names]

## Start Doing

- [Thing 1]
- [Thing 2]

## Stop Doing

- [Thing 1]
- [Thing 2]

## Continue Doing

- [Thing 1]
- [Thing 2]

## Top Action Items

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | [Action] | [Name] | [Date] |
| 2 | [Action] | [Name] | [Date] |
```

### 8.7 Lesson Learned Template

```markdown
# Lessons Learned

**Project:** Attendance Management System
**Date:** [Date]
**Author:** [Name]

## What Went Well

| Aspect | What Worked | Why |
|---|---|---|
| Communication | [Detail] | [Reason] |
| Technology | [Detail] | [Reason] |
| Process | [Detail] | [Reason] |

## What Could Be Improved

| Aspect | What Failed | Root Cause | Recommendation |
|---|---|---|---|
| Planning | [Detail] | [Cause] | [Fix] |
| Execution | [Detail] | [Cause] | [Fix] |

## Key Takeaways

1. [Takeaway]
2. [Takeaway]
3. [Takeaway]

## Advice for Future Teams

[1-2 paragraphs of advice]
```

---

## PART 9: QUALITY & TESTING GUIDE

### 9.1 Code Review Checklist

Before moving a card from "In Progress" to "Code Review", the developer must self-check:

**Backend code review checklist:**

- [ ] Code follows project conventions (naming, file structure)
- [ ] No console.log or debug code left in
- [ ] Error handling covers all failure cases (try/catch, proper HTTP status codes)
- [ ] Input validation (never trust user input)
- [ ] SQL injection prevention (use parameterized queries or ORM)
- [ ] Authentication and authorization checked on every protected route
- [ ] API responses follow consistent format (e.g., { success: true, data: {...} })
- [ ] No hardcoded secrets (use .env)
- [ ] Unit tests written for core logic
- [ ] Comments explain WHY, not WHAT (code should be self-documenting)

**Frontend code review checklist:**

- [ ] Code follows project conventions (component structure, naming)
- [ ] No console.log or debug code
- [ ] All API calls have error handling (try/catch, error states in UI)
- [ ] Loading states shown during API calls (spinner, skeleton)
- [ ] Form validation (required fields, email format, etc.)
- [ ] Responsive design works on mobile
- [ ] No hardcoded API URLs (use config file or env vars)
- [ ] Accessibility basics (alt text on images, proper heading structure)
- [ ] Components are reusable where appropriate

**Peer review process:**

1. Developer finishes task, moves card to "Code Review"
2. Assigns a reviewer (other developer) to the card
3. Reviewer reads the code, adds comments on GitHub PR or in Trello
4. Reviewer either approves or requests changes
5. If changes needed, developer fixes and moves back to "Code Review"
6. Once approved, card moves to "Testing"

### 9.2 Testing Levels

| Level | What It Tests | Who Does It | When |
|---|---|---|---|
| **Unit** | Individual functions, methods, components | Developer | During development |
| **Integration** | API + database together, frontend + backend together | Developer | After feature is built |
| **System** | Full end-to-end flow (UI -> API -> DB -> UI) | Developer + PM | End of sprint |
| **UAT** | Real user scenarios (admin adds student, faculty marks attendance) | PM | Before sprint review |

**Unit testing guidelines:**

- Backend: Use Jest (Node) or pytest (Python)
- Frontend: Use Jest + React Testing Library
- Test the happy path + error cases
- Aim for 70%+ code coverage on critical paths

**Integration testing guidelines:**

- Test API endpoints with a test database
- Test frontend + backend together in development
- Verify that data flows correctly through the entire system

**System testing (end of sprint):**

Create a test script that walks through every feature:

```markdown
## Sprint [N] — System Test

### Admin Flow
1. [ ] Register as admin
2. [ ] Log in
3. [ ] Add a student
4. [ ] Add a course
5. [ ] View student list
6. [ ] Log out

### Faculty Flow
1. [ ] Register as faculty
2. [ ] Log in
3. [ ] Select course
4. [ ] Mark attendance
5. [ ] View attendance report
6. [ ] Log out

### Student Flow
1. [ ] Register as student
2. [ ] Log in
3. [ ] View attendance
4. [ ] Log out
```

### 9.3 Definition of Done (Full Checklist)

A card is **Done** only when ALL of these are true:

- [ ] Code is implemented and works correctly
- [ ] Code has been peer reviewed
- [ ] Unit tests pass (if applicable)
- [ ] Integration tests pass (if applicable)
- [ ] UI matches the wireframe/design (frontend)
- [ ] API is documented (backend)
- [ ] No critical or high-priority bugs
- [ ] Works on Chrome and Firefox
- [ ] Mobile responsive (frontend)
- [ ] Card is in "Done" list on Trello

### 9.4 Bug Reporting

When a bug is found, create a card in the "Issues" list with:

```markdown
## Bug Report

**Bug ID:** BUG-00X
**Reported by:** [Name]
**Date:** [Date]
**Severity:** [Critical / Major / Minor]
**Environment:** [Browser, OS, Screen size]

### Description
[What happens?]

### Steps to Reproduce
1. Go to [page]
2. Click [button]
3. See [error]

### Expected Behavior
[What should happen?]

### Actual Behavior
[What actually happens?]

### Screenshots / Video
[Attach if applicable]

### Proposed Fix
[Optional: suggested solution]

### Status
[Open / In Progress / Resolved / Closed]
```

### 9.5 Quality Metrics to Track

| Metric | Target | How to Measure |
|---|---|---|
| Test coverage | >70% | Coverage report from test runner |
| Bug count | <5 open at any time | Count cards in Issues list |
| Sprint velocity | Consistent week to week | Story points completed per sprint |
| Code review turnaround | <24 hours | Time card spends in Code Review list |
| Demo acceptance rate | 100% | Did sprint review accept all demos? |

---

## PART 10: FINAL SUBMISSION CHECKLIST

### 10.1 Document Inventory

| # | Document | Creator | Due | Format |
|---|---|---|---|---|
| 1 | Project Charter (signed) | PM | Week 2 | PDF (signed) |
| 2 | SRS Document (IEEE 830) | PM (all contribute) | Week 2 (v1), Week 4 (final) | PDF |
| 3 | ER Diagram | Abhishek | Week 2 | PDF/image |
| 4 | DFD (Level 0, 1) | Abhishek | Week 2 | PDF/image |
| 5 | Wireframes | Ekata | Week 2 | PDF/image |
| 6 | System Architecture Diagram | Abhishek | Week 2 | PDF/image |
| 7 | Source Code (GitHub) | All | Ongoing | GitHub link |
| 8 | Test Reports | Both devs | Week 6 | PDF |
| 9 | User Manual | Ekata | Week 7 | PDF |
| 10 | Developer Guide | Abhishek | Week 7 | PDF |
| 11 | API Documentation | Abhishek | Week 7 | PDF / Postman |
| 12 | Weekly Status Reports | PM | Every Friday (Weeks 1-7) | PDF |
| 13 | Sprint Reports (5) | PM | End of each sprint | PDF |
| 14 | Final Report | PM (all contribute) | Week 7 | PDF |
| 15 | Presentation Slides | All | Week 7 | PPTX/PDF |
| 16 | Lessons Learned | All | Week 7 | PDF |
| 17 | Deployment Guide | Abhishek | Week 7 | PDF |

### 10.2 Document Template Reference

| Document | Where to Find Template |
|---|---|
| Project Charter | Use PMBOK template from course materials |
| SRS | Use IEEE 830 structure (see Trello checklist in Documentation list) |
| All reports | Use templates from Part 8 of this guide |

### 10.3 Submission Week Timeline (Aug 17-25)

| Day | Tasks |
|---|---|
| Aug 17 (Mon) | Sprint 5 kickoff. Bug fixing. Start Final Report outline. |
| Aug 18 (Tue) | Continue bug fixing. User Manual first draft. |
| Aug 19 (Wed) | Continue bug fixing. Final Report writing. |
| Aug 20 (Thu) | User Manual complete. Final Report first draft. |
| Aug 21 (Fri) | Sprint Review + Retro (final). Teacher demo. |
| Aug 22 (Sat) | **CODE FREEZE** — No more changes. Begin presentation. |
| Aug 23 (Sun) | Presentation complete. Practice demo. |
| Aug 24 (Mon) | Final review of all documents. Record demo video. |
| Aug 25 (Tue) | **SUBMISSION** — Upload everything. |

### 10.4 Submission Day Checklist

**PM does this final check:**

- [ ] GitHub repository is **public** (or accessible by teacher)
- [ ] All 17 documents from the inventory above are in the submission folder
- [ ] PDFs are named clearly (e.g., "01_Project_Charter.pdf", "02_SRS.pdf")
- [ ] README.md in GitHub has: project name, team members, how to run, links to docs
- [ ] Presentation slides are ready (PPTX + PDF)
- [ ] Demo video recorded (if required)
- [ ] All team members' names on cover page of every document

### 10.5 Final Report Structure

The Final Report should follow this outline:

```markdown
1. Executive Summary (1 page)
2. Introduction
   2.1 Project Background
   2.2 Objectives
   2.3 Scope
3. Project Management Approach
   3.1 Methodology (Scrumban)
   3.2 Team Structure & Roles
   3.3 Tools (Trello, GitHub)
   3.4 Communication Plan
4. Sprint Summaries
   4.1 Sprint 0: Design & Planning
   4.2 Sprint 1: Foundation & Auth
   4.3 Sprint 2: Core Attendance
   4.4 Sprint 3: Face Recognition
   4.5 Sprint 4: Reports & Testing
   4.6 Sprint 5: Finalization
5. System Architecture
   5.1 Technology Stack
   5.2 Architecture Diagram
   5.3 Database Design
   5.4 API Design
6. Feature Implementation
   6.1 User Management & Auth
   6.2 Attendance Tracking (Manual)
   6.3 Facial Recognition
   6.4 Reports & Analytics
7. Testing
   7.1 Test Strategy
   7.2 Test Results
   7.3 Defect Analysis
8. Challenges & Lessons Learned
9. Conclusion & Future Work
10. References
Appendices (Screenshots, Code Samples, etc.)
```

### 10.6 Presentation Outline (10-12 slides)

| Slide | Content | Presenter |
|---|---|---|
| 1 | Title slide (project name, team, course) | PM |
| 2 | Problem statement (why this project exists) | PM |
| 3 | Solution overview (what we built) | PM |
| 4 | Technology stack | Abhishek |
| 5 | System architecture diagram | Abhishek |
| 6 | Key features demo (screenshots or live) | Both devs |
| 7 | Face recognition approach | Abhishek |
| 8 | Project management (methodology, sprint summary) | PM |
| 9 | Challenges faced | All |
| 10 | Lessons learned | All |
| 11 | Q&A | All |

---

## APPENDIX A: GLOSSARY

| Term | Definition |
|---|---|
| **Scrum** | Agile framework with fixed-length sprints and defined roles |
| **Kanban** | Visual workflow management system |
| **PMBOK** | Project Management Body of Knowledge — industry standards |
| **Sprint** | A fixed time period (1 week) for completing work |
| **Product Backlog** | Prioritized list of all desired work |
| **Sprint Backlog** | Stories selected for the current sprint |
| **User Story** | Feature description from user perspective |
| **Story Points** | Unit of complexity estimation |
| **WIP Limit** | Maximum tasks allowed in a given state at once |
| **Velocity** | Story points completed per sprint |
| **Burndown** | Chart showing remaining work over time |
| **RBAC** | Role-Based Access Control |
| **JWT** | JSON Web Token — standard for auth |
| **CRUD** | Create, Read, Update, Delete |
| **ERD** | Entity-Relationship Diagram |
| **DFD** | Data Flow Diagram |
| **UAT** | User Acceptance Testing |
| **SRS** | Software Requirements Specification |

## APPENDIX B: QUICK REFERENCE CARDS

**For Abhishek (Backend):**

- Week 1: Set up dev environment, research face recognition
- Week 2: Design database, ERD, DFD, architecture
- Week 3: Auth APIs (register, login, JWT, RBAC)
- Week 4: Student/Course/Attendance APIs
- Week 5: Face recognition integration
- Week 6: Reports, export, testing
- Week 7: Bug fixes, deployment, documentation

**For Ekata (Frontend):**

- Week 1: Set up dev environment, design exploration
- Week 2: Wireframes for all pages
- Week 3: Login, register, dashboard shell
- Week 4: Student mgmt, course mgmt, attendance UI
- Week 5: Camera component, face registration, face attendance UI
- Week 6: Dashboard charts, reports, export, polish
- Week 7: User manual, bug fixes, presentation

**For Prizma (PM):**

- Daily: Run standup, update Trello, track risks
- Weekly: Status report, teacher meeting, update board
- Per Sprint: Planning, review, retro
- Project: Charter (W2), SRS (W2), Final Report (W7), all docs

## APPENDIX C: COMMUNICATION PROTOCOL

| Scenario | Channel | Response Time |
|---|---|---|
| Daily standup | In-person / Video call | 9:00 AM sharp |
| Quick question | WhatsApp / Discord | Within 1 hour (work hours) |
| Code review request | GitHub + Trello | Within 12 hours |
| Blocker | WhatsApp urgent + Trello | Within 30 min |
| Teacher meeting | Email + Schedule | Within 24 hours |
| Document review | Google Docs / Trello | Within 24 hours |

---

**End of Project Guide Book**

*Created July 7, 2026. Update as needed throughout the project.*
