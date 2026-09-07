from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

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
