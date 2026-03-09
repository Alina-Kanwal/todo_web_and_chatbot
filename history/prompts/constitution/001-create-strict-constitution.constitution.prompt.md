---
id: 001
title: create-strict-constitution
stage: constitution
date: 2026-02-20
surface: agent
model: qwen-code
feature: none
branch: main
user: a
command: /sp.constitution
labels: ["constitution", "architecture", "security", "authentication", "monorepo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document creation)
---

## Prompt

/sp.constitution You are an expert Spec-Driven Development Architect.

Create a strict SP.CONSTITUTION document for a Full-Stack Monorepo project named "Hackathon Todo App Phase II".

⚠️ Rules:
- Follow Spec-Kit Plus conventions.
- Output must be clean Markdown.
- No implementation code.
- No assumptions outside provided requirements.
- Define architectural laws that cannot be violated.

----------------------------------
PROJECT CONTEXT
----------------------------------

This project transforms a console todo app into a modern multi-user web application.

Tech Stack:
- Frontend: Next.js 16+ (App Router, TypeScript, Tailwind)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Spec-Driven: Spec-Kit Plus
- Monorepo structure

Authentication Model:
- Better Auth issues JWT tokens.
- JWT is sent via Authorization: Bearer <token>.
- Backend verifies token using shared BETTER_AUTH_SECRET.
- All endpoints must filter by authenticated user.
- No request allowed without valid JWT.

API Structure:
All endpoints under /api/
CRUD for tasks.
User isolation strictly enforced.

Database Rules:
- tasks table contains user_id foreign key.
- All queries must filter by user_id.
- No cross-user data exposure allowed.

----------------------------------
YOUR TASK
----------------------------------

Generate a strict SP.CONSTITUTION document that defines:

1. Architectural Principles
2. Security Laws
3. API Design Laws
4. Database Integrity Laws
5. Authentication & JWT Laws
6. Frontend–Backend Separation Rules
7. Spec-Driven Workflow Enforcement
8. Monorepo Governance Rules
9. Error Handling Standards
10. Deployment & Environment Variable Rules

The constitution must:
- Be authoritative and strict.
- Use MUST / MUST NOT language.
- Prevent architectural drift.
- Enforce stateless authentication.
- Enforce user data isolation.

Do NOT generate specs.
Do NOT generate code.
Do NOT generate plan.
Only generate the SP.CONSTITUTION document.

Be precise. Be strict. No fluff.

## Response snapshot

Created strict SP.CONSTITUTION document at `.specify/memory/constitution.md` with 10 core principles:

1. **Authentication & JWT Laws**: Stateless JWT authentication, user data isolation
2. **Security Laws**: No hardcoded secrets, CORS validation, audit logging
3. **API Design Laws**: `/api/` prefix, RESTful conventions, explicit contracts, HTTP status codes
4. **Database Integrity Laws**: Schema requirements, query isolation, migration policy
5. **Frontend-Backend Separation Rules**: Clear boundaries, API-only communication
6. **Monorepo Governance Rules**: Repository structure, dependency management, branch naming
7. **Spec-Driven Workflow Enforcement**: Spec-Kit Plus compliance, documentation requirements
8. **Error Handling Standards**: Structured error responses, logging requirements
9. **Deployment & Environment Variable Rules**: Environment validation, deployment isolation
10. **Architectural Principles**: Simplicity (YAGNI), testability, observability, incremental delivery

Version: 1.0.0 (initial constitution), ratified 2026-02-20.

## Outcome

- ✅ Impact: Established authoritative constitution preventing architectural drift for Full-Stack Monorepo
- 🧪 Tests: N/A (constitution document - compliance verified via PR reviews)
- 📁 Files: `.specify/memory/constitution.md` created
- 🔁 Next prompts: Consider running `/sp.adr` for any significant architectural decisions
- 🧠 Reflection: Constitution uses MUST/MUST NOT language throughout, enforces stateless JWT auth and user isolation as non-negotiable principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
