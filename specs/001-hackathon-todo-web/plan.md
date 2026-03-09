<!--
SYNC IMPACT REPORT
==================
Version Change: N/A (Plan document, not constitution amendment)
Modified Principles: None
Added Sections: N/A
Removed Sections: N/A
Templates Requiring Updates: None
Follow-up TODOs: None
-->

# Implementation Plan: Hackathon Todo App – Phase II (Web Version)

**Branch**: `001-hackathon-todo-web` | **Date**: 2026-02-20 | **Spec**: [specs/001-hackathon-todo-web/spec.md](../001-hackathon-todo-web/spec.md)

**Input**: Feature specification for transforming console-based todo app into multi-user full-stack web application with JWT authentication, persistent storage, and responsive UI.

## Summary

Transform a single-user console todo application into a production-ready, multi-user web application with:
- **Primary Requirement**: Multi-user authentication with JWT-based stateless sessions and complete task CRUD operations with strict user isolation
- **Technical Approach**: Monorepo with Next.js 16+ frontend (App Router, TypeScript, Tailwind) and FastAPI backend (Python, SQLModel, Neon PostgreSQL), using Better Auth for JWT issuance and shared `BETTER_AUTH_SECRET` for verification

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.x (Frontend)

**Primary Dependencies**: 
- Backend: FastAPI, SQLModel, Better Auth, Pydantic, Uvicorn
- Frontend: Next.js 16+, React 18+, Tailwind CSS, Better Auth client

**Storage**: Neon Serverless PostgreSQL (managed via `DATABASE_URL`)

**Testing**: 
- Backend: pytest, httpx (async test client), SQLModel test utilities
- Frontend: Jest, React Testing Library, Playwright (E2E)

**Target Platform**: Web (modern browsers: Chrome, Firefox, Safari, Edge)

**Project Type**: Full-stack web application (monorepo with separate frontend/backend)

**Performance Goals**:
- API p95 latency < 200ms for all endpoints
- Frontend initial page load < 2 seconds
- Task list rendering (100 tasks) < 100ms
- Support 100+ concurrent users

**Constraints**:
- All endpoints under `/api/` prefix
- Stateless JWT authentication (no server-side sessions)
- All queries MUST filter by `user_id` (user isolation)
- Environment variables via `.env` only (no hardcoded secrets)
- HTTPS required in production

**Scale/Scope**:
- Hackathon demonstration (99% uptime during demo period)
- Single tenant (no multi-tenancy requirements)
- MVP feature set (authentication + task CRUD + filtering/sorting)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Principle | Compliance Status | Justification |
|------------------------|-------------------|---------------|
| **I. Stateless JWT Authentication** | ✅ PASS | Better Auth issues stateless JWTs; backend verifies using `BETTER_AUTH_SECRET`; no server-side sessions |
| **I. User Data Isolation** | ✅ PASS | All queries filter by `user_id` extracted from JWT; cross-user exposure prevented via 404 on mismatch |
| **II. No Hardcoded Secrets** | ✅ PASS | All secrets loaded from `.env` (`DATABASE_URL`, `BETTER_AUTH_SECRET`, `NEXT_PUBLIC_API_BASE_URL`) |
| **II. CORS & Request Validation** | ✅ PASS | Pydantic schemas for all endpoints; CORS configured for trusted origins only |
| **II. Audit Logging** | ✅ PASS | Authentication events and write operations logged with user context |
| **III. API Structure** | ✅ PASS | All endpoints under `/api/`; RESTful conventions; implicit user scoping |
| **III. Endpoint Contracts** | ✅ PASS | Explicit request/response schemas; consistent JSON structures; contracts in `specs/###-feature/contracts/` |
| **III. HTTP Status Codes** | ✅ PASS | Standard codes (200/201/204/400/401/403/404/409/500) as specified |
| **IV. Schema Requirements** | ✅ PASS | `tasks` table includes `user_id` FK; SQLModel ORM for all operations |
| **IV. Query Isolation** | ✅ PASS | All queries include `WHERE user_id = :user_id`; repository layer enforces filtering |
| **V. Frontend-Backend Separation** | ✅ PASS | Independent services; API-only communication; no direct DB access from frontend |
| **VI. Monorepo Structure** | ✅ PASS | `frontend/` and `backend/` at root; separate dependency management |
| **VII. Spec-Driven Workflow** | ✅ PASS | Following Spec-Kit Plus: spec → plan → tasks → implementation |
| **VIII. Error Handling** | ✅ PASS | Structured JSON errors with `status_code`, `error_type`, `message`, `details` |
| **IX. Environment Variables** | ✅ PASS | Required vars documented; validated at startup; `.env.example` provided |
| **X. Simplicity (YAGNI)** | ✅ PASS | MVP scope; no unnecessary abstractions; simplest viable solution |

**GATE RESULT**: ✅ ALL PRINCIPLES PASS — Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-hackathon-todo-web/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology research)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (OpenAPI schemas)
│   ├── auth.yaml        # Authentication endpoint contracts
│   └── tasks.yaml       # Task endpoint contracts
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
<root>/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py      # Signup, signin, signout endpoints
│   │   │   │   └── tasks.py     # CRUD task endpoints
│   │   │   ├── deps.py          # Dependencies (JWT verification, user extraction)
│   │   │   └── error_handlers.py # Global exception handlers
│   │   ├── models/
│   │   │   ├── user.py          # User model (Better Auth managed)
│   │   │   └── task.py          # Task model with user_id FK
│   │   ├── services/
│   │   │   ├── auth.py          # Authentication service layer
│   │   │   └── tasks.py         # Task service with user isolation
│   │   ├── core/
│   │   │   ├── config.py        # Environment configuration
│   │   │   └── security.py      # JWT verification utilities
│   │   └── main.py              # FastAPI app initialization
│   ├── tests/
│   │   ├── contract/            # API contract tests
│   │   ├── integration/         # Integration tests (auth + CRUD)
│   │   └── unit/                # Unit tests (services, models)
│   ├── alembic/                 # Database migrations
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Backend environment variables
│
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router
│   │   │   ├── (auth)/
│   │   │   │   ├── signin/
│   │   │   │   └── signup/
│   │   │   ├── dashboard/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   ├── tasks/
│   │   │   └── ui/
│   │   ├── lib/
│   │   │   ├── api.ts           # API client with JWT injection
│   │   │   └── auth.ts          # Auth client (Better Auth)
│   │   └── types/
│   │       └── index.ts         # TypeScript types
│   ├── tests/
│   │   ├── components/          # Component tests
│   │   └── e2e/                 # Playwright E2E tests
│   ├── public/
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── package.json
│   └── .env.local               # Frontend environment variables
│
├── specs/
│   └── 001-hackathon-todo-web/  # Feature documentation
│
├── .specify/                    # Spec-Kit Plus configuration
├── .env.example                 # Template for environment variables
├── .gitignore
└── README.md
```

**Structure Decision**: Monorepo with `frontend/` and `backend/` directories at repository root. This structure:
- Enables independent deployment of frontend and backend
- Maintains clear separation of concerns (constitution Principle V)
- Allows separate dependency management (npm for frontend, pip for backend)
- Supports team parallelism (different developers can work on each side)

## Complexity Tracking

> **No constitution violations** — All principles pass. Complexity tracking not required.

---

## Phase Overview

The implementation is divided into 7 logical phases, sequenced to minimize risk and enable incremental validation:

| Phase | Name | Duration (Est.) | Primary Outcome |
|-------|------|-----------------|-----------------|
| 1 | Foundation Setup | 0.5 days | Project structure, environment config, dependency installation |
| 2 | Backend Core | 1 day | Database schema, models, migrations, basic API scaffolding |
| 3 | Auth Integration | 1 day | Better Auth setup, JWT issuance, token verification middleware |
| 4 | Secure API Enforcement | 1 day | User isolation in services, 401/403 enforcement, audit logging |
| 5 | Frontend Integration | 2 days | Auth UI, task CRUD UI, API client, responsive design |
| 6 | System Validation | 1 day | Integration tests, E2E tests, security validation, performance testing |
| 7 | Deployment Readiness | 0.5 days | Production config, health checks, documentation, runbooks |

**Total Estimated Duration**: 7 days (MVP ready for hackathon demonstration)

---

## Phase-by-Phase Strategy

### Phase 1: Foundation Setup

**Objective**: Establish monorepo structure, install dependencies, configure environment variables.

**Scope**:
- Create `frontend/` and `backend/` directory structure
- Initialize Next.js 16+ project with TypeScript and Tailwind
- Initialize FastAPI project with SQLModel
- Copy `.env` variables to both projects
- Create `.env.example` template
- Set up `.gitignore` for both projects

**Dependencies**: None (foundational phase)

**Success Criteria**:
- ✅ `frontend/package.json` and `backend/requirements.txt` created
- ✅ Environment variables accessible in both projects
- ✅ Basic "Hello World" endpoints return 200
- ✅ No secrets committed to version control

**Risks**:
- **Low**: Standard project initialization; well-documented tooling

---

### Phase 2: Backend Core

**Objective**: Implement database schema, models, and migrations.

**Scope**:
- Define `User` model (Better Auth managed)
- Define `Task` model with `user_id` foreign key
- Configure SQLModel with Neon PostgreSQL
- Create Alembic migrations for initial schema
- Implement database connection pooling
- Create basic health check endpoint

**Dependencies**: Phase 1 complete

**Success Criteria**:
- ✅ Database migrations run successfully
- ✅ `tasks` table includes `user_id` FK with `ON DELETE CASCADE`
- ✅ Health check endpoint (`/api/health`) returns 200 with DB status
- ✅ Indexes created on `user_id` and `user_id + completed`

**Risks**:
- **Low**: SQLModel and Alembic are mature tools
- **Medium**: Neon PostgreSQL connection issues (mitigation: verify connection string, SSL mode)

---

### Phase 3: Auth Integration

**Objective**: Implement Better Auth integration and JWT verification middleware.

**Scope**:
- Configure Better Auth with shared `BETTER_AUTH_SECRET`
- Implement `/api/auth/signup` endpoint
- Implement `/api/auth/signin` endpoint
- Implement `/api/auth/signout` endpoint (client-side notification)
- Create JWT verification dependency (`get_current_user`)
- Extract `user_id` from JWT token payload
- Implement token expiry validation

**Dependencies**: Phase 2 complete (database ready)

**Success Criteria**:
- ✅ Signup creates user and returns JWT
- ✅ Signin validates credentials and returns JWT
- ✅ Protected endpoints reject requests without valid JWT (401)
- ✅ `user_id` correctly extracted from token for all requests
- ✅ Token expiry enforced (default: 7 days)

**Risks**:
- **Medium**: JWT verification edge cases (mitigation: comprehensive contract tests)
- **Medium**: Better Auth configuration (mitigation: follow official documentation)

---

### Phase 4: Secure API Enforcement

**Objective**: Implement task CRUD with strict user isolation and security hardening.

**Scope**:
- Implement `/api/tasks` GET (list with filtering/sorting)
- Implement `/api/tasks` POST (create)
- Implement `/api/tasks/:id` GET (single)
- Implement `/api/tasks/:id` PUT/PATCH (update)
- Implement `/api/tasks/:id` DELETE (delete)
- Enforce `WHERE user_id = :user_id` in all queries
- Return 404 for tasks belonging to other users
- Implement structured error responses
- Add audit logging for all write operations
- Configure CORS for trusted origins

**Dependencies**: Phase 3 complete (auth working)

**Success Criteria**:
- ✅ All CRUD endpoints functional with JWT auth
- ✅ User A cannot access User B's tasks (404 returned)
- ✅ Filtering by status works correctly
- ✅ Sorting by `created_at` and `title` works
- ✅ Error responses follow contract (`status_code`, `error_type`, `message`)
- ✅ Audit logs capture all CREATE/UPDATE/DELETE operations

**Risks**:
- **High**: User isolation bugs (mitigation: contract tests, integration tests, manual validation)
- **Medium**: CORS misconfiguration (mitigation: test with frontend early)

---

### Phase 5: Frontend Integration

**Objective**: Build responsive UI with authentication flows and task management.

**Scope**:
- Create signin/signup pages with form validation
- Implement JWT storage (httpOnly cookie or secure storage)
- Create API client with automatic JWT injection
- Build task dashboard layout
- Implement task creation form
- Implement task list with completion toggles
- Implement task edit/delete actions
- Implement filter/sort controls
- Add loading states and error feedback
- Ensure responsive design (mobile/tablet/desktop)
- Implement accessibility features (keyboard nav, ARIA)

**Dependencies**: Phase 4 complete (API ready)

**Success Criteria**:
- ✅ Users can sign up and sign in
- ✅ JWT automatically attached to all API requests
- ✅ Task CRUD operations functional from UI
- ✅ Filter/sort controls update task list
- ✅ Responsive layout works on all screen sizes
- ✅ Loading states and error messages displayed
- ✅ Keyboard navigation works (Tab, Enter, Escape)

**Risks**:
- **Medium**: JWT storage security (mitigation: use httpOnly cookies if possible)
- **Medium**: State management complexity (mitigation: keep simple, use React state)
- **Low**: Responsive design (mitigation: Tailwind breakpoints)

---

### Phase 6: System Validation

**Objective**: Comprehensive testing and security validation.

**Scope**:
- Backend unit tests (services, models)
- API contract tests (all endpoints)
- Integration tests (auth + CRUD flows)
- Frontend component tests
- E2E tests (Playwright: signup → CRUD → signout)
- Security validation (user isolation, JWT expiry, input validation)
- Performance testing (p95 latency < 200ms)
- Accessibility testing (WCAG AA)

**Dependencies**: Phase 5 complete (full system functional)

**Success Criteria**:
- ✅ All unit tests pass
- ✅ All contract tests pass
- ✅ All integration tests pass
- ✅ E2E flow completes successfully
- ✅ User isolation validated (no cross-user data exposure)
- ✅ p95 latency < 200ms for all endpoints
- ✅ Accessibility audit passes (WCAG AA)

**Risks**:
- **Medium**: Test failures reveal architectural issues (mitigation: fix before proceeding)
- **Low**: Performance issues (mitigation: optimize queries, add caching if needed)

---

### Phase 7: Deployment Readiness

**Objective**: Prepare for production deployment.

**Scope**:
- Production environment configuration
- Health check endpoint validation
- Error monitoring setup (logging, alerting)
- Deployment runbook creation
- Rollback procedure documentation
- Final security review
- Performance baseline documentation
- User documentation (quickstart)

**Dependencies**: Phase 6 complete (all tests passing)

**Success Criteria**:
- ✅ Production `.env` template complete
- ✅ Health check returns 200 with all dependencies
- ✅ Logging captures all errors with user context
- ✅ Runbook documents deployment steps
- ✅ Rollback procedure tested
- ✅ Security review passes (no critical issues)
- ✅ Performance baseline documented

**Risks**:
- **Low**: Deployment configuration (mitigation: test in staging first)
- **Low**: Documentation gaps (mitigation: peer review)

---

## Technical Sequencing Justification

### Why Backend Precedes Frontend

1. **API Contract First**: Frontend depends on stable API contracts; building backend first ensures contracts are validated before UI implementation
2. **Authentication Foundation**: JWT issuance and verification must be functional before frontend can make authenticated requests
3. **Parallel Development**: Once API contracts are stable, frontend and backend can proceed in parallel for remaining features
4. **Risk Mitigation**: Backend bugs (especially in auth and user isolation) are harder to debug through frontend; isolate complexity early

### Why JWT Enforcement Precedes CRUD Exposure

1. **Security First**: Exposing CRUD endpoints without authentication creates security vulnerabilities; JWT enforcement is a constitution requirement (Principle I)
2. **User Context**: All CRUD operations require `user_id` from JWT; without auth middleware, user isolation cannot be enforced
3. **Testing Dependency**: Integration tests require valid tokens; implementing auth first enables comprehensive testing
4. **Constitution Compliance**: Principle I mandates "No request allowed without valid JWT" — this must be enforced before any protected endpoints are exposed

### Why User Isolation Must Be Validated Before UI Completion

1. **Security-Critical**: Cross-user data exposure is a critical vulnerability; must be validated before any user data is visible in UI
2. **API Contract Stability**: UI depends on correct API behavior; if user isolation logic changes, UI may need updates
3. **Test-Driven Validation**: Contract and integration tests for user isolation should pass before UI development completes
4. **Risk Containment**: Finding user isolation bugs after UI completion requires rework in both backend and frontend; catch early

---

## Environment & Configuration Strategy

### Environment Variables

| Variable | Used By | Purpose | Example |
|----------|---------|---------|---------|
| `DATABASE_URL` | Backend | Neon PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| `NEXT_PUBLIC_API_BASE_URL` | Frontend | Backend API base URL | `http://localhost:8000` (dev), `https://api.example.com` (prod) |
| `BETTER_AUTH_SECRET` | Both | Shared secret for JWT signing/verification | 32+ character random string |

### Configuration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Environment Variables                    │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│      Backend          │       │       Frontend        │
│  - DATABASE_URL       │       │  - NEXT_PUBLIC_API_   │
│  - BETTER_AUTH_SECRET │       │    BASE_URL           │
│                       │       │  - BETTER_AUTH_SECRET │
│  FastAPI App          │       │  Next.js App          │
│  - Verify JWT         │◄──────│  - Send JWT in        │
│  - Extract user_id    │  API  │    Authorization      │
│  - Filter by user_id  │       │    header             │
└───────────────────────┘       └───────────────────────┘
```

### Local vs Production Configuration

**Local Development**:
- `.env` files in `frontend/` and `backend/` root
- `DATABASE_URL`: Neon dev database
- `NEXT_PUBLIC_API_BASE_URL`: `http://localhost:8000`
- `BETTER_AUTH_SECRET`: Same value in both projects (can be dev secret)

**Production**:
- Environment variables set via deployment platform (Vercel, Railway, etc.)
- `DATABASE_URL`: Neon production database
- `NEXT_PUBLIC_API_BASE_URL`: Production API URL (HTTPS)
- `BETTER_AUTH_SECRET`: Secure 32+ character secret (never committed)

**Configuration Discipline**:
- ✅ Use `.env.example` as template for new developers
- ✅ Validate required env vars at startup (fail fast)
- ✅ Never commit `.env` files (listed in `.gitignore`)
- ✅ Use same `BETTER_AUTH_SECRET` in both frontend and backend

---

## Security Hardening Plan

### JWT Validation Flow

```
1. User submits credentials → /api/auth/signin
2. Better Auth validates → issues JWT (signed with BETTER_AUTH_SECRET)
3. Frontend stores JWT (httpOnly cookie or secure storage)
4. Frontend sends JWT in Authorization: Bearer <token> header
5. Backend middleware verifies:
   - Signature matches BETTER_AUTH_SECRET
   - Token not expired (exp claim)
   - Token not malformed
6. Backend extracts user_id from token payload
7. Request proceeds with user context
```

### 401/403 Enforcement

| Scenario | Response Code | Error Type | Message |
|----------|---------------|------------|---------|
| Missing `Authorization` header | 401 | `AuthenticationError` | "Authentication required" |
| Invalid JWT signature | 401 | `AuthenticationError` | "Invalid token" |
| Expired JWT | 401 | `AuthenticationError` | "Token expired" |
| Malformed JWT | 401 | `AuthenticationError` | "Invalid token format" |
| User A accesses User B's task | 404 | `NotFoundError` | "Resource not found" |
| User lacks permission | 403 | `AuthorizationError` | "Insufficient permissions" |

**Note**: User isolation violations return 404 (not 403) to avoid revealing existence of other users' resources.

### Cross-User Data Prevention

**Defense in Depth**:

1. **API Layer**: `get_current_user` dependency extracts `user_id` from JWT
2. **Service Layer**: All service methods accept `user_id` parameter
3. **Repository Layer**: All queries include `WHERE user_id = :user_id`
4. **Database Layer**: Foreign key constraint on `tasks.user_id`
5. **Test Layer**: Contract tests validate user isolation (User A cannot access User B's data)

**Validation Checklist**:
- ✅ All endpoints require JWT (except `/api/auth/signup`, `/api/auth/signin`)
- ✅ `user_id` extracted from JWT, never from request body
- ✅ All queries include `WHERE user_id = :user_id`
- ✅ 404 returned for tasks belonging to other users
- ✅ Integration tests validate cross-user isolation

### Token Expiry Handling

**Default Expiry**: 7 days (configurable)

**Frontend Behavior**:
- Check token expiry before API requests
- If expired → redirect to signin page
- Display user-friendly message: "Your session has expired. Please sign in again."

**Backend Behavior**:
- JWT verification checks `exp` claim
- Expired tokens → 401 Unauthorized
- No automatic token refresh (out of scope for MVP)

---

## Testing & Validation Strategy

### Testing Pyramid

```
                    /\
                   /  \
                  / E2E \         (Playwright: full user flows)
                 /--------\
                /Integration\      (httpx: API + database)
               /--------------\
              /     Unit       \    (pytest: services, models)
             /------------------\
```

### API Testing

**Contract Tests** (per endpoint):
- Valid request → correct response schema
- Missing auth → 401
- Invalid payload → 400
- Resource not found → 404
- Cross-user access → 404

**Integration Tests**:
- Signup → signin → CRUD → signout flow
- Filter/sort correctness
- Token expiry handling

### Auth Flow Validation

**Test Scenarios**:
1. Valid signup → JWT issued
2. Valid signin → JWT issued
3. Invalid credentials → 401
4. Expired token → 401
5. Missing token → 401
6. Malformed token → 401

### User Isolation Validation

**Test Matrix**:

| Test | Setup | Action | Expected |
|------|-------|--------|----------|
| T1 | User A has 3 tasks | User A lists tasks | Returns 3 tasks |
| T2 | User A has 3 tasks | User B lists tasks | Returns 0 tasks |
| T3 | User A has task T1 | User A gets T1 | Returns T1 |
| T4 | User A has task T1 | User B gets T1 | Returns 404 |
| T5 | User A has task T1 | User B deletes T1 | Returns 404, T1 unchanged |
| T6 | User A has task T1 | User A updates T1 | T1 updated, user_id unchanged |

### Integration Testing

**Full Flow Tests**:
1. User signup → signin → create task → list tasks → update task → delete task → signout
2. User signin → create multiple tasks → filter by status → sort by date → signout
3. User signin → create task → token expires → any API request → 401 → redirect to signin

### Failure Case Testing

**Error Scenarios**:
- Database connection failure → 500 with structured error
- Invalid request payload → 400 with field-level errors
- Concurrent updates to same resource → last-write-wins or optimistic locking
- Network timeout → frontend displays retry option

---

## Deployment Readiness Criteria

### Measurable Criteria

| Criterion | Target | Measurement Method |
|-----------|--------|-------------------|
| **Test Coverage** | >80% | `pytest --cov`, `npm run test:coverage` |
| **API Latency (p95)** | <200ms | Load testing with `locust` or `k6` |
| **Frontend Load Time** | <2s | Lighthouse, WebPageTest |
| **Zero Cross-User Exposure** | 0 incidents | Security audit, penetration testing |
| **Uptime** | 99% during demo | Monitoring (UptimeRobot, Pingdom) |
| **Error Rate** | <1% of requests | Log analysis, error tracking |
| **Accessibility** | WCAG AA | axe DevTools, manual audit |
| **Security** | No critical issues | OWASP ZAP scan, manual review |

### Pre-Deployment Checklist

- ✅ All tests passing (unit, integration, E2E)
- ✅ Performance benchmarks met
- ✅ Security audit complete (no critical issues)
- ✅ Environment variables documented in `.env.example`
- ✅ Production database migrations tested
- ✅ Health check endpoint functional
- ✅ Logging captures all errors with user context
- ✅ Rollback procedure documented and tested
- ✅ Runbook created (deployment steps, troubleshooting)
- ✅ Monitoring/alerting configured

### Rollback Strategy

**Trigger Conditions**:
- Critical security vulnerability discovered
- Data corruption or loss
- >5% error rate in production
- Performance degradation (>500ms p95)

**Rollback Steps**:
1. Deploy previous stable version (git checkout + redeploy)
2. Run database rollback migrations (if schema changed)
3. Verify health check passes
4. Notify stakeholders
5. Post-mortem analysis

---

## Constitution Re-Check (Post-Design)

*GATE: Must pass before Phase 2 (tasks). Re-evaluate after design decisions.*

| Constitution Principle | Design Decision | Compliance |
|------------------------|-----------------|------------|
| **I. Stateless JWT** | Better Auth + shared secret verification | ✅ PASS |
| **I. User Isolation** | `user_id` from JWT, filtered in all queries | ✅ PASS |
| **II. No Hardcoded Secrets** | All secrets via `.env` | ✅ PASS |
| **II. CORS & Validation** | Pydantic schemas, CORS middleware | ✅ PASS |
| **II. Audit Logging** | Write operations logged with user context | ✅ PASS |
| **III. API Structure** | All endpoints under `/api/` | ✅ PASS |
| **III. Endpoint Contracts** | OpenAPI schemas in `contracts/` | ✅ PASS |
| **IV. Schema Requirements** | `tasks.user_id` FK, SQLModel ORM | ✅ PASS |
| **IV. Query Isolation** | Repository enforces `WHERE user_id` | ✅ PASS |
| **V. Frontend-Backend Separation** | Independent services, API-only | ✅ PASS |
| **VI. Monorepo** | `frontend/` + `backend/` at root | ✅ PASS |
| **VII. Spec-Driven** | Following Spec-Kit Plus workflow | ✅ PASS |
| **VIII. Error Handling** | Structured JSON errors | ✅ PASS |
| **IX. Environment Variables** | Validated at startup, documented | ✅ PASS |
| **X. Simplicity** | MVP scope, no unnecessary abstractions | ✅ PASS |

**GATE RESULT**: ✅ ALL PRINCIPLES PASS — Proceed to `/sp.tasks`

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| User isolation bug | Critical | Low | Contract tests, integration tests, security audit |
| JWT secret mismatch | High | Low | Document setup clearly, validate at startup |
| CORS misconfiguration | Medium | Medium | Test with frontend early, use wildcard in dev only |
| Database connection issues | High | Low | Use connection pooling, test SSL mode, verify connection string |
| Token storage XSS | High | Low | Use httpOnly cookies, sanitize all user input |
| Performance degradation | Medium | Low | Load test early, optimize queries, add indexes |

---

## Next Steps

1. **Run `/sp.tasks`**: Generate task breakdown for implementation
2. **Create `research.md`**: Document technology decisions (if any unclear)
3. **Create `data-model.md`**: Define entity schemas and relationships
4. **Create `contracts/`**: Generate OpenAPI schemas for all endpoints
5. **Create `quickstart.md`**: Write setup instructions for developers

---

**Plan Status**: ✅ Complete — Ready for task breakdown

**Artifacts Generated**:
- `specs/001-hackathon-todo-web/plan.md` (this file)
- Pending: `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`

**Branch**: `001-hackathon-todo-web`
