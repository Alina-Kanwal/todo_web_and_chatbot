"""
Chatbot service layer.
Handles AI conversation logic and task operations.
"""

from typing import List, Dict, Optional, Any
from sqlmodel import Session
from openai import OpenAI
from src.core.config import get_settings
from src.services import task_service

settings = get_settings()


class ChatbotMessage:
    """Represents a message in the conversation."""
    def __init__(self, role: str, content: str):
        self.role = role  # 'user', 'assistant', or 'system'
        self.content = content


class ConversationContext:
    """Manages conversation context and history."""
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id
        self.messages: List[ChatbotMessage] = []
        self.user_tasks_cache: Optional[List] = None

    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.messages.append(ChatbotMessage(role, content))

    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent messages for API call."""
        recent = self.messages[-limit:] if len(self.messages) > limit else self.messages
        return [{"role": msg.role, "content": msg.content} for msg in recent]


class ChatbotService:
    """Service for handling chatbot interactions."""

    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature

        # Define function schemas for task operations (Groq-compatible format)
        self.functions = [
            {
                "name": "create_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The task title (what needs to be done)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Additional details about the task (optional)"
                        }
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List all tasks or filter by status (pending/completed)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "completed", "all"],
                            "description": "Filter tasks by status"
                        }
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task (mark complete/incomplete, change title)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_identifier": {
                            "type": "string",
                            "description": "Which task to update (can be task number, title, or description)"
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Mark task as complete (true) or incomplete (false)"
                        }
                    },
                    "required": ["task_identifier"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_identifier": {
                            "type": "string",
                            "description": "Which task to delete (can be task number, title, or description)"
                        }
                    },
                    "required": ["task_identifier"]
                }
            }
        ]

    def _find_task_by_identifier(
        self,
        tasks: List,
        identifier: str
    ) -> Optional[Any]:
        """
        Find a task by natural language identifier.

        Args:
            tasks: List of task objects
            identifier: Natural language description or number

        Returns:
            Task object if found, None otherwise
        """
        if not tasks:
            return None

        # Try to parse as number (1st, 2nd, 3rd task)
        import re
        number_match = re.search(r'(\d+)(?:st|nd|rd|th)?', identifier.lower())
        if number_match:
            index = int(number_match.group(1)) - 1
            if 0 <= index < len(tasks):
                return tasks[index]

        # Try to match by title or description
        identifier_lower = identifier.lower()
        for task in tasks:
            if (identifier_lower in task.title.lower() or
                (task.description and identifier_lower in task.description.lower())):
                return task

        return None

    def _format_tasks_for_display(self, tasks: List) -> str:
        """Format tasks for display in chat response."""
        if not tasks:
            return "You don't have any tasks yet."

        pending = [t for t in tasks if not t.completed]
        completed = [t for t in tasks if t.completed]

        response_parts = []

        if pending:
            response_parts.append(f"📌 **Pending** ({len(pending)}):")
            for i, task in enumerate(pending, 1):
                response_parts.append(f"{i}. {task.title}")
                if task.description:
                    response_parts.append(f"   _{task.description}_")

        if completed:
            response_parts.append(f"\n✅ **Completed** ({len(completed)}):")
            for i, task in enumerate(completed[:5], 1):  # Show max 5 completed
                response_parts.append(f"{i}. {task.title}")

        return "\n".join(response_parts)

    def process_message(
        self,
        user_message: str,
        user_id: int,
        session: Session,
        context: ConversationContext
    ) -> Dict[str, Any]:
        """
        Process user message and generate response.

        Args:
            user_message: The user's input message
            user_id: Current user's ID
            session: Database session
            context: Conversation context

        Returns:
            Dict with 'reply' and 'actions' keys
        """
        # Add user message to context
        context.add_message("user", user_message)

        # Prepare system message
        system_message = """You are a cheerful and efficient Task Buddy! 😊 Your role is to help users manage their tasks through natural conversation in a fun and motivating way.

Key capabilities:
- Create tasks with titles and descriptions
- List tasks (all, pending, or completed)
- Update tasks (mark complete/incomplete, change title)
- Delete tasks

Personality guidelines:
- Be super friendly and enthusiastic! Use emojis frequently 😊🎉✨
- Keep replies SHORT and MOTIVATING (2-3 sentences max)
- Celebrate when users complete tasks! 🎊
- Be encouraging: "You've got this!", "Great job!", "Almost there!"
- Use fun phrases: "Let's do this!", "On it! 🚀", "Super!"
- Format task lists clearly with emojis and numbers

Example interactions:
User: "Create a task to buy milk"
Bot: "Got it! 🎉 Created 'Buy milk' for you! Want to add anything else? 😊"

User: "Show my tasks"
Bot: "Here's what you've got! 📋\n\n📌 Pending (1):\n1. Buy milk\n\nYou've got this! 💪"

User: "Mark it complete"
Bot: "Boom! ✅ Task done! Great job! 🎊 You're crushing it today! 🚀"

If user sends empty message or just greetings:
- "Hey there! 👋 What can I help you with today? Try 'add task...' or 'show tasks'! 😊"

If you don't understand:
- "Hmm, I didn't quite catch that... 😅 Try saying 'add task [task name]' or 'show my tasks'! """

        # Get conversation history
        messages = [{"role": "system", "content": system_message}]
        messages.extend(context.get_recent_messages())

        try:
            # Call Groq API with function calling (Groq uses tools instead of functions)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                tools=[{"type": "function", "function": func} for func in self.functions],
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # Check if AI wants to call a function
            if assistant_message.tool_calls:
                tool_call = assistant_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = eval(tool_call.function.arguments)

                # Execute the function
                result = self._execute_function(
                    function_name,
                    function_args,
                    user_id,
                    session,
                    context
                )

                # Get final response from AI
                messages.append(assistant_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature
                )

                reply = final_response.choices[0].message.content

                # Add assistant response to context
                context.add_message("assistant", reply)

                return {
                    "reply": reply,
                    "actions": result.get("actions", [])
                }

            else:
                # No function call, just return the text response
                reply = assistant_message.content or "I understand. How can I help you with your tasks?"

                # Add assistant response to context
                context.add_message("assistant", reply)

                return {
                    "reply": reply,
                    "actions": []
                }

        except Exception as e:
            error_reply = f"I encountered an error: {str(e)}. Please try again or rephrase your request."
            context.add_message("assistant", error_reply)
            return {
                "reply": error_reply,
                "actions": []
            }

    def _execute_function(
        self,
        function_name: str,
        arguments: Dict,
        user_id: int,
        session: Session,
        context: ConversationContext
    ) -> Dict[str, Any]:
        """Execute a function call and return results."""

        if function_name == "create_task":
            task = task_service.create_task(
                session=session,
                user_id=user_id,
                title=arguments.get("title"),
                description=arguments.get("description")
            )
            return {
                "result": f"Created task: {task.title}",
                "actions": [{
                    "type": "create_task",
                    "task_id": task.id,
                    "data": {
                        "title": task.title,
                        "description": task.description
                    }
                }]
            }

        elif function_name == "list_tasks":
            status = arguments.get("status")
            if status == "all":
                status = None

            tasks = task_service.get_user_tasks(
                session=session,
                user_id=user_id,
                status=status,
                sort="created_at",
                order="desc"
            )

            # Cache tasks for potential follow-up operations
            context.user_tasks_cache = tasks

            formatted = self._format_tasks_for_display(tasks)
            return {
                "result": formatted,
                "actions": []
            }

        elif function_name == "update_task":
            # Refresh cache if needed
            if not context.user_tasks_cache:
                context.user_tasks_cache = task_service.get_user_tasks(
                    session=session,
                    user_id=user_id
                )

            task = self._find_task_by_identifier(
                context.user_tasks_cache,
                arguments.get("task_identifier", "")
            )

            if not task:
                return {
                    "result": "I couldn't find that task. Can you specify which one you mean?",
                    "actions": []
                }

            updates = {}
            if "title" in arguments:
                updates["title"] = arguments["title"]
            if "description" in arguments:
                updates["description"] = arguments["description"]
            if "completed" in arguments:
                updates["completed"] = arguments["completed"]

            updated_task = task_service.update_task(
                session=session,
                task_id=task.id,
                user_id=user_id,
                updates=updates
            )

            return {
                "result": f"Updated task: {updated_task.title}",
                "actions": [{
                    "type": "update_task",
                    "task_id": updated_task.id,
                    "data": updates
                }]
            }

        elif function_name == "delete_task":
            # Refresh cache if needed
            if not context.user_tasks_cache:
                context.user_tasks_cache = task_service.get_user_tasks(
                    session=session,
                    user_id=user_id
                )

            task = self._find_task_by_identifier(
                context.user_tasks_cache,
                arguments.get("task_identifier", "")
            )

            if not task:
                return {
                    "result": "I couldn't find that task. Can you specify which one you mean?",
                    "actions": []
                }

            success = task_service.delete_task(
                session=session,
                task_id=task.id,
                user_id=user_id
            )

            if success:
                return {
                    "result": f"Deleted task: {task.title}",
                    "actions": [{
                        "type": "delete_task",
                        "task_id": task.id,
                        "data": {"title": task.title}
                    }]
                }
            else:
                return {
                    "result": "Failed to delete that task.",
                    "actions": []
                }

        else:
            return {
                "result": f"Unknown function: {function_name}",
                "actions": []
            }
