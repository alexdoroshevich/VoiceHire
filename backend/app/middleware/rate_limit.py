"""Redis-backed rate limiter -- used as a FastAPI dependency on auth endpoints."""

from typing import Annotated

import structlog
from fastapi import Depends, HTTPException, Request, status

from app.config import settings
from app.redis_client import get_redis

logger = structlog.get_logger(__name__)


async def auth_rate_limit(request: Request) -> None:
    """Dependency that enforces rate limiting per IP on auth endpoints."""
    redis = await get_redis()
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:auth:{client_ip}"

    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, settings.rate_limit_auth_window_seconds)

        if count > settings.rate_limit_auth_requests:
            logger.warning(
                "auth.rate_limit_exceeded",
                count=count,
                limit=settings.rate_limit_auth_requests,
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please wait before trying again.",
                headers={"Retry-After": str(settings.rate_limit_auth_window_seconds)},
            )
    except HTTPException:
        raise
    except Exception as exc:
        # Redis unavailable -- fail open
        logger.error("auth.rate_limit_error", error=str(exc))


RateLimit = Annotated[None, Depends(auth_rate_limit)]
