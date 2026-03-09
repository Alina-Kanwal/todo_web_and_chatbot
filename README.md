# Hackathon Todo App – Phase II

A modern, multi-user web application for task management with JWT-based authentication.

## Overview

This project transforms a console-based todo application into a production-ready, full-stack web application with:

- **Multi-user authentication** with stateless JWT sessions
- **Complete CRUD operations** for tasks with strict user isolation
- **Filtering and sorting** capabilities
- **Responsive design** for desktop and mobile devices
- **RESTful API** with explicit contracts

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT)
- **Migrations**: Alembic

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth client

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes and dependencies
│   │   ├── models/         # SQLModel entities
│   │   ├── services/       # Business logic
│   │   ├── core/           # Configuration and utilities
│   │   └── main.py         # Application entry point
│   ├── tests/
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── .env
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and API client
│   │   └── types/         # TypeScript types
│   ├── tests/
│   ├── package.json
│   └── .env.local
├── specs/                  # Feature specifications
│   └── 001-hackathon-todo-web/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── .specify/              # Spec-Kit Plus configuration
├── .env.example           # Environment variable template
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm or npm

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env` with your values:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env  # Unix
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```

API docs available at: http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy `.env.local` with your values:
   ```bash
   copy .env.example .env.local  # Windows
   cp .env.example .env.local  # Unix
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

Application available at: http://localhost:3000

## Environment Variables

See `.env.example` for required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://...` |
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | Shared JWT secret (32+ chars) | `your-secret-key` |

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/signin` - Sign in with credentials
- `POST /api/auth/signout` - Sign out (client-side)

### Tasks
- `GET /api/tasks` - List all user's tasks
- `GET /api/tasks/{id}` - Get single task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}` - Partial update
- `DELETE /api/tasks/{id}` - Delete task

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest tests/contract/      # API contract tests
pytest tests/integration/   # Integration tests
pytest tests/unit/          # Unit tests
```

### Frontend Tests
```bash
cd frontend
npm test                    # Unit tests
npm run test:e2e           # E2E tests
```

## Security

- JWT tokens for stateless authentication
- User data isolation (users can only access their own data)
- Input validation on all endpoints
- CORS configured for trusted origins only
- No hardcoded secrets

## Documentation

- [Feature Specification](specs/001-hackathon-todo-web/spec.md)
- [Implementation Plan](specs/001-hackathon-todo-web/plan.md)
- [Task Breakdown](specs/001-hackathon-todo-web/tasks.md)
- [API Documentation](http://localhost:8000/docs)

## License

MIT
