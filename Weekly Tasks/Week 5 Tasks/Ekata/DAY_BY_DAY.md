# Week 5 (Aug 3–9) — Sprint 3: Face Recognition
## Ekata Rimal — Frontend

**Sprint Goal:** camera capture UI for face registration and recognition-based attendance.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 28 (Mon, Aug 3) — Camera Component
- [ ] Build a reusable camera capture component (browser `getUserMedia` if React, or an `<input type=file capture>` fallback for a simpler build)
- [ ] Capture a still frame as an image blob, ready to POST

```bash
git checkout -b feature/camera-component develop
git add frontend/src/components/Camera.*
git commit -m "[US-07] Add camera capture component"
git push origin feature/camera-component
```

---

### Day 29 (Tue, Aug 4) — Face Registration Page
- [ ] Pick a student → capture photo → POST to Abhishek's face registration endpoint (confirm exact path with him — it's new this sprint)
- [ ] Show clear success/error (e.g. "no face detected", "multiple faces detected")

```bash
git checkout -b feature/face-registration-ui develop
git add frontend/src/pages/FaceRegister.*
git commit -m "[US-07] Add face registration UI"
git push origin feature/face-registration-ui
```

---

### Day 30 (Wed, Aug 5) — Recognition Attendance UI
- [ ] Camera view → capture → POST to the recognition endpoint → show recognized student name + confidence, or "no match"
- [ ] Confirm button before the attendance record actually gets created (don't auto-save on every frame)

```bash
git checkout -b feature/face-attendance-ui develop
git add frontend/src/pages/FaceAttendance.*
git commit -m "[US-08] Add recognition-based attendance UI"
git push origin feature/face-attendance-ui
```

---

### Day 31 (Thu, Aug 6) — Loading & Error States
- [ ] Add loading spinner while the image uploads and processes (this can take a few seconds)
- [ ] Handle camera permission denied, no camera found

```bash
git add frontend/src/
git commit -m "[US-08] Add loading and error states to face flows"
git push origin feature/face-attendance-ui
```

---

### Day 32 (Fri, Aug 7) — Integration & Review
- [ ] Live test with Abhishek's real endpoints
- [ ] PR all branches into `develop`

```bash
git checkout develop
git merge feature/camera-component
git merge feature/face-registration-ui
git merge feature/face-attendance-ui
git push origin develop
```

### Day 33–34 (Sat–Sun) — Sprint Review, Retro, Buffer
- [ ] Demo the camera flow live
- [ ] Prep Week 6: dashboard, reports, export UI
