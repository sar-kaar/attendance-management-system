# Week 6 (Aug 10–16) — Sprint 4: Reports & Testing
## Ekata Rimal — Frontend

**Sprint Goal:** dashboard with charts, report page with filters, export buttons, full UI polish pass.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 35 (Mon, Aug 10) — Dashboard Page
- [ ] Summary cards + charts hitting Abhishek's new dashboard stats endpoint
- [ ] Pick a charting library that fits your framework (e.g. Recharts for React)

```bash
git checkout -b feature/dashboard-ui develop
git add frontend/src/pages/Dashboard.*
git commit -m "[US-11] Add dashboard with charts"
git push origin feature/dashboard-ui
```

---

### Day 36 (Tue, Aug 11) — Report Page with Filters
- [ ] Filter by course, student, date range, hitting `/api/attendance/report/`
- [ ] Show totals and percentage clearly

```bash
git checkout -b feature/report-page develop
git add frontend/src/pages/Report.*
git commit -m "[US-09] Add attendance report page with filters"
git push origin feature/report-page
```

---

### Day 37 (Wed, Aug 12) — Export Buttons
- [ ] CSV and PDF download buttons on the report page, hitting Abhishek's export endpoints
- [ ] Trigger a real file download, not just open in a new tab

```bash
git add frontend/src/pages/Report.*
git commit -m "[US-10] Add CSV/PDF export buttons"
git push origin feature/report-page
```

---

### Day 38 (Thu, Aug 13) — UI Polish Pass
- [ ] Consistent loading states, error states, empty states across every page built so far
- [ ] Responsive check on mobile widths for the main flows (login, dashboard, attendance marking)

```bash
git add frontend/src/
git commit -m "[chore] UI polish: loading, error, empty states, responsive fixes"
git push origin feature/dashboard-ui
```

---

### Day 39 (Fri, Aug 14) — Integration & Review
- [ ] PR all branches into `develop`
- [ ] Full click-through test of every page built to date

```bash
git checkout develop
git merge feature/dashboard-ui
git merge feature/report-page
git push origin develop
```

### Day 40 (Sat, Aug 15) — Sprint Review & Retro
- [ ] Demo dashboard, reports, exports
- [ ] Start user manual draft — screenshot every page now while it's fresh
