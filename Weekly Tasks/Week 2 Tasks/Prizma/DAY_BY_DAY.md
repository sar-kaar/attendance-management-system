# Week 2 (Jul 13–19) — Sprint 1: Dashboard Features
## Prizma Subedi — Project Manager

**Updated plan based on Google Sheets analysis (Jul 10).** 10 new user stories (US-06 to US-15) were discovered from existing Google Sheets. These represent dashboard/analytics features already expected by stakeholders. Sprint 1 now prioritized around implementing these.

**New GitHub Issues:** #17-#26 on `sar-kaar/attendance-management-system`
**New Trello cards:** Cards 86-95 in Product Backlog

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 7 (Mon, Jul 13) — SRS Update + Backlog Reprioritization
- [ ] Update SRS to include new FRs (FR-12 to FR-21) from Google Sheets analysis
- [ ] Move high-priority dashboard stories (US-06, US-07, US-09, US-10, US-15) from Backlog → Sprint 1
- [ ] Assign: Abhishek — dashboard APIs; Ekata — dashboard frontend pages

```bash
git checkout -b docs/srs-update develop
git add docs/SRS.md
git commit -m "[docs] Add dashboard analytics requirements from Google Sheets"
git push origin docs/srs-update
```

---

### Day 8 (Tue, Jul 14) — Project Charter Update + Stakeholder Communication
- [ ] Update Project Charter: note Google Sheets dashboards exist and define expected features
- [ ] Update Stakeholder Register if needed
- [ ] Post in Discord: "Dashboard features identified from existing Google Sheets — 10 new user stories created. See Issues #17-#26."

```bash
git checkout -b docs/project-charter develop
git add docs/project-charter.md
git commit -m "[docs] Update project charter with dashboard feature findings"
git push origin docs/project-charter
```

---

### Day 9 (Wed, Jul 15) — Risk Register + Quality Plan
- [ ] Add new risks: dashboard scope from sheets, API performance with aggregation queries
- [ ] Quality plan: API must return paginated results, dashboard endpoints should respond <1s
- [ ] Move remaining lower-priority stories (US-11, US-12, US-14) to later sprint if needed

```bash
git checkout -b docs/risk-register develop
git add docs/risk-register.md docs/quality-plan.md
git commit -m "[docs] Add dashboard scope risks and API quality plan"
git push origin docs/risk-register
```

---

### Day 10 (Thu, Jul 16) — Sprint Tracking
- [ ] Track progress: check Abhishek's dashboard API branches, Ekata's frontend pages
- [ ] Update Trello Sprint Backlog with daily status
- [ ] Prepare Sprint Review agenda: demo dashboard features

```bash
git checkout -b docs/sprint-1-plan develop
git add docs/sprint-1-plan.md
git commit -m "[docs] Track Sprint 1 dashboard feature progress"
git push origin docs/sprint-1-plan
```

---

### Day 11 (Fri, Jul 17) — Sprint Review & Retro
- [ ] Demo: Dashboard search, attendance stats, at-risk, faculty perf, latecomers, enrollment API
- [ ] Run retro (start/stop/continue)
- [ ] Merge all branches

```bash
git checkout develop
git merge docs/srs-update
git merge docs/project-charter
git merge docs/risk-register
git merge docs/sprint-1-plan
git push origin develop
```

### Day 12–13 (Sat–Sun) — Sprint 2 Planning
- [ ] Review remaining backlog stories (US-11, US-12, US-14, plus existing unstarted T-cards)
- [ ] Sprint goal: "Complete remaining dashboard features + face recognition integration"
- [ ] Move next sprint stories into Sprint Backlog
