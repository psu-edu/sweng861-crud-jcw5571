from datetime import datetime

from sqlalchemy.orm import Session

from backend.database import models
from backend.tasks.schemas import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    user: models.User,
    task_data: TaskCreate,
) -> models.Task:
    """Create and persist a task owned by the authenticated user."""

    now = datetime.utcnow()

    task = models.Task(
        user_id=user.id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        created_at=now,
        updated_at=now,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    user: models.User,
) -> list[models.Task]:
    """Return all tasks owned by the authenticated user."""

    # Filter by user ID to prevent users from seeing other users' tasks.
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user.id)
        .order_by(models.Task.created_at.desc())
        .all()
    )


def get_task(
    db: Session,
    user: models.User,
    task_id: int,
) -> models.Task | None:
    """Return a specific task; task must be owned by the authenticated user."""

    # Require both the task ID and the authenticated user's ID to match.
    # This prevents users from accessing tasks they do not own.
    return (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id,
            models.Task.user_id == user.id,
        )
        .first()
    )


def update_task(
    db: Session,
    user: models.User,
    task_id: int,
    task_data: TaskUpdate,
) -> models.Task | None:
    """Update a task; task must be owned by the authenticated user."""

    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id,
            models.Task.user_id == user.id,
        )
        .first()
    )

    if task is None:
        return None

    # Only update fields that were provided by the client.
    # The updated_at timestamp is always updated automatically.
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    user: models.User,
    task_id: int,
) -> bool:
    """Delete a task; task must be owned by the authenticated user."""

    # Require both the task ID and owner ID to match before deleting.
    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id,
            models.Task.user_id == user.id,
        )
        .first()
    )

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True
