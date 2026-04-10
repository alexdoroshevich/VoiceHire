"""Health check endpoint tests."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_ok(client: AsyncClient, mock_db: AsyncMock) -> None:
    """Health check returns 200 when DB is reachable."""
    mock_result = MagicMock()
    mock_db.execute.return_value = mock_result

    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_db_down(client: AsyncClient, mock_db: AsyncMock) -> None:
    """Health check returns 503 when DB is unreachable."""
    mock_db.execute.side_effect = ConnectionError("DB down")

    response = await client.get("/health")
    assert response.status_code == 503
