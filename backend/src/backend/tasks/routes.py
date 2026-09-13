from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import require_jwt
from backend.database import models
from backend.database.connection import get_db
from backend.ai.cohere import CohereAPIError, CohereResponseError, generate_task
from backend.events.task_events import (
    TaskCreated,
    TaskDeleted,
    TaskUpdated,
    handle_task_created,
    handle_task_deleted,
    handle_task_updated,
)
from backend.tasks import service
from backend.tasks.schemas import (
    TaskCreate,
    TaskFromDescriptionRequest,
    TaskResponse,
    TaskUpdate,
)


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    user: models.User = Depends(require_jwt),
    db: Session = Depends(get_db),
):
    task = service.create_task(db, user, task_data)
    
    # Publish the domain event after the task is successfully created.
    event = TaskCreated(
        task_id=task.id,
        user_id=user.id,
        title=task.title,
        created_at=task.created_at,
    )
    background_tasks.add_task(handle_task_created, event)

    return task


@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    user: models.User = Depends(require_jwt),
    db: Session = Depends(get_db),
):
    # Only return tasks belonging to the authenticated user.
    return service.get_tasks(db, user)


@router.post(
    "/from-description",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_from_description(
    request: TaskFromDescriptionRequest,
    background_tasks: BackgroundTasks,
    user: models.User = Depends(require_jwt),
    db: Session = Depends(get_db),
):

    # Convert the user's natural-language description into a validated
    # TaskCreate object using the Cohere integration.
    try:
        task_data = generate_task(request.description)
    except CohereAPIError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "AI service unavailable",
                "message": "The task-generation service is currently unavailable.",
            },
        )
    except CohereResponseError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "Invalid AI response",
                "message": "The task-generation service returned invalid data.",
            },
        )
    task = service.create_task(
        db,
        user,
        task_data,
    )

    # Publish the domain event after the task is successfully created.
    # Same as create_task endpoint.
    event = TaskCreated(
        task_id=task.id,
        user_id=user.id,
        title=task.title,
        created_at=task.created_at,
    )

    background_tasks.add_task(handle_task_created, event)

    return task


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    user: models.User = Depends(require_jwt),
    db: Session = Depends(get_db),
):
    # The service checks both the task ID and the authenticated user's ownership.
    task = service.get_task(db, user, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    user: models.User = Depends(require_jwt),
    db: Session = Depends(get_db),
):
    # Ensure that at least one field is provided for update.
    if not task_data.model_dump(exclude_none=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update.",
        )

    # The service only updates tasks owned by the authenticated user.
    task = service.update_task(db, user, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Publish the domain event after the task is successfully updated.
    event = TaskUpdated(
        task_id=task.id,
        user_id=user.id,
        updated_at=task.updated_at,
    )

    background_tasks.add_task(handle_task_updated, event)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    user: models.User = Depends(require_jwt),
    db: Session = Depends(get_db),
):
    # The service verifies ownership before deleting the task.
    deleted = service.delete_task(db, user, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Publish the domain event after the task is successfully deleted.
    event = TaskDeleted(
        task_id=task_id,
        user_id=user.id,
    )

    background_tasks.add_task(handle_task_deleted, event)


    # Successful deletion returns 204 No Content, so no response body is needed.
