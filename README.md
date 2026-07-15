# Attendance Management System

Face Recognition Based Attendance System for Model Institute of Technology.

## Tech Stack

### Frontend
- React 19 + Vite
- React Router DOM (client-side routing)
- Axios (API communication with JWT auto-refresh)
- Chart.js + react-chartjs-2 (dashboard visualizations)

### Backend (Django)
- Django + Django REST Framework
- JWT Authentication (SimpleJWT)
- SQLite (development) / PostgreSQL (production)
- face_recognition / dlib (face recognition module)
- ReportLab (PDF exports)

## Project Structure

```
├── config/             # Django settings, URLs, WSGI/ASGI
├── accounts/           # User model (admin/faculty/student roles), JWT auth
├── students/           # Student CRUD (with program, section, face_encoding)
├── courses/            # Course CRUD + Enrollment management
├── attendance/         # Attendance CRUD, bulk mark, dashboard stats, CSV/PDF export
├── face/               # Face registration, recognition, face-based attendance
├── wireframes/         # HTML wireframes (login, dashboard, students)
├── docs/               # Architecture, ER diagrams, requirements
├── src/                # React frontend
│   ├── pages/          # Login, Register, Dashboard, Students, Courses, Attendance, FaceRecognition, StudentDashboard
│   ├── layouts/        # DashboardLayout (sidebar + topbar)
│   ├── context/        # AuthContext (JWT auth state)
│   ├── services/       # API service layer (axios with interceptors)
│   └── styles/         # CSS (login, layout, dashboard, table)
├── .github/workflows/  # CI pipeline (GitHub Actions)
└── package.json        # Frontend dependencies
```

## Getting Started

### Backend
```bash
cd attendance-management-system
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` with API proxy to Django at `http://localhost:8000`.

## API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/auth/register/` | POST | Register (defaults to student role) |
| `/api/auth/login/` | POST | JWT token pair (access + refresh) |
| `/api/auth/token/refresh/` | POST | Refresh access token |
| `/api/auth/me/` | GET, PUT, PATCH | Current user profile |
| `/api/students/` | CRUD | Student management |
| `/api/courses/` | CRUD | Course management |
| `/api/enrollments/` | CRUD | Enrollment (filter: ?course=, ?student=, ?is_active=) |
| `/api/attendance/` | CRUD | Attendance records (filter: ?course=, ?date=, ?student=) |
| `/api/attendance/mark_bulk/` | POST | Bulk attendance marking |
| `/api/attendance/my_attendance/` | GET | Student's own attendance |
| `/api/attendance/report/` | GET | Attendance statistics |
| `/api/attendance/dashboard/` | GET | Dashboard stats (today/overall/recent) |
| `/api/attendance/export_csv/` | GET | CSV export |
| `/api/attendance/export_pdf/` | GET | PDF export |
| `/api/face/register/` | POST | Register face (student_id + image) |
| `/api/face/recognize/` | POST | Identify face from image |
| `/api/face/mark-attendance/` | POST | Face-based attendance marking |
| `/api/face/registered/` | GET | List students with registered faces |

## User Roles

- **Admin**: Full access to all features
- **Faculty**: Manage students, courses, attendance
- **Student**: View own attendance, self-service portal
