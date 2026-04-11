"""Agency model -- the tenant table."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.ats_connection import ATSConnection  # lgtm[py/unsafe-cyclic-import]
    from app.models.call import Call  # lgtm[py/unsafe-cyclic-import]
    from app.models.candidate import Candidate  # lgtm[py/unsafe-cyclic-import]
    from app.models.compliance_log import ComplianceLog  # lgtm[py/unsafe-cyclic-import]
    from app.models.screening_flow import ScreeningFlow  # lgtm[py/unsafe-cyclic-import]
    from app.models.subscription import Subscription  # lgtm[py/unsafe-cyclic-import]
    from app.models.user import User  # lgtm[py/unsafe-cyclic-import]


class Agency(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agencies"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    plan: Mapped[str] = mapped_column(String(20), nullable=False, default="trial")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    settings: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    users: Mapped[list[User]] = relationship(back_populates="agency", cascade="all, delete-orphan")
    screening_flows: Mapped[list[ScreeningFlow]] = relationship(back_populates="agency")
    calls: Mapped[list[Call]] = relationship(back_populates="agency")
    candidates: Mapped[list[Candidate]] = relationship(back_populates="agency")
    ats_connections: Mapped[list[ATSConnection]] = relationship(back_populates="agency")
    compliance_logs: Mapped[list[ComplianceLog]] = relationship(back_populates="agency")
    subscription: Mapped[Subscription | None] = relationship(back_populates="agency", uselist=False)
