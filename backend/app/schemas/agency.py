"""Agency request/response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class AgencyResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    plan: str
    is_active: bool
    settings: dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AgencyUpdate(BaseModel):
    name: str | None = None
    settings: dict | None = None
