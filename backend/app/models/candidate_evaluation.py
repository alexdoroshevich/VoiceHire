"""CandidateEvaluation model -- Claude-generated screening scores."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.call import Call
    from app.models.candidate import Candidate


class CandidateEvaluation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "candidate_evaluations"

    call_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calls.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )
    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id"),
        nullable=False,
        index=True,
    )
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    question_scores: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    knockout_triggered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    knockout_question_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    evaluation_model: Mapped[str] = mapped_column(String(50), nullable=False)
    evaluation_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    synced_to_ats: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    call: Mapped[Call] = relationship(back_populates="evaluation")
    candidate: Mapped[Candidate] = relationship(back_populates="evaluations")
