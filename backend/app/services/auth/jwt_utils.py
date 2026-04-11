"""JWT token creation and decoding."""

import uuid
from datetime import UTC, datetime, timedelta

import jwt

from app.config import settings


def create_access_token(user_id: uuid.UUID, agency_id: uuid.UUID | None = None) -> str:
    """Create a short-lived access token with user_id and agency_id claims."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload: dict = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }
    if agency_id is not None:
        payload["agency_id"] = str(agency_id)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(user_id: uuid.UUID) -> str:
    """Create a long-lived refresh token."""
    expire = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_token_expire_days)
    payload: dict = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises jwt.PyJWTError on failure."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
