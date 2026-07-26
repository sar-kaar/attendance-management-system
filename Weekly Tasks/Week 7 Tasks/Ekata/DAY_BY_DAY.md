# Week 7 (Aug 17–25) — Sprint 5: Finalization
## Ekata Rimal — Frontend

**Sprint Goal:** UI polish complete, user manual finished, deployed and pointed at the real backend URL.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 41 (Mon, Aug 17) — Build for Production
- [ ] Point the frontend's API base URL at Abhishek's deployed backend (env variable, not hardcoded)
- [ ] Production build, fix any build-only errors

```bash
git checkout -b chore/production-build develop
git add frontend/
git commit -m "[chore] Configure frontend for production API URL"
git push origin chore/production-build
```

---

### Day 42 (Tue, Aug 18) — Final Polish
- [ ] Last pass on responsive design, accessibility basics (alt text, heading structure)
- [ ] Fix anything left from Week 6's bug list

### Day 43 (Wed, Aug 19) — Deploy Frontend
- [ ] Deploy to whatever host the team picked (Vercel/Netlify or similar)
- [ ] Full click-through test on the deployed site against the deployed backend

```bash
git checkout develop
git merge chore/production-build
git push origin develop
```

---

### Day 44 (Thu, Aug 20) — User Manual
- [ ] Finish the user manual with real screenshots from the deployed app, one section per role (admin, faculty, student)

### Day 45 (Fri, Aug 21) — Sprint Review + Final Demo
- [ ] Support the live demo on the deployed URL

### Day 46 (Sat, Aug 22) — Code Freeze
### Day 47–48 (Sun–Mon) — Buffer, only teacher-flagged fixes
### Day 49 (Tue, Aug 25) — Submission
- [ ] Confirm user manual is in the submission folder
