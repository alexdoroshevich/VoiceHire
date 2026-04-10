"""ATSConnection model -- encrypted ATS credentials per agency."""

from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.agency import Agency


class ATSProviderType(enum.StrEnum):
    bullhorn = "bullhorn"
    avionte = "avionte"
    tempworks = "tempworks"


class ATSConnection(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ats_connections"

    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    provider: Mapped[ATSProviderType] = mapped_column(
        Enum(ATSProviderType, name="ats_provider_type"), nullable=False
    )
    credentials: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_sync_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sync_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sync_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    agency: Mapped[Agency] = relationship(back_populates="ats_connections")
