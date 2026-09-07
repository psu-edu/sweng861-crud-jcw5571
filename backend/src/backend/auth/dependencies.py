from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.database import models
from backend.database.connection import get_db


def require_auth(
    request: Request,
    db: Session = Depends(get_db),
) -> models.User:
    # Get the local user ID stored in the authenticated session.
    user_id = request.session.get("user_id")

    # No session: request is unauthenticated.
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Unauthorized",
                "message": "Valid authentication is required",
            },
        )

    # Look up the authenticated user in our local database.
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # The session refers to a user that no longer exists.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Unauthorized",
                "message": "Valid authentication is required",
            },
        )

    return user
