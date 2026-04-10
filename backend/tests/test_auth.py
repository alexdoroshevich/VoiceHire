"""Auth endpoint tests."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from app.models.user import AgencyRole, User, UserRole
from app.services.auth.password import hash_password


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, mock_db: AsyncMock) -> None:
    """Registration creates agency + user and returns token."""
    # Mock: no existing user or agency with that slug
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "owner@test.com",
            "password": "StrongPass123!",
            "full_name": "Test Owner",
            "agency_name": "Test Agency",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, mock_db: AsyncMock) -> None:
    """Registration fails if email already exists."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = User(email="existing@test.com")
    mock_db.execute.return_value = mock_result

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "existing@test.com",
            "password": "StrongPass123!",
            "full_name": "Test",
            "agency_name": "Test Agency",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, mock_db: AsyncMock) -> None:
    """Login returns access token for valid credentials."""
    import uuid

    user = User(
        id=uuid.uuid4(),
        email="test@test.com",
        hashed_password=hash_password("correct_password"),
        full_name="Test User",
        role=UserRole.user,
        agency_id=uuid.uuid4(),
        agency_role=AgencyRole.recruiter,
        is_active=True,
        failed_login_attempts=0,
        locked_until=None,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_db.execute.return_value = mock_result

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@test.com", "password": "correct_password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, mock_db: AsyncMock) -> None:
    """Login fails with wrong password."""
    import uuid

    user = User(
        id=uuid.uuid4(),
        email="test@test.com",
        hashed_password=hash_password("correct_password"),
        full_name="Test User",
        role=UserRole.user,
        agency_id=uuid.uuid4(),
        agency_role=AgencyRole.recruiter,
        is_active=True,
        failed_login_attempts=0,
        locked_until=None,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_db.execute.return_value = mock_result

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@test.com", "password": "wrong_password"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_unauthenticated(client: AsyncClient) -> None:
    """GET /me returns 401 without token."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
