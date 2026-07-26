# Week 2 (Jul 13–19) — Sprint 1: Dashboard Frontend + API Integration
## Ekata Rimal — Frontend

**Updated plan based on Google Sheets analysis (Jul 10).** Existing Google Sheets dashboards (SUM I Dashboard, Testing Dashboard, Student Master Dashboard) define the dashboard layout. Backend will implement dashboard APIs this week. Frontend focus: React scaffold + dashboard pages matching the sheet layouts.

**Reference dashboards** (read-only links from Composio):
- SUM I 2026: https://docs.google.com/spreadsheets/d/14cQTeuRuA6GQB73f3Wzh4mnqsZFwzr2Fcr_8DnzaYCQ
- Testing: https://docs.google.com/spreadsheets/d/1H3tESuWBB9cyPLivJH4yidrnfnd_ptPotieFjN3RGCw
- Student Master: https://docs.google.com/spreadsheets/d/1AMui6udlHjt09hoNuCSL1VRXiVxBJ9XM0NbtEuFOZMs

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 7 (Mon, Jul 13) — Framework Decision + React Scaffold
**Before you start:** talk to Prizma and Abhishek before picking. Abhishek's CORS is already locked to localhost:3000.

- [ ] Decide React + Vite + MUI (consistent with existing plan and CORS config)
- [ ] `npm create vite@latest frontend -- --template react`
- [ ] Install: `@mui/material @emotion/react @emotion/styled @mui/icons-material react-router-dom axios @mui/x-data-grid`
- [ ] Set up theme.js, App.js with routing (login, register, dashboard, students, courses, attendance, reports)
- [ ] Create base layout: Navbar + Sidebar (240px) + Outlet

```bash
git checkout -b feature/frontend-scaffold develop
git add frontend/
git commit -m "[chore] Initialize React frontend with MUI and routing"
git push origin feature/frontend-scaffold
```

---

### Day 8 (Tue, Jul 14) — Wireframes + Design System
- [ ] Wireframe dashboard pages matching Google Sheets layout: search bar, subject table, stats tabs
- [ ] Pick color palette, typography, spacing — write `docs/design-system.md`
- [ ] Reusable components: Button, Input, Card, DataTable

```bash
git checkout -b docs/wireframes develop
git add docs/wireframes/ docs/design-system.md
git commit -m "[docs] Add wireframes and design system"
git push origin docs/wireframes
```

---

### Day 9 (Wed, Jul 15) — Dashboard Page: Overview + Student Search
- [ ] Dashboard page with search bar (program/section dropdowns + student name auto-complete)
- [ ] Subject-wise attendance table with color-coded % (🟢 ≥75%, 🟡 60-74%, 🔴 <60%)
- [ ] Connect to Abhishek's dashboard APIs (US-06, US-07) once available

```bash
git checkout -b feature/dashboard-overview develop
git add frontend/src/pages/Dashboard.jsx frontend/src/components/
git commit -m "[feat] Add dashboard overview page with search and stats table"
git push origin feature/dashboard-overview
```

---

### Day 10 (Thu, Jul 16) — Analytics Pages: At-Risk, Latecomers, Faculty
- [ ] At-Risk Students page (US-09): table with subject breakdown, poor attendance flag
- [ ] Chronic Latecomers page (US-10): LP breakdown per student, total LP
- [ ] Faculty Performance page (US-08): per-faculty stats table
- [ ] Connect to backend APIs

```bash
git checkout -b feature/analytics-pages develop
git add frontend/src/pages/
git commit -m "[feat] Add at-risk, latecomers, and faculty analytics pages"
git push origin feature/analytics-pages
```

---

### Day 11 (Fri, Jul 17) — Student Detail + Incomplete Records
- [ ] Student detail page: per-subject attendance breakdown (following US-06 detail endpoint)
- [ ] Incomplete Records page (US-13): subjects with data issues
- [ ] Login + Register pages connecting to real auth API
- [ ] Merge all branches into `develop`

```bash
git checkout develop
git merge feature/frontend-scaffold
git merge docs/wireframes
git merge feature/dashboard-overview
git merge feature/analytics-pages
git push origin develop
```

### Day 12–13 (Sat–Sun) — Buffer
- [ ] Catch up on pending pages
- [ ] Read Week 3 tasks before Monday
