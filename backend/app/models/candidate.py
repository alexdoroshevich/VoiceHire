"""Candidate model -- synced from ATS or manually created."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.agency import Agency  # lgtm[py/cyclic-import]
    from app.models.call import Call  # lgtm[py/cyclic-import]
    from app.models.candidate_evaluation import CandidateEvaluation  # lgtm[py/cyclic-import]


class Candidate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "candidates"

    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ats_candidate_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    ats_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    agency: Mapped[Agency] = relationship(back_populates="candidates")
    calls: Mapped[list[Call]] = relationship(back_populates="candidate")
    evaluations: Mapped[list[CandidateEvaluation]] = relationship(back_populates="candidate")
