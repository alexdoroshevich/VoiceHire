"""ComplianceLog model -- immutable audit trail for regulatory compliance."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.agency import Agency  # lgtm[py/unsafe-cyclic-import]
    from app.models.call import Call  # lgtm[py/unsafe-cyclic-import]


class ComplianceEventType(enum.StrEnum):
    consent_given = "consent_given"
    consent_refused = "consent_refused"
    ai_disclosure_played = "ai_disclosure_played"
    recording_started = "recording_started"
    recording_stopped = "recording_stopped"
    call_terminated_by_candidate = "call_terminated_by_candidate"
    data_deletion_requested = "data_deletion_requested"


class ComplianceLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "compliance_logs"

    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id"),
        nullable=False,
        index=True,
    )
    call_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calls.id"),
        nullable=True,
        index=True,
    )
    candidate_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id"),
        nullable=True,
    )
    event_type: Mapped[ComplianceEventType] = mapped_column(
        Enum(ComplianceEventType, name="compliance_event_type"), nullable=False
    )
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    agency: Mapped[Agency] = relationship(back_populates="compliance_logs")
    call: Mapped[Call | None] = relationship(back_populates="compliance_logs")
