import logging
from dataclasses import dataclass
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TaskCreated:
    """Domain event emitted when a task is successfully created."""

    task_id: int
    user_id: int
    title: str
    created_at: datetime


@dataclass(frozen=True)
class TaskUpdated:
    """Domain event emitted when a task is successfully updated."""

    task_id: int
    user_id: int
    updated_at: datetime


@dataclass(frozen=True)
class TaskDeleted:
    """Domain event emitted when a task is successfully deleted."""

    task_id: int
    user_id: int


def handle_task_created(event: TaskCreated) -> None:
    """Handle a TaskCreated event by logging it."""

    logger.info(
        "TaskCreated event: task_id=%s user_id=%s title=%s",
        event.task_id,
        event.user_id,
        event.title,
    )


def handle_task_updated(event: TaskUpdated) -> None:
    """Handle a TaskUpdated event by logging it."""

    logger.info(
        "TaskUpdated event: task_id=%s user_id=%s",
        event.task_id,
        event.user_id,
    )


def handle_task_deleted(event: TaskDeleted) -> None:
    """Handle a TaskDeleted event by logging it."""

    logger.info(
        "TaskDeleted event: task_id=%s user_id=%s",
        event.task_id,
        event.user_id,
    )
