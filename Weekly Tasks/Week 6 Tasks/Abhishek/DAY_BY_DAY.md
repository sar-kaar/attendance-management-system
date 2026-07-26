# Week 6 (Aug 10–16) — Sprint 4: Reports & Testing
## Abhishek Rokaya — Backend

**Sprint Goal:** CSV/PDF export and dashboard stats built (the basic `/api/attendance/report/` endpoint already exists — this sprint extends it).

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 35 (Mon, Aug 10) — Dashboard Stats Endpoint
- [ ] New endpoint (e.g. `GET /api/attendance/dashboard_stats/`): total students, total courses, today's attendance %, trend over last 7 days
- [ ] Use `pandas`/`numpy` if the aggregation gets complex, otherwise plain Django ORM aggregates are enough

```bash
git checkout -b feature/dashboard-stats develop
git add attendance/views.py
git commit -m "[US-11] Add dashboard stats endpoint"
git push origin feature/dashboard-stats
```

---

### Day 36 (Tue, Aug 11) — CSV Export
- [ ] New endpoint (e.g. `GET /api/attendance/export_csv/?course=&start_date=&end_date=`) using Python's built-in `csv` module, streamed as a file response

```bash
git checkout -b feature/export-endpoints develop
git add attendance/views.py
git commit -m "[US-10] Add CSV export endpoint"
git push origin feature/export-endpoints
```

---

### Day 37 (Wed, Aug 12) — PDF Export
- [ ] Same filters, PDF output using `reportlab` (already in requirements.txt, unused until now)
- [ ] Keep it simple: table of student, course, date, status

```bash
git add attendance/views.py
git commit -m "[US-10] Add PDF export endpoint using reportlab"
git push origin feature/export-endpoints
```

---

### Day 38 (Thu, Aug 13) — Integration Testing Pass
- [ ] Run the full test suite (`python manage.py test`)
- [ ] Test every endpoint with Postman one more time end to end: auth, students, courses, attendance, face registration/recognition, exports
- [ ] Log bugs found on Trello, fix what's quick, flag what isn't

```bash
git checkout develop
git merge feature/dashboard-stats
git merge feature/export-endpoints
git push origin develop
```

---

### Day 39 (Fri, Aug 14) — Bug Fixes
- [ ] Fix bugs from Thursday's testing pass
- [ ] Confirm exports work with real data volumes, not just 2–3 test rows

### Day 40 (Sat, Aug 15) — Sprint Review & Retro
- [ ] Demo dashboard stats + CSV/PDF export
- [ ] Prep Week 7: production config, deployment, API docs
