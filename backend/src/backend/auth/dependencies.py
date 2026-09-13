from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from backend.database import models
from backend.database.connection import get_db
from backend.auth.jwt import decode_access_token


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


# Extracts a Bearer token from the Authorization header.
bearer_scheme = HTTPBearer()


def require_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """Authenticate a request using an application JWT."""

    try:
        # Decode and validate the JWT, then retrieve the local user ID.
        user_id = decode_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Unauthorized",
                "message": "Valid authentication is required",
            },
        )

    # Find the local user represented by the JWT.
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Unauthorized",
                "message": "Valid authentication is required",
            },
        )

    return user
