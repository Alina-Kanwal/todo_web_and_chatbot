# Task Assistant Chatbot - Feature Specification

## Overview

Integrate a conversational AI chatbot into the existing Todo web application that helps users manage their tasks through natural language conversation.

**Current Project:** `phase_three_final` (Todo Web App)
**Feature:** Task Assistant Chatbot
**Purpose:** Enable users to create, view, update, and delete tasks using natural conversation

---

## 1. Chatbot UI Placement & Design

### 1.1 Primary Location
- **Floating chat widget** in the bottom-right corner of all authenticated pages
- Collapsible panel that expands when clicked
- Persistent across page navigation (dashboard, etc.)
- **Badge indicator** showing unread messages or bot suggestions

### 1.2 UI Components
```
┌─────────────────────────────────────┐
│  Todo Dashboard                     │
│                                     │
│  [Task List]                        │
│  ┌──────┐                           │
│  │ Task │                           │
│  └──────┘                           │
│                                     │
│                    ┌──────────────┐ │
│                    │ 💬 Chat      │ │ ← Floating button (collapsed state)
│                    └──────────────┘ │
└─────────────────────────────────────┘

When expanded:
┌─────────────────────────────────────┐
│  Todo Dashboard                     │
│                                     │
│  [Task List]        ┌────────────┐ │
│                     │ Task       │ │
│                     │ Assistant  │ │
│                     │ ───────────│ │
│                     │ [Chat      │ │
│                     │  History]  │ │
│                     │ [Input     │ │
│                     │  Box]      │ │
│                     └────────────┘ │
└─────────────────────────────────────┘
```

### 1.3 Chat Interface Elements
- **Header**: "Task Assistant" title + minimize/close buttons
- **Message area**: Scrollable conversation history
- **Input area**: Text input field + send button
- **Quick actions**: Suggested prompts (e.g., "Show my tasks", "Create a task")
- **Typing indicator**: Shows when bot is "thinking"

---

## 2. Technical Architecture Decisions

### 2.1 AI Service Selection
**Recommendation: OpenAI GPT-4o or GPT-4o-mini**

**Reasoning:**
- Excellent natural language understanding
- Good at intent recognition (create, update, delete, view tasks)
- Fast response times
- Cost-effective with GPT-4o-mini for most queries
- Easy integration with function calling

**Alternative:** Anthropic Claude 3.5 Sonnet (if preferred)

### 2.2 Backend Integration
**Approach: New Chatbot Endpoint in FastAPI**

```
Frontend (Next.js)          Backend (FastAPI)           AI Service
      │                          │                          │
      │  1. User message         │                          │
      ├─────────────────────────>│                          │
      │  POST /api/chat          │                          │
      │                          │                          │
      │                          │  2. Process with AI      │
      │                          ├─────────────────────────>│
      │                          │  (OpenAI API)            │
      │                          │                          │
      │                          │  3. AI response +        │
      │                          │     function calls       │
      │                          │<─────────────────────────┤
      │                          │                          │
      │  4. Execute functions    │                          │
      │     (create_task,        │                          │
      │      get_tasks, etc.)    │                          │
      │<─────────────────────────┤                          │
      │                          │                          │
      │  5. Final response       │                          │
      ├─────────────────────────>│                          │
      │  (with task data)        │                          │
```

### 2.3 Function Calling Strategy
The AI will use OpenAI's function calling to:
- `create_task(title, description)` - Create a new task
- `list_tasks(status, filter)` - Get user's tasks
- `update_task(task_id, updates)` - Modify a task
- `delete_task(task_id)` - Remove a task
- `toggle_task(task_id)` - Mark complete/incomplete

### 2.4 Conversation Memory
- **Session-based**: Store conversation context in memory during session
- **User-specific**: Each user has their own conversation context
- **No persistent history**: Conversations reset when browser refreshes (Phase 1)
- **Future enhancement**: Store conversation history in database (Phase 2)

---

## 3. User Stories & Example Conversations

### Story 1: Creating a Task
**User**: "I need to remember to call the dentist tomorrow"

**Bot**: "I've created that task for you! 📝

**Task:** Call the dentist tomorrow
**Status:** Pending

Would you like to add a deadline or description?"

**User**: "Make it for 3pm"

**Bot**: "Updated! Your task is now set for 3pm tomorrow."

---

### Story 2: Viewing All Tasks
**User**: "What tasks do I have?"

**Bot**: "You have 3 tasks:

📌 **Pending** (2):
1. Call the dentist tomorrow
2. Review project proposal

✅ **Completed** (1):
1. Buy groceries

Would you like me to help you with any of these?"

---

### Story 3: Updating a Task
**User**: "Mark the dentist task as done"

**Bot**: "Done! ✅ I've marked 'Call the dentist tomorrow' as complete."

---

### Story 4: Deleting a Task
**User**: "I don't need the project proposal task anymore"

**Bot**: "I've deleted 'Review project proposal'. You now have 1 pending task remaining."

---

### Story 5: Complex Multi-step
**User**: "Show me my overdue tasks"

**Bot**: "Looking at your tasks... You don't have any with specific deadlines yet. Would you like me to help you add deadlines to your existing tasks?"

**User**: "Yes, add a deadline to the dentist task for tomorrow at 3pm"

**Bot**: "Perfect! I've updated 'Call the dentist' with a deadline for tomorrow at 3pm. 📅"

---

## 4. Required API Endpoints

### 4.1 New Endpoint: Chatbot Interaction
```
POST /api/chat
```

**Request:**
```json
{
  "message": "Create a task to call the dentist",
  "conversation_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I've created that task for you! 📝\n\n**Task:** Call the dentist\n**Status:** Pending",
  "actions_performed": [
    {
      "type": "create_task",
      "task_id": 123,
      "details": {
        "title": "Call the dentist",
        "description": null
      }
    }
  ],
  "conversation_id": "session-uuid-123"
}
```

### 4.2 Existing Endpoints (Reuse)
The chatbot will use existing task endpoints internally:
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/toggle` - Toggle completion

### 4.3 Authentication
- Use existing JWT authentication
- Include `Authorization: Bearer <token>` header
- Chatbot inherits user's permissions automatically

---

## 5. Data Flow Summary

### 5.1 User Message Flow
```
1. User types message in chat UI
   ↓
2. Frontend sends POST /api/chat with message + JWT token
   ↓
3. Backend verifies JWT, extracts user_id
   ↓
4. Backend sends conversation history to OpenAI with function definitions
   ↓
5. OpenAI returns response + function call requests
   ↓
6. Backend executes requested functions (using existing task service)
   ↓
7. Backend formats response with task data
   ↓
8. Response sent back to frontend
   ↓
9. Frontend displays bot response + updates task list (if changed)
```

### 5.2 State Management
- **Frontend**: Chat messages stored in component state (React useState)
- **Backend**: Conversation context stored in memory during session
- **Task updates**: Refetch task list after chatbot actions to sync UI

### 5.3 Error Handling
- **AI service down**: Graceful fallback to predefined responses
- **Invalid user input**: Bot asks for clarification
- **Task operation fails**: Bot explains error and suggests solution
- **Authentication expired**: Redirect to login with message

---

## 6. Success Criteria

### 6.1 Functional Requirements
- ✅ Users can create tasks using natural language
- ✅ Users can view all their tasks via chat
- ✅ Users can update existing tasks (title, description, status)
- ✅ Users can delete tasks
- ✅ Chatbot understands context and follow-up questions
- ✅ Chatbot handles ambiguous requests with clarification questions

### 6.2 Non-Functional Requirements
- **Response time**: < 3 seconds for bot responses
- **Accuracy**: 90%+ correct intent recognition
- **Uptime**: Chatbot available 99.5% of the time
- **Cost**: Keep API costs under $50/month for reasonable usage

### 6.3 User Experience
- **Easy to use**: No instructions needed, intuitive interface
- **Helpful error messages**: Clear guidance when something goes wrong
- **Smooth integration**: Doesn't disrupt existing task management workflow

---

## 7. Implementation Phases

### Phase 1: MVP (Minimum Viable Product)
- Basic chatbot UI (floating widget)
- Core AI integration (OpenAI)
- 5 basic operations: create, view, update, delete, toggle tasks
- Simple conversation handling
- Session-based memory only

### Phase 2: Enhancements (Future)
- Persistent conversation history in database
- Task suggestions based on user patterns
- Smart deadline detection and reminders
- Multi-language support
- Voice input/output
- Chatbot analytics dashboard

---

## 8. File Structure (New Files)

### Backend
```
backend/
├── src/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py              # NEW: Chatbot endpoint
│   ├── services/
│   │   └── chatbot_service.py       # NEW: AI integration logic
│   └── core/
│       └── openai_client.py         # NEW: OpenAI client setup
```

### Frontend
```
frontend/
├── src/
│   ├── components/
│   │   └── chatbot/
│   │       ├── ChatWidget.tsx       # NEW: Floating chat button
│   │       ├── ChatPanel.tsx        # NEW: Expanded chat interface
│   │       └── MessageList.tsx      # NEW: Message history display
│   └── lib/
│       └── chatbot.ts               # NEW: Chatbot API client
```

---

## 9. Environment Variables Required

```bash
# Backend (.env)
OPENAI_API_KEY=sk-...                    # OpenAI API key
OPENAI_MODEL=gpt-4o-mini                 # Model to use
OPENAI_TEMPERATURE=0.7                   # Creativity level

# Optional:
CHATBOT_ENABLED=true                     # Feature flag
CHATBOT_MAX_HISTORY=10                   # Conversation history length
```

---

## 10. Open Questions & Decisions Needed

1. **AI Service**: Confirm OpenAI GPT-4o-mini or prefer Anthropic Claude?
2. **Budget**: What's the acceptable monthly cost for AI API calls?
3. **Conversation History**: Store in database (Phase 2) or keep session-only for now?
4. **Branding**: Should the chatbot have a name/personality?
5. **Launch**: Gradual rollout (beta users) or full release?

---

**Next Step**: Review this specification and provide feedback or approval to proceed with implementation! 🚀
