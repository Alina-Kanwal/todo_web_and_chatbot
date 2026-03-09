"""
Chatbot API routes.
Provides conversational interface for task management.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict, Generator
from sqlmodel import Session, create_engine
from src.services.chatbot_service import ChatbotService, ConversationContext
from src.core.openai_client import get_openai_client
from src.core.config import get_settings
from src.services.auth_service import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid

settings = get_settings()

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])
security = HTTPBearer(auto_error=False)


def get_db_session() -> Generator[Session, None, None]:
    """Get database session."""
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    engine = create_engine(settings.database_url, connect_args=connect_args)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Get current user ID from JWT token.

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        int: User ID

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload["user_id"]


# Request/Response schemas
class ChatRequest(BaseModel):
    """Request schema for chat message."""
    message: str = Field(min_length=1, max_length=2000, description="User's message to the chatbot")
    conversation_id: Optional[str] = Field(default=None, description="Conversation session ID for context")


class ChatAction(BaseModel):
    """Schema for an action performed by the chatbot."""
    type: str = Field(description="Type of action (create_task, update_task, delete_task, etc.)")
    task_id: Optional[int] = Field(default=None, description="ID of the task affected")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional action data")


class ChatResponse(BaseModel):
    """Response schema for chat message."""
    response: str = Field(description="Chatbot's natural language response")
    actions_performed: List[ChatAction] = Field(default_factory=list, description="Actions performed by the chatbot")
    conversation_id: str = Field(description="Conversation session ID")


class ErrorResponse(BaseModel):
    """Generic error response."""
    status_code: int
    error_type: str
    message: str


# In-memory conversation storage (simple implementation)
# In production, use Redis or database for persistence
_conversations: Dict[str, ConversationContext] = {}


def get_or_create_conversation(conversation_id: Optional[str]) -> ConversationContext:
    """Get existing conversation or create new one."""
    if conversation_id and conversation_id in _conversations:
        return _conversations[conversation_id]

    new_id = str(uuid.uuid4())
    new_conversation = ConversationContext(session_id=new_id)
    _conversations[new_id] = new_conversation
    return new_conversation


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Chat with the AI task assistant.

    - **message**: Your message to the chatbot (1-2000 characters)
    - **conversation_id**: Optional session ID for maintaining conversation context

    The chatbot can help you:
    - Create new tasks
    - List and view tasks
    - Update existing tasks
    - Delete tasks
    - Answer questions about your tasks

    Example:
    ```
    POST /api/chat
    {
        "message": "Create a task to buy milk",
        "conversation_id": "optional-session-id"
    }
    ```

    Response:
    ```json
    {
        "response": "I've created that task for you! 📝\\n\\n**Task:** Buy milk\\n**Status:** Pending",
        "actions_performed": [
            {
                "type": "create_task",
                "task_id": 123,
                "data": {"title": "Buy milk", "description": null}
            }
        ],
        "conversation_id": "session-uuid"
    }
    ```
    """

    # Edge case: Empty or whitespace-only message
    message = request.message.strip()
    if not message:
        return ChatResponse(
            response="Kuch to type karo yaar! 😄 Try 'add task [task name]' or 'show my tasks'!",
            actions_performed=[],
            conversation_id=request.conversation_id or str(uuid.uuid4())
        )

    # Edge case: Greeting only
    greetings = ['hi', 'hello', 'hey', 'hola', 'thanks', 'thank you', 'thx']
    if message.lower() in greetings:
        return ChatResponse(
            response="Hey there! 👋 What can I help you with today? Try 'add task...' or 'show tasks'! 😊",
            actions_performed=[],
            conversation_id=request.conversation_id or str(uuid.uuid4())
        )

    try:
        # Validate OpenAI API key is configured
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )

        # Get or create conversation context
        conversation = get_or_create_conversation(request.conversation_id)

        # Get OpenAI client
        openai_client = get_openai_client()

        # Create chatbot service
        chatbot_service = ChatbotService(openai_client)

        # Process the message
        result = chatbot_service.process_message(
            user_message=message,
            user_id=user_id,
            session=session,
            context=conversation
        )

        # Format actions for response
        actions = [
            ChatAction(
                type=action.get("type"),
                task_id=action.get("task_id"),
                data=action.get("data", {})
            )
            for action in result.get("actions", [])
        ]

        return ChatResponse(
            response=result["reply"],
            actions_performed=actions,
            conversation_id=conversation.session_id
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle ValueError (e.g., missing API key)
        import traceback
        print(f"❌ ValueError in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected errors
        import traceback
        print(f"❌ Exception in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Conversation not found"},
    },
)
async def clear_conversation(
    conversation_id: str,
    user_id: int = Depends(get_current_user_id),
):
    """
    Clear a conversation's history.

    Use this endpoint to reset the conversation context and start fresh.

    - **conversation_id**: The session ID to clear

    Returns 204 No Content on success.
    """
    if conversation_id not in _conversations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    del _conversations[conversation_id]
