# Week 5 (Aug 3–9) — Sprint 3: Face Recognition
## Abhishek Rokaya — Backend

**Sprint Goal:** face registration and recognition actually working. This is genuinely new code — nothing here exists yet, unlike Sprints 1–2.

Routine every day: see `Weekly Tasks/TEAM_SYNC_PROTOCOL.md`.

---

### Day 28 (Mon, Aug 3) — Face Detection Test
- [ ] Confirm `opencv-python` + `opencv-contrib-python` import correctly (`python -c "import cv2; print(cv2.__version__)"`)
- [ ] Test Haar cascade or DNN face detector on 3–5 sample photos
- [ ] Decide the encoding library: `face_recognition` (needs dlib, heavier install) vs OpenCV's own face recognizer — write the decision and why in `docs/face-recognition-approach.md`

```bash
git checkout -b feature/face-detection-poc develop
git add docs/face-recognition-approach.md
git commit -m "[US-07] Confirm face detection approach"
git push origin feature/face-detection-poc
```

**If the chosen library won't install:** fall back to OpenCV's built-in LBPH recognizer — slower but no extra dependencies.

---

### Day 29 (Tue, Aug 4) — Face Registration Endpoint
- [ ] New endpoint (e.g. `POST /api/students/<id>/register_face/`): accept an image, detect the face, compute the encoding, store it in the existing `face_encoding` TextField (as JSON)
- [ ] Reject images with no face or more than one face, with a clear error message

```bash
git add students/views.py students/serializers.py
git commit -m "[US-07] Add face registration endpoint"
git push origin feature/face-detection-poc
```

---

### Day 30 (Wed, Aug 5) — Face Recognition Endpoint
- [ ] New endpoint (e.g. `POST /api/attendance/recognize/`): accept an image, compare against stored encodings, return the best match and confidence score
- [ ] Set a confidence threshold — below it, return "no match" instead of guessing

```bash
git checkout -b feature/face-recognition-api develop
git add attendance/views.py
git commit -m "[US-08] Add face recognition matching endpoint"
git push origin feature/face-recognition-api
```

---

### Day 31 (Thu, Aug 6) — Wire to Attendance
- [ ] On a successful match, create an Attendance record with `marked_by='face'`
- [ ] Test with multiple students registered, varied lighting if possible
- [ ] Document known limitations (lighting, angle, glasses) in `docs/face-recognition-approach.md`

```bash
git add attendance/views.py docs/face-recognition-approach.md
git commit -m "[US-08] Auto-mark attendance on face match, document limitations"
git push origin feature/face-recognition-api
```

---

### Day 32 (Fri, Aug 7) — Integration & Review
- [ ] PR both branches into `develop`
- [ ] Live test with Ekata's camera UI once it's ready

```bash
git checkout develop
git merge feature/face-detection-poc
git merge feature/face-recognition-api
git push origin develop
```

### Day 33–34 (Sat–Sun) — Sprint Review, Retro, Buffer
- [ ] Demo: register a face, recognize it, see attendance auto-marked
- [ ] If accuracy is bad, confirm manual attendance stays as the fallback — don't force it into the demo
