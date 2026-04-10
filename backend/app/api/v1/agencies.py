"""Agency routes -- current agency CRUD and user management."""

from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.agency import Agency
from app.models.user import AgencyRole, User
from app.schemas.agency import AgencyResponse, AgencyUpdate
from app.schemas.auth import UserResponse
from app.services.auth.dependencies import CurrentAgencyId, CurrentUser

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/agencies", tags=["agencies"])


@router.get("/current", response_model=AgencyResponse)
async def get_current_agency(
    current_user: CurrentUser,
    agency_id: CurrentAgencyId,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AgencyResponse:
    """Get the current user's agency."""
    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    agency = result.scalar_one_or_none()
    if agency is None:
        raise HTTPException(status_code=404, detail="Agency not found")
    return AgencyResponse.model_validate(agency)


@router.patch("/current", response_model=AgencyResponse)
async def update_current_agency(
    body: AgencyUpdate,
    current_user: CurrentUser,
    agency_id: CurrentAgencyId,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AgencyResponse:
    """Update agency settings. Owner or admin only."""
    if current_user.agency_role not in (AgencyRole.owner, AgencyRole.admin):
        raise HTTPException(status_code=403, detail="Owner or admin access required")

    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    agency = result.scalar_one_or_none()
    if agency is None:
        raise HTTPException(status_code=404, detail="Agency not found")

    if body.name is not None:
        agency.name = body.name
    if body.settings is not None:
        agency.settings = body.settings

    await db.commit()
    await db.refresh(agency)
    return AgencyResponse.model_validate(agency)


@router.get("/current/users", response_model=list[UserResponse])
async def list_agency_users(
    current_user: CurrentUser,
    agency_id: CurrentAgencyId,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[UserResponse]:
    """List all users in the current agency."""
    result = await db.execute(
        select(User).where(User.agency_id == agency_id).order_by(User.created_at)
    )
    users = result.scalars().all()
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            role=u.role.value,
            agency_id=u.agency_id,
            agency_role=u.agency_role.value,
        )
        for u in users
    ]
