from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import require_auth
from backend.database import models
from backend.database.connection import get_db
from backend.tasks import service
from backend.tasks.schemas import TaskCreate, TaskResponse


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
