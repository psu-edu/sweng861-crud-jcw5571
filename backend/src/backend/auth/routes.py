from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.auth.oauth import oauth
from backend.database import models
from backend.database.connection import get_db


router = APIRouter()

@router.get("/auth/login")
async def login(request: Request):
    # Build Google's authorization URL and redirect the user's browser there.
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback", name="auth_callback")
async def auth_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    # Exchange Google's authorization code for tokens.
    token = await oauth.google.authorize_access_token(request)

    # Extract the user's identity from Google's ID token.
    user_info = token.get("userinfo")

    # Look for an existing local user with this Google ID.
    user = (
        db.query(models.User)
        .filter(models.User.provider_id == user_info["sub"])
        .first()
    )

    now = datetime.utcnow()

    if user:
        # Existing user: update their profile and login timestamp.
        user.email = user_info.get("email")
        user.name = user_info.get("name")
        user.updated_at = now
        user.last_login_at = now
    else:
        # New user: create a local record linked to their Google identity.
        user = models.User(
            provider_id=user_info["sub"],
            email=user_info.get("email"),
            name=user_info.get("name"),
            created_at=now,
            updated_at=now,
            last_login_at=now,
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    # Store our local user ID in the authenticated session.
    request.session["user_id"] = user.id

    return {
        "message": "Google authentication successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
    }
