# Feature Specification: Hackathon Todo App – Phase II (Web Version)

**Feature Branch**: `001-hackathon-todo-web`
**Created**: 2026-02-20
**Status**: Draft
**Input**: Transform console-based todo app into multi-user full-stack web application with persistent storage

---

## 1. Product Overview

**Product Name**: Hackathon Todo App – Phase II (Web Version)

**Purpose**: Transform a single-user console-based todo application into a modern, multi-user web application with persistent storage, authentication, and a responsive user interface.

**Scope**:
- Multi-user authentication system with JWT-based stateless sessions
- Complete CRUD operations for tasks with user isolation
- Filtering and sorting capabilities for task management
- Responsive web interface accessible on desktop and mobile devices
- RESTful API with explicit contracts and error handling

**Out of Scope**:
- Real-time collaboration features
- Task sharing between users
- File attachments to tasks
- Task categories or tags
- Email notifications or reminders
- Dark mode theming

**Success Metrics**:
- Users can complete signup and signin flow in under 60 seconds
- Task CRUD operations complete with p95 latency < 200ms
- Zero cross-user data exposure incidents
- 99% uptime during hackathon demonstration period

---

## 2. Target Users

**Primary Users**:
- Individual users seeking a simple, reliable task management tool
- Tech-savvy users comfortable with web applications
- Users requiring persistent storage across devices

**User Personas**:

1. **Quick Task Creator**: Needs to rapidly add, complete, and delete tasks without friction
2. **Organized Planner**: Requires ability to review pending vs. completed tasks, sort by date
3. **Multi-Device User**: Accesses application from different devices, expects data synchronization

**User Needs**:
- Secure account creation and authentication
- Fast, responsive task management
- Clear visual feedback on task status
- Reliable data persistence
- Intuitive filtering and sorting

---

## 3. Functional Requirements

### 3.1 User Authentication

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-AUTH-001 | System MUST allow users to create an account with email and password | P1 |
| FR-AUTH-002 | System MUST validate email format during signup | P1 |
| FR-AUTH-003 | System MUST enforce minimum password requirements (8+ characters) | P1 |
| FR-AUTH-004 | System MUST allow users to sign in with email and password | P1 |
| FR-AUTH-005 | System MUST issue a JWT token upon successful authentication | P1 |
| FR-AUTH-006 | JWT tokens MUST have a configurable expiry time (default: 7 days) | P2 |
| FR-AUTH-007 | System MUST allow users to sign out (client-side token removal) | P2 |
| FR-AUTH-008 | System MUST reject requests with expired or invalid tokens | P1 |
| FR-AUTH-009 | System MUST provide clear error messages for authentication failures | P2 |

### 3.2 Task CRUD Operations

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-TASK-001 | Authenticated users MUST be able to create new tasks with a title | P1 |
| FR-TASK-002 | Tasks MUST be automatically associated with the creating user's `user_id` | P1 |
| FR-TASK-003 | System MUST allow users to view a list of all their tasks | P1 |
| FR-AUTH-004 | Task list MUST be filtered by authenticated user's `user_id` server-side | P1 |
| FR-TASK-005 | System MUST allow users to view a single task by ID | P1 |
| FR-TASK-006 | System MUST return 404 if task does not exist or belongs to another user | P1 |
| FR-TASK-007 | System MUST allow users to update task title and completion status | P1 |
| FR-TASK-008 | System MUST allow users to delete their tasks | P1 |
| FR-TASK-009 | System MUST allow users to toggle task completion status (pending/completed) | P1 |
| FR-TASK-010 | Deleted tasks MUST be permanently removed from the database | P2 |

### 3.3 Filtering & Sorting

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-FILTER-001 | System MUST allow filtering tasks by status (pending, completed, all) | P2 |
| FR-FILTER-002 | System MUST allow sorting tasks by created date (newest/oldest first) | P3 |
| FR-FILTER-003 | System MUST allow sorting tasks by title (alphabetical A-Z/Z-A) | P3 |
| FR-FILTER-004 | Filter and sort operations MUST respect user isolation | P2 |

---

## 4. Authentication Specification

### 4.1 Authentication Flow

**Signup Process**:
1. User provides email and password via frontend form
2. Frontend sends POST request to `/api/auth/signup`
3. Backend validates input, forwards to Better Auth
4. Better Auth creates user record, returns JWT token
5. Frontend stores token securely (httpOnly cookie or secure storage)
6. User is redirected to task dashboard

**Signin Process**:
1. User provides email and password via frontend form
2. Frontend sends POST request to `/api/auth/signin`
3. Backend validates credentials via Better Auth
4. Better Auth returns JWT token on success
5. Frontend stores token, redirects to dashboard
6. Failed attempts return generic error message (security)

**Token Management**:
- JWT tokens MUST be included in `Authorization: Bearer <token>` header
- Frontend MUST attach token to all API requests automatically
- Backend MUST verify token signature using `BETTER_AUTH_SECRET`
- Backend MUST extract `user_id` from token payload for all operations
- Expired tokens MUST return 401 Unauthorized
- Token refresh mechanism is out of scope (user re-signs in)

**Logout Process**:
- Client-side only: Remove stored token from browser storage
- Clear any httpOnly cookies if used
- Redirect to signin page
- No server-side session invalidation required (stateless)

### 4.2 Security Requirements

- Passwords MUST be hashed by Better Auth before storage
- JWT tokens MUST use HS256 or RS256 signing algorithm
- `BETTER_AUTH_SECRET` MUST be minimum 32 characters
- Authentication endpoints MUST be rate-limited (prevent brute force)
- Failed login attempts MUST NOT reveal whether email exists

---

## 5. Task Management Specification

### 5.1 Task Entity

**Attributes**:
- `id`: UUID or auto-increment integer (primary key)
- `user_id`: Foreign key referencing users table
- `title`: String (1-500 characters, required)
- `description`: String (optional, max 2000 characters)
- `completed`: Boolean (default: false)
- `created_at`: Timestamp (auto-generated, immutable)
- `updated_at`: Timestamp (auto-updated on modification)

**Constraints**:
- `title` MUST NOT be empty or whitespace-only
- `user_id` MUST reference a valid user (foreign key constraint)
- `completed` MUST default to `false` on creation

### 5.2 Task Operations

**Create Task**:
- Input: `title` (required), `description` (optional)
- Output: Created task object with all fields
- Validation: Title length, authenticated user
- User ID: Extracted from JWT, not from request body

**Read Tasks**:
- List: Returns array of tasks filtered by `user_id`
- Single: Returns task if exists and belongs to user, else 404
- Supports query parameters for filtering/sorting

**Update Task**:
- Input: Partial task object (title, description, completed)
- Output: Updated task object with new `updated_at`
- Validation: At least one field provided, user ownership
- User ID: Extracted from JWT, validated against task owner

**Delete Task**:
- Input: Task ID in URL path
- Output: 204 No Content on success
- Validation: User ownership verified before deletion
- Behavior: Permanent deletion, no soft delete

**Toggle Completion**:
- Input: Task ID in URL path
- Output: Updated task with toggled `completed` status
- Implementation: PATCH operation or dedicated endpoint

---

## 6. API Contract Requirements

### 6.1 Base Configuration

- **Base URL**: `/api/`
- **Content-Type**: `application/json`
- **Authentication**: Bearer token in `Authorization` header (except auth endpoints)

### 6.2 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | Create new user account | No |
| POST | `/api/auth/signin` | Authenticate user, return JWT | No |
| POST | `/api/auth/signout` | Client-side logout (optional server notification) | Yes |

### 6.3 Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks` | List all user's tasks | Yes |
| GET | `/api/tasks/:id` | Get single task by ID | Yes |
| POST | `/api/tasks` | Create new task | Yes |
| PUT | `/api/tasks/:id` | Update task (full replace) | Yes |
| PATCH | `/api/tasks/:id` | Update task (partial) | Yes |
| DELETE | `/api/tasks/:id` | Delete task | Yes |

### 6.4 Query Parameters (GET /api/tasks)

| Parameter | Type | Values | Default |
|-----------|------|--------|---------|
| `status` | string | `pending`, `completed`, `all` | `all` |
| `sort` | string | `created_at`, `title` | `created_at` |
| `order` | string | `asc`, `desc` | `desc` |

### 6.5 Response Formats

**Success Response (Single Resource)**:
```json
{
  "id": "uuid-or-int",
  "user_id": "uuid-or-int",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-02-20T10:00:00Z",
  "updated_at": "2026-02-20T10:00:00Z"
}
```

**Success Response (List)**:
```json
{
  "tasks": [...],
  "total": 10,
  "filters": {
    "status": "pending",
    "sort": "created_at",
    "order": "desc"
  }
}
```

**Error Response**:
```json
{
  "status_code": 400,
  "error_type": "ValidationError",
  "message": "Human-readable error message",
  "details": {
    "field": "reason"
  }
}
```

### 6.6 Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | `ValidationError` | Invalid request payload or missing fields |
| 401 | `AuthenticationError` | Missing, expired, or invalid JWT token |
| 403 | `AuthorizationError` | User lacks permission (accessing another user's resource) |
| 404 | `NotFoundError` | Resource does not exist or belongs to another user |
| 409 | `ConflictError` | Duplicate resource or constraint violation |
| 500 | `InternalServerError` | Server-side error, database failure |

---

## 7. Database Requirements

### 7.1 Database Technology

- **Provider**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (Python)
- **Connection**: Managed via `DATABASE_URL` environment variable

### 7.2 Schema Requirements

**Users Table** (managed by Better Auth):
- `id`: Primary key (UUID or integer)
- `email`: Unique, indexed, not null
- `password_hash`: Not null
- `created_at`: Timestamp, not null
- Additional Better Auth fields as required

**Tasks Table**:
- `id`: Primary key (UUID or auto-increment integer)
- `user_id`: Foreign key → users.id, indexed, not null
- `title`: VARCHAR(500), not null
- `description`: TEXT, nullable
- `completed`: BOOLEAN, default false, not null
- `created_at`: TIMESTAMP, default now(), not null
- `updated_at`: TIMESTAMP, auto-update on modification

### 7.3 Indexing Strategy

- `tasks.user_id`: Index for user isolation queries
- `tasks.user_id + tasks.completed`: Composite index for filtered queries
- `users.email`: Unique index (managed by Better Auth)

### 7.4 Migration Requirements

- All schema changes MUST use SQLModel migration system
- Migrations MUST be version-controlled in repository
- Migrations MUST include rollback (downgrade) scripts
- Initial migration MUST create users and tasks tables

### 7.5 Data Integrity

- Foreign key constraints MUST be enforced
- `ON DELETE CASCADE` for tasks when user is deleted
- No orphaned tasks allowed
- Database-level constraints complement application validation

---

## 8. UI/UX Requirements

### 8.1 Design System

- **Framework**: Tailwind CSS
- **Design Principles**: Clean, minimal, task-focused
- **Color Palette**: High contrast, accessible (WCAG AA minimum)
- **Typography**: System fonts for performance

### 8.2 Page Layouts

**Signup/Signin Pages**:
- Centered card layout
- Email and password input fields
- Submit button with loading state
- Link to toggle between signup/signin
- Error message display area
- Responsive: Full-width on mobile, constrained on desktop

**Task Dashboard**:
- Header with user email and logout button
- Task creation form (input + submit button)
- Filter/sort controls (dropdown or toggle buttons)
- Task list with completion toggles
- Individual task items with edit/delete actions
- Empty state message when no tasks exist

**Responsive Breakpoints**:
- Mobile: < 640px (single column, stacked layout)
- Tablet: 640px – 1024px (optimized touch targets)
- Desktop: > 1024px (max-width container, centered)

### 8.3 Interaction Requirements

**Task Creation**:
- Input field with placeholder text
- Enter key submits form
- Clear input on successful creation
- Show validation errors inline

**Task Completion Toggle**:
- Checkbox or toggle button per task
- Immediate visual feedback on toggle
- Optimistic UI update (revert on error)

**Task Editing**:
- Inline edit or modal dialog
- Save/Cancel actions
- Validation on save

**Task Deletion**:
- Confirmation dialog before deletion
- Destructive action styling (red/warning)

**Loading States**:
- Skeleton loaders or spinners for async operations
- Disabled buttons during submission
- Clear feedback on success/error

**Error Handling**:
- Inline validation errors (field-level)
- Toast notifications for API errors
- Persistent error banner for authentication failures

### 8.4 Accessibility Requirements

- All interactive elements MUST be keyboard accessible
- Form inputs MUST have associated labels
- Error messages MUST be associated with inputs via `aria-describedby`
- Color MUST NOT be the sole indicator of status (use icons/text)
- Focus states MUST be visible
- Screen reader announcements for dynamic content (ARIA live regions)

---

## 9. Non-Functional Requirements

### 9.1 Security

| ID | Requirement |
|----|-------------|
| NFR-SEC-001 | All API endpoints MUST validate JWT tokens before processing (except auth endpoints) |
| NFR-SEC-002 | All database queries MUST filter by authenticated user's `user_id` |
| NFR-SEC-003 | Passwords MUST be hashed using bcrypt or equivalent (via Better Auth) |
| NFR-SEC-004 | JWT tokens MUST be transmitted over HTTPS only in production |
| NFR-SEC-005 | Sensitive data (passwords, tokens) MUST NOT be logged |
| NFR-SEC-006 | Authentication endpoints MUST implement rate limiting |
| NFR-SEC-007 | CORS MUST be configured to allow only trusted origins |
| NFR-SEC-008 | Input payloads MUST be validated against explicit schemas |
| NFR-SEC-009 | SQL injection MUST be prevented via ORM parameterization |
| NFR-SEC-010 | XSS MUST be prevented via React's built-in escaping |

### 9.2 Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-PERF-001 | API p95 latency (all endpoints) | < 200ms |
| NFR-PERF-002 | Frontend initial page load | < 2 seconds |
| NFR-PERF-003 | Task list rendering (100 tasks) | < 100ms |
| NFR-PERF-004 | Database query time (indexed) | < 50ms |
| NFR-PERF-005 | Concurrent user support | 100+ users |
| NFR-PERF-006 | API throughput | 100 requests/second |

### 9.3 Scalability

| ID | Requirement |
|----|-------------|
| NFR-SCALE-001 | Backend MUST be stateless to enable horizontal scaling |
| NFR-SCALE-002 | Database MUST support connection pooling |
| NFR-SCALE-003 | JWT verification MUST NOT require database lookups |
| NFR-SCALE-004 | Frontend assets MUST be cacheable via CDN |
| NFR-SCALE-005 | API MUST support pagination if task lists exceed 1000 items |

### 9.4 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-MAINT-001 | Code MUST follow established style guides (ESLint, Black, mypy) |
| NFR-MAINT-002 | All public APIs MUST be documented in OpenAPI/Swagger format |
| NFR-MAINT-003 | Environment variables MUST be documented in `.env.example` |
| NFR-MAINT-004 | Dependencies MUST be pinned to specific versions |
| NFR-MAINT-005 | Git commits MUST follow conventional commit format |
| NFR-MAINT-006 | All features MUST have corresponding test coverage |
| NFR-MAINT-007 | Code MUST be modular with clear separation of concerns |
| NFR-MAINT-008 | Error messages MUST be user-friendly and actionable |

### 9.5 Reliability

| ID | Requirement |
|----|-------------|
| NFR-REL-001 | Backend MUST implement graceful error handling (no raw stack traces to clients) |
| NFR-REL-002 | Database connections MUST be resilient to transient failures |
| NFR-REL-003 | Frontend MUST handle API failures gracefully (user feedback) |
| NFR-REL-004 | Health check endpoint MUST verify database connectivity |
| NFR-REL-005 | Application startup MUST validate required environment variables |

---

## 10. Acceptance Criteria

### 10.1 Authentication Acceptance Criteria

**AC-AUTH-001: Successful Signup**
- **Given** a user with valid email and password (8+ chars)
- **When** they submit the signup form
- **Then** an account is created
- **And** a JWT token is issued
- **And** the user is redirected to the task dashboard

**AC-AUTH-002: Signup Validation**
- **Given** a user enters invalid email or short password (<8 chars)
- **When** they submit the signup form
- **Then** the form displays inline validation errors
- **And** no account is created

**AC-AUTH-003: Successful Signin**
- **Given** a registered user with correct credentials
- **When** they submit the signin form
- **Then** a JWT token is issued
- **And** the user is redirected to the task dashboard

**AC-AUTH-004: Failed Signin**
- **Given** a user enters incorrect email or password
- **When** they submit the signin form
- **Then** a generic error message is displayed
- **And** no token is issued

**AC-AUTH-005: Protected Route Without Token**
- **Given** an unauthenticated user
- **When** they attempt to access `/api/tasks`
- **Then** the API returns 401 Unauthorized

**AC-AUTH-006: Token Expiry**
- **Given** a user with an expired JWT token
- **When** they make an API request
- **Then** the API returns 401 Unauthorized
- **And** the frontend redirects to signin page

### 10.2 Task CRUD Acceptance Criteria

**AC-TASK-001: Create Task**
- **Given** an authenticated user
- **When** they submit a task with a valid title
- **Then** the task is created with `completed: false`
- **And** the task is associated with the user's `user_id`
- **And** the task appears in the task list

**AC-TASK-002: Create Task Validation**
- **Given** an authenticated user
- **When** they submit a task with empty or whitespace-only title
- **Then** the API returns 400 Bad Request
- **And** no task is created

**AC-TASK-003: View All Tasks**
- **Given** an authenticated user with multiple tasks
- **When** they request the task list
- **Then** only their tasks are returned
- **And** tasks are sorted by created date (newest first by default)

**AC-TASK-004: View Single Task**
- **Given** an authenticated user with an existing task
- **When** they request the task by ID
- **Then** the task is returned if it belongs to them
- **And** the API returns 404 if the task belongs to another user

**AC-TASK-005: Update Task**
- **Given** an authenticated user with an existing task
- **When** they update the task title or completion status
- **Then** the task is updated
- **And** the `updated_at` timestamp is modified
- **And** the API returns the updated task

**AC-TASK-006: Delete Task**
- **Given** an authenticated user with an existing task
- **When** they delete the task
- **Then** the task is permanently removed
- **And** the API returns 204 No Content
- **And** the task no longer appears in the list

**AC-TASK-007: Toggle Completion**
- **Given** an authenticated user with a pending task
- **When** they toggle the task completion
- **Then** the `completed` status is inverted
- **And** the UI reflects the new status immediately

**AC-TASK-008: User Isolation**
- **Given** two users (User A and User B) with separate tasks
- **When** User A requests all tasks
- **Then** only User A's tasks are returned
- **And** User B's tasks are never exposed to User A

### 10.3 Filtering & Sorting Acceptance Criteria

**AC-FILTER-001: Filter by Pending**
- **Given** an authenticated user with mixed task statuses
- **When** they filter by `status=pending`
- **Then** only incomplete tasks are returned

**AC-FILTER-002: Filter by Completed**
- **Given** an authenticated user with mixed task statuses
- **When** they filter by `status=completed`
- **Then** only completed tasks are returned

**AC-SORT-001: Sort by Date**
- **Given** an authenticated user with multiple tasks
- **When** they sort by `created_at` descending
- **Then** newest tasks appear first

**AC-SORT-002: Sort by Title**
- **Given** an authenticated user with multiple tasks
- **When** they sort by `title` ascending
- **Then** tasks are ordered alphabetically (A-Z)

### 10.4 UI Acceptance Criteria

**AC-UI-001: Responsive Layout**
- **Given** the application is accessed on mobile, tablet, and desktop
- **When** the page loads
- **Then** the layout adapts to screen size
- **And** all functionality remains accessible

**AC-UI-002: Loading States**
- **Given** an async operation (API call)
- **When** the operation is in progress
- **Then** a loading indicator is displayed
- **And** the triggering button is disabled

**AC-UI-003: Error Feedback**
- **Given** an API error occurs
- **When** the error response is received
- **Then** a user-friendly error message is displayed
- **And** the user can retry the operation

**AC-UI-004: Empty State**
- **Given** a user has no tasks
- **When** the task list loads
- **Then** a friendly empty state message is displayed
- **And** the user is prompted to create their first task

**AC-UI-005: Keyboard Navigation**
- **Given** a user navigates via keyboard
- **When** they use Tab, Enter, and Escape keys
- **Then** all interactive elements are accessible
- **And** focus states are visible

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| JWT | JSON Web Token – stateless authentication token |
| Better Auth | Authentication library issuing JWT tokens |
| User Isolation | Enforcement that users can only access their own data |
| Stateless | No server-side session storage; each request is self-contained |
| Monorepo | Single repository containing both frontend and backend codebases |

## Appendix B: References

- **Constitution**: `.specify/memory/constitution.md`
- **Spec-Kit Plus Workflow**: `.specify/templates/`
- **Better Auth Documentation**: [External reference]
- **Next.js 16 App Router**: [External reference]
- **FastAPI Documentation**: [External reference]
- **SQLModel Documentation**: [External reference]
- **Neon PostgreSQL**: [External reference]
