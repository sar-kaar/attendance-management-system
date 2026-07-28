# Mobile

React Native (Expo, managed workflow) + TypeScript client for the Attendance Management System. See [docs/mobile-architecture.md](../docs/mobile-architecture.md), [docs/mobile-requirements.md](../docs/mobile-requirements.md) and [docs/decisions.md](../docs/decisions.md) (ADR-008) for the full plan. Tracked under GitHub Epic #34.

Consumes the same Django/DRF backend as `frontend/` — no separate mobile backend.

## Setup

```bash
npm install
npm start
```

Then press `a` for Android, `i` for iOS (macOS only), or `w` for web, or scan the QR code with Expo Go.

## Environment Variables

Copy `.env.example` to `.env` and configure:

```
EXPO_PUBLIC_API_URL=http://localhost:8000/api
```

## Status

Phase 15 (Foundation & Scaffold) only: booting auth/unauth shell with role-based navigator stubs. No features implemented yet — see [docs/phases.md](../docs/phases.md) Phases 16-23 for what's next.

## Scripts

- `npm run lint` — eslint
- `npm run typecheck` — tsc --noEmit
