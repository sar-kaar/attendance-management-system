# Design Guidelines — Attendance Management System

> **Purpose:** Documents the frontend's actual visual/UI conventions so new screens stay consistent with existing ones.
> **Scope:** Frontend (`frontend/src/styles/*`, page components). This is a description of the **current, shipped** design, not an aspirational design system — AMS has no design tool source (Figma) checked in; `wireframes/*.html` are the original static mockups, not always matching the built UI 1:1.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Current State](#current-state)
- [Layout](#layout)
- [Color](#color)
- [Typography](#typography)
- [Components](#components)
- [Responsive Behavior](#responsive-behavior)
- [Accessibility](#accessibility)
- [Dark Mode](#dark-mode)
- [Guidelines for New Screens](#guidelines-for-new-screens)

## Current State

The frontend uses **plain CSS** (one stylesheet per feature area under `frontend/src/styles/`: `dashboard.css`, `face.css`, `layout.css`, `login.css`, `notifications.css`, `reports.css`, `table.css`) — no CSS-in-JS, no Tailwind, no Material UI (despite early planning notes in `Guidelines/REALITY_CHECK.md` mentioning MUI, the shipped app does not depend on it — see `frontend/package.json`). No design tokens file or theme object exists yet.

**This document records what exists so it can be extended consistently. It intentionally does not invent a token system, spacing scale, or breakpoint table that isn't already reflected in the CSS** — adding one is future work (see [phases.md](phases.md)).

## Layout

- `layouts/DashboardLayout.jsx` provides shared chrome (nav/sidebar) for all authenticated pages; unauthenticated pages (`Login`, `Register`, `VerifyEmail`) render standalone.
- Tables (`table.css`) are the primary data-display pattern across Students, Courses, Attendance, Reports.
- Icons come from `react-icons` and `public/icons.svg` (inline sprite) — prefer `react-icons` for new work since it's already a dependency; keep `icons.svg` for icons not covered by the library.

## Color

No centralized palette file exists — colors are set per-stylesheet. **When adding new UI, inspect the existing page's CSS file for the color already in use for that context (success/error/warning, primary action, table borders) rather than picking a new hex value.** If a genuinely new semantic color is needed, add it as a CSS custom property at the top of the relevant stylesheet, not an inline hex, so it can be centralized later.

## Typography

No typography scale is currently defined in a shared file — each stylesheet sets its own font sizes. Follow the sizing already used by sibling elements on the same page rather than introducing a new size.

## Components

Known reusable pieces:

- **Toasts / confirm dialogs** — `NotificationContext` (`frontend/src/context/NotificationContext.jsx`) plus `notifications.css`. As of 2026-07-20, native `alert()`/`confirm()` calls were replaced across Attendance, AttendanceCodes, Courses, Enrollments, and Students with this toast/confirm system — **new destructive/confirmation UI must use this system, not native dialogs** (see [rules.md](rules.md)).
- **Social login button** — `components/SocialLogin.jsx`.
- **Webcam capture** — `react-webcam`, used in `FaceRecognition.jsx`.

## Responsive Behavior

No documented breakpoint system exists. Verify new screens at common widths (mobile ~375px, tablet ~768px, desktop ~1280px) manually since there's no shared media-query scale to rely on yet.

## Accessibility

No formal audit has been done. Baseline expectations for new work:

- Use semantic HTML elements (`<button>`, `<table>`, `<label>`) — don't build interactive elements out of `<div>`s.
- Every form input needs an associated `<label>`.
- Toast/confirm dialogs (not native `alert`/`confirm`) so screen readers and keyboard users get consistent behavior.

## Dark Mode

Not implemented. All current stylesheets assume a single (light) theme.

## Guidelines for New Screens

1. Reuse `DashboardLayout` for any authenticated page.
2. Add a new `styles/<feature>.css` file per new feature area, matching the existing one-file-per-feature convention — don't grow an existing file with unrelated styles.
3. Reuse the toast/confirm system for all user feedback and confirmations.
4. Match existing table/form patterns (`table.css`) before introducing a new layout primitive.
5. If you introduce a genuinely new visual pattern more than one page will reuse, extract it into `components/` rather than duplicating markup/CSS across pages.
