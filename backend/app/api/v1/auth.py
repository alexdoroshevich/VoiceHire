"""Auth routes -- register, login, refresh, me."""

import re
import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.rate_limit import RateLimit
from app.models.agency import Agency
from app.models.user import AgencyRole, User, UserRole
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth.dependencies import CurrentUser
from app.services.auth.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.services.auth.password import hash_password, verify_password

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _slugify(name: str) -> str:
    """Convert agency name to URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:100]


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    _rate: RateLimit,
) -> TokenResponse:
    """Register a new user and create their agency."""
    # Check if email already exists
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create agency
    slug = _slugify(body.agency_name)
    # Ensure slug uniqueness
    slug_check = await db.execute(select(Agency).where(Agency.slug == slug))
    if slug_check.scalar_one_or_none() is not None:
        slug = f"{slug}-{int(datetime.now(UTC).timestamp()) % 10000}"

    agency = Agency(name=body.agency_name, slug=slug)
    db.add(agency)
    await db.flush()

    # Create user as agency owner
    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
        role=UserRole.user,
        agency_id=agency.id,
        agency_role=AgencyRole.owner,
    )
    db.add(user)
    await db.commit()

    logger.info("auth.register", user_id=str(user.id), agency_id=str(agency.id))

    access_token = create_access_token(user.id, agency.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    _rate: RateLimit,
) -> TokenResponse:
    """Authenticate with email and password."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user is None or user.hashed_password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Check lockout
    if user.locked_until and user.locked_until > datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Account temporarily locked. Try again later.",
        )

    if not verify_password(body.password, user.hashed_password):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.now(UTC) + timedelta(minutes=15)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Reset on successful login
    user.failed_login_attempts = 0
    user.locked_until = None
    await db.commit()

    access_token = create_access_token(user.id, user.agency_id)
    refresh_token = create_refresh_token(user.id)

    # Set refresh token as httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """Refresh the access token using the refresh cookie."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
        )

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    new_access = create_access_token(user.id, user.agency_id)
    new_refresh = create_refresh_token(user.id)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return TokenResponse(access_token=new_access)


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser) -> UserResponse:
    """Return the current authenticated user."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
        agency_id=current_user.agency_id,
        agency_role=current_user.agency_role.value,
        agency_name=current_user.agency.name if current_user.agency else None,
    )
