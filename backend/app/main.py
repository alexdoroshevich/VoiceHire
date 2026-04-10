"""VoiceHire -- FastAPI application entry point."""

import typing
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import structlog
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.agencies import router as agencies_router
from app.api.v1.auth import router as auth_router
from app.config import settings
from app.database import get_db
from app.logging import configure_logging
from app.redis_client import close_redis

configure_logging()

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Application lifespan -- startup and shutdown hooks."""
    logger.info("voicehire.startup", env=settings.app_env, debug=settings.debug)
    yield
    await close_redis()
    logger.info("voicehire.shutdown")


app = FastAPI(
    title="VoiceHire API",
    version="0.1.0",
    description="Voice AI platform for staffing agencies",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(agencies_router)


@app.get("/health", tags=["ops"])
async def health_check(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, typing.Any]:
    """Readiness probe -- checks process is up AND database is reachable."""
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        logger.error("health.db_unreachable", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unreachable",
        )
    return {"status": "ok", "version": "0.1.0"}
