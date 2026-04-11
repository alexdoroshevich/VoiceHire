"""ScreeningFlow model -- configurable screening templates per agency."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.agency import Agency  # lgtm[py/unsafe-cyclic-import]
    from app.models.screening_question import ScreeningQuestion  # lgtm[py/unsafe-cyclic-import]


class ScreeningFlow(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "screening_flows"

    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    voice_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    max_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=300)
    pass_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=70)

    agency: Mapped[Agency] = relationship(back_populates="screening_flows")
    questions: Mapped[list[ScreeningQuestion]] = relationship(
        back_populates="flow",
        order_by="ScreeningQuestion.position",
        cascade="all, delete-orphan",
    )
