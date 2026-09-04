from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# SQLite stores the development database in a local file.
DATABASE_URL = "sqlite:///./app.db"


# The engine manages communication between SQLAlchemy and SQLite.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# SessionLocal creates database sessions for individual operations.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base is the parent class for our database models.
class Base(DeclarativeBase):
    pass
