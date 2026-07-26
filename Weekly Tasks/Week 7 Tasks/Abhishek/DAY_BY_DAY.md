# Week 7 (Aug 17–25) — Sprint 5: Finalization
## Abhishek Rokaya — Backend

**Sprint Goal:** production-ready backend, deployed, documented.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 41 (Mon, Aug 17) — Production Config
- [ ] `DEBUG = False`, real `ALLOWED_HOSTS`, `SECRET_KEY` from environment (should already be done since Week 2 — verify)
- [ ] Restrict `CORS_ALLOWED_ORIGINS` to the real deployed frontend URL
- [ ] Switch `db.sqlite3` to a real DB if the host requires it, otherwise SQLite is fine for a student project — confirm with Prizma what the deployment target actually needs

```bash
git checkout -b chore/production-config develop
git add config/settings.py
git commit -m "[chore] Production settings: DEBUG off, real hosts, restricted CORS"
git push origin chore/production-config
```

---

### Day 42 (Tue, Aug 18) — API Documentation
- [ ] Generate OpenAPI/Swagger docs (`drf-spectacular` or similar) covering every real endpoint including face recognition and exports
- [ ] Save/export as PDF for submission

```bash
git checkout -b docs/api-documentation develop
git add docs/
git commit -m "[docs] Generate full API documentation"
git push origin docs/api-documentation
```

---

### Day 43 (Wed, Aug 19) — Deploy
- [ ] Deploy to whatever host the team picked (Render/Railway or similar)
- [ ] Confirm the deployed API responds correctly to a real login + CRUD call

```bash
git checkout develop
git merge chore/production-config
git merge docs/api-documentation
git push origin develop
```

---

### Day 44 (Thu, Aug 20) — Final Bug Fixes
- [ ] Fix anything found during deployment testing
- [ ] Re-run full test suite one more time

### Day 45 (Fri, Aug 21) — Sprint Review + Final Demo
- [ ] Live demo on the deployed URL, not localhost

### Day 46 (Sat, Aug 22) — Code Freeze
- [ ] No more feature changes after today

### Day 47–48 (Sun–Mon) — Buffer
- [ ] Only fix anything the teacher flags

### Day 49 (Tue, Aug 25) — Submission
- [ ] Confirm repo is accessible, README is accurate, all docs in the submission folder
