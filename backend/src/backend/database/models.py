from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.connection import Base


class User(Base):
    # Tell SQLAlchemy which database table this model represents.
    __tablename__ = "users"

    # The application's own identifier for the user.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Google's stable identifier for this user.
    provider_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # Basic profile information supplied by Google.
    email: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

    # Timestamps let us track when the account was created and modified.
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    last_login_at: Mapped[datetime] = mapped_column(DateTime)
    
    # Tasks owned by this user.
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

class Task(Base):
    # Tell SQLAlchemy which database table this model represents.
    __tablename__ = "tasks"

    # Unique identifier for the task.
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID of the user who owns this task.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    # Task information.
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    priority: Mapped[str] = mapped_column(String(20), default="medium")

    # Optional deadline.
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Timestamps.
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)

    # The user who owns this task.
    user: Mapped["User"] = relationship(
        back_populates="tasks",
    )
