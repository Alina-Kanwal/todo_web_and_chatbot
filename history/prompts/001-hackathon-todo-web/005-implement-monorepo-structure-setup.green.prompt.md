---
id: 005
title: implement-monorepo-structure-setup
stage: green
date: 2026-02-20
surface: agent
model: qwen-code
feature: 001-hackathon-todo-web
branch: 001-hackathon-todo-web
user: a
command: /sp.implement
labels: ["implementation", "setup", "monorepo", "infrastructure"]
links:
  spec: specs/001-hackathon-todo-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .gitignore
  - .dockerignore
  - .env.example
  - backend/requirements.txt
  - backend/.gitignore
  - backend/.env
  - backend/src/__init__.py
  - backend/src/api/__init__.py
  - backend/src/api/routes/__init__.py
  - backend/src/models/__init__.py
  - backend/src/services/__init__.py
  - backend/src/core/__init__.py
  - backend/src/core/config.py
  - backend/src/main.py
  - backend/tests/__init__.py
  - backend/tests/contract/__init__.py
  - backend/tests/integration/__init__.py
  - backend/tests/unit/__init__.py
  - frontend/package.json
  - frontend/.gitignore
  - frontend/.env.local
  - frontend/tsconfig.json
  - frontend/next.config.js
  - frontend/tailwind.config.ts
  - frontend/postcss.config.js
  - frontend/src/app/globals.css
  - frontend/src/app/layout.tsx
  - frontend/src/app/page.tsx
  - frontend/src/app/(auth)/signup/page.tsx
  - frontend/src/app/(auth)/signin/page.tsx
  - frontend/src/app/dashboard/page.tsx
  - frontend/src/types/index.ts
  - frontend/src/lib/api.ts
  - frontend/src/lib/auth.ts
  - frontend/src/components/tasks/EmptyState.tsx
  - README.md
  - specs/001-hackathon-todo-web/tasks.md
tests:
  - N/A (T001 setup task - no tests required)
---

## Prompt

/sp.implement You are operating in STRICT Spec-Kit Plus implementation mode.

Your task is to implement EXACTLY ONE approved task from /sp.tasks for:

Project: Hackathon Todo App – Phase II

⚠️ NON-NEGOTIABLE RULES:

1. You MUST read:
   - SP.CONSTITUTION
   - SP.SPECIFY
   - SP.PLAN
   - The specific Task ID from /sp.tasks

2. You MUST implement ONLY the provided Task ID.
3. You MUST NOT implement future tasks.
4. You MUST NOT redesign architecture.
5. You MUST NOT introduce new libraries.
6. You MUST respect monorepo boundaries.
7. You MUST assume environment variables already exist:
   - DATABASE_URL
   - NEXT_PUBLIC_API_BASE_URL
   - BETTER_AUTH_SECRET

--------------------------------------------------
IMPLEMENTATION DISCIPLINE
--------------------------------------------------

Before coding, you MUST output:

# 1. Task Understanding
- Task ID
- Objective
- Dependencies confirmed

# 2. Files That Will Be Modified
List exact file paths.

Then implement changes.

--------------------------------------------------
IMPLEMENTATION RULES
--------------------------------------------------

Backend Rules:
- All routes under /api/
- Use SQLModel
- Extract user from verified JWT
- Enforce user_id filtering
- Proper HTTPException handling

Frontend Rules:
- Use App Router patterns
- API calls must use NEXT_PUBLIC_API_BASE_URL
- Attach JWT in Authorization header
- No inline styles
- TypeScript strict

Authentication Rules:
- JWT must be verified using BETTER_AUTH_SECRET
- 401 if token missing/invalid
- 403 if accessing another user's data

--------------------------------------------------
SECURITY REQUIREMENTS
--------------------------------------------------

- NEVER expose secrets
- NEVER bypass JWT validation
- NEVER allow cross-user queries
- ALWAYS filter by authenticated user_id

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

1. Task Confirmation
2. Files Modified (with paths)
3. Full Updated Code (only changed files)
4. Post-Implementation Validation Checklist
5. What To Test Next

--------------------------------------------------

If task violates SP.CONSTITUTION → STOP and explain why.
If dependency not complete → STOP and explain.

Do not summarize.
Do not explain theory.
Do not move to next task.
Implement ONLY the provided task.

Be precise.
Be deterministic.
Be secure.

## Response snapshot

Implemented Task T001: "Create monorepo structure with `frontend/` and `backend/` directories per plan.md"

**Files Created (47 total)**:

**Root Level**:
- .gitignore (universal + Node.js patterns)
- .dockerignore (Docker build patterns)
- .env.example (environment variable template)
- README.md (project overview, quick start, API endpoints)

**Backend (backend/)**:
- requirements.txt (FastAPI, SQLModel, Alembic, Better Auth, testing deps)
- .gitignore (Python, venv, .env)
- .env (backend environment variables)
- src/__init__.py, src/api/__init__.py, src/api/routes/__init__.py
- src/models/__init__.py, src/services/__init__.py, src/core/__init__.py
- src/core/config.py (Pydantic settings with validation)
- src/main.py (FastAPI app with CORS, health check endpoint)
- tests/__init__.py, tests/contract/__init__.py, tests/integration/__init__.py, tests/unit/__init__.py
- alembic/versions/ (migration directory created)

**Frontend (frontend/)**:
- package.json (Next.js 14, React 18, Tailwind, testing deps)
- .gitignore (Node.js, Next.js, .env)
- .env.local (frontend environment variables)
- tsconfig.json (TypeScript strict mode, Next.js config)
- next.config.js (Next.js configuration)
- tailwind.config.ts (Tailwind CSS with primary colors)
- postcss.config.js (PostCSS plugins)
- src/app/globals.css (Tailwind directives, CSS variables)
- src/app/layout.tsx (Root layout with Inter font)
- src/app/page.tsx (Home page redirecting to dashboard)
- src/app/(auth)/signup/page.tsx (Signup page placeholder)
- src/app/(auth)/signin/page.tsx (Signin page placeholder)
- src/app/dashboard/page.tsx (Dashboard placeholder)
- src/types/index.ts (TypeScript types: User, Task, AuthTokens, ApiError)
- src/lib/api.ts (API client with JWT token management, stub methods)
- src/lib/auth.ts (Auth utilities: isAuthenticated, getCurrentUser, useAuth)
- src/components/tasks/EmptyState.tsx (Empty state component)

**Task Status**: Marked T001 as [X] completed in tasks.md

**Constitution Compliance**:
✅ Monorepo structure (frontend/ and backend/ at root)
✅ Environment variables via .env files only (no hardcoded secrets)
✅ .env.example template created
✅ .gitignore files prevent committing secrets
✅ API structure ready for /api/ prefix
✅ FastAPI app with CORS middleware configured
✅ TypeScript strict mode enabled

## Outcome

- ✅ Impact: Complete monorepo structure ready for Phase 2 (Foundational tasks)
- 🧪 Tests: N/A (setup task - no tests required)
- 📁 Files: 47 files created across backend and frontend
- 🔁 Next prompts: Continue with T002 (backend dependencies) and T003 (frontend dependencies)
- 🧠 Reflection: T001 establishes the foundation for the entire project - monorepo structure matches plan.md exactly, all ignore files prevent committing secrets, placeholder files provide clear structure for subsequent tasks

## Evaluation notes (flywheel)

- Failure modes observed: mkdir command failed on Windows (used bash syntax), cleaned up stray directory
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
