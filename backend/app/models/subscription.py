"""Subscription model -- Stripe billing and usage tracking."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.agency import Agency  # lgtm[py/cyclic-import]


class Subscription(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "subscriptions"

    agency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agencies.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    plan: Mapped[str] = mapped_column(String(20), nullable=False, default="trial")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    included_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    used_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    overage_rate_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    agency: Mapped[Agency] = relationship(back_populates="subscription")
