from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.enums import AlertSeverity, AlertStatus
from backend.models.mixins import TimestampMixin

from decimal import Decimal

class Alert(TimestampMixin, Base):
    __tablename__ = "alerts"
    __table_args__ = (
        Index("ix_alerts_status", "status"),
        Index("ix_alerts_wallet_id", "wallet_id"),
        Index("ix_alerts_exchange_account_id", "exchange_account_id"),
        Index("ix_alerts_project_id", "project_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    alert_code: Mapped[str] = mapped_column(String(64), nullable=False)
    alert_name: Mapped[str] = mapped_column(String(128), nullable=False)
    severity: Mapped[AlertSeverity] = mapped_column(SAEnum(AlertSeverity, native_enum=False), nullable=False)
    status: Mapped[AlertStatus] = mapped_column(SAEnum(AlertStatus, native_enum=False), nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("project_master.id", ondelete="SET NULL"), nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category_master.id", ondelete="SET NULL"), nullable=True)
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id", ondelete="SET NULL"), nullable=True)
    exchange_account_id: Mapped[int | None] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="SET NULL"), nullable=True)
    threshold_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    project = relationship("ProjectMaster")
    category = relationship("CategoryMaster")
    wallet = relationship("Wallet")
    exchange_account = relationship("ExchangeAccount")


class AlertEvent(TimestampMixin, Base):
    __tablename__ = "alert_events"
    __table_args__ = (
        Index("ix_alert_events_alert_id", "alert_id"),
        Index("ix_alert_events_triggered_at", "triggered_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False)
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    observed_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    threshold_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_status: Mapped[str | None] = mapped_column(String(32), nullable=True)

    alert = relationship("Alert")