from datetime import datetime, timedelta, timezone

import jwt

from backend.config import settings


# JWTs expire after one hour.
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Identifies the algorithm used to sign the JWTs.
ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    """Create a signed JWT representing an authenticated application user."""

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> int:
    """Validate a JWT and return the local user ID stored in its subject."""

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Token does not contain a user ID.")

        return int(user_id)

    except (jwt.PyJWTError, ValueError) as exc:
        raise ValueError("Invalid access token.") from exc
