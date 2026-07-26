# Trello Workflow Guide — Daily Operations

## How to Use the Board Every Day

### Your Board: https://trello.com/b/ecB6ppQa/attendance-management-system

**Correction (2026-07-21):** this guide previously linked `tf3ceNmA`, an abandoned practice board that was never actually used. The real board is `ecB6ppQa`, and it runs a simpler 5-list Kanban flow (Product Backlog, Sprint Planning, To Do, Doing, Done), not the 25-list, 4-zone structure this guide documents below. The zone structure below reflects what was originally designed, not what the team is actually using.

---

## 1. Board Structure Overview

Our board has 25 lists divided into 4 zones:

| Zone | Lists | Purpose |
|------|-------|---------|
| **PLANNING** (left side) | Project Resources → Product Backlog | Strategy, documents, backlog |
| **ACTIVE** (middle) | Sprint Planning → Done | Current sprint execution |
| **DOCS** (lower) | Documentation → Project Reports | Reference materials |
| **CLOSURE** (far right) | Completed Sprints → Archive | Historical |

---

## 2. Daily Workflow — Card Movement

```
📦 Product Backlog → 📋 To Do → 🔨 In Progress → 👀 Code Review → 🧪 Testing → ✅ Ready for Demo → ✔️ Done
```

### Step-by-Step:

**Morning (9:00 AM after standup):**
1. Open your board
2. Find your tasks in **To Do** list
3. Drag **ONE** card to **In Progress** (WIP limit: 2 per person max)
4. Update the card description with today's goal

**During the day:**
5. Comment on the card with progress updates
6. When code is ready, move to **Code Review** and @mention your reviewer in a comment

**Code Review process:**
7. Reviewer checks code, adds comments on GitHub PR
8. If approved → move card to **Testing**
9. If changes needed → move back to **In Progress**

**End of day:**
10. Update card comments with what was accomplished
11. If blocked: move to **Blocked** and add blocker description
12. If done: move to **Done** (if reviewed and tested)

---

## 3. Sprint Lifecycle in the Board

### Start of Sprint:
1. PM moves the Sprint card from **Sprint Planning** → **Sprint Backlog**
2. PM pulls user stories from **Product Backlog** → **Sprint Backlog** (as checklist items on sprint card)
3. Team moves individual task cards from **Product Backlog** → **To Do**

### During Sprint:
4. Cards flow left-to-right through the active lists
5. Daily standup happens in front of the board (screen share)

### End of Sprint:
6. PM moves all **Done** cards → **Completed Sprints** list (attached to sprint card)
7. Any unfinished cards go back to **Product Backlog**
8. Sprint card moves from **Sprint Backlog** → **Completed Sprints**
9. PM adds Sprint Review & Retro notes as card comments

---

## 4. When to Use Each List — Detailed

### 📋 Project Resources (READ ONLY)
- Contains: Project brief, tech stack, team norms
- NEVER move cards FROM here. Copy if needed.

### 💡 Ideas & Research
- New feature ideas go here
- When approved → move to Product Backlog

### 🎯 Product Vision (READ ONLY)
- Vision statement, KPIs, target audience
- Never changes during project

### 📄 Project Charter (READ ONLY)
- Formal documents
- Update only when teacher requests changes

### 👥 Stakeholders (READ ONLY)
- Stakeholder register, communication plan
- Update when stakeholders change

### 📝 Requirements (READ ONLY after Sprint 0)
- All requirement artifacts
- Reference only after Sprint 0

### 📦 Product Backlog
- ALL future work lives here
- Prioritized by PM (top = most important)
- PM adds new cards here as requirements emerge
- Each card should have: Description, Priority label, Story Points

### 📅 Sprint Planning
- Sprint goal cards for FUTURE sprints
- Created by PM before sprint planning
- Contains checklist of deliverables for that sprint

### 🏃 Sprint Backlog
- Contains: CURRENT sprint goal card + committed stories
- Only ONE sprint active at a time
- Sprint goal card sits at top of this list

### 📋 To Do
- Tasks for CURRENT sprint, ready to pick up
- PM moves items here from Product Backlog during sprint planning
- Developers pick from top (priority order)

### 🔨 In Progress
- Cards being actively worked on
- **WIP Limit: MAX 2 per person**
- Must have yourself as member on the card

### 👀 Code Review
- Code is complete, waiting for peer review
- Reviewer is assigned as member on card
- **Time limit: Review within 24 hours**
- How to review: GitHub PR review + comments on Trello card

### 🧪 Testing
- Code reviewed, now being tested
- PM or developer tests according to acceptance criteria
- If bug found: move back to In Progress with bug description

### 🚫 Blocked
- Something is preventing progress
- **MUST include comment explaining the blocker**
- PM's job: resolve block within 24 hours
- When unblocked: move back to In Progress

### ✅ Ready for Demo
- Completed, reviewed, tested, waiting for Sprint Review
- PM reviews before demo

### ✔️ Done
- Completed in current sprint
- Moves to Completed Sprints list at sprint end

### 📚 Documentation (READ ONLY)
- All project documents live here
- Updated by PM as documents are finalized

### 📓 Meeting Notes
- PM adds meeting minutes after every meeting
- Include: date, attendees, decisions, action items

### ⚠️ Risks / 🐛 Issues / 🔄 Change Requests
- PM manages these lists
- Team members report risks/issues to PM
- PM logs and tracks resolution

### 📊 Project Reports
- Weekly status reports added by PM
- Teacher can check progress here

### 🏁 Completed Sprints
- Sprint cards from all completed sprints
- Contains sprint goal, deliverables, review & retro notes

### 🎬 Project Closure (Week 7)
- Final deliverables during Week 7
- Moved to Archive after submission

### 🗄️ Archive
- Old cards no longer active
- Historical reference only

---

## 5. Label Usage Guide

| Label | When to Use |
|-------|-------------|
| Priority: Critical | Must do NOW. Sprint goal items |
| Priority: High | Important, do this sprint |
| Priority: Medium | Do if time permits |
| Priority: Low | Nice-to-have |
| Bug | Defect found during testing |
| Feature | New functionality |
| Enhancement | Improve existing feature |
| Research | Investigate before building |
| Backend | Backend code task |
| Frontend | Frontend code task |
| Database | Database schema or query task |
| Testing | Test writing or execution |
| Documentation | Document writing |
| Review | Needs review |
| Blocked | Has a blocker |
| PM Task | PM's administrative task |
| Sprint Goal | Marks the sprint goal card |
| Risk | Risk management item |
| Meeting | Meeting note card |

**Every card should have at least 2 labels:**
1. Priority label (Critical/High/Medium/Low)
2. Domain label (Backend/Frontend/Database/Testing/Documentation)

---

## 6. Card Writing Standards

### Title Format:
```
[Type] Short Description
```
Examples:
- `US-01: User Registration API`
- `Bug: Fix 500 error on login`
- `Research: Face recognition libraries`

### Card Description Template:
```
## Description
[What needs to be done]

## Acceptance Criteria
- [ ] [criteria 1]
- [ ] [criteria 2]

## Technical Notes
[Implementation details if any]

## Definition of Done
- [ ] Code complete
- [ ] Peer reviewed
- [ ] Tested
- [ ] No known bugs
```

---

## 7. WIP Limits (IMPORTANT)

| List | Max Cards | Why |
|------|-----------|-----|
| In Progress | 2 per person | Focus, avoid multitasking |
| Code Review | 3 total | Reviews should be fast |
| Testing | 3 total | Test one at a time |
| To Do | 8 total | Don't overload sprint |

**If a list is full, finish something first before pulling more work.**

---

## 8. Weekly Board Maintenance (PM's Job)

### Every Monday:
- [ ] Archive any cards in Done that are >1 week old
- [ ] Check Product Backlog is prioritized
- [ ] Update any stale card descriptions

### Every Friday (after sprint review):
- [ ] Move sprint cards to Completed Sprints
- [ ] Move unfinished work back to Product Backlog
- [ ] Update sprint report card
- [ ] Clean up labels

### End of Project:
- [ ] All cards moved to Archive or Project Closure
- [ ] Export board as JSON backup
- [ ] Take screenshots for final report

---

## 9. Quick Reference (Cheat Sheet)

```
START YOUR DAY:
1. Standup (9:00 AM)
2. Check Trello
3. Pick 1 task from To Do → In Progress
4. Work on it
5. When done → Code Review
6. Review teammate's code
7. End of day → Update card comments

TRELLO RULES:
- Every card has: Title, Description, Priority Label, Domain Label, Member
- WIP: 2 cards per person IN PROGRESS max
- Blocked? → Move to Blocked list + comment why
- Done? → Must be reviewed AND tested first
- Always comment before moving a card
```

---

## 10. Common Mistakes to Avoid

| Mistake | Correct Way |
|---------|-------------|
| Working on 3+ tasks at once | Stick to 1-2, finish before starting new |
| Not updating card status | Move card when you start/stop working |
| Skipping code review | All code must be reviewed |
| Cards without labels | Always add priority + domain labels |
| Cards without members | Always assign yourself to your cards |
| Forgetting to comment | Comment on card when significant progress |
| Moving cards backward without communication | Before moving back, discuss with team |
