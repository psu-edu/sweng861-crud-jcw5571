from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import require_auth
from backend.database import models
from backend.database.connection import get_db
from backend.tasks import service
from backend.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    user: models.User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    return service.create_task(db, user, task_data)


@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    user: models.User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    # Only return tasks belonging to the authenticated user.
    return service.get_tasks(db, user)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    user: models.User = Depends(require_auth),
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
    user: models.User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    # The service only updates tasks owned by the authenticated user.
    task = service.update_task(db, user, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    user: models.User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    # The service verifies ownership before deleting the task.
    deleted = service.delete_task(db, user, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Successful deletion returns 204 No Content, so no response body is needed.
