# Week 3 (Jul 20–26) — Sprint 1: Auth
## Abhishek Rokaya — Backend

**Sprint Goal:** auth is secured, tested, and documented for the frontend to build against. It already works — this sprint is not "build register/login".

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 14 (Mon, Jul 20) — Verify Auth End to End
**Before you start:** `git pull origin develop`. Confirm Ekata has the endpoint list from Week 2.

- [ ] Test with Postman: register → login (check response is `{access, refresh}`) → GET `/api/auth/me/` with Bearer token → refresh token
- [ ] Confirm role field comes back correctly on `/api/auth/me/`
- [ ] Fix anything broken

```bash
git checkout -b test/auth-verification develop
git add accounts/tests.py
git commit -m "[test] Verify auth flow end to end"
git push origin test/auth-verification
```

---

### Day 15 (Tue, Jul 21) — Write Auth Tests
- [ ] Django test cases in `accounts/tests.py`: register success, duplicate email/username, login success, login wrong password, `/me/` without token returns 401, `/me/` with token returns user
- [ ] Run `python manage.py test accounts`

```bash
git add accounts/tests.py
git commit -m "[test] Add auth test cases"
git push origin test/auth-verification
```

---

### Day 16 (Wed, Jul 22) — CORS & Permissions Hardening
- [ ] Restrict `CORS_ALLOW_ALL_ORIGINS` — set `CORS_ALLOWED_ORIGINS` to the frontend dev URL Ekata is using (e.g. `http://localhost:5173`) once she confirms it
- [ ] Double-check `IsAdminOrFaculty` permission classes on students/courses/attendance still work after any settings change

```bash
git checkout -b chore/cors-restrict develop
git add config/settings.py
git commit -m "[chore] Restrict CORS to real frontend origin"
git push origin chore/cors-restrict
```

**If Ekata's dev URL isn't known yet:** ask in Discord before end of day, don't guess.

---

### Day 17 (Thu, Jul 23) — API Docs for Frontend
- [ ] Update `docs/api-endpoints.md` with exact request/response bodies for register, login, refresh, me
- [ ] Confirm with Ekata she can hit these from her dev environment (test a real call together)

```bash
git add docs/api-endpoints.md
git commit -m "[docs] Finalize auth request/response docs for frontend integration"
git push origin docs/api-endpoints
```

---

### Day 18 (Fri, Jul 24) — Integration & Review
- [ ] PR: `test/auth-verification` and `chore/cors-restrict` → `develop`
- [ ] Pair with Ekata for 20 min: watch her frontend hit the real login endpoint live
- [ ] Merge after review

```bash
git checkout develop
git merge test/auth-verification
git merge chore/cors-restrict
git push origin develop
```

### Day 19–20 (Sat–Sun) — Sprint Review & Retro
- [ ] Demo: tested auth, restricted CORS, frontend logging in against real API
- [ ] Retro notes, prep Week 4 (student/course/attendance CRUD verification)
