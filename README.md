# Attendance Management System

Attendance Management System with facial recognition — CSE 405.

## Project layout

```
attendance-management-system/
├── backend/     # Django + DRF API (see backend/.env.example)
├── frontend/    # React + Vite UI (see frontend/.env.example)
└── docs/        # architecture, schema, requirements docs
```

Backend and frontend are independent projects with their own dependencies and env config — set up each one separately.

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # then fill in SECRET_KEY
python manage.py migrate
python manage.py runserver
```

API runs at `http://localhost:8000`. See `docs/system-architecture.md` for the endpoint list.

## Frontend

```bash
cd frontend
npm install
copy .env.example .env        # points VITE_API_URL at the backend
npm run dev
```

UI runs at `http://localhost:5173` by default (Vite).

## Docs

- `docs/system-architecture.md` — stack, apps, endpoints
- `docs/database-schema.md` — data model
- `Guidelines/REALITY_CHECK.md` — source of truth on current state
- `Weekly Tasks/GIT_WORKFLOW.md` — branching and PR conventions
