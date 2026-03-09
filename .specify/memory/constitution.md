<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0 (Authentication Implementation)
Modified Principles:
  - I. Authentication & JWT Laws (updated with implementation details)
  - II. Security Laws (added password requirements)
  - IX. Deployment & Environment Variable Rules (added SQLite for dev)
Added Sections:
  - XI. Frontend Authentication Rules
  - XII. Development Workflow Rules
Templates Requiring Updates:
  - .specify/templates/plan-template.md ✅ No updates needed
  - .specify/templates/spec-template.md ✅ No updates needed
  - .specify/templates/tasks-template.md ✅ No updates needed
Follow-up TODOs: None
-->

# Hackathon Todo App Phase II Constitution

## Core Principles

### I. Authentication & JWT Laws

**Stateless JWT Authentication (NON-NEGOTIABLE)**

All authentication MUST use stateless JWT tokens. The backend MUST verify tokens using the shared `BETTER_AUTH_SECRET` with HS256 algorithm. No session state MAY be stored on the server. Every request to protected endpoints MUST include a valid JWT in the `Authorization: Bearer <token>` header. Requests without valid tokens MUST be rejected with 401 Unauthorized.

**Rationale:** Stateless authentication ensures horizontal scalability, eliminates session synchronization complexity, and enables independent service deployment.

**JWT Token Structure**

All JWT tokens MUST contain:
- `user_id`: Integer user identifier
- `email`: User email address
- `exp`: Expiration timestamp (default: 7 days from issuance)

**Token Expiry**

JWT tokens MUST expire after 7 days (10080 minutes). Expired tokens MUST return 401 Unauthorized. Clients MUST redirect users to signin upon token expiry. Token refresh is out of scope; users must re-authenticate.

**User Data Isolation (NON-NEGOTIABLE)**

All database queries MUST filter by the authenticated user's `user_id`. No endpoint MAY return data belonging to another user. Cross-user data exposure is strictly prohibited. The `user_id` MUST be extracted from the verified JWT and used in every database operation. Backend services MUST validate that the `user_id` in the request context matches the `user_id` on the target resource for write operations.

**Rationale:** User isolation is a security-critical requirement. Explicit filtering at every query layer prevents unauthorized data access.

### II. Security Laws

**No Hardcoded Secrets**

Secrets (API keys, database URLs, auth secrets) MUST be loaded from environment variables via `.env` files. No secret MAY be committed to version control. The `.env` file MUST be listed in `.gitignore`. Secrets MUST be documented in a `.env.example` file with placeholder values.

**Password Requirements**

All passwords MUST:
- Be minimum 8 characters in length
- Be hashed using bcrypt before storage
- Never be logged or transmitted in plain text outside HTTPS

**CORS & Request Validation**

All API endpoints MUST validate request payloads against explicit schemas. Unexpected fields MUST be rejected. CORS policies MUST be configured to allow only trusted origins in production. Input sanitization MUST be applied to all user-provided data before database operations.

**Audit Logging**

All authentication events (login, logout, token refresh, failed attempts) MUST be logged with timestamps and IP addresses. All write operations (CREATE, UPDATE, DELETE) MUST be logged with user context for audit trails.

### III. API Design Laws

**API Structure**

All API endpoints MUST be prefixed with `/api/`. Endpoints MUST follow RESTful conventions. Task endpoints MUST be scoped to the authenticated user implicitly (no `user_id` in path). Example: `GET /api/tasks` returns only the requesting user's tasks.

**Authentication Endpoints**

The following endpoints MUST NOT require authentication:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login

The following endpoints MUST require authentication:
- `POST /api/auth/signout` - User logout (for audit logging)
- `GET /api/auth/me` - Get current user info
- All `/api/tasks/*` endpoints

**Endpoint Contracts**

All endpoints MUST define explicit request/response schemas using Pydantic. Success responses MUST return consistent JSON structures. Error responses MUST include: `status_code`, `error_type`, `message`, and optional `details`. All endpoints MUST document their contracts in `specs/###-feature/contracts/`.

**HTTP Status Codes**

- 200: Successful GET/PUT/PATCH
- 201: Successful POST (resource created)
- 204: Successful DELETE (no content)
- 400: Bad Request (validation error)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (user lacks permission)
- 404: Not Found (resource doesn't exist or belongs to another user)
- 409: Conflict (duplicate resource, constraint violation)
- 500: Internal Server Error

**Idempotency**

PUT and DELETE operations MUST be idempotent. POST operations creating resources MUST check for duplicates to prevent unintended duplication on retry.

### IV. Database Integrity Laws

**Schema Requirements**

The `users` table MUST include:
- `id`: Primary key (auto-increment integer)
- `email`: Unique, indexed, NOT NULL
- `password_hash`: NOT NULL (bcrypt hash)
- `created_at`: Timestamp, NOT NULL
- `updated_at`: Timestamp, nullable

The `tasks` table MUST include:
- `id`: Primary key (auto-increment integer)
- `user_id`: Foreign key referencing users.id, indexed, NOT NULL
- `title`: VARCHAR(500), NOT NULL
- `description`: TEXT, nullable
- `completed`: BOOLEAN, default false, NOT NULL
- `created_at`: Timestamp, auto-generated, NOT NULL
- `updated_at`: Timestamp, auto-updated on modification

**Query Isolation**

No query MAY omit the `user_id` filter. Repository/service layers MUST enforce user filtering at the method level. Bulk operations MUST validate that all affected records belong to the authenticated user.

**Migration Policy**

All schema changes MUST be versioned via Alembic migrations. Migrations MUST be reversible (include downgrade paths). Production migrations MUST be tested in a staging environment first.

**Database Configuration**

Development MAY use SQLite for local testing. Production MUST use Neon PostgreSQL with SSL. Database URLs MUST be configured via `DATABASE_URL` environment variable.

### V. Frontend-Backend Separation Rules

**Clear Boundaries**

Frontend (Next.js) and Backend (FastAPI) MUST be deployed as independent services. Frontend MUST NOT access the database directly. All data access MUST occur via API calls. Backend MUST NOT serve frontend assets.

**API-Only Communication**

Frontend MUST communicate with backend exclusively through defined API contracts. No direct service-to-service imports MAY cross the boundary. Shared types MUST be documented, not imported across the boundary.

**State Management**

Frontend MUST manage its own client-side state using localStorage for JWT tokens. Backend MUST remain stateless between requests. No server-side session state MAY be assumed.

### VI. Monorepo Governance Rules

**Repository Structure**

```
<root>/
├── frontend/          # Next.js 16+ application
├── backend/           # FastAPI application
├── specs/             # Feature specifications
├── .specify/          # Spec-Kit Plus configuration
├── history/           # PHRs and ADRs
└── docs/              # Shared documentation
```

**Dependency Management**

Frontend and backend dependencies MUST be managed separately. No cross-contamination of package managers (npm/pnpm for frontend, pip/poetry for backend). Shared configuration MUST be documented, not duplicated.

**Branch Naming**

Feature branches MUST follow the pattern: `###-feature-name` (e.g., `001-user-authentication`). PRs MUST reference the feature specification path.

### VII. Spec-Driven Workflow Enforcement

**Spec-Kit Plus Compliance**

All features MUST follow Spec-Kit Plus workflow:
1. Constitution check (`.specify/memory/constitution.md`)
2. Specification (`specs/###-feature/spec.md`)
3. Plan (`specs/###-feature/plan.md`)
4. Tasks (`specs/###-feature/tasks.md`)
5. Implementation (tasks → tests → code)
6. Prompt History Record (`history/prompts/`)

**Documentation Requirements**

No feature MAY be implemented without a specification. All architectural decisions MUST be documented in ADRs (`history/adr/`). All user interactions MUST be captured in PHRs.

**Test-First Discipline**

Tests MUST be written before implementation code when tests are requested. Red-Green-Refactor cycle MUST be followed. Contract tests MUST validate API boundaries.

### VIII. Error Handling Standards

**Structured Error Responses**

All API errors MUST return JSON with:
```json
{
  "status_code": 400,
  "error_type": "ValidationError",
  "message": "Human-readable description",
  "details": {}  // Optional context
}
```

**Error Classification**

- **Client Errors (4xx)**: Validation failures, authentication errors, permission denials
- **Server Errors (5xx)**: Database failures, external service failures, unhandled exceptions

**Logging Requirements**

All errors MUST be logged with: timestamp, user_id (if authenticated), request path, error type, stack trace (server-side only). Sensitive data (passwords, tokens) MUST NOT be logged.

**Graceful Degradation**

Non-critical failures (logging errors, audit failures) MUST NOT cause request failures. Critical failures (auth, database) MUST fail fast with clear error messages.

### IX. Deployment & Environment Variable Rules

**Environment Variables**

Required backend variables MUST be documented in `.env`:
- `DATABASE_URL`: Database connection string (SQLite for dev, PostgreSQL for prod)
- `BETTER_AUTH_SECRET`: Shared secret for JWT verification (min 32 chars)
- `allowed_origins`: Comma-separated CORS origins
- `app_name`: Application name
- `debug`: Debug mode flag

Required frontend variables MUST be documented in `.env.local`:
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL

**Configuration Validation**

Applications MUST validate required environment variables at startup. Missing variables MUST cause immediate failure with clear error messages. Default values MUST NOT be used for security-critical configuration.

**Deployment Isolation**

Development, staging, and production environments MUST use separate databases and secrets. No shared state between environments.

**Health Checks**

Backend MUST expose `/api/health` endpoint for deployment verification. Health checks MUST return service status and version.

### X. Architectural Principles

**Simplicity (YAGNI)**

No abstraction MAY be added without a concrete, immediate need. Start with the simplest solution that works. Complexity MUST be justified in the implementation plan.

**Testability**

All code MUST be independently testable. Services MUST accept dependencies as parameters (dependency injection). No hidden global state.

**Observability**

All user-facing operations MUST be traceable via logs. Performance-critical operations MUST be measurable. Debugging MUST be possible via logs alone.

**Incremental Delivery**

Features MUST be deliverable in independent slices. Each user story MUST provide standalone value. MVP delivery MUST be possible after any user story completion.

### XI. Frontend Authentication Rules

**Token Storage**

JWT tokens MUST be stored in browser localStorage. Tokens MUST be retrieved and attached to all API requests automatically via the API client.

**Authentication Flow**

1. Signup: Create account → receive JWT → store token → redirect to dashboard
2. Signin: Authenticate → receive JWT → store token → redirect to dashboard
3. Signout: Clear token → redirect to signin page

**Protected Routes**

All routes except `/signin` and `/signup` MUST require authentication. Unauthenticated users MUST be redirected to `/signin`.

**Client-Side Validation**

Frontend MUST validate:
- Email format before submission
- Password length (min 8 characters)
- Password confirmation match
- Required fields are not empty

**Loading States**

All async operations MUST display loading states. Buttons MUST be disabled during submission. Users MUST receive clear feedback on success/error.

### XII. Development Workflow Rules

**Local Development**

Developers MAY use SQLite for local development to avoid database setup complexity. Production configurations MUST be tested before deployment.

**Starting Development Servers**

Use `start-dev.bat` (Windows) to start both frontend and backend servers simultaneously. Backend runs on port 8000, frontend on port 3000.

**API Documentation**

Backend MUST maintain auto-generated OpenAPI docs at `/docs`. All endpoints MUST be testable via the Swagger UI.

**Code Style**

Backend Python code MUST follow PEP 8. Frontend TypeScript code MUST follow project ESLint rules. All code MUST pass linting before commit.

## Governance

**Compliance Verification**

All PRs MUST include a constitution compliance checklist. Reviewers MUST verify adherence to principles. Violations MUST be documented with justification or rejected.

**Amendment Process**

Constitution amendments require:
1. Proposed change with rationale
2. Impact analysis on existing features
3. Version bump according to semantic versioning
4. Documentation in Sync Impact Report (HTML comment at top)
5. Migration plan if principles are removed or redefined

**Versioning Policy**

- **MAJOR**: Backward-incompatible changes (principle removal, redefinition)
- **MINOR**: New principles, material expansions, new sections
- **PATCH**: Clarifications, wording improvements, typo fixes

**Review Cadence**

Constitution compliance MUST be reviewed quarterly. Outdated principles MUST be amended or deprecated.

**Version**: 1.1.0 | **Ratified**: 2026-02-20 | **Last Amended**: 2026-02-21
