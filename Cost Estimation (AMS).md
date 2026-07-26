# Cost Estimation — Attendance Management System

**Course:** CSE 405 — Software Project Management
**Project:** Attendance Management System (Facial Recognition + Manual Attendance)
**Team:** Prizma Subedi (PM) · Abhishek Rokaya (Backend) · Ekata Rimal (Frontend)
**Duration:** 7 Weeks (Jul 7 – Aug 25, 2026)
**Currency:** NPR (Nepalese Rupee)
**Prepared:** Jul 19, 2026
**Type:** Cost outflow estimate only (no benefits/ROI included)

---

## 1. Purpose & Basis of Estimate

This document estimates the **total cost of building and delivering** the AMS project, split into:

- **Tangible costs** — quantifiable cash/opportunity-cost outflows (labor, tools, hosting, utilities).
- **Intangible costs** — real but non-monetary costs (stress, learning curve, coordination overhead, risk exposure) that affect the project even though they carry no NPR figure.

**Basis of labor estimate:** Hours for Sprints 1–4 (Weeks 3–6) are taken directly from the task-level effort tables in the [Project Guide Book](Guidelines/00_COMPLETE_PROJECT_GUIDE_BOOK.md). Hours for Week 1 (Initiation), Week 2 (Sprint 0 design), Week 7 (Finalization), and all PM effort are **estimated** using the routines and deliverables described in the same guide, since they weren't tabulated with exact hours. This is a *planning estimate*, not an actuals report — actual hours should be reconciled against the Personal Log / Sprint Backlog sheets as the project progresses.

**Labor is costed at opportunity-cost rates** (i.e., "what this would cost if a client had to pay for it"), not actual cash paid — since this is unpaid academic work. This is standard practice for a PMBOK-style Business Case cost section.

---

## 2. Tangible Costs

### 2.1 Labor (Opportunity Cost)

| Week | Phase | Backend Hrs (Abhishek) | Frontend Hrs (Ekata) | PM Hrs (Prizma) | Basis |
|---|---|---|---|---|---|
| 1 | Initiation & Requirements | 12 | 12 | 18 | Estimated |
| 2 | Sprint 0 — Design & Planning | 16 | 16 | 22 | Estimated |
| 3 | Sprint 1 — Foundation & Auth | 25 | 24 | 10 | Guide book table |
| 4 | Sprint 2 — Core Attendance | 26 | 26 | 10 | Guide book table |
| 5 | Sprint 3 — Face Recognition | 34 | 21 | 12 | Guide book table |
| 6 | Sprint 4 — Reports & Testing | 20 | 22 | 14 | Guide book table |
| 7 | Sprint 5 — Finalization | 13 | 11 | 12 | Estimated |
| **Total Hours** | | **146** | **132** | **98** | |

| Role | Total Hours | Rate (NPR/hr)* | Opportunity Cost (NPR) |
|---|---|---|---|
| Backend Developer (Abhishek) — specialized: Django/DRF + face recognition (OpenCV/dlib) | 146 | 400 | **58,400** |
| Frontend Developer (Ekata) — React, UI/UX, camera integration | 132 | 350 | **46,200** |
| Project Manager (Prizma) — planning, docs, ceremonies, reporting | 98 | 350 | **34,300** |
| **Subtotal — Labor** | **376** | | **139,900... see note** |

\* Rates approximate entry-level/junior developer market rates in Nepal (NPR 350–400/hr ≈ NPR 55,000–65,000/month equivalent). Backend is rated slightly higher for the specialized face-recognition/ML work.

**Labor Subtotal: NPR 138,900**

> Note: 146×400 + 132×350 + 98×350 = 58,400 + 46,200 + 34,300 = **138,900**

### 2.2 Software & Tools

| Item | License | Cost (NPR) |
|---|---|---|
| Django + Django REST Framework | Open-source | 0 |
| SimpleJWT | Open-source | 0 |
| SQLite (dev) | Open-source | 0 |
| React (Vite), Tailwind/Bootstrap, Axios, Chart.js/Recharts | Open-source | 0 |
| OpenCV, dlib, face_recognition (Python) | Open-source | 0 |
| VS Code / PyCharm Community | Free | 0 |
| GitHub (repo, PRs, CI) | Free tier | 0 |
| Trello (board) | Free tier | 0 |
| Figma (wireframes) | Free tier | 0 |
| Google Workspace (Docs/Sheets trackers) | Free (personal account) | 0 |
| **Subtotal — Software & Tools** | | **0** |

### 2.3 Hosting & Deployment

| Item | Notes | Cost (NPR) |
|---|---|---|
| Backend hosting (Railway/Render/Heroku) | Free tier for dev; may need a paid hobby tier (~$5/mo) for the last ~1 month if usage/uptime exceeds free limits | 700 |
| Frontend hosting (Vercel/Netlify) | Free tier is sufficient | 0 |
| PostgreSQL (prod DB) | Free tier add-on | 0 |
| SSL/TLS | Included free with host | 0 |
| Custom domain *(optional)* | Only if a branded demo URL is wanted for the final presentation | 1,500 |
| **Subtotal — Hosting (mandatory)** | | **700** |
| **Optional add-on (domain)** | | **1,500** |

### 2.4 Hardware & Equipment

| Item | Status | Incremental Cost (NPR) |
|---|---|---|
| 3× personal laptops | Already owned by each team member | 0 (sunk cost, not project outflow) |
| Laptop webcams | Already owned — used for face recognition testing | 0 |
| External webcam *(optional upgrade)* | Only if built-in webcam accuracy is insufficient for Sprint 3 testing | 2,500 |
| **Subtotal — Hardware (mandatory)** | | **0** |
| **Optional add-on (webcam)** | | **2,500** |

### 2.5 Connectivity & Utilities

| Item | Notes | Cost (NPR) |
|---|---|---|
| Incremental internet usage | Video calls, testing, deployment, across 3 members × 7 weeks | 2,200 |
| Electricity (extra laptop/device usage) | Attributable share across 7 weeks | 800 |
| **Subtotal — Connectivity & Utilities** | | **3,000** |

### 2.6 Miscellaneous

| Item | Notes | Cost (NPR) |
|---|---|---|
| Printing (final report, handouts) | Physical submission copy if required | 500 |
| Presentation materials | Slide printouts / poster if required | 300 |
| **Subtotal — Miscellaneous** | | **800** |

### 2.7 Contingency Reserve

A **10% contingency** is applied to (Labor + mandatory non-labor costs) to cover schedule slippage, rework from teacher-requested scope changes, or unplanned tool upgrades — consistent with the project's own Risk Register practice.

| Base for Contingency | Amount (NPR) |
|---|---|
| Labor (138,900) + Mandatory non-labor (700 + 0 + 3,000 + 800 = 4,500) | 143,400 |
| **Contingency @ 10%** | **14,340** |

---

## 3. Tangible Cost Summary

| Category | Cost (NPR) |
|---|---|
| Labor (opportunity cost) | 138,900 |
| Software & Tools | 0 |
| Hosting & Deployment (mandatory) | 700 |
| Hardware & Equipment (mandatory) | 0 |
| Connectivity & Utilities | 3,000 |
| Miscellaneous | 800 |
| Contingency Reserve (10%) | 14,340 |
| **Total Mandatory Tangible Cost** | **157,740** |
| Optional: Custom domain | +1,500 |
| Optional: External webcam | +2,500 |
| **Total Tangible Cost (with all optional add-ons)** | **161,740** |

---

## 4. Intangible Costs

These carry no direct NPR value but represent real costs to the team, the project, and its stakeholders.

| # | Category | Description | Who Bears It | Relative Impact |
|---|---|---|---|---|
| 1 | **Learning-curve cost** | First-time use of Django/DRF, SimpleJWT, OpenCV/dlib/face_recognition, and React camera integration slows early velocity and increases error rates | Abhishek, Ekata | High |
| 2 | **Academic opportunity cost** | ~376 hours diverted from other coursework, rest, and personal time over 7 weeks; risk of trade-off against other subjects' grades | All 3 members | High |
| 3 | **Stress from high-risk sprint** | Sprint 3 (Face Recognition) is explicitly flagged as highest-risk in the project's own Risk Register (R-003, score 16/25) — creates concentrated pressure and anxiety mid-project | Abhishek primarily; whole team indirectly | High |
| 4 | **Coordination & meeting overhead** | Daily standups, sprint ceremonies, and cross-review time reduce hours available for pure build work; risk of miscommunication causing rework | All 3 members | Medium |
| 5 | **Rework risk from feedback cycles** | Teacher feedback after each Sprint Review may require redesign of already-built features, costing morale and previously "sunk" effort | Abhishek, Ekata | Medium |
| 6 | **Biometric data handling risk** | Face recognition data is sensitive; even in an academic sandbox, mishandling raises ethical/privacy exposure and potential loss of trust if tested with real student volunteers | Whole team, indirectly the university | Medium |
| 7 | **Grade / academic reputation risk** | Project outcome directly affects course grade and team's academic standing — underperformance has a cost beyond the project itself | All 3 members | High |
| 8 | **Bus-factor / key-person risk** | 3-person team with hard role ownership (PM / Backend / Frontend) — illness or unavailability of any one member has outsized schedule impact | All 3 members | Medium |
| 9 | **Context-switching cost** | Juggling Trello, GitHub, 2 Google Sheets, WhatsApp/Discord, and 4+ other courses fragments focus and adds low-grade daily friction | All 3 members | Low–Medium |
| 10 | **Technical debt / knowledge-transfer cost** | Compressed Sprint 5 (finalization) increases risk of under-documented code and rushed handover, reducing the system's post-submission usability | Whole team | Medium |

---

## 5. Assumptions & Notes

- Labor rates (NPR 350–400/hr) are illustrative opportunity-cost figures for entry-level Nepali developers/PMs, not actual payments — no cash wages are exchanged among team members.
- All software, frameworks, and libraries used (Django, React, OpenCV, etc.) are open-source with zero licensing cost.
- Hosting is assumed to stay within free tiers for most of the project; a small paid-tier buffer is included for the final deployment weeks (Sprint 5).
- Hardware (laptops, webcams) is already owned by each team member and treated as a **sunk cost**, not a project cash outflow.
- Optional line items (custom domain, external webcam) are **not** included in the mandatory total — add them only if the team decides to use them.
- This estimate does not include intangible costs in the NPR total, since they are not meaningfully quantifiable — they are listed qualitatively in Section 4 per PMBOK practice.
- Figures should be reconciled against actual hours logged in the **Personal Log** and **Sprint Backlog** tabs as the project progresses; this document is a planning-stage estimate (prepared Week 2 timeframe, mid-Sprint 0/Sprint 1).

---

**Grand Total (Mandatory Tangible Cost Outflow): NPR 157,740**
**Grand Total (incl. all optional add-ons): NPR 161,740**
