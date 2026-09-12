from datetime import datetime

from sqlalchemy.orm import Session

from backend.database import models
from backend.tasks.schemas import TaskCreate


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
