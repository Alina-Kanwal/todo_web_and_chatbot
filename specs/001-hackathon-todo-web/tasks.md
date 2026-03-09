# Tasks: Hackathon Todo App – Phase II (Web Version)

**Input**: Design documents from `/specs/001-hackathon-todo-web/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (N/A), data-model.md (N/A), contracts/ (N/A)

**Tests**: Tests are OPTIONAL for this project. This task list includes contract and integration tests to ensure API reliability and user isolation validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Monorepo root**: Repository root directory

<!--
  ============================================================================
  Task Organization Summary:
  - Phase 1: Setup (3 tasks) - Project initialization
  - Phase 2: Foundational (8 tasks) - Blocking prerequisites
  - Phase 3: User Story 1 - Authentication (10 tasks) - MVP
  - Phase 4: User Story 2 - Task CRUD Core (12 tasks)
  - Phase 5: User Story 3 - Filtering & Sorting (8 tasks)
  - Phase 6: Polish & Cross-Cutting Concerns (6 tasks)
  Total: 47 tasks
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create monorepo structure with `frontend/` and `backend/` directories per plan.md
- [X] T002 [P] Initialize backend FastAPI project with requirements.txt in `backend/`
- [X] T003 [P] Initialize frontend Next.js 16+ project with package.json in `frontend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Create backend directory structure: `backend/src/api/routes/`, `backend/src/models/`, `backend/src/services/`, `backend/src/core/` in `backend/src/`
- [ ] T005 [P] Create frontend directory structure: `frontend/src/app/`, `frontend/src/components/`, `frontend/src/lib/`, `frontend/src/types/` in `frontend/src/`
- [ ] T006 [P] Configure backend dependencies in `backend/requirements.txt`: fastapi, sqlmodel, uvicorn, pydantic, better-auth, python-jose
- [ ] T007 [P] Configure frontend dependencies in `frontend/package.json`: next, react, tailwindcss, better-auth client, typescript
- [ ] T008 [P] Create `.env.example` at repository root with DATABASE_URL, NEXT_PUBLIC_API_BASE_URL, BETTER_AUTH_SECRET placeholders
- [ ] T009 [P] Create `backend/.env` and `frontend/.env.local` copying existing environment variables from project root
- [ ] T010 [P] Setup Alembic migrations framework in `backend/alembic/` with SQLModel integration
- [ ] T011 Create database configuration in `backend/src/core/config.py` loading DATABASE_URL with validation
- [ ] T012 [P] Create FastAPI app initialization in `backend/src/main.py` with CORS middleware configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authentication & JWT Issuance (Priority: P1) 🎯 MVP

**Goal**: Implement complete authentication flow with Better Auth integration, JWT issuance, and token verification middleware

**Independent Test**: Users can sign up, sign in, receive JWT tokens, and access protected endpoints with valid authentication

### Tests for User Story 1 (Contract & Integration) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Create contract test for signup endpoint in `backend/tests/contract/test_auth.py` - validates 201 response with JWT
- [ ] T014 [P] [US1] Create contract test for signin endpoint in `backend/tests/contract/test_auth.py` - validates 200 response with JWT
- [ ] T015 [P] [US1] Create contract test for protected endpoint without token in `backend/tests/contract/test_auth.py` - validates 401 response
- [ ] T016 [P] [US1] Create integration test for auth flow in `backend/tests/integration/test_auth_flow.py` - signup → signin → protected access

### Implementation for User Story 1

- [ ] T017 [P] [US1] Create User model with SQLModel in `backend/src/models/user.py` (id, email, password_hash, created_at)
- [ ] T018 [P] [US1] Create JWT token utilities in `backend/src/core/security.py` - create_token(), verify_token(), extract_user_id()
- [ ] T019 [US1] Create authentication dependency in `backend/src/api/deps.py` - get_current_user() extracting user_id from JWT
- [ ] T020 [US1] Implement signup endpoint in `backend/src/api/routes/auth.py` - POST /api/auth/signup with Better Auth integration
- [ ] T021 [US1] Implement signin endpoint in `backend/src/api/routes/auth.py` - POST /api/auth/signin with credential validation
- [ ] T022 [US1] Implement signout endpoint in `backend/src/api/routes/auth.py` - POST /api/auth/signout (client-side notification)
- [ ] T023 [US1] Add request/response schemas with Pydantic in `backend/src/api/routes/auth.py` - SignupRequest, SigninRequest, TokenResponse
- [ ] T024 [US1] Add audit logging for authentication events in `backend/src/api/routes/auth.py` - log signup, signin, signout with timestamps
- [ ] T025 [US1] Create signup page in `frontend/src/app/(auth)/signup/page.tsx` with email/password form and validation
- [ ] T026 [US1] Create signin page in `frontend/src/app/(auth)/signin/page.tsx` with email/password form
- [ ] T027 [US1] Create API client in `frontend/src/lib/api.ts` with automatic JWT injection in Authorization header
- [ ] T028 [US1] Create auth client in `frontend/src/lib/auth.ts` for Better Auth integration and token storage
- [ ] T029 [US1] Add JWT storage utility in `frontend/src/lib/auth.ts` - store/retrieve/remove token securely
- [ ] T030 [US1] Add authentication state management in `frontend/src/app/layout.tsx` - check token on mount, redirect if expired

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - users can sign up, sign in, and JWT is verified on protected endpoints

---

## Phase 4: User Story 2 - Task CRUD Core (Priority: P1)

**Goal**: Implement complete task CRUD operations with strict user isolation and JWT enforcement

**Independent Test**: Authenticated users can create, read, update, and delete their own tasks; cannot access other users' tasks (404 returned)

### Tests for User Story 2 (Contract & Integration) ⚠️

- [ ] T031 [P] [US2] Create contract test for create task endpoint in `backend/tests/contract/test_tasks.py` - validates 201 with task object
- [ ] T032 [P] [US2] Create contract test for list tasks endpoint in `backend/tests/contract/test_tasks.py` - validates 200 with tasks array
- [ ] T033 [P] [US2] Create contract test for get single task in `backend/tests/contract/test_tasks.py` - validates 200 or 404
- [ ] T034 [P] [US2] Create contract test for update task in `backend/tests/contract/test_tasks.py` - validates 200 with updated task
- [ ] T035 [P] [US2] Create contract test for delete task in `backend/tests/contract/test_tasks.py` - validates 204 No Content
- [ ] T036 [P] [US2] Create integration test for user isolation in `backend/tests/integration/test_user_isolation.py` - User A cannot access User B's tasks (404)
- [ ] T037 [P] [US2] Create integration test for full CRUD flow in `backend/tests/integration/test_tasks_crud.py` - create → read → update → delete

### Implementation for User Story 2

- [ ] T038 [P] [US2] Create Task model with SQLModel in `backend/src/models/task.py` - id, user_id (FK), title, description, completed, created_at, updated_at
- [ ] T039 [US2] Create initial Alembic migration in `backend/alembic/versions/001_create_tasks_table.py` - create tasks table with user_id FK and indexes
- [ ] T040 [US2] Create TaskService in `backend/src/services/tasks.py` - create_task(), get_task(), list_tasks(), update_task(), delete_task() with user_id filtering
- [ ] T041 [US2] Implement create task endpoint in `backend/src/api/routes/tasks.py` - POST /api/tasks with title validation
- [ ] T042 [US2] Implement list tasks endpoint in `backend/src/api/routes/tasks.py` - GET /api/tasks returning all user's tasks
- [ ] T043 [US2] Implement get single task endpoint in `backend/src/api/routes/tasks.py` - GET /api/tasks/{id} with ownership validation
- [ ] T044 [US2] Implement update task endpoint in `backend/src/api/routes/tasks.py` - PUT/PATCH /api/tasks/{id} with partial update support
- [ ] T045 [US2] Implement delete task endpoint in `backend/src/api/routes/tasks.py` - DELETE /api/tasks/{id} with permanent removal
- [ ] T046 [US2] Add structured error handler in `backend/src/api/error_handlers.py` - return {status_code, error_type, message, details}
- [ ] T047 [US2] Add audit logging for task write operations in `backend/src/services/tasks.py` - log CREATE, UPDATE, DELETE with user context
- [ ] T048 [US2] Create task types in `frontend/src/types/index.ts` - Task interface with all fields
- [ ] T049 [US2] Create task API service in `frontend/src/lib/api.ts` - createTask(), getTasks(), getTask(), updateTask(), deleteTask()
- [ ] T050 [US2] Create task dashboard page in `frontend/src/app/dashboard/page.tsx` with task list and creation form
- [ ] T051 [US2] Create task item component in `frontend/src/components/tasks/TaskItem.tsx` with title, completion toggle, edit/delete actions
- [ ] T052 [US2] Create task form component in `frontend/src/components/tasks/TaskForm.tsx` with validation and submit handling
- [ ] T053 [US2] Add loading states in `frontend/src/components/tasks/TaskList.tsx` - skeleton loaders during API calls
- [ ] T054 [US2] Add error feedback in `frontend/src/components/tasks/TaskList.tsx` - display API errors with retry option
- [ ] T055 [US2] Add empty state in `frontend/src/components/tasks/EmptyState.tsx` - friendly message when no tasks exist

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full authentication + complete task CRUD with user isolation

---

## Phase 5: User Story 3 - Filtering & Sorting (Priority: P2)

**Goal**: Implement task filtering by status and sorting by date/title with query parameters

**Independent Test**: Users can filter tasks by pending/completed/all and sort by created_at or title; filters respect user isolation

### Tests for User Story 3 (Contract & Integration) ⚠️

- [ ] T056 [P] [US3] Create contract test for filter by status in `backend/tests/contract/test_tasks.py` - validates filtered results
- [ ] T057 [P] [US3] Create contract test for sort by date in `backend/tests/contract/test_tasks.py` - validates ordering
- [ ] T058 [P] [US3] Create contract test for sort by title in `backend/tests/contract/test_tasks.py` - validates alphabetical ordering
- [ ] T059 [P] [US3] Create integration test for filter + user isolation in `backend/tests/integration/test_filtering.py` - User A's filtered results don't include User B's tasks

### Implementation for User Story 3

- [ ] T060 [P] [US3] Add query parameter support in `backend/src/api/routes/tasks.py` - status (pending/completed/all), sort (created_at/title), order (asc/desc)
- [ ] T061 [US3] Update TaskService list_tasks() in `backend/src/services/tasks.py` - add filtering and sorting logic with user_id constraint
- [ ] T062 [US3] Add composite index migration in `backend/alembic/versions/002_add_composite_index.py` - index on (user_id, completed) for filtered queries
- [ ] T063 [US3] Create filter/sort controls component in `frontend/src/components/tasks/FilterSortControls.tsx` with dropdowns/toggles
- [ ] T064 [US3] Update task dashboard in `frontend/src/app/dashboard/page.tsx` - integrate filter/sort controls, update API calls with query params
- [ ] T065 [US3] Add URL query parameter sync in `frontend/src/app/dashboard/page.tsx` - persist filters in URL for bookmarking
- [ ] T066 [US3] Add responsive styling for filter controls in `frontend/src/components/tasks/FilterSortControls.tsx` - mobile-friendly layout

**Checkpoint**: All user stories should now be independently functional - authentication + CRUD + filtering/sorting complete

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, security hardening, and deployment readiness

- [ ] T067 [P] Create health check endpoint in `backend/src/api/routes/health.py` - GET /api/health with database connectivity validation
- [ ] T068 [P] Add environment variable validation at startup in `backend/src/main.py` - fail fast if DATABASE_URL, BETTER_AUTH_SECRET missing
- [ ] T069 [P] Create OpenAPI documentation in `backend/src/main.py` - configure Swagger UI at /docs with all endpoint contracts
- [ ] T070 [P] Add rate limiting for auth endpoints in `backend/src/api/routes/auth.py` - prevent brute force attacks
- [ ] T071 [P] Create quickstart.md in `specs/001-hackathon-todo-web/quickstart.md` - setup instructions for developers
- [ ] T072 [P] Update README.md at repository root with project overview, tech stack, and quick start guide
- [ ] T073 [P] Add accessibility features in `frontend/src/components/` - ARIA labels, keyboard navigation, focus states
- [ ] T074 [P] Add responsive design validation in `frontend/src/app/` - mobile (<640px), tablet (640-1024px), desktop (>1024px)
- [ ] T075 [P] Create Playwright E2E test in `frontend/tests/e2e/test_full_flow.ts` - signup → signin → CRUD → signout flow
- [ ] T076 [P] Run security audit checklist - verify user isolation, JWT validation, input sanitization, CORS configuration
- [ ] T077 [P] Run performance test with locust/k6 - validate p95 latency < 200ms for all endpoints
- [ ] T078 [P] Create deployment runbook in `docs/deployment.md` - production deployment steps, rollback procedure, monitoring setup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Story 1 (Phase 3)**: Depends on Foundational - enables authentication
- **User Story 2 (Phase 4)**: Depends on Foundational + Story 1 (auth required for CRUD)
- **User Story 3 (Phase 5)**: Depends on Foundational + Story 2 (CRUD required for filtering)
- **Polish (Phase 6)**: Depends on all user stories being functional

### User Story Dependencies

- **User Story 1 (Authentication)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Task CRUD)**: Depends on Story 1 completion (JWT auth required) - Independently testable
- **User Story 3 (Filtering)**: Depends on Story 2 completion (CRUD required) - Independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002 (backend init) and T003 (frontend init) can run in parallel

**Phase 2 (Foundational)**:
- T004, T005, T006, T007, T008, T009, T010, T012 can all run in parallel (different files)
- T011 (config) should complete before T020+ (auth endpoints)

**Phase 3 (User Story 1 - Auth)**:
- T013, T014, T015, T016 (tests) can run in parallel
- T017 (User model) and T018 (security utils) can run in parallel
- T025 (signup page) and T026 (signin page) can run in parallel
- T027 (API client) and T028 (auth client) can run in parallel

**Phase 4 (User Story 2 - CRUD)**:
- T031-T037 (tests) can all run in parallel
- T038 (Task model) can run in parallel with backend tests
- T050 (dashboard), T051 (TaskItem), T052 (TaskForm) can run in parallel
- T053 (loading), T054 (errors), T055 (empty state) can run in parallel

**Phase 5 (User Story 3 - Filtering)**:
- T056, T057, T058, T059 (tests) can run in parallel
- T063 (filter controls) and T060 (backend params) can run in parallel

**Phase 6 (Polish)**:
- T067-T078 can mostly run in parallel (different files/domains)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all tests for User Story 1 together:
Task: "T013 [P] [US1] Create contract test for signup endpoint in backend/tests/contract/test_auth.py"
Task: "T014 [P] [US1] Create contract test for signin endpoint in backend/tests/contract/test_auth.py"
Task: "T015 [P] [US1] Create contract test for protected endpoint in backend/tests/contract/test_auth.py"
Task: "T016 [P] [US1] Create integration test for auth flow in backend/tests/integration/test_auth_flow.py"

# Launch all models/utils for User Story 1 together:
Task: "T017 [P] [US1] Create User model with SQLModel in backend/src/models/user.py"
Task: "T018 [P] [US1] Create JWT token utilities in backend/src/core/security.py"

# Launch all frontend pages for User Story 1 together:
Task: "T025 [P] [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx"
Task: "T026 [P] [US1] Create signin page in frontend/src/app/(auth)/signin/page.tsx"
```

---

## Parallel Example: User Story 2 (Task CRUD)

```bash
# Launch all tests for User Story 2 together:
Task: "T031 [P] [US2] Create contract test for create task in backend/tests/contract/test_tasks.py"
Task: "T032 [P] [US2] Create contract test for list tasks in backend/tests/contract/test_tasks.py"
Task: "T033 [P] [US2] Create contract test for get single task in backend/tests/contract/test_tasks.py"
Task: "T034 [P] [US2] Create contract test for update task in backend/tests/contract/test_tasks.py"
Task: "T035 [P] [US2] Create contract test for delete task in backend/tests/contract/test_tasks.py"
Task: "T036 [P] [US2] Create integration test for user isolation in backend/tests/integration/test_user_isolation.py"
Task: "T037 [P] [US2] Create integration test for CRUD flow in backend/tests/integration/test_tasks_crud.py"

# Launch all models for User Story 2 together:
Task: "T038 [P] [US2] Create Task model with SQLModel in backend/src/models/task.py"

# Launch all frontend components for User Story 2 together:
Task: "T051 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx"
Task: "T052 [P] [US2] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx"
Task: "T053 [P] [US2] Add loading states in frontend/src/components/tasks/TaskList.tsx"
Task: "T054 [P] [US2] Add error feedback in frontend/src/components/tasks/TaskList.tsx"
Task: "T055 [P] [US2] Add empty state in frontend/src/components/tasks/EmptyState.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T012)
3. Complete Phase 3: User Story 1 - Authentication (T013-T030)
4. **STOP and VALIDATE**: 
   - Test signup flow end-to-end
   - Test signin flow end-to-end
   - Verify JWT is issued and stored
   - Verify protected endpoint returns 401 without token
   - Verify protected endpoint accepts valid token
5. Deploy/demo if ready (authentication MVP)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Authentication) → Test independently → Deploy/Demo (Auth MVP!)
3. Add User Story 2 (Task CRUD) → Test independently → Deploy/Demo (Full CRUD!)
4. Add User Story 3 (Filtering & Sorting) → Test independently → Deploy/Demo (Complete!)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With 2-3 developers:

**Developer A (Backend Specialist)**:
- Phase 2: T004, T006, T008, T010, T011, T012
- Phase 3: T013-T019, T020-T024 (backend auth)
- Phase 4: T031-T047 (backend CRUD + tests)
- Phase 5: T056-T062 (backend filtering)

**Developer B (Frontend Specialist)**:
- Phase 2: T005, T007, T009
- Phase 3: T025-T030 (frontend auth)
- Phase 4: T048-T055 (frontend CRUD)
- Phase 5: T063-T067 (frontend filtering)

**Developer C (Full-Stack / QA)**:
- Phase 6: T067-T078 (polish, deployment, E2E)
- Support: Integration tests, security audit, performance testing

### Critical Path

**Minimum sequence for MVP (User Story 1 + 2)**:
```
T001 → T004-T012 (Foundation) → T017-T024 (Backend Auth) → T025-T030 (Frontend Auth)
→ T038-T047 (Backend CRUD) → T048-T055 (Frontend CRUD) → MVP Ready
```

**Estimated Duration**: 5-7 days for MVP (Auth + CRUD)

---

## Task Summary

| Phase | Description | Task Count | Owner |
|-------|-------------|------------|-------|
| Phase 1 | Setup | 3 | Full-stack |
| Phase 2 | Foundational | 8 | Full-stack |
| Phase 3 | User Story 1 (Auth) | 18 | Full-stack |
| Phase 4 | User Story 2 (CRUD) | 25 | Full-stack |
| Phase 5 | User Story 3 (Filtering) | 8 | Full-stack |
| Phase 6 | Polish | 12 | Full-stack |
| **Total** | **All Phases** | **74** | **-** |

**Test Tasks**: 16 (contract + integration tests)
**Backend Tasks**: 32
**Frontend Tasks**: 26
**Infrastructure/Polish**: 12

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **User isolation validation is CRITICAL** - T036 must pass before production
- **JWT enforcement is CRITICAL** - T015 must pass before exposing CRUD endpoints
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Validation Checklist

Before marking each phase complete:

**Phase 1 (Setup) Complete When**:
- ✅ `backend/` directory exists with requirements.txt
- ✅ `frontend/` directory exists with package.json
- ✅ Both projects can start (hello world)

**Phase 2 (Foundational) Complete When**:
- ✅ Directory structures created
- ✅ Dependencies installed
- ✅ Environment variables configured
- ✅ Alembic migrations configured
- ✅ FastAPI app starts with CORS

**Phase 3 (User Story 1 - Auth) Complete When**:
- ✅ Users can sign up and receive JWT
- ✅ Users can sign in and receive JWT
- ✅ Protected endpoints reject invalid tokens (401)
- ✅ Frontend can authenticate and store JWT
- ✅ T013-T016 (tests) all pass

**Phase 4 (User Story 2 - CRUD) Complete When**:
- ✅ Users can create tasks (201)
- ✅ Users can list their tasks only
- ✅ Users can view single task (404 for others' tasks)
- ✅ Users can update their tasks
- ✅ Users can delete their tasks
- ✅ T031-T037 (tests) all pass
- ✅ T036 (user isolation) passes - CRITICAL

**Phase 5 (User Story 3 - Filtering) Complete When**:
- ✅ Filter by status works (pending/completed/all)
- ✅ Sort by created_at works (asc/desc)
- ✅ Sort by title works (asc/desc)
- ✅ Filters respect user isolation
- ✅ T056-T059 (tests) all pass

**Phase 6 (Polish) Complete When**:
- ✅ Health check endpoint returns 200
- ✅ Environment validation at startup
- ✅ OpenAPI docs available at /docs
- ✅ E2E test passes (T075)
- ✅ Security audit passes (T076)
- ✅ Performance test passes (T077)
