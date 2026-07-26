# SPM Process Audit: Guidelines vs Trello vs GitHub

Prepared July 21, 2026. Cross checks three sources against each other: the CSE 405 course requirements, this team's own Guidelines/ process documents, and what Trello and GitHub actually show happened. Written by Abhishek, first person where it concerns my own work, third person for the team level findings.

## A note on the course requirements source

`Guidelines/Course Syllabus CSE 405.pdf` is a generic IAU template syllabus built around eight individual lessons, each with its own case study essay and Turnitin submission, mapped to Schwalbe chapters (Ch1 Intro, Ch2 PM and IT context, Ch3 Process Groups plus Ch4 Integration, Ch7 Cost, Ch6 Schedule plus Ch11 Risk, Ch8 Quality plus Ch9 Resource, Ch12 Procurement plus Ch13 Stakeholder, Ch8 Quality plus Ch10 Communications). It does not itself describe our specific three person team project, our sprints, or a Trello requirement. The actual Project Charter (see below) names Pratik Bhusal as project champion and Model Institute of Technology as sponsor, which does not match the IAU letterhead on the syllabus PDF, so this file is best read as a generic reference document, not the literal brief Prof. Bhusal gave us for the team project. That separate project brief is not among the files I have access to. Given that, the course requirement column below is built from the syllabus CLOs and PMBOK knowledge areas, which is the part I can verify directly.

The four CLOs: lifecycle management across SDLC models, strategic planning through requirements engineering and feasibility techniques, risk and activity control through planning and estimation, and quality and leadership through controlling deliverables and leading a team. Everything below maps back to one or more of these.

## Process area by process area

### Project Charter

Guidelines say: Trello_Workspace_Design.md specifies a full Charter card with a nine item checklist (authorization, business case, objectives, scope, stakeholders, milestones, budget, PM authority, signatures). GitHub issue T-007 tracks it, assigned to Prizma.

What actually exists: a real Project Charter does exist as a Google Doc (`Project Charter (AMS).gdoc`), not just a stub. It has a genuine Executive Summary, Objectives, Team Roles, a PACT analysis, a SWOT analysis, and a PESTEL style factor analysis. This is real PM work, not nothing.

Where it diverges from reality: three specific mismatches.
1. The Charter states an Expected Completion Date of August 3, 2026. The team's own `01_WEEKLY_ROADMAP.md` and `04_DELIVERABLES_CHECKLIST.md` both target August 25, 2026 as final submission. That is a three week gap between the authorizing document and the operating plan, and nothing in the repo reconciles it.
2. The Charter's Technologies field lists HTML, CSS, JavaScript, React, Node.js, Express, and MySQL. The system actually built and deployed uses Django plus DRF and SQLite, confirmed directly in `backend/config/settings.py` and every commit since day one. The formally authorizing document names a different backend language, framework, and database than what exists in production, and there is no change request anywhere recording that switch.
3. GitHub issue T-007 (Project Charter) is still open. The document backing it is real and done, so this is a tracking gap, not a delivery gap, but it means anyone checking GitHub alone would wrongly conclude the Charter was never written.

Alignment verdict: partially done, real content exists, but not reconciled with the rest of the plan and not closed out in the tracker.

### SRS and Requirements

Guidelines say: `04_DELIVERABLES_CHECKLIST.md` requires an SRS (IEEE 830) by end of Week 1. `Trello_Workspace_Design.md` specifies a full IEEE 830 structure (Introduction, Overall Description, Specific Requirements with FR-01 through FR-12 and NFR-01 through NFR-08, Use Cases, ER Diagram, DFD, Wireframes). GitHub issues T-002 (Requirements Gathering) and T-003 (SRS Document) both exist, assigned to Prizma.

What actually happened: T-002 and T-003 are both still open on GitHub, zero percent complete, roughly two weeks past their Week 1 to 2 deadline as of today. `REALITY_CHECK.md` (the team's own working document) explicitly documents the real database schema, real API endpoints, and real roles, which functions as an informal substitute for a chunk of what a real SRS would cover on the backend side, but it is not a requirements document, it is a code state document written after the fact.

Alignment verdict: not done. This is the clearest, least ambiguous gap in the whole audit. Two required documents, both untouched, both overdue.

### WBS (Work Breakdown Structure)

Guidelines say: no Guidelines document explicitly calls for a hierarchical WBS diagram. The closest proxies are `03_PROJECT_TRACKER.csv` (a flat 42 row task list with dependencies and story points) and the User Story Catalog in `00_COMPLETE_PROJECT_GUIDE_BOOK.md` (15 user stories mapped to sprints).

What actually happened: the task list and user story catalog exist and are reasonably detailed, but neither decomposes deliverables hierarchically the way a WBS is meant to (Level 1 deliverables broken into Level 2 and Level 3 work packages). What exists is a task list, not a WBS.

Alignment verdict: a functional substitute exists, but no team document uses WBS as taught in the course (Ch3, Ch6 in Schwalbe) as its organizing structure. Worth naming explicitly as a gap since Lesson 3 to 5 case studies in the syllabus directly test WBS adjacent concepts (critical path, work packages).

### Scheduling

Guidelines say: `01_WEEKLY_ROADMAP.md` lays out a 7 week, 6 sprint schedule (Week 1 Initiation, Week 2 Sprint 0 Design, Week 3 Sprint 1 Auth, Week 4 Sprint 2 Core Attendance, Week 5 Sprint 3 Face Recognition, Week 6 Sprint 4 Reports, Week 7 Sprint 5 Finalization). `03_PROJECT_TRACKER.csv` has per task start and end dates.

What actually happened: as of today, July 21, we are two days into Week 3 (Sprint 1) by the calendar. The tracker CSV still shows Sprint 1 tasks as "In Progress" and Sprint 2 through 5 as "Not Started," 14 percent complete overall. Reality is close to the opposite on the backend: auth, student and course CRUD, attendance, face recognition with two providers, dashboard analytics, CSV and PDF export, and a live Azure deployment with CI/CD are already built, none of which the tracker reflects. `HANDOFF.md` already flags this and tells readers to trust it over the tracker.

Alignment verdict: badly out of sync, but in an unusual direction. The schedule artifact understates progress rather than overstating it. The real risk this creates is that the schedule can no longer be used for its intended purpose, which is to tell you what is actually left to do and by when, since it has not been updated to reflect three to four sprints worth of work that already shipped early.

### Risk Plan

Guidelines say: a Risk Register table exists in `01_WEEKLY_ROADMAP.md` (5 entries) and a fuller Risk Register template with a worked example (R-003, Face Recognition Accuracy) in `00_COMPLETE_PROJECT_GUIDE_BOOK.md`. `Trello_Workspace_Design.md` specifies a dedicated Risks list with 9 categorized risk cards (R-001 through R-009) and a full checklist per risk (probability, impact, score, trigger, mitigation, contingency, owner, status).

What actually happened: the live Trello board the team actually uses (`Attendance Management System`, 5 lists: Product Backlog, Sprint Planning, To Do, Doing, Done) has no Risks list at all. The one board that did have a Risks list (the abandoned 25 list `AMS` board) had exactly 1 risk card ever created, on day one, never updated again since that board stopped being used after July 8. The two risks the roadmap itself called highest priority, face recognition accuracy and the missing Enrollment table, were both real risks that got resolved through good engineering, but neither resolution is reflected back into any risk register as closed.

Alignment verdict: written once, never operated as a living document. The team correctly identified and mitigated its real risks in practice, it just never tracked that in the artifact meant to hold it.

### Sprint Ceremonies (standup, planning, review, retrospective)

Guidelines say: extremely detailed. `02_MEETING_SCRUM_GUIDE.md` gives full scripts for daily standups, sprint planning, sprint review, and sprint retrospective, including a specific "Sprint 0 Retrospective (Jul 17)" and "Sprint 1 Retrospective (Jul 26)" with named action items marked as implemented. `Trello_Workspace_Design.md` specifies a Meeting Notes list with a Daily Scrum card meant to repeat every day.

What actually happened, checked directly against the real Trello board: the live board has no Meeting Notes list at all, that list only ever existed on the abandoned 25 list board, where it holds exactly 2 cards total, both dated from initial setup, not an ongoing log. A separate board named "Scrum Meeting Planning and All the things about Scrum before updating in main board and other" was created specifically to hold this ceremony, and has never been opened since creation, its last activity timestamp is null. A third board named plainly "Sprint Planning" also has zero lists and null activity. Across all boards, there is no comment thread, card, or artifact anywhere that independently corroborates a standup, planning session, review, or retrospective actually happening, beyond the fact that work clearly got planned and built somehow.

Alignment verdict: the scripted retrospectives in `02_MEETING_SCRUM_GUIDE.md` read as detailed, specific, dated transcripts, which could be mistaken for real minutes. I want to flag that distinction directly rather than let it stand unchallenged: nothing outside that one markdown file supports them having actually happened. Given the same document elsewhere describes itself as team guidance and scripts to use, the honest read is that these are training examples, not records, and the ceremonies they describe have not been running.

### Retrospectives specifically

Same evidence as above. Zero Trello cards logging an actual retrospective outcome anywhere on any of the seven Trello boards checked. No repo file records real retrospective outcomes distinct from the templates. This retrospective document itself (`07_SPRINT_RETROSPECTIVE_AND_FEASIBILITY.md`, written earlier this week) is, as far as I can tell, the first retrospective this project has actually produced from real evidence rather than from a script.

### Stakeholder Management and Communications (bonus, syllabus Lessons 7 and 8)

Guidelines say: `Trello_Workspace_Design.md` specifies a Stakeholders list (Stakeholder Register, Power Interest Grid, Communication Plan) and a Communications Plan checklist. The Project Charter Google Doc actually names real stakeholders (Faculty Supervisor, PM, Frontend Developer, Backend Developer, Teachers, Students, System Administrator).

What actually happened: the stakeholder list in the Charter is real and reasonably complete. No Power Interest Grid or standalone Communication Plan document was found anywhere in the repo or Guidelines folder. `Weekly Tasks/TEAM_SYNC_PROTOCOL.md` functions as an informal communications plan (Discord for daily updates, GitHub for code, Trello for tasks) but was not being followed in practice as of the last Trello check (board stale for three days, zero card comments across 52 cards).

Alignment verdict: partially done. Stakeholder identification happened. The communication plan that was written was not being operated.

## The official tracker sheet, checked against a real previous cohort's sample

This section was added after finding the professor's own resource folder (`Books & Resources`), which contains something more useful than the generic syllabus: his actual Lesson 1 slide notes, and `Sample of Last session_Project.xlsx`, a real completed submission from a previous team in this exact course (a Nepali expense tracker project, team members Ram, Bhim, Bir, Ujjwal, Arav). That sample has 11 tabs: Starting, Agile User Story, User Story Map Board, Agile Release Plan, BDD Scenarios, Sprint 1 through 5 Backlog, Sprint Review Retro, and Status. Every one of those tabs in the sample is filled in with real content, including named, specific retrospective comments per sprint, for example "Ujjwal, BDD was entirely new topic for me, I found it really interesting" and "Risk management for dashain vacation was not done," a real risk that actually materialized.

Our own team's Project Tracker Google Sheet (`1B2m9trSqt1Vl2SHmgeCLXnJxx1nJuS3GUKxXHmV-cKM`, the one `00_COMPLETE_PROJECT_GUIDE_BOOK.md` calls the source for burndown and velocity data) uses the identical tab structure: Sprint Summary, Release Plan, User Stories, Sprint 1 through 5 Backlog, Sprint Review and Retro, BDD Scenarios. I read every one of those tabs directly. Here is what is actually in them, as of today:

Sprint Review and Retro: headers only, plus the sprint name and date range for all 6 sprints. Every other column, What Worked Well, What Didnt Work, Individual Contributions, Action Items, Retro Date, is empty for every single sprint, including Sprint 0, which the tracker elsewhere claims is 100 percent complete. Compare this to the real sample, where every sprint has multiple named, specific comments. This is the clearest evidence in this whole audit that the detailed retrospective scripts in `02_MEETING_SCRUM_GUIDE.md` were never transcribed into the artifact actually meant to hold them, whether or not the conversations behind them happened at all.

BDD Scenarios: contains only the template placeholder row (Feature Name, Scenario description, Given, When, Then, all still in bracket placeholder text, Status "Pending"). Zero real BDD scenarios exist for any of the features that have actually shipped, despite BDD being an explicit deliverable in the professor's own reference sample and in Lesson 1's INVEST criteria (a story must be Testable).

Sprint 1 through 5 Backlog: every task row still shows Status "Not Started" and every Day 1 through Day 5 hour column and the Actual hrs column are empty, for all five sprints, for both Abhishek and Ekata's rows. This is despite auth, CRUD, face recognition, dashboards, exports, and a live deployment all actually existing in the GitHub repo right now. The team's own guide book calls daily hour logging into this exact sheet mandatory ("Every team member must fill their hours in 2 places each day"). It has never happened, not once, for either developer.

Sprint Summary and Release Plan: match the stale `03_PROJECT_TRACKER.csv` exactly, Sprint 0 at 100 percent, Sprints 1 through 5 at 0 percent, all Release Plan rows still marked "Not Started."

Alignment verdict: this is the most unambiguous gap in the entire audit, because it is a direct, tab-for-tab comparison against a real successful precedent from the same course, not an inference from Trello or git. On the actual gradable process artifact the professor's own materials model, the project is at zero percent operational compliance, while the real product is close to done. Fixing this does not require new engineering, it requires going back and filling in six sprints of retrospective notes and hours from memory and from the git log timestamps, which is very doable in one sitting since the actual work already happened, it was just never written down where it needs to be.

## Per person breakdown

### Abhishek (me), Backend Developer

Delivered: functionally, almost the entire technical build. Every one of the 9 closed GitHub issues traces to my work. Auth, RBAC, student and course CRUD, attendance including bulk marking, face recognition with a local dlib path and a second Azure AI Face API path added specifically to work around dlib not building on constrained Azure App Service plans, dashboard analytics, CSV and PDF export, OTP email verification, social sign in, a live CI and CD pipeline on GitLab, and the live Azure deployment itself. I also personally fixed a real regression this week, a test suite that had been failing on GitLab CI since July 20 because a refactor removed a function the tests were still mocking, and confirmed all 73 backend tests pass before promoting anything to main.

Against role requirement: my assigned role per the Charter is backend, database, and authentication. I have covered that and also absorbed most of the frontend build (the original React scaffold traces to Ekata's one push, but the CRUD UX, dashboard layout, and most feature pages since have been mine), plus deployment and DevOps end to end, which were never formally mine alone.

Gap: I have not been closing GitHub issues once work ships (6 dashboard issues remain open despite being done since July 18), and I have been merging my own code without another person reviewing it, which is a real gap against our own Definition of Done.

### Prizma, Project Manager

Delivered: the Project Charter (real, substantive, though not reconciled with the rest of the plan or the actual tech stack), 13 tracked actions on the live Trello board (more than the frontend side), and whatever produced the detailed Guidelines documentation set itself (00 through 07, the meeting guide, the Trello workspace design), which is thorough as written even where it was not operationalized.

Against role requirement: her role per the Charter is project planning, sprint planning, backlog management, documentation, meetings, progress tracking, risk management, and communication. Of those, documentation happened in part (Charter, but not SRS, Requirements, or Team Norms), and I found no evidence any of the ceremonial responsibilities (leading standups, running sprint planning or review, maintaining the risk register, tracking progress against the tracker CSV) were actually operating day to day.

Gap: T-002 (Requirements Gathering), T-003 (SRS), T-008 (Team Norms) are all open, zero percent complete, and overdue against the Week 1 to 2 deadlines the team's own checklist set. The risk register and meeting notes lists are effectively unused. The tracker CSV she owns has not been updated to reflect that the project is running three to four sprints ahead on the technical side.

### Ekata, Frontend Developer

Delivered: one substantial contribution. On July 15 she pushed a full first version of the React frontend to her own branch, `feature/react-frontend`, roughly 30 files and 5,500 lines, covering login, register, dashboard, students, courses, and face recognition pages, styling, an API service layer, and an auth context. This is real, non trivial work, and it is the actual origin of the UI and UX still in use today, even though her authorship does not show in the current project history because that branch was never merged through a pull request.

Against role requirement: her role per the Charter is UI design and frontend development, integrating with backend APIs. The one push covers a meaningful slice of that. A second, smaller commit on July 17 (`Add React frontend structure`) exists on the same unmerged branch, apparently a duplicate or misplaced attempt at the same scaffold.

Gap: since July 17, zero further commits, zero pull requests, zero PR reviews, zero comments anywhere on GitHub. Her only later GitHub activity, a push event on July 20, carried zero new commits, meaning nothing new was added. Her two Trello assigned cards are open. Dashboard UI (issue 1, US-10) and ECA Tracking (issue 23, US-12) remain unbuilt by her, and the dashboard UI that does exist now was built by me, not by her, meaning her assigned scope is being absorbed rather than delivered.

## Findings summary, ranked for action before the next deadline

1. Fill in the actual Project Tracker Google Sheet, the same one the professor's own reference sample shows filled in for a previous cohort. Sprint Review and Retro, BDD Scenarios, and all five Sprint Backlog hour logs are effectively empty right now. This is the single most gradable, most directly comparable gap in the audit, and it is catch-up writing, not new engineering, since the real work already happened.
2. Prizma's two blocking documents, Requirements Gathering and the SRS, are the next biggest gap. They are zero percent done and already overdue.
3. Reconcile the Project Charter against reality on two specific points: the completion date (Charter says August 3, roadmap says August 25) and the tech stack (Charter says Node.js, Express, MySQL, actual system is Django, DRF, SQLite). This is a five minute edit to the Charter doc, not new work, and it closes an obvious inconsistency an instructor would catch immediately.
4. Get Ekata committing again. Her one push is the real origin of the current UI, she should get credit for it by having that branch actually merged through a PR, and she needs to pick up Dashboard UI and ECA Tracking herself rather than have them continue being absorbed into the backend developer's work.
5. Start actually running one real ceremony a week, even briefly, and log it in the tracker sheet itself, not just Trello or this file.
6. Close the paper trail gaps that make the project look worse than it is: 6 dashboard GitHub issues that are done but not closed, T-007 (Charter) not closed despite the Charter being real, and the tracker CSV and Sprint Summary tab still showing 14 percent complete when the backend is closer to sprint 5 level maturity.
7. Update or retire the risk register. The two risks the team flagged as highest priority at the start were both real and both got resolved through actual engineering decisions, that is a good outcome worth recording as closed, not leaving the register looking abandoned.
