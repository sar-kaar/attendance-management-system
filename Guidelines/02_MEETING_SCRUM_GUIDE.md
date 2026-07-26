# Meeting & Scrum Guide — Attendance Management System

**Team:** Prizma Subedi (PM), Abhishek Rokaya (Dev), Ekata Rimal (Dev)  
**Project:** Attendance Management System (AMS)  
**Duration:** July 7 – August 25, 2026

---

## Table of Contents

1. [Daily Standup Guide](#1-daily-standup-guide)
2. [Sprint Planning Guide](#2-sprint-planning-guide)
3. [Sprint Review Guide](#3-sprint-review-guide)
4. [Sprint Retrospective Guide](#4-sprint-retrospective-guide)
5. [Weekly Teacher Meeting Guide](#5-weekly-teacher-meeting-guide)
6. [Meeting Minutes Template](#6-meeting-minutes-template)
7. [Communication Rules](#7-communication-rules)

---

## 1. Daily Standup Guide

### Details

| Item | Value |
|------|-------|
| Time | 9:00 AM every day (including weekends if working) |
| Duration | 15 minutes maximum |
| Platform | WhatsApp call / Google Meet / Discord |
| Format | 3 questions only — no deep discussions |
| Rule | If you're blocked, say it immediately. Don't wait. |

### The 3 Questions

1. **What did I work on yesterday?**
2. **What am I working on today?**
3. **Is there anything blocking me?**

### Standup Script — Day 1 (Jul 7)

```
PM (Prizma): "Good morning team! Let's do our first standup.
Abhishek, what did you do yesterday and what are you doing today?"

Abhishek: "Yesterday was the kickoff. Today I'm setting up the
backend project structure — Django with DRF and SQLite."

PM: "Ekata, your turn."

Ekata: "Yesterday I set up my dev environment — installed Python,
VS Code extensions. Today I'll create the React project
using Vite and set up MUI."

PM: "My update: I finalized the Trello board with our backlog
lists and created the initial user stories. No blockers from me.
Let's connect on WhatsApp if anything comes up. Great first standup!"
```

### Standup Script — Typical Day During Sprint 2

```
PM (Prizma): "Morning team! Quick standup. Abhishek?"

Abhishek: "Yesterday I finished the Student CRUD API — all four
endpoints tested with Postman. Today I'm starting the Course CRUD
API. No blockers."

PM: "Ekata?"

Ekata: "Yesterday I built the student list page with the table
and the add/edit modal. Today I'll connect it to Abhishek's API.
Slight blocker — I need the API base URL to confirm the endpoint."

Abhishek: "It's http://localhost:5000/api. I'll share the full
Postman collection after standup."

PM: "Great, that's resolved. My update: I updated the risk register
and prepared the status report for the teacher. All good. Let's
keep it moving!"
```

### Blockers Protocol

If a team member reports a blocker:
1. The PM acknowledges the blocker and adds a Trello card labeled "blocker"
2. If resolvable within 2 minutes, discuss after standup
3. If not resolvable immediately, the PM assigns an owner and follow-up time
4. The blocker must be resolved before the next standup, or escalated

### Standup Etiquette
- Be on time. If you're late, message the group chat.
- No sidebar discussions during standup. Take them offline.
- Keep updates concise — 1–2 minutes per person max.
- If you weren't working (holiday, sick), say "No update" clearly.

---

## 2. Sprint Planning Guide

### Details

| Item | Value |
|------|-------|
| Duration | 2 hours (max) |
| When | First day of each sprint (Monday morning) |
| Who | All 3 team members |
| Tools | Trello board (Sprint Planning view), time timer |

### Agenda

| Time | Activity | Description |
|------|----------|-------------|
| 0:00–0:10 | Review sprint goal | Read sprint goal aloud. Confirm it's still valid. |
| 0:10–0:40 | Review product backlog top items | Go through highest-priority user stories. Discuss scope. |
| 0:40–1:20 | Estimate and assign | Assign story points (1, 2, 3, 5, 8). Assign owner. |
| 1:20–1:40 | Set sprint backlog | Move selected stories to Sprint Backlog list. |
| 1:40–1:50 | Confirm Definition of Done | Review DoD checklist for each story. |
| 1:50–2:00 | Q&A | Clarify questions. Confirm next standup time. |

### Story Pointing Scale

| Points | Meaning | Example |
|--------|---------|---------|
| 1 | Trivial (minutes) | Fix typo, update config |
| 2 | Small (half day) | Add a form field, write a query |
| 3 | Medium (1 day) | Build a new page, create an API endpoint |
| 5 | Large (2–3 days) | Full CRUD for a resource, face recognition integration |
| 8 | Very Large (4+ days) | Should be broken down further |

### Definition of Done (DoD) Checklist

For every user story, ALL of these must be true before marking "Done":

- [ ] Code written and committed to GitHub
- [ ] Code reviewed by at least one other team member
- [ ] All acceptance criteria met
- [ ] API endpoints tested with Postman (backend stories)
- [ ] UI renders correctly on Chrome + Firefox (frontend stories)
- [ ] Error states handled (loading, empty, error)
- [ ] No console errors
- [ ] Works with real backend data (not mocked)
- [ ] PM has reviewed the feature

### Full Script — Sprint 1 Planning (Jul 20)

```
PM (Prizma): "Welcome to Sprint 1 Planning. Today is July 20.
Our sprint goal is: 'User authentication and role management
work end-to-end — users can register, log in, and access
role-specific pages.'

Let's review the top backlog items.

First up: US-01 — User Registration. Scope: a form with name,
email, password, role selector. Backend validates, hashes password,
stores in SQLite. Frontend shows success/error feedback.

Abhishek, can you estimate this?"

Abhishek: "Backend side is straightforward. I'd say 3 points."

PM: "Ekata, frontend?"

Ekata: "Also 3 points since I need the form, validation, and
API integration."

PM: "Okay, US-01: 6 total points. Abhishek takes backend,
Ekata takes frontend. Next: US-02 — User Login..."

(Run through remaining stories)

PM: "Great. So our sprint backlog is:
- US-01 (Register): Abhishek (backend), Ekata (frontend)
- US-02 (Login): Abhishek (backend), Ekata (frontend)
- US-03 (RBAC): Prizma (documentation + coordination)
- US-04 (Auth Middleware): Abhishek
- US-05 (Protected Routes): Ekata

Total sprint points: 21. Team velocity estimate: 18–22.

Definition of Done review — everyone clear on the checklist?"

Team: "Yes."

PM: "Any questions before we close?"

Abhishek: "For US-01, should I use express-validator or Joi?"

PM: "Let's go with express-validator since we used it in the
design doc. Ekata, any questions?"

Ekata: "For UI, should I build a custom form or use MUI components?"

PM: "Use MUI TextField and Button. Keep it simple."

PM: "Alright! Sprint 1 starts now. Next standup tomorrow 9 AM.
Let's go!"
```

---

## 3. Sprint Review Guide

### Details

| Item | Value |
|------|-------|
| Duration | 1 hour |
| When | Last day of sprint (Friday) |
| Who | All team members + Teacher (invited) |
| Tools | Live demo (localhost or deployed), Trello board |

### Agenda

| Time | Activity | Description |
|------|----------|-------------|
| 0:00–0:05 | Opening | PM thanks team, states sprint goal |
| 0:05–0:20 | Abhishek demo | Show backend work: API endpoints, Postman tests |
| 0:20–0:35 | Ekata demo | Show frontend work: UI, flows, user experience |
| 0:35–0:45 | PM summary | Sprint metrics: planned vs completed, velocity |
| 0:45–0:55 | Teacher feedback | Teacher asks questions, provides feedback |
| 0:55–1:00 | Closing | PM notes action items, announces next sprint goal |

### Demo Checklist

Before the review, ensure:
- [ ] Backend server is running (localhost or deployed)
- [ ] Frontend dev server is running
- [ ] Test data is seeded (sample users, courses, students)
- [ ] Any known bugs are documented (don't try to hide them)
- [ ] Presentation slides are ready (if needed for Week 7)

### Full Script — Sprint 1 Review (Jul 25)

```
PM (Prizma): "Hello everyone! Welcome to the Sprint 1 Review.
Our sprint goal was: 'User authentication and role management
work end-to-end.' Let's see what we built.

Abhishek, you're up first."

Abhishek: "Thanks. I'll demo the backend APIs using Postman.

First, POST /api/auth/register — I'll register a new teacher.
[Sends request, shows response]
You can see we get back a success message. Password is hashed
with bcrypt — I'll show you the Django admin panel.

Next, POST /api/auth/login — I'll log in with those credentials.
[Sends request, shows response]
We get back a JWT token. I'll use this token to access a
protected route.

GET /api/auth/me — this returns the current user's profile.
[Sends request with token header, shows response]
If I remove the token, it returns 401. If I use a student token
on a teacher-only route, it returns 403.

That's the backend demo."

PM: "Great! Ekata, your turn."

Ekata: "I'll demo the frontend. Here's the login page.
[Shows browser]
MUI components, form validation — if I leave fields empty,
I get error messages. If I enter wrong credentials, a toast
shows 'Invalid email or password.'

Here's the register page — role selector, password confirmation.
[Shows registration flow]
After successful registration, it redirects to login.

After login, I'm redirected to the dashboard. Right now it's
a placeholder since that's Sprint 2. But the protected route
works — if I'm not logged in and try to go to /dashboard,
it redirects to /login.

I also added an auth context so the user state persists on
refresh. And the navbar shows the user's name and role."

PM: "Excellent work! Here are our sprint metrics:
- Planned: 21 story points
- Completed: 19 story points
- US-05 (Protected Routes) partially done — remaining work
  carried over to Sprint 2
- No critical bugs found

Teacher, do you have any questions or feedback?"

Teacher: "Good progress. Can you show what happens when the
JWT expires?"

Abhishek: "The backend returns 401. On the frontend, Ekata
added an interceptor that redirects to login when that happens."

Ekata: "I can show that — I'll wait 5 seconds... [demonstrates]"

Teacher: "Looks solid. For next sprint, make sure the dashboard
has real data, not placeholders."

PM: "Noted. Thank you! Our next sprint goal will be attendance
management. Sprint Planning is Monday 10 AM. Great work everyone!"
```

---

## 4. Sprint Retrospective Guide

### Details

| Item | Value |
|------|-------|
| Duration | 45 minutes |
| When | Saturday after sprint review |
| Format | Start — Stop — Continue |
| Platform | Google Meet / Discord |
| Tool | Shared Google Doc or Miro board |

### Agenda

| Time | Activity | Description |
|------|----------|-------------|
| 0:00–0:05 | Set the stage | PM explains retrospective goal — improvement, not blame |
| 0:05–0:15 | Start doing | What should we START doing? |
| 0:05–0:15 | Stop doing | What should we STOP doing? |
| 0:05–0:15 | Continue doing | What should we CONTINUE doing? |
| 0:15–0:20 | Vote | Each person votes on top 2 items to action |
| 0:20–0:35 | Action plan | Define 1–2 concrete improvement actions for next sprint |
| 0:35–0:45 | Close | Review actions, assign owners |

### Retro Template (Copy into Google Doc)

```
# Sprint [N] Retrospective
**Date:** [Date]
**Sprint Goal:** [Goal]

---

## Start Doing (New habits to adopt)
- 
- 

## Stop Doing (Bad habits to drop)
- 
- 

## Continue Doing (Keep these up)
- 
- 

## Top Votes
1. [item] — [votes]
2. [item] — [votes]

## Action Items for Next Sprint
| Action | Owner | Due |
|--------|-------|-----|
| [action] | [name] | [date] |
| [action] | [name] | [date] |

## Rating (1–5)
Team morale: ___/5
Sprint productivity: ___/5
```

### Full Script — Sprint 1 Retro (Jul 26)

```
PM (Prizma): "Welcome to our first retrospective! Remember,
this is a safe space. We're here to improve how we work,
not to blame anyone. We'll use Start-Stop-Continue format.

Let's each share one thing for each category. I'll start.

START: I think we should start writing unit tests earlier.
We didn't write any this sprint and it bit us with the
protected routes bug.

STOP: I think we should stop waiting until the last day
to connect frontend to backend. Let's connect earlier.

CONTINUE: Our standups were short and focused. Let's
keep that up.

Abhishek, your turn."

Abhishek: "START: We should start using feature branches.
I committed straight to main and it got messy.

STOP: Stop over-estimating. US-04 (Auth Middleware) took
me 2 hours, not a full day.

CONTINUE: Ekata and I had good async communication on
WhatsApp. Let's continue that."

Ekata: "START: We should start doing quick code reviews.
Even a 10-minute review before merging would catch issues.

STOP: Stop having undefined API contracts. I started the
frontend before the API was done and had to change things.

CONTINUE: Daily standups were effective. Let's continue
them."

PM: "Great insights. Let's vote on the top 2 action items."

(Each person votes. Results: "Connect frontend earlier" = 3 votes,
"Feature branches" = 2 votes)

PM: "Okay, our two action items:
1. CONNECT EARLY: Abhishek will share the API contract
   (Swagger/Postman collection) on Day 1 of sprint.
   Ekata will use mock data until real API is ready.
2. FEATURE BRANCHES: Starting Sprint 2, every task gets
   its own branch. Abhishek will set up branch protection.

Team morale: 4/5. Sprint productivity: 4/5.

Great retro, team! See you Monday for Sprint Planning."
```

### Previous Retro Results (Reference)

**Sprint 0 Retrospective (Jul 17):**
| Action | Owner | Status |
|--------|-------|--------|
| Use feature branches for all work | Abhishek | ✅ Implemented Sprint 1 |
| Create API contract before frontend starts | Abhishek | ✅ Done for Sprint 1 |
| Daily standups at 9 AM sharp | All | ✅ Ongoing |

**Sprint 1 Retrospective (Jul 26):**
| Action | Owner | Due |
|--------|-------|-----|
| Share API contract on Day 1 of sprint | Abhishek | Sprint 2 |
| Use feature branches for every task | Abhishek | By Sprint 2 start |
| Quick code reviews (10 min) before merge | All | Sprint 2 |

---

## 5. Weekly Teacher Meeting Guide

### Details

| Item | Value |
|------|-------|
| When | Every Friday after Sprint Review (or as scheduled) |
| Duration | 20–30 minutes |
| Platform | Google Meet / In-person |
| Who | All 3 team members + Teacher |

### What to Prepare

Before each teacher meeting:
- [ ] Trello board open showing Sprint Backlog (Done column highlighted)
- [ ] Demo ready (if applicable)
- [ ] Status report (1-page summary)
- [ ] List of questions or blockers for teacher
- [ ] Laptop with screen sharing ready

### Status Report Template

```
# Weekly Status Report — Week [N]
**Date:** [Date]
**Team:** Prizma, Abhishek, Ekata

## Completed This Week
- [feature 1]
- [feature 2]

## In Progress
- [feature 3] — [X]% complete

## Planned Next Week
- [feature 4]
- [feature 5]

## Blockers
- [blocker description]
- [resolution needed by]

## Questions for Teacher
1. [question]
2. [question]
```

### Full Script — Week 1 Teacher Meeting (Jul 11)

```
PM (Prizma): "Hello teacher! Thanks for meeting with us.
Here's our progress this week:

We completed the project kickoff, set up GitHub and Trello,
and drafted the SRS document. We've identified three user
roles: Admin, Teacher, and Student. Our core features are
manual attendance and face recognition attendance.

Abhishek, can you show the Trello board?"

Abhishek: "Sure. [Shares screen] Here's our backlog with
12 user stories. The board has Backlog, To Do, In Progress,
Review, and Done columns."

PM: "Ekata, anything to add?"

Ekata: "We researched tech options. Backend will use Django
with DRF and SQLite. Frontend will use React with MUI. For face
recognition, we're using OpenCV with the face_recognition
library."

PM: "For next week, we're working on system design — database
schema, wireframes, architecture diagrams. Do you have any
feedback on our SRS or current progress?"

Teacher: "The SRS looks good. Make sure you include a section
on non-functional requirements — especially performance for
face recognition. Also, add an ER diagram in the appendix."

PM: "Noted. We'll add both. Any other concerns?"

Teacher: "How are you handling the face recognition accuracy?"

Abhishek: "We're planning to test with multiple lighting
conditions and angles. We'll also have a manual fallback
if recognition fails."

Teacher: "Good plan. Keep me updated on the testing results."

PM: "Thank you! We'll send the updated SRS by Monday.
Have a great weekend!"
```

### Full Script — Week 3 Teacher Meeting (Jul 25, After Sprint 1 Review)

```
PM (Prizma): "Hello teacher! Here's our Sprint 1 update:

Abhishek completed the authentication API — register, login,
JWT, RBAC middleware. Ekata built the login and register pages
with form validation and protected routes.

We completed 19 out of 21 planned story points. The remaining
work on protected route edge cases carries to Sprint 2.

Abhishek, can you show the demo?"

Abhishek: "Sure. [Shares screen] I'll register a new user,
log in, show the JWT token, then access a protected route.
If I use the wrong role, I get a 403 error."

Ekata: "And here's the frontend. [Shares screen] Login page,
register page, and the dashboard placeholder with auth context
showing the user's name and role."

PM: "For Sprint 2, we're working on attendance management —
student CRUD, course CRUD, and manual attendance marking.
Do you have feedback?"

Teacher: "Good progress. The UI looks clean. One suggestion —
add 'loading' spinners to the buttons during API calls so
users know something is happening."

Ekata: "Good idea. I'll add that in Sprint 2."

Teacher: "Also, start thinking about how attendance data
will be displayed. Charts? Tables? Both?"

PM: "We're planning a dashboard with summary cards and a
chart for weekly trends. Detailed data in tables with filters."

Teacher: "Sounds good. Keep it up!"
```

### Teacher Meeting Schedule

| Week | Date | Focus |
|------|------|-------|
| Week 1 | Jul 11 | SRS review, project scope |
| Week 2 | Jul 17 | Design docs review (ERD, wireframes) |
| Week 3 | Jul 25 | Sprint 1 demo — Auth working |
| Week 4 | Aug 1 | Sprint 2 demo — Attendance working |
| Week 5 | Aug 8 | Sprint 3 demo — Face recognition |
| Week 6 | Aug 15 | Sprint 4 demo — Reports & dashboard |
| Week 7 | Aug 21 | Final submission, presentation |

---

## 6. Meeting Minutes Template

### Full Template

```
================================================================================
                          MEETING MINUTES
                    Attendance Management System
================================================================================

Meeting Details:
  Date:        [Date]
  Time:        [Start time] – [End time]
  Location:    [Google Meet / Room / Discord]
  Type:        [Daily Standup / Sprint Planning / Sprint Review /
                Sprint Retrospective / Teacher Meeting]
  Facilitator: [Name]
  Minutes By:  [Name]

Attendees:
  ☐ Prizma Subedi (PM)
  ☐ Abhishek Rokaya (Developer)
  ☐ Ekata Rimal (Developer)
  ☐ [Teacher Name] (if applicable)

--------------------------------------------------------------------------------
AGENDA
--------------------------------------------------------------------------------
1. [Agenda item]
2. [Agenda item]
3. [Agenda item]

--------------------------------------------------------------------------------
DISCUSSION NOTES
--------------------------------------------------------------------------------

1. [Topic 1]
   - [Key point discussed]
   - [Decision made]

2. [Topic 2]
   - [Key point discussed]
   - [Decision made]

3. [Blockers / Risks]
   - [Blocker description]
   - [Resolution or next step]

--------------------------------------------------------------------------------
ACTION ITEMS
--------------------------------------------------------------------------------

| # | Task Description                          | Owner         | Due Date   |
|---|-------------------------------------------|---------------|------------|
| 1 | [Describe the action item]                | [Name]        | [Date]     |
| 2 | [Describe the action item]                | [Name]        | [Date]     |
| 3 | [Describe the action item]                | [Name]        | [Date]     |
| 4 | [Describe the action item]                | [Name]        | [Date]     |

--------------------------------------------------------------------------------
NEXT MEETING
--------------------------------------------------------------------------------
  Date: [Next meeting date]
  Time: [Next meeting time]
  Type: [Next meeting type]

================================================================================
```

### Filled Example — Sprint Planning Sprint 2 (Jul 27)

```
================================================================================
                          MEETING MINUTES
                    Attendance Management System
================================================================================

Meeting Details:
  Date:        July 27, 2026
  Time:        10:00 AM – 11:45 AM
  Location:    Google Meet
  Type:        Sprint Planning — Sprint 2
  Facilitator: Prizma Subedi
  Minutes By:  Prizma Subedi

Attendees:
  ☑ Prizma Subedi (PM)
  ☑ Abhishek Rokaya (Developer)
  ☑ Ekata Rimal (Developer)
  ☐ [Teacher Name] (not present)

--------------------------------------------------------------------------------
AGENDA
--------------------------------------------------------------------------------
1. Review sprint goal
2. Review product backlog top items (US-06 to US-10)
3. Estimate and assign
4. Set sprint backlog
5. Confirm Definition of Done

--------------------------------------------------------------------------------
DISCUSSION NOTES
--------------------------------------------------------------------------------

1. Sprint Goal
   - Goal: "Teachers can manage students, courses, and mark
     attendance manually."
   - All agreed goal is achievable in 1 week.

2. Backlog Review
   - US-06: Student CRUD (Backend). Estimated: 5 points.
   - US-07: Student Management UI. Estimated: 5 points.
   - US-08: Course CRUD (Backend). Estimated: 3 points.
   - US-09: Course Management UI. Estimated: 3 points.
   - US-10: Manual Attendance Marking. Estimated: 8 points
     (split into US-10a Backend 3pts + US-10b Frontend 5pts).

3. Assignments
   - US-06: Abhishek
   - US-07: Ekata
   - US-08: Abhishek
   - US-09: Ekata
   - US-10a: Abhishek
   - US-10b: Ekata

4. Total Sprint Points: 24
   - Team confidence: High

5. Action from Retro
   - Abhishek will share API contracts before starting US-07
   - All work on feature branches (sprint2/us-06, etc.)

--------------------------------------------------------------------------------
ACTION ITEMS
--------------------------------------------------------------------------------

| # | Task Description                          | Owner         | Due Date   |
|---|-------------------------------------------|---------------|------------|
| 1 | Share Postman collection for Student API  | Abhishek      | Jul 27     |
| 2 | Create feature branches for Sprint 2      | Abhishek      | Jul 27     |
| 3 | Seed test data (5 sample students)        | Abhishek      | Jul 28     |
| 4 | Review US-06 PR before merging            | Ekata         | Jul 28     |

--------------------------------------------------------------------------------
NEXT MEETING
--------------------------------------------------------------------------------
  Date: July 28, 2026
  Time: 9:00 AM
  Type: Daily Standup

================================================================================
```

---

## 7. Communication Rules

### Communication Channels

| Channel | Purpose | Response Time | Link / Access |
|---------|---------|---------------|---------------|
| WhatsApp Group | Daily updates, quick questions, emergencies | Within 1 hour (9 AM–6 PM) | [Group link] |
| Trello Comments | Task-specific discussions, feedback | Within 4 hours | [Board link] |
| Google Drive | Document sharing, collaborative editing | N/A | [Drive link] |
| GitHub | Code repository, issues, pull requests | Within 24 hours | [Repo link] |
| Email | Teacher communication, formal updates | Within 24 hours | [Teacher email] |

### Rules

#### 1. WhatsApp Group Etiquette
- Use the group for quick updates only. No deep technical discussions.
- If a conversation goes beyond 5 messages, take it to a call.
- Use `@Prizma` if something needs PM attention.
- Use `@Abhishek` or `@Ekata` if you need a specific person.
- Don't send code screenshots. Paste code in a Trello comment or GitHub.
- Respond within 1 hour during working hours (9 AM – 6 PM).

#### 2. Trello Workflow
- Every task must have a Trello card.
- Cards move through: Backlog → To Do → In Progress → Review → Done.
- Comment on cards for task-specific questions.
- PM reviews cards in "Review" and moves to "Done" or sends back.
- Labels: `backend`, `frontend`, `documentation`, `bug`, `blocker`.

#### 3. GitHub Workflow
- Feature branches only (no direct commits to main).
- Branch naming: `<sprint>/<us-number>-<short-desc>` (e.g., `sprint2/us-06-student-crud`).
- At least one review required before merging.
- Keep commits small and meaningful.
- Write descriptive commit messages: `feat: add student CRUD API`.
- Push at least once per day.

#### 4. Google Drive Organization

```
Attendance Management System/
├── 01_Project_Management/
│   ├── Project_Charter.docx
│   ├── Risk_Register.xlsx
│   └── Weekly_Reports/
├── 02_Requirements/
│   ├── SRS_v1.docx
│   └── SRS_v2.docx (with teacher feedback)
├── 03_Design/
│   ├── ER_Diagram.png
│   ├── DFD_Level0.png
│   ├── DFD_Level1.png
│   ├── Wireframes/
│   └── API_Design.docx
├── 04_Development/
│   └── (GitHub reference)
├── 05_Testing/
│   ├── Test_Cases.xlsx
│   └── Test_Report.docx
├── 06_Final_Submission/
│   ├── Final_Report.docx
│   ├── User_Manual.docx
│   ├── Presentation.pptx
│   └── Deployment_Guide.docx
└── 07_Meetings/
    ├── Meeting_Minutes/
    └── Retrospectives/
```

#### 5. Emergency Protocol

| Situation | Action | Channel |
|-----------|--------|---------|
| Server down | Immediately notify team | WhatsApp + Call |
| Blocked > 2 hours | Raise in standup, add Trello blocker label | Trello |
| Sick day | Notify team before 8:30 AM | WhatsApp |
| Missed deadline | Communicate ASAP, suggest recovery plan | WhatsApp + Trello |
| Team conflict | PM mediates. If unresolved, escalate to teacher. | Private WhatsApp → Teacher |

#### 6. Teacher Communication
- All teacher communication goes through the PM.
- Teacher email subject format: `[AMS] <Topic> — Team <Section>`.
- Teacher feedback is documented in Trello as a card.
- Teacher meeting minutes are sent to teacher within 24 hours.
- Never approach the teacher with an issue without the PM knowing.

---

## Quick Reference Card

| Ceremony | When | Duration | Key Output |
|----------|------|----------|------------|
| Daily Standup | 9:00 AM daily | 15 min | 3 updates per person |
| Sprint Planning | Mon (sprint start) | 2 hours | Sprint backlog |
| Sprint Review | Fri (sprint end) | 1 hour | Demo + feedback |
| Sprint Retrospective | Sat (after review) | 45 min | Action items |
| Teacher Meeting | Fri (after review) | 30 min | Feedback + approval |

---

*Created by Prizma Subedi — Project Manager*  
*Last updated: July 7, 2026*
