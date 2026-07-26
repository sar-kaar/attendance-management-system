# Week 3 (Jul 20–26) — Sprint 1: Auth
## Ekata Rimal — Frontend

**Sprint Goal:** login/register/dashboard shell working against the real Django API.

**Important:** `TokenObtainPairView` (SimpleJWT default) logs in with `username` + `password`, not email, unless Abhishek changes `USERNAME_FIELD` on the User model. Confirm which one with him Monday before building the form.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 14 (Mon, Jul 20) — Confirm Contract, Build Register Page
**Before you start:** confirm login field (username vs email) with Abhishek. Confirm register requires: username, email, password, role, first_name, last_name (see `accounts/serializers.py`).

- [ ] Build register page with those exact fields
- [ ] POST to `/api/auth/register/`, handle validation errors from DRF (they come back as `{field: [errors]}`, not a flat message)

```bash
git checkout -b feature/register-page develop
git add frontend/src/pages/Register.*
git commit -m "[US-01] Add register page matching real API fields"
git push origin feature/register-page
```

---

### Day 15 (Tue, Jul 21) — Login Page
- [ ] Build login page (username + password per confirmed contract)
- [ ] POST to `/api/auth/login/`, store `access` and `refresh` from the response (not a custom `token` field)
- [ ] Attach `Authorization: Bearer <access>` header on subsequent requests

```bash
git checkout -b feature/login-page develop
git add frontend/src/pages/Login.*
git commit -m "[US-02] Add login page storing access/refresh tokens"
git push origin feature/login-page
```

---

### Day 16 (Wed, Jul 22) — Dashboard Shell + Auth State
- [ ] Build sidebar/header layout matching Week 2 wireframes
- [ ] Auth state (context or store) that reads role from `/api/auth/me/` and shows/hides nav items for admin/faculty/student
- [ ] Protected routing — redirect to login if no token

```bash
git checkout -b feature/dashboard-shell develop
git add frontend/src/
git commit -m "[US-02] Add dashboard shell with role-aware navigation"
git push origin feature/dashboard-shell
```

---

### Day 17 (Thu, Jul 23) — Token Refresh
- [ ] On a 401 response, call `/api/auth/token/refresh/` with the stored refresh token, retry the original request once
- [ ] If refresh also fails, clear tokens and redirect to login

```bash
git add frontend/src/
git commit -m "[US-03] Add automatic token refresh on 401"
git push origin feature/dashboard-shell
```

---

### Day 18 (Fri, Jul 24) — Integration & Review
- [ ] Live test with Abhishek: register → login → dashboard shows correct role → refresh works
- [ ] PR all Sprint 1 branches into `develop`, fix review comments

```bash
git checkout develop
git merge feature/register-page
git merge feature/login-page
git merge feature/dashboard-shell
git push origin develop
```

### Day 19–20 (Sat–Sun) — Sprint Review & Retro
- [ ] Demo full auth flow live
- [ ] Retro, prep Week 4 (student/course/attendance UI against real CRUD endpoints)
