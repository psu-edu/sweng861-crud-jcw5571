import json

import cohere

from backend.config import settings
from backend.tasks.schemas import TaskCreate


class CohereServiceError(Exception):
    """Base exception for Cohere integration failures."""


class CohereAPIError(CohereServiceError):
    """Raised when the Cohere API request fails."""


class CohereResponseError(CohereServiceError):
    """Raised when Cohere returns unusable task data."""

# Cohere model used to convert natural-language descriptions
# into structured task data.
MODEL = "command-a-plus-05-2026"

# JSON schema supplied to Cohere so the model returns task data
# in the structure expected by the application's TaskCreate model.
TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "A short, clear title for the task.",
        },
        "description": {
            "type": ["string", "null"],
            "description": "A concise description of what needs to be done.",
        },
        "status": {
            "type": "string",
            "enum": ["pending", "completed"],
            "description": "The current task status.",
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "The task priority.",
        },
        "due_date": {
            "type": ["string", "null"],
            "description": (
                "The task deadline as an ISO 8601 datetime string, "
                "or null if no deadline is specified."
            ),
        },
    },
    "required": [
        "title",
        "description",
        "status",
        "priority",
        "due_date",
    ],
}

client = cohere.ClientV2(
    api_key=settings.cohere_api_key,
)

def generate_task(description: str) -> TaskCreate:
    """Convert a natural-language task description into a validated task."""

    prompt = f"""
Create a task from the following user description.

Generate a JSON object containing:
- title
- description
- status
- priority
- due_date

Use "pending" as the status unless the user explicitly indicates
that the task is already completed.

Infer priority from the user's wording when possible. If no priority
is indicated, use "medium".

If no due date is provided or can reasonably be determined, use null.

The due_date must be an ISO 8601 datetime string when a deadline is
provided.

User description:
{description}
"""

    try:
        response = client.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format={
                "type": "json_object",
                "schema": TASK_SCHEMA,
            },
        )
    except Exception as exc:
        raise CohereAPIError(
            "The task-generation service is currently unavailable."
        ) from exc
    
    # ClientV2 responses can contain different content item types.
    # Extract the text item containing the structured JSON response.
    response_text = None

    for content_item in response.message.content:
        if content_item.type == "text":
            response_text = content_item.text
            break

    if response_text is None:
        raise CohereResponseError(
            "The task-generation service returned an empty response."
        )
    
    # Parse the JSON response and validate it against the TaskCreate model.
    try:
        task_data = json.loads(response_text)
        return TaskCreate.model_validate(task_data)
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise CohereResponseError(
            "The task-generation service returned invalid task data."
        ) from exc
