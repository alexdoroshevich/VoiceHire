"""ScreeningQuestion model -- individual questions within a flow."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.screening_flow import ScreeningFlow  # lgtm[py/unsafe-cyclic-import]


class QuestionType(enum.StrEnum):
    yes_no = "yes_no"
    open_ended = "open_ended"
    multiple_choice = "multiple_choice"
    availability = "availability"
    certification = "certification"


class ScreeningQuestion(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "screening_questions"

    flow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("screening_flows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_knockout: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expected_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    scoring_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    follow_up_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    flow: Mapped[ScreeningFlow] = relationship(back_populates="questions")
