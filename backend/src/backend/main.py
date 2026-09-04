
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.config import settings
from backend.auth.routes import router as auth_router


app = FastAPI()

# SessionMiddleware gives Authlib a server-side mechanism for
# maintaining OAuth state between the login redirect and callback.
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
)

# Add authentication-related routes to the application.
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}
