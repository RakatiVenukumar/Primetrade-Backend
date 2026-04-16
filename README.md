# PrimeTrade Full-Stack Assignment

A full-stack task management application with JWT auth, role-based access control, FastAPI backend, and React frontend.

## Stack

- Backend: FastAPI, SQLAlchemy, SQLite/PostgreSQL, JWT, bcrypt
- Frontend: React + TypeScript + Vite
- Auth: Bearer token (JWT)
- Roles: `user`, `admin`

## Project Structure

- `backend/` FastAPI service
- `frontend/` React application

## Features Implemented

### Backend

- User registration and login
- JWT token generation and verification
- Protected routes (`/api/v1/auth/me`)
- Role-based admin routes (`/api/v1/admin/*`)
- Task CRUD routes with per-user ownership (`/api/v1/tasks/*`)
- Global standardized error handling
- API versioning under `/api/v1`
- Swagger/OpenAPI metadata and tag documentation

### Frontend

- Login page with API integration
- Protected routes (`/login`, `/dashboard`)
- Persistent auth session via localStorage
- Session validation on app startup (`/api/v1/auth/me`)
- Dashboard task management (create/list/toggle/delete)
- Task filters (all/open/done) with counters
- Centralized frontend API client and error parsing

## Quick Start

## 1) Backend

```powershell
cd backend
.\.venv\Scripts\activate
```

Install dependencies (if needed):

```powershell
pip install -r requirements.txt
```

Run with SQLite:

```powershell
$env:USE_SQLITE = "true"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Backend URLs:

- API base: `http://127.0.0.1:8000/api/v1`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## 2) Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

- `http://127.0.0.1:5173`

Optional environment variable:

- `VITE_API_BASE_URL` (default: `http://127.0.0.1:8000/api/v1`)

## Core API Endpoints

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Tasks

- `POST /api/v1/tasks`
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `PUT /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`

### Admin

- `GET /api/v1/admin/users`
- `GET /api/v1/admin/users/{user_id}`
- `PUT /api/v1/admin/users/{user_id}/role`
- `DELETE /api/v1/admin/users/{user_id}`

## Environment Notes

Use `.env.example` at repository root as reference.

Important keys:

- `SECRET_KEY` (set a strong secret in non-dev environments)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `USE_SQLITE` (`true` for local quick start)
- PostgreSQL connection settings when `USE_SQLITE=false`

## Deployment Notes

### Backend

- Set `SECRET_KEY` securely via environment variable
- Use PostgreSQL for production
- Keep `SQL_ECHO=false`
- Run behind a process manager / container runtime
- Restrict CORS to frontend origin(s)

### Frontend

- Build with `npm run build`
- Serve static files from `frontend/dist`
- Set `VITE_API_BASE_URL` to your deployed backend `/api/v1` URL

## Scalability Considerations

- Add database migrations (Alembic) before production schema evolution
- Add rate limiting and request logging middleware
- Add refresh token strategy and token revocation list
- Add background workers for long-running tasks
- Add pagination and indexing strategy as task volume grows
- Add CI pipeline for lint/test/build gates

## Current Status

Completed through step 20 with incremental commits and validated build checks.
