"""Call model -- records of screening calls made via Retell.ai."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.agency import Agency  # lgtm[py/cyclic-import]
    from app.models.call_transcript import CallTranscript  # lgtm[py/cyclic-import]
    from app.models.candidate import Candidate  # lgtm[py/cyclic-import]
    from app.models.candidate_evaluation import CandidateEvaluation  # lgtm[py/cyclic-import]
    from app.models.compliance_log import ComplianceLog  # lgtm[py/cyclic-import]
    from app.models.screening_flow import ScreeningFlow  # lgtm[py/cyclic-import]


class CallDirection(enum.StrEnum):
    outbound = "outbound"
    inbound = "inbound"


class CallStatus(enum.StrEnum):
    queued = "queued"
    ringing = "ringing"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    no_answer = "no_answer"
    voicemail = "voicemail"


class Call(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "calls"

    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )
    screening_flow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("screening_flows.id"),
        nullable=False,
    )
    retell_call_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True, index=True
    )
    direction: Mapped[CallDirection] = mapped_column(
        Enum(CallDirection, name="call_direction"), nullable=False
    )
    status: Mapped[CallStatus] = mapped_column(
        Enum(CallStatus, name="call_status"), nullable=False, default=CallStatus.queued
    )
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recording_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    cost_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agency: Mapped[Agency] = relationship(back_populates="calls")
    candidate: Mapped[Candidate] = relationship(back_populates="calls")
    screening_flow: Mapped[ScreeningFlow] = relationship()
    transcript: Mapped[CallTranscript | None] = relationship(back_populates="call", uselist=False)
    evaluation: Mapped[CandidateEvaluation | None] = relationship(
        back_populates="call", uselist=False
    )
    compliance_logs: Mapped[list[ComplianceLog]] = relationship(back_populates="call")
