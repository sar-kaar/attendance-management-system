# Week 3 (Jul 20–26) — Sprint 1: Auth
## Prizma Subedi — Project Manager

**Sprint Goal:** frontend connects to the already-working auth API; auth gets tested and secured.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 14 (Mon, Jul 20) — Sprint 1 Kickoff
- [ ] Lead sprint planning: confirm goal is verify + connect, not build from zero
- [ ] Make sure Abhishek and Ekata agree on the login field (username vs email) before either starts coding
- [ ] Update Trello: move Sprint 1 stories to Sprint Backlog

```bash
git checkout -b docs/sprint-1-plan develop
git add docs/sprint-1.md
git commit -m "[docs] Sprint 1 plan"
git push origin docs/sprint-1-plan
```

---

### Day 15–17 (Tue–Thu) — Daily PM Work
Each day:
- [ ] 9 AM standup — note blockers, chase them same day
- [ ] Update Trello card statuses
- [ ] Confirm Abhishek and Ekata are actually talking about the API contract, not assuming
- [ ] Update risk register if anything changes (e.g. CORS origin still needs to be set)

---

### Day 18 (Fri, Jul 24) — Sprint Review Prep
- [ ] Confirm all PRs are merged
- [ ] Prepare demo agenda: register → login → dashboard → token refresh
- [ ] Status report to teacher

---

### Day 19 (Sat, Jul 25) — Sprint Review
- [ ] Run the demo with the teacher
- [ ] Collect feedback, log it

### Day 20 (Sun, Jul 26) — Retro
- [ ] Start-stop-continue
- [ ] Draft Sprint 2 plan: student/course/attendance frontend UI (APIs already exist), Enrollment table decision

```bash
git checkout develop
git merge docs/sprint-1-plan
git push origin develop
```
