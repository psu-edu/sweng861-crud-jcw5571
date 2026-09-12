
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware

from backend.config import settings
from backend.auth.routes import router as auth_router
from backend.auth.dependencies import require_auth

from backend.database.connection import Base, engine
from backend.database import models

from backend.tasks.routes import router as tasks_router

app = FastAPI()

# Create database tables defined by our SQLAlchemy models.
Base.metadata.create_all(bind=engine)

# SessionMiddleware gives Authlib a server-side mechanism for
# maintaining OAuth state between the login redirect and callback.
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
)

# Add authentication-related routes to the application.
app.include_router(auth_router)

# Add task-related routes to the application.
app.include_router(tasks_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/hello")
def hello(user: models.User = Depends(require_auth)):
    return {
        "message": f"Hello, {user.email}!"
    }

@app.get("/")
def frontend():
    return FileResponse("src/backend/frontend/index.html")

@app.get("/api/me")
def me(user: models.User = Depends(require_auth)):
    return {
        "email": user.email,
        "name": user.name,
    }
