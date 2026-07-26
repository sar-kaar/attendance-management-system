# Trello Workspace Design Document
## Attendance Management System — CSE 405 Software Project Management

---

# 1. WORKSPACE

### Workspace Name
`CSE405 — Attendance Management System`

### Workspace Description
Enterprise-grade Agile workspace for the Attendance Management System project. This workspace houses all project boards, documentation, and artifacts required for CSE 405 — Software Project Management. The workspace follows Agile Scrum methodology integrated with PMBOK best practices. It supports a 3-member team through full SDLC from initiation to project closure.

### Workspace Visibility
**Private** — Only invited members can access. Prevents unauthorized viewing of academic project artifacts.

### Workspace Settings
| Setting | Value |
|---------|-------|
| Team Members | 3 (PM, Backend Dev, Frontend Dev) |
| Board Creation | Admins only |
| Invitation Permissions | Admins only |
| Organization Type | University Course Project |
| Default Permission Level | Private |
| Tags | `cse405`, `attendance-system`, `university-project` |

### Recommended Power-Ups
| Power-Up | Purpose |
|----------|---------|
| **Custom Fields** | Add Story Points, Priority, Hours, Status metadata to every card |
| **Calendar** | View sprint timelines, due dates, and milestones |
| **Card Repeater** | Automate recurring checklist items (Daily Scrum, weekly reports) |
| **Google Drive** | Link SRS, project charter, and documentation directly |
| **Butler** | Automate rule-based card movements, assignments, and notifications |
| **Time Tracking (Toggl)** | Track actual hours vs estimated hours per task |
| **Voting** | Allow team to vote on backlog priority |
| **Dashboard** | Generate burndown charts, velocity tracking, sprint progress |
| **GitHub** | Link pull requests and commits directly to Trello cards |
| **Slack** | Get real-time notifications on task updates |
| **Unito** | Sync with GitHub issues for two-way traceability |
| **Planyview** | Gantt chart and timeline visualization |

### Recommended Integrations
| Integration | Purpose |
|-------------|---------|
| **GitHub** | Link PRs, commits, and issues to Trello cards for traceability |
| **Google Workspace** | Store documents (SRS, reports, presentations) |
| **Slack / Discord** | Real-time notifications |
| **Toggl / Harvest** | Time tracking per task |
| **Zapier** | Cross-platform automation (e.g., form submissions → Trello cards) |

### Recommended Automation (Butler)
(See Section 10 for full Butler automation rules)

### Recommended Custom Fields
| Field Name | Type | Values |
|------------|------|--------|
| `Priority` | Dropdown | Critical, High, Medium, Low |
| `Story Points` | Number | 1, 2, 3, 5, 8, 13 |
| `Estimated Hours` | Number | — |
| `Actual Hours` | Number | — |
| `Sprint` | Dropdown | Sprint 0, Sprint 1, ..., Sprint 5 |
| `Status` | Dropdown | Not Started, In Progress, Review, Done |
| `Risk Level` | Dropdown | Low, Medium, High, Critical |
| `Role` | Dropdown | PM, Backend, Frontend, Shared |

---

# 2. BOARD

### Board Name
`Attendance Management System — CSE 405`

### Board Description
**Purpose:** Single-source-of-truth board for managing all aspects of the Attendance Management System project. Follows Agile Scrum with PMBOK-aligned project management practices.

**Scope:**
- Product vision → Requirements → Backlog → Sprints → Closure
- Documentation lifecycle (SRS → Reports → Final Submission)
- Risk tracking, issue tracking, change management
- Meeting minutes and stakeholder communication

### Board Background Suggestion
**Color:** Professional dark blue (#043395 → #122634 gradient)  
**Why:** Dark backgrounds reduce eye strain during long sprint planning sessions and give a professional enterprise feel.

### Board Visibility
**Private** — Only the 3 team members and course instructor (as observer).

### Purpose
To provide complete end-to-end visibility of the Attendance Management System project. Every artifact — from the initial project charter to the final deployment guide — is tracked in this board.

### Expected Workflow
```
Ideas & Research
    ↓
Product Vision → Project Charter
    ↓
Requirements & Stakeholders
    ↓
Product Backlog (Prioritized User Stories)
    ↓
Sprint Planning → Sprint Backlog → To Do
    ↓
In Progress ← (Daily Scrum updates)
    ↓
Code Review ← (Peer review)
    ↓
Testing ← (QA verification)
    ↓
Ready for Demo → Done
    ↓
Documentation & Project Reports
    ↓
Completed Sprints → Project Closure
```

---

# 3. LABELS

## Color Convention
- **Red** = Urgent / Blocking / Critical
- **Orange** = Medium priority
- **Yellow** = Low priority / Waiting
- **Green** = Completed / Ready
- **Blue** = Technical (Backend/DB)
- **Purple** = Frontend/UI
- **Pink** = Testing/QA
- **Sky** = Documentation
- **Lime** = Enhancement/Feature
- **Black** = Research

## Complete Label Set

| Label | Color | Hex | Purpose | Usage Example |
|-------|-------|-----|---------|---------------|
| `Priority: Critical` | Red | `#EB5A46` | Blocking issue, must resolve immediately | Server outage, data loss bug |
| `Priority: High` | Orange | `#FF9F1C` | Important but not blocking | Missing feature for sprint goal |
| `Priority: Medium` | Yellow | `#F5DD29` | Normal priority | Standard feature work |
| `Priority: Low` | Green | `#61BD4F` | Nice-to-have | Future enhancement |
| `Bug` | Red | `#EB5A46` | Defect in the system | Login button not working |
| `Feature` | Lime | `#51E898` | New functionality | Add biometric login |
| `Enhancement` | Lime | `#51E898` | Improvement to existing | Optimize query speed |
| `Research` | Black | `#4D4D4D` | Investigation needed | Research face recognition APIs |
| `Backend` | Blue | `#0079BF` | Backend-related task | Create API endpoint |
| `Frontend` | Purple | `#C377E0` | Frontend-related task | Design login page |
| `Database` | Blue | `#0079BF` | Database task | Design schema |
| `Testing` | Pink | `#FF78CB` | Testing activity | Write unit tests |
| `Documentation` | Sky | `#00C2E0` | Documentation task | Write SRS |
| `Review` | Green | `#61BD4F` | Pending review | Code review needed |
| `Blocked` | Red | `#EB5A46` | Blocked by dependency | Waiting for API |
| `Done` | Green | `#61BD4F` | Completed | Task is finished |
| `Urgent` | Red | `#EB5A46` | Immediate attention | Server down |
| `Low Priority` | Yellow | `#F5DD29` | Deprioritized | Nice-to-have feature |
| `High Priority` | Orange | `#FF9F1C` | Important | Sprint commitment |
| `Critical` | Red-dark | `#B04632` | System-critical | Data integrity issue |
| `Frontend: UI/UX` | Purple | `#C377E0` | UI/UX task | Responsive design |
| `Frontend: Testing` | Pink | `#FF78CB` | Frontend testing | Cross-browser test |
| `API` | Blue-dark | `#055A8C` | API work | REST endpoint |
| `Auth` | Blue-dark | `#055A8C` | Authentication | Login/OAuth |
| `Sprint Goal` | Lime | `#51E898` | Sprint commitment | Must-deliver item |
| `PM Task` | Sky | `#00C2E0` | PM responsibility | Stakeholder meeting |
| `Risk` | Red | `#EB5A46` | Risk item | Identified risk |
| `Change Request` | Orange | `#FF9F1C` | Change request | Scope change |
| `Meeting` | Black | `#4D4D4D` | Meeting notes | Daily Scrum notes |

---

# 4. LISTS

The board uses a **phase-gate** approach where cards flow left-to-right through the SDLC.

### List 1: 📋 Project Resources
**Purpose:** Central repository of all project reference materials, templates, and guidelines. Every team member starts here.
**Cards:** Project brief, templates, university guidelines, reference links, useful tools, glossary

### List 2: 💡 Ideas & Research
**Purpose:** Capture raw ideas, research findings, and exploration notes. Not yet committed to backlog.
**Cards:** Technology research, competitor analysis, feasibility studies

### List 3: 🎯 Product Vision
**Purpose:** Define and communicate the overall product vision statement.
**Cards:** Vision Statement, Elevator Pitch, Target Audience, Success Metrics

### List 4: 📄 Project Charter
**Purpose:** PMBOK-aligned formal authorization of the project.
**Cards:** Project Charter, Scope Statement, Business Case, Stakeholder Register

### List 5: 👥 Stakeholders
**Purpose:** Identify and manage all stakeholders.
**Cards:** Stakeholder Register, Stakeholder Analysis, Communication Plan

### List 6: 📝 Requirements
**Purpose:** All requirements artifacts live here.
**Cards:** Functional Requirements, Non-Functional Requirements, User Stories, Use Cases, Actors, Acceptance Criteria, Business Rules, Assumptions, Dependencies, Constraints

### List 7: 📦 Product Backlog
**Purpose:** Prioritized list of all features, enhancements, and fixes.
**Cards:** Each user story as a card with priority, story points, and acceptance criteria

### List 8: 📅 Sprint Planning
**Purpose:** Sprint planning artifacts and sprint backlogs.
**Cards:** Sprint 1, Sprint 2, Sprint 3, Sprint 4, Sprint 5, Sprint 6, Sprint Goal, Sprint Plan, Sprint Backlog

### List 9: 🏃 Sprint Backlog
**Purpose:** Work committed for the current sprint.
**Cards:** Selected user stories for the active sprint

### List 10: 📋 To Do
**Purpose:** Tasks ready to be worked on, fully refined.
**Cards:** Individual developer tasks broken down from stories

### List 11: 🔨 In Progress
**Purpose:** Work actively being done.
**Cards:** Tasks with assigned developer, started work

### List 12: 👀 Code Review
**Purpose:** Peer review before merging.
**Cards:** Completed code awaiting review

### List 13: 🧪 Testing
**Purpose:** QA verification.
**Cards:** Features undergoing testing (unit, integration, UAT)

### List 14: 🚫 Blocked
**Purpose:** Tasks that cannot proceed.
**Cards:** Blocked items with reason and dependency noted

### List 15: ✅ Ready for Demo
**Purpose:** Completed work ready for sprint review demonstration.
**Cards:** Verified features awaiting demo

### List 16: ✔️ Done
**Purpose:** Completed and accepted work.
**Cards:** All finished tasks, features, and documentation

### List 17: 📚 Documentation
**Purpose:** All project documentation artifacts.
**Cards:** SRS, Project Charter, Risk Register, Communication Plan, Quality Plan, Meeting Minutes, Final Report, Presentation, Deployment Guide, User Manual, Developer Guide, Testing Report, API Documentation, Database Documentation, Sprint Reports

### List 18: 📓 Meeting Notes
**Purpose:** All meeting minutes and action items.
**Cards:** Kickoff Meeting, Daily Scrum (by date), Sprint Planning (by sprint), Sprint Review (by sprint), Sprint Retrospective (by sprint), Stakeholder Meeting, Instructor Meeting

### List 19: ⚠️ Risks
**Purpose:** Risk register for the project.
**Cards:** Technical Risks, Schedule Risks, Resource Risks, External Risks

### List 20: 🐛 Issues
**Purpose:** Track project issues and impediments.
**Cards:** Active issues with severity, status, resolution plan

### List 21: 🔄 Change Requests
**Purpose:** Manage scope changes formally.
**Cards:** Change requests with impact analysis, approval status

### List 22: 📊 Project Reports
**Purpose:** Periodic project status reports and metrics.
**Cards:** Weekly Status Reports, Sprint Reports, Velocity Chart, Burndown Chart, Quality Metrics

### List 23: 🏁 Completed Sprints
**Purpose:** Archive of completed sprint artifacts.
**Cards:** Sprint Results (one per completed sprint)

### List 24: 🎬 Project Closure
**Purpose:** Project closing artifacts.
**Cards:** Closing Report, Lessons Learned, Final Delivery Checklist, Project Handover

### List 25: 🗄️ Archive
**Purpose:** Store inactive/old cards for reference.
**Cards:** Obsolete tasks, completed research, deprecated docs

---

# 5. CARDS

Below is the complete card inventory for every list.

### LIST: 📋 Project Resources

#### Card 1: Project Brief
- **Description:** One-page summary of the Attendance Management System project including objectives, scope, team, and timeline.
- **Objectives:** Provide a quick reference for anyone joining the project.
- **Checklist:**
  - [ ] Project title and course code
  - [ ] Team member names and roles
  - [ ] Project objectives (bullet points)
  - [ ] High-level scope
  - [ ] Technology stack (proposed)
  - [ ] Sprint timeline (6 sprints)
- **Attachments Needed:** Course syllabus, assignment brief
- **Responsible Role:** Project Manager
- **Priority:** High
- **Estimated Hours:** 2
- **Story Points:** 1
- **Dependencies:** None
- **Definition of Done:** Approved by all team members
- **Acceptance Criteria:** Contains all checklist items
- **Due Date Recommendation:** Sprint 0, Day 1
- **Risk Level:** Low
- **Labels:** Documentation, PM Task
- **Custom Fields:** Priority: High, Role: PM
- **Comments Template:** `@PM Please review and approve the project brief.`

#### Card 2: Technology Stack Reference
- **Description:** Document the chosen technologies: frontend framework, backend framework, database, hosting, APIs.
- **Objectives:** Standardize technology choices across the team.
- **Checklist:**
  - [ ] Frontend framework (React/Angular/Vue)
  - [ ] Backend framework (Django/Flask/Express/.NET)
  - [ ] Database (PostgreSQL/SQLite/MongoDB/Firebase)
  - [ ] Hosting/platform
  - [ ] Version control (GitHub)
  - [ ] Testing tools
  - [ ] CI/CD pipeline
- **Attachments Needed:** Research notes
- **Responsible Role:** Backend Developer + Frontend Developer
- **Priority:** High
- **Estimated Hours:** 3
- **Story Points:** 2
- **Dependencies:** Project Brief
- **Labels:** Backend, Frontend, Documentation
- **Custom Fields:** Priority: High, Role: Shared

#### Card 3: Team Norms & Guidelines
- **Description:** Define team working agreements — communication channels, meeting times, code review expectations, definition of ready/done.
- **Objectives:** Establish team culture and expectations.
- **Checklist:**
  - [ ] Communication channels (WhatsApp/Discord/Slack)
  - [ ] Daily standup time
  - [ ] Code review process
  - [ ] Branch naming convention
  - [ ] Commit message format
  - [ ] Definition of Ready
  - [ ] Definition of Done
  - [ ] Meeting attendance policy
- **Responsible Role:** Project Manager
- **Priority:** Medium
- **Estimated Hours:** 1
- **Story Points:** 1
- **Labels:** Documentation, PM Task
- **Custom Fields:** Priority: Medium, Role: PM

#### Card 4: Useful Links & References
- **Description:** Curated list of learning resources, documentation links, API references, and tool guides.
- **Checklist:**
  - [ ] Framework official docs
  - [ ] Database docs
  - [ ] Trello guides
  - [ ] Scrum guide links
  - [ ] University submission portal
- **Responsible Role:** All members
- **Labels:** Documentation
- **Custom Fields:** Priority: Low, Role: Shared

---

### LIST: 💡 Ideas & Research

#### Card 1: Technology Research — Face Recognition APIs
- **Description:** Research available face recognition APIs (OpenCV, Azure Face API, AWS Rekognition, etc.). Compare features, pricing, accuracy, and ease of integration.
- **Objectives:** Determine the best facial recognition approach for attendance marking.
- **Checklist:**
  - [ ] Research OpenCV + dlib
  - [ ] Research Azure Face API
  - [ ] Research AWS Rekognition
  - [ ] Research Face++ / alternative APIs
  - [ ] Compare accuracy metrics
  - [ ] Compare pricing
  - [ ] Compare integration complexity
  - [ ] Make recommendation with justification
- **Attachments Needed:** API documentation links, comparison table
- **Responsible Role:** Backend Developer
- **Priority:** High
- **Estimated Hours:** 6
- **Story Points:** 3
- **Dependencies:** None
- **Definition of Done:** Recommendation documented with pros/cons
- **Labels:** Research, Backend
- **Custom Fields:** Priority: High, Role: Backend

#### Card 2: Competitor Analysis
- **Description:** Analyze existing attendance management solutions (e.g., Keka, Zoho People, GreytHR, in-house university systems). Identify gaps and opportunities.
- **Checklist:**
  - [ ] List direct competitors
  - [ ] Analyze features
  - [ ] Identify gaps
  - [ ] Note unique selling points for our system
  - [ ] Document findings
- **Responsible Role:** Project Manager
- **Priority:** Medium
- **Estimated Hours:** 4
- **Story Points:** 2
- **Labels:** Research, Documentation
- **Custom Fields:** Priority: Medium, Role: PM

#### Card 3: UI/UX Design Exploration
- **Description:** Explore design inspiration (Dribbble, Behance, Material Design). Collect screenshots, color palettes, and component ideas.
- **Checklist:**
  - [ ] Collect dashboard design references
  - [ ] Collect login/signup design references
  - [ ] Design color palette
  - [ ] Design typography system
  - [ ] Create mood board
- **Responsible Role:** Frontend Developer
- **Priority:** Medium
- **Estimated Hours:** 4
- **Story Points:** 2
- **Labels:** Research, Frontend
- **Custom Fields:** Priority: Medium, Role: Frontend

---

### LIST: 🎯 Product Vision

#### Card 1: Product Vision Statement
- **Description:** "For university administrators and faculty who need a reliable way to track student attendance, the Attendance Management System is a web-based application that automates attendance recording, generates insightful reports, and integrates facial recognition for frictionless check-in. Unlike manual spreadsheets, our system provides real-time analytics and role-based access."
- **Checklist:**
  - [ ] Draft vision statement
  - [ ] Review with team
  - [ ] Finalize and pin to list
- **Responsible Role:** Project Manager
- **Priority:** High
- **Labels:** Documentation, PM Task
- **Custom Fields:** Priority: High, Role: PM

#### Card 2: Elevator Pitch
- **Description:** 30-second pitch: "Attendance Management System eliminates manual attendance tracking. Students check in with a single tap — or via facial recognition — and faculty get real-time attendance reports."
- **Responsible Role:** Project Manager
- **Priority:** Medium
- **Labels:** Documentation

#### Card 3: Target Audience
- **Description:** Define primary and secondary user groups.
- **Checklist:**
  - [ ] Primary: University faculty/administrators
  - [ ] Secondary: Students
  - [ ] Tertiary: Department heads, admin staff
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 4: Success Metrics (KPIs)
- **Description:** Define how we measure project success.
- **Checklist:**
  - [ ] 95%+ attendance tracking accuracy
  - [ ] <2s face recognition time
  - [ ] 99.9% uptime
  - [ ] User satisfaction score >4/5
- **Responsible Role:** Project Manager
- **Labels:** Documentation, PM Task

---

### LIST: 📄 Project Charter

#### Card 1: Project Charter
- **Description:** Formal document authorizing the project. Includes project purpose, objectives, scope, key stakeholders, budget, milestone schedule, and PM authority level.
- **Checklist:**
  - [ ] Title and project authorization
  - [ ] Project purpose / business case
  - [ ] Measurable project objectives
  - [ ] High-level scope description
  - [ ] Key stakeholders list
  - [ ] Milestone schedule
  - [ ] Budget estimate
  - [ ] Project manager authority
  - [ ] Approval signatures
- **Attachments Needed:** Signed charter document
- **Responsible Role:** Project Manager
- **Priority:** Critical
- **Estimated Hours:** 4
- **Story Points:** 3
- **Labels:** Documentation, Priority: Critical
- **Custom Fields:** Priority: Critical, Role: PM

#### Card 2: Business Case
- **Description:** Justification for the project. Problems with manual attendance, cost/benefit analysis, ROI.
- **Checklist:**
  - [ ] Problem statement
  - [ ] Analysis of current system (manual)
  - [ ] Proposed solution benefits
  - [ ] Cost-benefit analysis
  - [ ] ROI estimation
- **Responsible Role:** Project Manager
- **Priority:** High
- **Labels:** Documentation

#### Card 3: Scope Statement
- **Description:** Defines what is IN and OUT of scope for the project.
- **Checklist:**
  - [ ] In-scope features
  - [ ] Out-of-scope features
  - [ ] Constraints
  - [ ] Assumptions
- **Responsible Role:** Project Manager
- **Priority:** High
- **Labels:** Documentation

---

### LIST: 👥 Stakeholders

#### Card 1: Stakeholder Register
- **Description:** List all stakeholders with name, role, influence level, interest level, communication needs.
- **Checklist:**
  - [ ] Course Instructor
  - [ ] Team Members (3)
  - [ ] University IT Department
  - [ ] Students (end users)
  - [ ] Faculty (end users)
- **Responsible Role:** Project Manager
- **Priority:** High
- **Labels:** Documentation, PM Task

#### Card 2: Stakeholder Analysis (Power/Interest Grid)
- **Description:** Map stakeholders on power/interest grid to determine engagement strategy.
- **Checklist:**
  - [ ] Create power/interest matrix
  - [ ] Classify each stakeholder
  - [ ] Define engagement strategy per quadrant
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 3: Communication Plan
- **Description:** Who gets what information, how often, through which channel.
- **Checklist:**
  - [ ] Define communication matrix
  - [ ] Set meeting schedule
  - [ ] Define reporting cadence
  - [ ] Establish escalation path
- **Responsible Role:** Project Manager
- **Priority:** High
- **Labels:** Documentation, PM Task

---

### LIST: 📝 Requirements

#### Card 1: Functional Requirements
- **Description:** List of functional requirements organized by module.
- **Checklist:**
  - [ ] FR-01: User Registration & Login (Admin, Faculty, Student)
  - [ ] FR-02: Role-based Access Control (RBAC)
  - [ ] FR-03: Add/Edit/Delete Student Records
  - [ ] FR-04: Add/Edit/Delete Course Records
  - [ ] FR-05: Mark Attendance (Manual entry)
  - [ ] FR-06: Mark Attendance (Facial Recognition)
  - [ ] FR-07: View Attendance Reports
  - [ ] FR-08: Export Attendance to CSV/PDF
  - [ ] FR-09: Dashboard with Visual Analytics
  - [ ] FR-10: Email/SMS Notifications
  - [ ] FR-11: Attendance Modification Requests
  - [ ] FR-12: Audit Log for Changes
- **Responsible Role:** All members
- **Priority:** Critical
- **Estimated Hours:** 6
- **Story Points:** 5
- **Labels:** Documentation, Priority: Critical
- **Custom Fields:** Priority: Critical, Role: Shared

#### Card 2: Non-Functional Requirements
- **Description:** Performance, security, usability, and reliability requirements.
- **Checklist:**
  - [ ] NFR-01: Response time <2 seconds
  - [ ] NFR-02: 99.9% uptime
  - [ ] NFR-03: Support 500+ concurrent users
  - [ ] NFR-04: Encrypted data storage (AES-256)
  - [ ] NFR-05: HTTPS/TLS for all communications
  - [ ] NFR-06: Cross-browser compatibility
  - [ ] NFR-07: Mobile-responsive design
  - [ ] NFR-08: Backup and recovery
- **Responsible Role:** All members
- **Priority:** High
- **Labels:** Documentation

#### Card 3: User Stories
- **Description:** Complete set of user stories in "As a [role], I want [feature] so that [benefit]" format.
- **Checklist:**
  - [ ] US-01: As an admin, I want to add new students so that they can be registered in the system.
  - [ ] US-02: As a faculty member, I want to mark attendance quickly so that I save time.
  - [ ] US-03: As a faculty member, I want to use facial recognition for attendance so that it's contactless.
  - [ ] US-04: As a student, I want to view my attendance record so that I know my status.
  - [ ] US-05: As an admin, I want to generate attendance reports so that I can monitor trends.
  - [ ] US-06: As a faculty member, I want to edit attendance so that I can correct errors.
  - [ ] US-07: As a student, I want to receive notifications when attendance is marked.
  - [ ] US-08: As an admin, I want role-based access so that data is secure.
  - [ ] US-09: As a faculty member, I want to export attendance reports to CSV/PDF.
  - [ ] US-10: As an admin, I want an audit log so that I can track changes.
- **Responsible Role:** All members
- **Priority:** Critical
- **Labels:** Documentation

#### Card 4: Use Cases
- **Description:** UML use case descriptions for key system interactions.
- **Checklist:**
  - [ ] UC-01: Login
  - [ ] UC-02: Register Student
  - [ ] UC-03: Mark Attendance (Manual)
  - [ ] UC-04: Mark Attendance (Face Recognition)
  - [ ] UC-05: View Attendance Report
  - [ ] UC-06: Export Report
  - [ ] UC-07: Manage Users
  - [ ] UC-08: Manage Courses
- **Responsible Role:** Backend Developer
- **Labels:** Documentation, Backend

#### Card 5: Actors
- **Description:** Define all system actors.
- **Checklist:**
  - [ ] Admin (system administrator)
  - [ ] Faculty (instructor/teacher)
  - [ ] Student
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 6: Acceptance Criteria
- **Description:** Detailed acceptance criteria for each user story.
- **Checklist:**
  - [ ] US-01 AC: Admin can add student with name, email, ID, course
  - [ ] US-02 AC: Faculty can mark attendance in <3 clicks
  - [ ] ... (expand for all stories)
- **Responsible Role:** All members
- **Labels:** Documentation

#### Card 7: Business Rules
- **Description:** Business logic rules.
- **Checklist:**
  - [ ] BR-01: Only faculty can mark attendance
  - [ ] BR-02: Attendance can only be marked within class time ± 15 min
  - [ ] BR-03: Students need 75% attendance to be eligible for exams
  - [ ] BR-04: Attendance records are immutable after 24 hours (audit trail)
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 8: Assumptions
- **Description:** Assumptions made during planning.
- **Checklist:**
  - [ ] Stable internet connectivity
  - [ ] Faculty have smartphones/laptops
  - [ ] Students have registered photos for face recognition
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 9: Dependencies
- **Description:** External dependencies.
- **Checklist:**
  - [ ] Face recognition library availability
  - [ ] University database access (if needed)
  - [ ] Hosting platform availability
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 10: Constraints
- **Description:** Project constraints.
- **Checklist:**
  - [ ] Must be completed within semester (16 weeks)
  - [ ] Team of 3 members
  - [ ] Open-source technologies preferred
- **Responsible Role:** Project Manager
- **Labels:** Documentation

---

### LIST: 📦 Product Backlog

#### Individual User Story Cards (one per story)
Each user story from the Requirements list becomes a card in the Product Backlog with:

- **Description:** Full user story text
- **Acceptance Criteria:** Bullet points
- **Priority:** Critical / High / Medium / Low
- **Story Points:** 1, 2, 3, 5, 8, or 13
- **Labels:** Feature, Backend/Frontend
- **Custom Fields:** Priority, Story Points, Sprint
- **Checklist:**
  - [ ] Refined by team
  - [ ] Estimated
  - [ ] Acceptance criteria defined
  - [ ] Dependencies identified

Sample backlog cards:
| Card | Story Points | Priority |
|------|-------------|----------|
| US-01: Admin adds students | 3 | High |
| US-02: Faculty marks attendance (manual) | 5 | Critical |
| US-03: Facial recognition attendance | 13 | High |
| US-04: Student views attendance | 3 | Medium |
| US-05: Generate attendance reports | 8 | High |
| US-06: Edit attendance | 5 | Medium |
| US-07: Email/SMS notifications | 3 | Low |
| US-08: Role-based access control | 5 | Critical |
| US-09: Export to CSV/PDF | 3 | Medium |
| US-10: Audit log | 5 | Low |

---

### LIST: 📅 Sprint Planning

#### Card 1: Sprint 1
- **Description:** Sprint 1 — Foundation & Authentication. Duration: 2 weeks.
- **Checklist:**
  - [ ] Sprint Goal defined
  - [ ] Stories committed
  - [ ] Tasks broken down
  - [ ] Effort estimated
  - [ ] Team capacity confirmed
- **Responsible Role:** Project Manager
- **Labels:** Feature, Sprint Goal

#### Card 2: Sprint 2
- **Description:** Sprint 2 — Core Attendance Features.
- **(same checklist structure)**

#### Card 3: Sprint 3
- **Description:** Sprint 3 — Face Recognition Integration.

#### Card 4: Sprint 4
- **Description:** Sprint 4 — Reports & Dashboard.

#### Card 5: Sprint 5
- **Description:** Sprint 5 — Testing, Bug Fixes & Deployment.

#### Card 6: Sprint 6
- **Description:** Sprint 6 — Project Closure & Documentation.

#### Card 7: Sprint Goal (Current Sprint)
- **Description:** The specific goal for the active sprint.
- **Checklist:**
  - [ ] Goal communicated to team
  - [ ] Stories aligned with goal
- **Responsible Role:** Project Manager
- **Labels:** Sprint Goal

#### Card 8: Sprint Plan (Current Sprint)
- **Description:** Detailed plan for the current sprint including stories, tasks, assignments, and capacity.
- **Checklist:**
  - [ ] Sprint backlog finalized
  - [ ] Task breakdown complete
  - [ ] Assignments made
  - [ ] Capacity plan verified
- **Responsible Role:** Project Manager

---

### LIST: 🏃 Sprint Backlog

**Cards:** User stories selected for the current sprint, with:
- Broken-down tasks as checklists
- Developer assignments
- Story points
- Acceptance criteria

#### Sample Sprint 1 Backlog Cards:

**Card: US-08 — Role-based Access Control**
- **Assigned To:** Backend Developer
- **Story Points:** 5
- **Description:** As an admin, I want role-based access so that data is secure.
- **Checklist:**
  - [ ] Design user roles (Admin, Faculty, Student)
  - [ ] Create User model with role field
  - [ ] Implement JWT authentication
  - [ ] Create middleware for role verification
  - [ ] Write tests for RBAC
  - [ ] Documentation
- **Acceptance Criteria:**
  - Admin can access all routes
  - Faculty cannot access admin routes
  - Student can only access own data
- **Labels:** Backend, Feature, Priority: Critical

**Card: US-01 — Admin Adds Students**
- **Assigned To:** Backend Developer (API) + Frontend Developer (UI)
- **Story Points:** 3
- **Checklist:**
  - [ ] Create Student model (Backend)
  - [ ] Create CRUD API endpoints (Backend)
  - [ ] Create student registration form (Frontend)
  - [ ] Form validation (Frontend)
  - [ ] Display student list (Frontend)
  - [ ] End-to-end test
- **Labels:** Backend, Frontend, Feature

---

### LIST: 📋 To Do → 🔨 In Progress → 👀 Code Review → 🧪 Testing → 🚫 Blocked → ✅ Ready for Demo → ✔️ Done

These six lists form the **development pipeline**. Cards move left-to-right through:
1. **To Do** — Tasks refined, estimated, and ready for development
2. **In Progress** — Developer actively working
3. **Code Review** — Pull request created, awaiting peer review
4. **Testing** — Code merged, under QA verification
5. **Blocked** — Cannot proceed (note blocker reason)
6. **Ready for Demo** — Verified, awaiting sprint demo
7. **Done** — Demo accepted, work complete

Each card in these lists follows the **Card Template** (see Section 14: Best Practices).

---

### LIST: 📚 Documentation

#### Card 1: SRS (Software Requirements Specification)
- **Description:** Complete SRS document per IEEE 830 standard.
- **Checklist:**
  - [ ] Cover Page
  - [ ] Table of Contents
  - [ ] 1. Introduction
    - [ ] 1.1 Purpose
    - [ ] 1.2 Scope
    - [ ] 1.3 Definitions & Acronyms
    - [ ] 1.4 References
    - [ ] 1.5 Overview
  - [ ] 2. Overall Description
    - [ ] 2.1 Product Perspective
    - [ ] 2.2 Product Functions
    - [ ] 2.3 User Characteristics
    - [ ] 2.4 Constraints
    - [ ] 2.5 Assumptions & Dependencies
  - [ ] 3. Specific Requirements
    - [ ] 3.1 Functional Requirements (FR-01 to FR-12)
    - [ ] 3.2 Non-Functional Requirements (NFR-01 to NFR-08)
    - [ ] 3.3 External Interface Requirements
  - [ ] 4. Use Cases (UC-01 to UC-08)
  - [ ] 5. ER Diagram
  - [ ] 6. DFD (Level 0, 1)
  - [ ] 7. Wireframes / Mockups
  - [ ] 8. References
- **Responsible Role:** All members (PM leads)
- **Priority:** Critical
- **Estimated Hours:** 20
- **Story Points:** 13
- **Labels:** Documentation, Priority: Critical
- **Custom Fields:** Priority: Critical, Role: Shared
- **Due Date:** End of Sprint 2

#### Card 2: Project Charter (Formal)
- **Checklist:**
  - [ ] Cover page
  - [ ] Project title and authorization
  - [ ] Business case summary
  - [ ] Project objectives
  - [ ] Scope statement
  - [ ] Milestone schedule
  - [ ] Budget
  - [ ] Stakeholder list
  - [ ] PM authority
  - [ ] Approval signatures
- **Responsible Role:** Project Manager
- **Priority:** Critical
- **Labels:** Documentation

#### Card 3: Risk Register
- **Checklist:**
  - [ ] Risk ID
  - [ ] Risk description
  - [ ] Probability (1-5)
  - [ ] Impact (1-5)
  - [ ] Risk score (P x I)
  - [ ] Risk category (Technical/Schedule/Resource/External)
  - [ ] Mitigation strategy
  - [ ] Contingency plan
  - [ ] Owner
  - [ ] Status
  - [ ] Review date
- **Responsible Role:** Project Manager
- **Priority:** High
- **Estimated Hours:** 4
- **Story Points:** 3
- **Labels:** Documentation, Risk

#### Card 4: Communication Plan
- **Checklist:**
  - [ ] Stakeholder name
  - [ ] Information needs
  - [ ] Delivery method
  - [ ] Frequency
  - [ ] Responsible person
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 5: Quality Plan
- **Checklist:**
  - [ ] Quality objectives
  - [ ] Standards (ISO 9126, IEEE)
  - [ ] Review process
  - [ ] Testing strategy
  - [ ] Metrics (defect density, test coverage)
- **Responsible Role:** Project Manager
- **Labels:** Documentation

#### Card 6: Meeting Minutes (Master Card)
- **Description:** Template and logs for all meeting minutes.
- **Checklist:**
  - [ ] Date, time, location
  - [ ] Attendees
  - [ ] Agenda
  - [ ] Discussion points
  - [ ] Decisions made
  - [ ] Action items (with owner and due date)
  - [ ] Next meeting date
- **Responsible Role:** Project Manager
- **Labels:** Documentation, Meeting

#### Card 7: Final Report
- **Checklist:**
  - [ ] Executive summary
  - [ ] Project overview
  - [ ] Methodology (Agile Scrum)
  - [ ] Sprint summaries (all 6)
  - [ ] Technical architecture
  - [ ] Testing summary
  - [ ] Challenges and lessons learned
  - [ ] Conclusion
- **Responsible Role:** All members
- **Priority:** Critical
- **Labels:** Documentation

#### Card 8: Presentation
- **Checklist:**
  - [ ] Title slide
  - [ ] Problem statement
  - [ ] Solution overview
  - [ ] Architecture
  - [ ] Demo screenshots
  - [ ] Sprint summary
  - [ ] Lessons learned
  - [ ] Q&A
- **Responsible Role:** All members
- **Priority:** High
- **Labels:** Documentation

#### Card 9: Deployment Guide
- **Checklist:**
  - [ ] Prerequisites
  - [ ] Environment setup
  - [ ] Installation steps
  - [ ] Configuration
  - [ ] Deployment to production
  - [ ] Verification steps
- **Responsible Role:** Backend Developer
- **Labels:** Documentation, Backend

#### Card 10: User Manual
- **Checklist:**
  - [ ] Introduction
  - [ ] Getting started
  - [ ] Admin guide
  - [ ] Faculty guide
  - [ ] Student guide
  - [ ] Troubleshooting
- **Responsible Role:** Frontend Developer
- **Labels:** Documentation, Frontend

#### Card 11: Developer Guide
- **Checklist:**
  - [ ] Architecture overview
  - [ ] Setup instructions
  - [ ] Code conventions
  - [ ] API documentation
  - [ ] Database schema
  - [ ] Testing guide
- **Responsible Role:** Backend Developer
- **Labels:** Documentation, Backend

#### Card 12: Testing Report
- **Checklist:**
  - [ ] Test plan
  - [ ] Test cases (unit, integration, system, UAT)
  - [ ] Test results
  - [ ] Defect report
  - [ ] Coverage report
- **Responsible Role:** Frontend Developer
- **Labels:** Documentation, Testing

#### Card 13: API Documentation
- **Checklist:**
  - [ ] API overview
  - [ ] Authentication endpoints
  - [ ] Student endpoints
  - [ ] Attendance endpoints
  - [ ] Report endpoints
  - [ ] Error codes
- **Responsible Role:** Backend Developer
- **Labels:** Documentation, Backend, API

#### Card 14: Database Documentation
- **Checklist:**
  - [ ] ER Diagram
  - [ ] Table definitions
  - [ ] Indexes
  - [ ] Relationships
  - [ ] Backup strategy
- **Responsible Role:** Backend Developer
- **Labels:** Documentation, Backend, Database

---

### LIST: 📓 Meeting Notes

#### Card 1: Kickoff Meeting
- **Checklist:**
  - [ ] Introductions
  - [ ] Project overview
  - [ ] Roles and responsibilities
  - [ ] Tools setup (GitHub, Trello)
  - [ ] Sprint 0 planning
  - [ ] Action items
- **Responsible Role:** Project Manager

#### Card 2: Daily Scrum — [Date] (repeating card)
- **Checklist:**
  - [ ] What did I do yesterday?
  - [ ] What will I do today?
  - [ ] What blockers do I have?
  - [ ] Updates to board
- **Responsible Role:** All members (rotate note-taking)
- **Note:** Use Card Repeater Power-Up to auto-create daily

#### Card 3: Sprint Planning — Sprint [N]
- **Checklist:**
  - [ ] Review product backlog
  - [ ] Set sprint goal
  - [ ] Select stories for sprint
  - [ ] Break down into tasks
  - [ ] Estimate effort
  - [ ] Assign tasks
  - [ ] Confirm capacity
- **Responsible Role:** Project Manager

#### Card 4: Sprint Review — Sprint [N]
- **Checklist:**
  - [ ] Demo completed work
  - [ ] Stakeholder feedback
  - [ ] Update product backlog
  - [ ] Review Definition of Done
- **Responsible Role:** All members

#### Card 5: Sprint Retrospective — Sprint [N]
- **Checklist:**
  - [ ] What went well?
  - [ ] What could improve?
  - [ ] Action items for next sprint
  - [ ] Start/Stop/Continue
- **Responsible Role:** All members

#### Card 6: Stakeholder / Instructor Meeting
- **Checklist:**
  - [ ] Progress update
  - [ ] Demo
  - [ ] Feedback collection
  - [ ] Action items
- **Responsible Role:** Project Manager

---

### LIST: ⚠️ Risks

#### Card 1: Technical Risks
- **Checklist:**
  - [ ] R-001: Facial recognition accuracy <90% → Mitigation: Use multiple models
  - [ ] R-002: Database performance issues → Mitigation: Index and optimize queries
  - [ ] R-003: Integration difficulties with face API → Mitigation: Fallback to manual mode

#### Card 2: Schedule Risks
- **Checklist:**
  - [ ] R-004: Sprint delays → Mitigation: Buffer days in schedule
  - [ ] R-005: Team member unavailability → Mitigation: Cross-train tasks

#### Card 3: Resource Risks
- **Checklist:**
  - [ ] R-006: Limited hosting budget → Mitigation: Use free tier (Heroku/Railway)
  - [ ] R-007: No prior face recognition experience → Mitigation: Allocate learning time in Sprint 0

#### Card 4: External Risks
- **Checklist:**
  - [ ] R-008: API deprecation → Mitigation: Abstract API layer
  - [ ] R-009: Changes in university policy → Mitigation: Flexible architecture

---

### LIST: 🐛 Issues

#### Card: Active Issue Template
- **Description:** Track each issue with severity and resolution.
- **Checklist:**
  - [ ] Issue ID
  - [ ] Description
  - [ ] Severity (Critical/Major/Minor)
  - [ ] Reported by
  - [ ] Date reported
  - [ ] Root cause
  - [ ] Resolution plan
  - [ ] ETA
  - [ ] Status (Open/In Progress/Resolved/Closed)

---

### LIST: 🔄 Change Requests

#### Card: Change Request Template
- **Checklist:**
  - [ ] CR ID
  - [ ] Requester
  - [ ] Date
  - [ ] Description of change
  - [ ] Justification
  - [ ] Impact analysis (scope, schedule, cost)
  - [ ] Approval status (Pending/Approved/Rejected)
  - [ ] Implementation plan
  - [ ] Verified

---

### LIST: 📊 Project Reports

#### Card 1: Weekly Status Report — Week [N]
- **Checklist:**
  - [ ] Progress summary
  - [ ] Completed tasks
  - [ ] In-progress tasks
  - [ ] Upcoming tasks
  - [ ] Risks/issues
  - [ ] Planned vs actual

#### Card 2: Sprint Report — Sprint [N]
- **Checklist:**
  - [ ] Sprint goal
  - [ ] Stories completed / total
  - [ ] Velocity (story points)
  - [ ] Burndown chart
  - [ ] Key achievements
  - [ ] Improvement areas

#### Card 3: Velocity Chart
- **Checklist:**
  - [ ] Track story points per sprint
  - [ ] Calculate average velocity
  - [ ] Use for capacity planning

#### Card 4: Burndown Chart (per sprint)
- **Checklist:**
  - [ ] Day 0: Total effort remaining
  - [ ] Daily updates
  - [ ] Compare actual vs ideal burndown

#### Card 5: Quality Metrics
- **Checklist:**
  - [ ] Test coverage %
  - [ ] Defect count (by severity)
  - [ ] Pass/fail ratio
  - [ ] Performance benchmarks

---

### LIST: 🏁 Completed Sprints

#### Card: Sprint [N] Results
- **Description:** Archive card with all sprint artifacts.
- **Checklist:**
  - [ ] Sprint goal
  - [ ] Completed stories
  - [ ] Incomplete stories (carried over)
  - [ ] Velocity
  - [ ] Burndown chart
  - [ ] Review notes
  - [ ] Retrospective outcomes
- **Labels:** Done

---

### LIST: 🎬 Project Closure

#### Card 1: Project Closing Report
- **Checklist:**
  - [ ] Project summary
  - [ ] Final deliverables
  - [ ] Lessons learned
  - [ ] Recommendations

#### Card 2: Lessons Learned
- **Checklist:**
  - [ ] What went well
  - [ ] What went wrong
  - [ ] What would we do differently
  - [ ] Advice for future teams

#### Card 3: Final Delivery Checklist
- **Checklist:**
  - [ ] SRS submitted
  - [ ] Project charter submitted
  - [ ] All reports submitted
  - [ ] Presentation ready
  - [ ] Source code on GitHub
  - [ ] Deployment live (if applicable)
  - [ ] User manual submitted

#### Card 4: Project Handover
- **Checklist:**
  - [ ] GitHub repository transferred
  - [ ] Trello board archived
  - [ ] Documentation packaged
  - [ ] Credentials handed over

---

### LIST: 🗄️ Archive

**Cards:** Any card from any list that is no longer active. Move here for historical reference.

---

# 6. EVERY CARD TEMPLATE

Below is the standard template used for every task card in the development pipeline:

```
## Description
[Clear description of the task]

## Objectives
- Objective 1
- Objective 2

## Checklist
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Attachments Needed
- [List of files/docs to attach]

## Assignment
- **Responsible Role:** [PM / Backend / Frontend / Shared]
- **Priority:** [Critical / High / Medium / Low]
- **Risk Level:** [Low / Medium / High / Critical]

## Estimates
- **Estimated Hours:** [X]
- **Story Points:** [X]
- **Sprint:** [Sprint N]

## Dependencies
- Depends on: [Card name]

## Definition of Done
- [ ] Code written
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Demo-ready

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Due Date
- **Target:** [Date]

## Labels
[Label1, Label2]

## Custom Fields
- Priority: [X]
- Story Points: [X]
- Role: [X]
- Status: [Not Started / In Progress / Review / Done]

## Comments
- [Date]: [Comment by Member]
```

---

# 7. CHECKLISTS — DETAILED

## SRS Checklist (expanded)
```
□ Cover Page
□ Table of Contents
□ 1. Introduction
  □ 1.1 Purpose
  □ 1.2 Scope
  □ 1.3 Definitions, Acronyms, Abbreviations
  □ 1.4 References
  □ 1.5 Overview
□ 2. Overall Description
  □ 2.1 Product Perspective
  □ 2.2 Product Functions
  □ 2.3 User Characteristics
  □ 2.4 Constraints
  □ 2.5 Assumptions & Dependencies
  □ 2.6 Apportioning of Requirements
□ 3. Specific Requirements
  □ 3.1 External Interface Requirements
    □ 3.1.1 User Interfaces
    □ 3.1.2 Hardware Interfaces
    □ 3.1.3 Software Interfaces
    □ 3.1.4 Communication Interfaces
  □ 3.2 Functional Requirements
    □ FR-01 through FR-12
  □ 3.3 Non-Functional Requirements
    □ NFR-01 through NFR-08
□ 4. Use Case Descriptions
  □ UC-01 through UC-08
□ 5. Data Models
  □ ER Diagram
  □ Class Diagram
□ 6. Process Models
  □ DFD Level 0
  □ DFD Level 1
□ 7. System Architecture
  □ Architecture Diagram
  □ Technology Stack
□ 8. User Interface Design
  □ Wireframes
  □ Mockups
□ 9. References
□ 10. Appendices
□ Final review and sign-off
```

## Project Charter Checklist (expanded)
```
□ Document title and project name
□ Project authorization section
□ Business case summary
□ Project purpose / justification
□ Measurable project objectives
□ High-level requirements
□ Project boundaries (scope)
□ Key deliverables
□ Milestone schedule
  □ Sprint 0: Setup complete
  □ Sprint 1: Auth system complete
  □ Sprint 2: Core attendance features
  □ Sprint 3: Face recognition
  □ Sprint 4: Reports & dashboard
  □ Sprint 5: Testing & deployment
  □ Sprint 6: Closure & documentation
□ Budget estimate
□ Stakeholder list
□ Team structure
□ Project manager authority level
□ Assumptions and constraints
□ Approval signatures
□ Version history table
```

## Risk Register Checklist
```
□ Risk ID (R-001 to R-009)
□ Risk description for each
□ Probability rating (1-5)
□ Impact rating (1-5)
□ Risk score (P × I)
□ Risk category
□ Trigger conditions
□ Mitigation strategy
□ Contingency plan
□ Risk owner
□ Status (Open/Mitigated/Closed)
□ Review date
□ Last updated
```

## Communication Plan Checklist
```
□ Stakeholder name and role
□ Information to communicate
□ Communication method (email, meeting, Trello)
□ Frequency (daily, weekly, milestone)
□ Format (status report, dashboard, verbal)
□ Responsible party
□ Escalation path
□ Feedback mechanism
```

## Sprint Planning Meeting Checklist
```
□ Review product backlog (prioritized)
□ Confirm sprint goal
□ Select stories for sprint
□ Break stories into tasks
□ Estimate tasks (hours)
□ Calculate team capacity
□ Assign task owners
□ Update Trello board
□ Review Definition of Ready
□ Confirm meeting schedule for sprint
  □ Daily standup time
  □ Review date
  □ Retrospective date
□ Capture action items
```

## Sprint Retrospective Checklist
```
□ Set the stage (review sprint goal)
□ Gather data
  □ What went well?
  □ What could be improved?
  □ What was surprising?
□ Generate insights
  □ Root cause analysis
  □ Pattern recognition
□ Decide what to do
  □ Top 3 action items
  □ Owner for each
□ Close
  □ Thank team
  □ Update Trello
```

## Daily Scrum Checklist
```
□ What did I complete yesterday?
□ What am I working on today?
□ Any blockers/impediments?
□ Any updates needed on Trello cards?
□ Any help needed from teammates?
```

## Deployment Guide Checklist
```
□ Prerequisites listed
□ System requirements documented
□ Step 1: Clone repository
□ Step 2: Install dependencies
□ Step 3: Configure environment variables
□ Step 4: Set up database
□ Step 5: Run migrations
□ Step 6: Start application
□ Step 7: Verify installation
□ Production deployment steps
□ Rollback procedure
□ Monitoring setup
□ Troubleshooting guide
```

## User Manual Checklist
```
□ Introduction to the system
□ System requirements
□ Login / Registration guide
□ Admin user guide
  □ Dashboard overview
  □ Manage students
  □ Manage courses
  □ View reports
□ Faculty user guide
  □ Mark attendance (manual)
  □ Mark attendance (face recognition)
  □ View/edit attendance
  □ Export reports
□ Student user guide
  □ View attendance
  □ Profile management
□ Troubleshooting
□ FAQ
□ Contact / Support
```

## Developer Guide Checklist
```
□ Architecture overview
□ Technology stack
□ Local development setup
□ Code structure / directory layout
□ Coding conventions
  □ Naming conventions
  □ File organization
  □ Comment style
□ API documentation
  □ Endpoint list
  □ Request/response examples
  □ Authentication
□ Database schema
  □ Entity relationships
  □ Migration guide
□ Testing guide
  □ Running tests
  □ Writing tests
  □ Coverage reports
□ CI/CD pipeline
□ Deployment process
□ Contribution guidelines
```

## Final Report Checklist
```
□ Executive Summary
□ 1. Introduction
  □ 1.1 Background
  □ 1.2 Objectives
  □ 1.3 Scope
□ 2. Project Management
  □ 2.1 Methodology (Agile Scrum)
  □ 2.2 Team structure
  □ 2.3 Tools used (Trello, GitHub)
  □ 2.4 Sprint summary
    □ Sprint 0: Setup
    □ Sprint 1: Foundation & Auth
    □ Sprint 2: Core attendance
    □ Sprint 3: Face recognition
    □ Sprint 4: Reports & Dashboard
    □ Sprint 5: Testing & Deployment
    □ Sprint 6: Closure
□ 3. System Architecture
  □ 3.1 Architecture diagram
  □ 3.2 Technology stack
  □ 3.3 Database design
  □ 3.4 API design
□ 4. Feature Implementation
  □ 4.1 User management
  □ 4.2 Attendance tracking
  □ 4.3 Face recognition
  □ 4.4 Reports & analytics
□ 5. Testing
  □ 5.1 Test strategy
  □ 5.2 Test results
  □ 5.3 Defect analysis
□ 6. Challenges & Lessons Learned
□ 7. Conclusion & Future Work
□ 8. References
□ Appendices
```

---

# 8. SCRUM WORKFLOW

## How the Trello Board is Used Daily

### Sprint Planning (First day of each sprint)
1. **PM** moves to `Sprint Planning` list and creates a Sprint [N] card
2. **Team** reviews `Product Backlog`, selects stories for the sprint
3. **PM** creates `Sprint Goal` card with the commitment
4. **Team** breaks stories into tasks, moves them to `Sprint Backlog`
5. **PM** updates Custom Fields: Sprint, Priority, Story Points
6. **Result:** `Sprint Backlog` is populated with committed cards

### Daily Scrum (Every day, 15 min)
1. **Team** gathers (physical or virtual)
2. Each member answers the 3 Daily Scrum questions
3. **PM** updates the `Daily Scrum — [Date]` card with notes
4. **Team** updates card positions on the board (move cards as status changes)
5. **PM** checks for blocked items in `🚫 Blocked` list
6. **Result:** Board reflects current state of work

### Task Assignment
1. Cards in `To Do` are assigned to a member (via "Members" field)
2. Developer moves card to `In Progress` when starting work
3. Developer updates progress via checklist items
4. Labels and custom fields indicate priority and type

### Progress Tracking
1. **Visual:** Board shows cards flowing left → right
2. **Quantitative:** Burndown chart (Dashboard Power-Up)
3. **Qualitative:** Daily Scrum updates
4. **Velocity:** Tracked per sprint in `Velocity Chart` card

### Sprint Review (Last day of sprint)
1. **Team** moves completed cards from `Ready for Demo` to `Done`
2. **Team** demos completed work
3. **PM** captures feedback in `Sprint Review — Sprint [N]` card
4. **PM** updates product backlog based on feedback
5. **Result:** Stakeholders see working software

### Sprint Retrospective (After review)
1. **Team** holds retrospective (Start/Stop/Continue format)
2. **PM** documents in `Sprint Retrospective — Sprint [N]` card
3. **Team** identifies top 3 action items
4. **PM** adds action items to next sprint's planning
5. **Result:** Continuous improvement

### Definition of Ready (DoR) — A card must have:
- [ ] Clear description
- [ ] Acceptance criteria defined
- [ ] Story points estimated
- [ ] Dependencies identified
- [ ] Priority assigned
- [ ] Labels applied

### Definition of Done (DoD) — A card must meet:
- [ ] Code implemented and merged
- [ ] Code reviewed by peer
- [ ] Unit tests passing
- [ ] Integration tests passed (if applicable)
- [ ] UI matches design spec (Frontend)
- [ ] API documented (Backend)
- [ ] No critical/high bugs
- [ ] Demo-ready

### Velocity Tracking
- Sum of story points completed per sprint
- Recorded in `Velocity Chart` card
- Used for capacity planning in future sprints
- Recalculate after 2-3 sprints for accuracy

### Burndown Tracking
- Update remaining work hours daily
- Dashboard Power-Up visualizes burndown
- Compare actual vs ideal burndown line
- If above ideal line → team is behind → adjust scope

### Issue Tracking
- All bugs captured in `Issues` list
- Each issue card has severity, status, and resolution
- Critical issues are moved to top of backlog
- Linked to related development cards

### Risk Tracking
- Risk register reviewed weekly by PM
- Risk status updated in `Risks` list
- High-scoring risks (P × I > 15) get mitigation cards
- New risks added as discovered

### Change Tracking
- Any scope change goes through `Change Requests` list
- Impact analysis documented on card
- Only approved changes move to backlog
- PM communicates approved changes to stakeholders

### Documentation Tracking
- Documentation cards move through the same workflow as code
- SRS, reports, guides are tracked with checklists
- Documentation is reviewed alongside code
- All docs attached to cards for version control

---

# 9. MEMBER ASSIGNMENT

## Assignment Matrix

| Card Type | Owner | Reviewer |
|-----------|-------|----------|
| Project Charter | PM | All |
| SRS | All (PM leads) | All |
| Risk Register | PM | All |
| Communication Plan | PM | All |
| Quality Plan | PM | All |
| Meeting Minutes | PM (rotating note-taker) | All |
| Weekly Status Reports | PM | All |
| Sprint Planning | PM | All |
| Sprint Review | All | PM |
| Sprint Retrospective | All | PM |
| Stakeholder Management | PM | All |
| Change Requests | PM | All |
| Final Report | All (PM leads) | All |
| Presentation | All | All |

| User Authentication API | Backend Dev | Frontend Dev |
| Student CRUD API | Backend Dev | PM |
| Attendance CRUD API | Backend Dev | PM |
| Face Recognition Logic | Backend Dev | Frontend Dev |
| Reports API | Backend Dev | Frontend Dev |
| Database Schema Design | Backend Dev | PM |
| Deployment Setup | Backend Dev | Frontend Dev |
| API Documentation | Backend Dev | PM |
| Database Documentation | Backend Dev | PM |
| Developer Guide | Backend Dev | PM |

| Login/Register UI | Frontend Dev | Backend Dev |
| Dashboard UI | Frontend Dev | PM |
| Student Management UI | Frontend Dev | Backend Dev |
| Attendance UI | Frontend Dev | Backend Dev |
| Face Recognition UI | Frontend Dev | Backend Dev |
| Reports UI | Frontend Dev | Backend Dev |
| User Manual | Frontend Dev | PM |
| UI/UX Design | Frontend Dev | All |
| Testing (Unit/Integration) | Frontend Dev | Backend Dev |
| Testing Report | Frontend Dev | PM |

| Product Backlog Refinement | Shared | — |
| Daily Scrum | Shared | — |
| Code Review | Shared | — |
| Architecture Decisions | Shared | — |
| Technology Research | Shared | — |
| Bug Fixing | Shared | — |

---

# 10. BUTLER AUTOMATION

## 20+ Automation Rules

### Card Movement Automations
1. **When a card moves to `In Progress`** → Set custom field "Status" to "In Progress" and set due date to +7 days
2. **When a card is moved to `Code Review`** → Add label "Review" and assign to the other developer (not the creator)
3. **When a card is moved to `Testing`** → Remove label "Review", add label "Testing", assign to Frontend Dev (tester)
4. **When a card moves to `Blocked`** → Add label "Blocked", add comment: "🚫 This card is blocked. Please describe the blocker in the comments.", notify @PM
5. **When a card moves to `Ready for Demo`** → Add label "Done", sort list by priority
6. **When a card moves to `Done`** → Mark checklist complete, set custom field "Status" to "Done", archive card after 7 days

### Checklist Automations
7. **When all checklist items are complete** → Move card to `Code Review`, add comment: "✅ All checklist items complete. Ready for review."
8. **When a checklist item is checked** → Log timestamp in card description
9. **When a checklist is 50% complete** → Add label "In Progress" if not already present
10. **When a checklist is 100% complete** → Remove "In Progress" label, add "Review" label

### Due Date Automations
11. **When a card's due date arrives** → Notify all members of the card: "⏰ Due date reached for [card name]"
12. **When a card is overdue by 1 day** → Add label "Urgent", notify @PM
13. **When a card is overdue by 3 days** → Move to top of its list, add comment: "⚠️ Overdue by 3 days — needs attention"
14. **When a due date is set** → Sort list by due date ascending

### Label Automations
15. **When label "Critical" is added** → Notify @PM and all members: "🚨 Critical item: [card name]"
16. **When label "Blocked" is removed** → Add comment: "Blocker resolved. Ready to proceed."
17. **When label "Bug" is added** → Move card to top of `Product Backlog`, add label "High Priority"
18. **When label "Documentation" is added** → Add checklist item: "Team review required"

### Assignment Automations
19. **When a card is assigned to Backend Dev** → Add label "Backend"
20. **When a card is assigned to Frontend Dev** → Add label "Frontend"
21. **When a card is assigned to PM** → Add label "PM Task"
22. **When a member is added to a card** → Add comment: "👤 [member] has been assigned to this card."

### Recurring Card Automations
23. **Every day at 9:00 AM (Mon-Fri)** → Create card `Daily Scrum — [date]` in `Meeting Notes` list with checklist template
24. **Every Friday at 5:00 PM** → Create card `Weekly Status Report — Week [N]` in `Project Reports` list
25. **At the end of each sprint** → Move all `Done` cards to `Completed Sprints`, create `Sprint [N+1]` card in `Sprint Planning`

### Board Maintenance
26. **When a card has been in `Done` for 14 days** → Archive the card
27. **When a card has been in `Ideas & Research` for 30 days** → Add comment: "This idea has been sitting for 30 days. Move to backlog or archive?"
28. **Weekly on Sunday** → Sort `Product Backlog` by priority (Critical → High → Medium → Low)

### Notification Automations
29. **When a comment is added** → Notify all members of the card
30. **When a card is created in `Risks`** → Notify @PM: "New risk identified: [card name]"

---

# 11. POWER-UPS — DETAILED

| Power-Up | Why It's Essential | Free/Paid |
|----------|-------------------|-----------|
| **Custom Fields** | Add structured metadata (Priority, Story Points, Hours, Sprint) to every card. Essential for filtering, sorting, and reporting. | Free |
| **Calendar** | View sprint deadlines, due dates, and milestones on a calendar. See what's due this week at a glance. | Free |
| **Butler** | Automate card movements, assignments, label changes, and recurring cards. Saves hours of manual board management. | Free (limited) |
| **Card Repeater** | Auto-create Daily Scrum, Weekly Status Report, and recurring meeting cards on schedule. | Free |
| **Google Drive** | Attach and preview Google Docs (SRS, reports) directly on cards. Keeps docs and tasks together. | Free |
| **GitHub** | Link Trello cards to GitHub PRs, commits, and branches. Two-way traceability between code and tasks. | Free |
| **Dashboard** | Generate burndown charts, velocity tracking, cumulative flow diagrams. Critical for sprint progress visibility. | Free |
| **Voting** | Team votes on backlog priority. Democratic prioritization for a 3-person team. | Free |
| **Time Tracking (Toggl)** | Track actual hours vs estimated hours. Improves estimation accuracy over time. | Free (basic) |
| **Slack** | Real-time notifications when cards move, comments are added, or due dates approach. | Free |
| **Unito** | Bi-directional sync with GitHub. Issues created in GitHub auto-create Trello cards and vice versa. | Paid (trial) |
| **Planyview** | Gantt chart view of sprint timelines. Useful for PM to visualize dependencies. | Free (basic) |
| **Screenful** | Advanced reporting, dashboards, and portfolio views. Track team productivity over time. | Free (30-day) |

---

# 12. SPRINT PLAN

## Sprint Schedule (16-Week Semester)

| Sprint | Duration | Weeks | Goal | Key Deliverables | Meetings |
|--------|----------|-------|------|-----------------|----------|
| **Sprint 0** | 1 week | Week 1 | Project setup | Trello board, GitHub repo, team norms, technology selection, initial project charter draft | Kickoff meeting |
| **Sprint 1** | 2 weeks | Weeks 2-3 | Foundation & Auth | User authentication (login/register), role-based access, user management, project charter finalized, SRS draft | Sprint Planning, Daily Scrum, Review, Retro |
| **Sprint 2** | 2 weeks | Weeks 4-5 | Core Attendance | Student CRUD, course management, manual attendance marking, attendance list view, SRS v2 | Sprint Planning, Daily Scrum, Review, Retro |
| **Sprint 3** | 3 weeks | Weeks 6-8 | Face Recognition | Face recognition integration, camera capture, face registration, auto-attendance marking, UI for face recognition | Sprint Planning, Daily Scrum, Review, Retro |
| **Sprint 4** | 2 weeks | Weeks 9-10 | Reports & Dashboard | Attendance reports, CSV/PDF export, visual dashboards, charts, admin analytics | Sprint Planning, Daily Scrum, Review, Retro |
| **Sprint 5** | 3 weeks | Weeks 11-13 | Testing & Deployment | Comprehensive testing, bug fixes, deployment to production, performance optimization, user manual | Sprint Planning, Daily Scrum, Review, Retro |
| **Sprint 6** | 3 weeks | Weeks 14-16 | Closure | Final documentation, final report, presentation, lessons learned, project handover, final submission | Final Review, Stakeholder Demo |

## Milestones
| Milestone | Due | Deliverable |
|-----------|-----|-------------|
| M0: Project Setup | End of Week 1 | GitHub repo, Trello board, team norms, tech stack decided |
| M1: Auth System | End of Week 3 | Login/register working, RBAC functional |
| M2: Core Attendance | End of Week 5 | Manual attendance marking + student management |
| M3: Face Recognition | End of Week 8 | Face detection and auto-attendance working |
| M4: Reports & Dashboard | End of Week 10 | Analytics dashboard, export functionality |
| M5: Production Release | End of Week 13 | Deployed system, user manual, testing report |
| M6: Project Closure | End of Week 16 | All documentation, final report, presentation |

## Ceremony Schedule (Per Sprint)
| Ceremony | Day | Duration |
|----------|-----|----------|
| Sprint Planning | Sprint Day 1 | 2 hours |
| Daily Scrum | Every day | 15 min |
| Sprint Review | Last day of sprint | 1 hour |
| Sprint Retrospective | Last day of sprint | 1 hour |
| Backlog Refinement | Mid-sprint (weekly) | 30 min |

---

# 13. PROFESSIONAL IMPROVEMENTS

## Multi-Board vs Single-Board Recommendation

### Recommended: Single-Board Approach
For a **3-person university project**, a single well-organized board is **superior** to multiple boards.

**Reasons:**
1. **Team size**: 3 people means low volume of simultaneous work. One board provides full visibility.
2. **Simplicity**: No switching between boards. Everything in one place.
3. **Context**: Developers see the full picture — requirements, backlog, progress, risks, docs.
4. **Instructor review**: Easy for the instructor to see everything on one board.
5. **Maintenance burden**: Multiple boards require more upkeep than a 3-person team can sustain.

### When to Add Additional Boards
If the project grows or has clear separation, consider:

| Board | When to Use | Audience |
|-------|-------------|----------|
| **Product Backlog Board** | When backlog exceeds 50+ items | PM + Team |
| **Sprint Board** (per sprint) | When using multi-board approach (template → copy per sprint) | Team |
| **Documentation Board** | When documentation volume is very high | All |
| **Testing Board** | When formal QA process is needed | Tester |
| **Risk/Issue Board** | If risk tracking becomes complex | PM |

### Recommendation for this project:
**Start with 1 board** organized with 25 lists.
If Sprint Backlog + To Do + In Progress become crowded (>20 cards), create a separate **Sprint Board** for Sprint 3 onwards.

---

## Additional Improvements

### Card Templates
Create 5 card templates (as "keep in list" cards or in a separate templates list):
1. **User Story Template** — Standard story format
2. **Task Template** — Standard development task
3. **Bug Template** — Bug report format
4. **Meeting Notes Template** — Standard meeting minutes
5. **Documentation Template** — Doc creation checklist

### Color-Coded List Headers
Use emoji prefixes consistently:
- 📋 = Resources
- 💡 = Ideas
- 🎯 = Vision
- 📄 = Charter
- 👥 = Stakeholders
- 📝 = Requirements
- 📦 = Backlog
- 📅 = Planning
- 🏃 = Active sprint
- 🔨 = Work in progress
- 👀 = Review
- 🧪 = Testing
- 🚫 = Blocked
- ✅ = Ready
- ✔️ = Done
- 📚 = Docs
- 📓 = Meetings
- ⚠️ = Risks
- 🐛 = Issues
- 🔄 = Changes
- 📊 = Reports
- 🏁 = Completed
- 🎬 = Closure
- 🗄️ = Archive

### Saved Filters (for quick views)
1. **My Tasks** — Cards assigned to me
2. **Critical Priority** — Cards with Critical priority
3. **Backend Work** — Cards with Backend label
4. **Frontend Work** — Cards with Frontend label
5. **Needs Review** — Cards in Code Review list
6. **Due This Week** — Cards due within 7 days

---

# 14. BEST PRACTICES

## Naming Conventions

### Card Titles
- **User Stories:** `US-NN: Short title` (e.g., `US-01: Admin adds students`)
- **Tasks:** `[Module] — Action` (e.g., `Auth — Implement JWT middleware`)
- **Bugs:** `BUG-NN: Short description` (e.g., `BUG-01: Login fails on empty email`)
- **Documentation:** `[Doc Type]: [Title]` (e.g., `SRS: Attendance Management System`)
- **Meeting Notes:** `[Type] — [Date/Sprint]` (e.g., `Daily Scrum — 2026-07-08`)
- **Sprints:** `Sprint N — [Goal]` (e.g., `Sprint 1 — Foundation & Auth`)

### Checklist Items
- Start with **action verbs**: Create, Implement, Test, Document, Review, Deploy
- Be specific: `Create User model with role field` (not `Work on models`)
- Use consistent prefixes: `FR-01:`, `NFR-02:`, `US-03:`

### Labels
- Use `Category: Specific` format for consistency
- Examples: `Priority: High`, `Frontend: UI/UX`, `Backend: API`

## Card Templates (Use 'Copy Card' for consistency)

### User Story Card
```
Title: [US-NN]: [Title]
Description:
  As a [user role],
  I want [feature/goal]
  so that [benefit].

Acceptance Criteria:
  □ [Criterion 1]
  □ [Criterion 2]

Labels: Feature, [Backend/Frontend]
Priority: [Critical/High/Medium/Low]
Story Points: [1/2/3/5/8/13]
```

### Bug Card
```
Title: BUG-NN: [Short description]
Description:
  Steps to reproduce:
  1. Go to [page]
  2. Click [button]
  3. See error

  Expected: [expected behavior]
  Actual: [actual behavior]

Environment: [Browser/OS]
Severity: [Critical/Major/Minor]
Labels: Bug, [Backend/Frontend]
```

## Documentation Workflow
1. Create documentation card in `Documentation` list
2. Add checklist with SRS sections (or other doc sections)
3. Assign to responsible member(s)
4. Attach Google Doc link (using Google Drive Power-Up)
5. Move to `In Progress` when writing begins
6. Move to `Code Review` when draft is complete (peer review)
7. Move to `Testing` when review is done (verify against requirements)
8. Move to `Done` when approved

## Meeting Workflow
1. PM creates meeting card (use Card Repeater for recurring)
2. Checklist items = agenda
3. During meeting, members comment with updates
4. After meeting, PM updates action items with owners
5. Move to `Done` when minutes are finalized

## Sprint Workflow
1. **Sprint Planning Day:**
   - PM creates Sprint [N] card
   - Team selects backlog items
   - Stories moved to Sprint Backlog
   - Tasks broken out
2. **During Sprint:**
   - Daily standup (check board)
   - Cards flow left → right
   - Blockers handled immediately
3. **Sprint End:**
   - Review: Demo cards in Ready for Demo
   - Retro: Document lessons
   - Move completed to Done → Completed Sprints
   - Unfinished work back to Product Backlog

## Risk Management
1. Maintain Risk Register in `Risks` list
2. Review at every Sprint Planning
3. High risk items get mitigation cards in the sprint
4. PM updates risk status weekly
5. Use P × I scoring: >15 = critical, 8-14 = high, <8 = medium

## Communication
1. **Daily:** 15-min standup, update Trello board
2. **Weekly:** PM sends status report (card in Project Reports)
3. **Bi-weekly:** Sprint review with demo
4. **Ad-hoc:** Comments on relevant cards
5. **Instructor:** Forward sprint reports and board link

## Version Control Integration (GitHub)
1. Create branch with Trello card ID: `feature/US-01-add-students`
2. Commit messages reference cards: `[US-01] Add student CRUD endpoints`
3. PR descriptions link to Trello: `Closes #card-id`
4. GitHub Power-Up shows PR status on Trello card
5. When PR merges → move card to `Code Review` → `Testing`

## GitHub + Trello Workflow
1. Backlog → Card in `Sprint Backlog`
2. Developer takes card → moves to `In Progress`
3. Create branch: `feature/US-NN-description`
4. Code, commit, push
5. Create PR → link Trello card
6. Move card to `Code Review`
7. Reviewer approves → merge PR
8. Move card to `Testing`
9. Tests pass → move to `Ready for Demo`
10. Demo accepted → move to `Done`

## Board Maintenance
- **Weekly:** Archive cards in `Done` older than 2 sprints
- **Sprint start:** Clean up `Ideas`, `Research`, `Archive`
- **Monthly:** Review and update labels
- **Sprint end:** Move all completed to `Completed Sprints`
- **PM daily:** Check for stale cards (no movement in 3 days)

---

# APPENDIX: QUICK REFERENCE CARD

## 30-Second Board Tour
```
Left Side (Planning):
  📋 Project Resources → 💡 Ideas → 🎯 Vision → 📄 Charter → 👥 Stakeholders → 📝 Requirements

Middle Left (Backlog):
  📦 Product Backlog → 📅 Sprint Planning → 🏃 Sprint Backlog

Middle (Development Pipeline):
  📋 To Do → 🔨 In Progress → 👀 Code Review → 🧪 Testing → 🚫 Blocked → ✅ Ready → ✔️ Done

Right Side (Management):
  📚 Documentation → 📓 Meeting Notes → ⚠️ Risks → 🐛 Issues → 🔄 Changes

Far Right (Reports & Archive):
  📊 Project Reports → 🏁 Completed Sprints → 🎬 Project Closure → 🗄️ Archive
```

## Daily Routine
| Time | Activity | Who |
|------|----------|-----|
| 9:00 AM | Daily Scrum (15 min) | All |
| 9:15 AM | Update board positions | All |
| 9:30 AM | Start work on To Do items | All |
| 5:00 PM | Update task progress | All |

## Sprint Cadence
| Day | Activity |
|-----|----------|
| Sprint Day 1 | Sprint Planning |
| Days 2-13 | Development + Daily Scrums |
| Sprint Last Day | Sprint Review + Retrospective |

---

*Document prepared for CSE 405 — Software Project Management*
*Attendance Management System — Enterprise Trello Workspace Design*
*July 2026*
