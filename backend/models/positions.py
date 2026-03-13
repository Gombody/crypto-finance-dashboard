from datetime import datetime

from sqlalchemy import (
    BigInteger,
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
from backend.models.enums import PositionSide, PositionStatus
from backend.models.mixins import TimestampMixin

from decimal import Decimal

class Position(TimestampMixin, Base):
    __tablename__ = "positions"
    __table_args__ = (
        Index("ix_positions_exchange_account_id", "exchange_account_id"),
        Index("ix_positions_token_id", "token_id"),
        Index("ix_positions_status", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    exchange_account_id: Mapped[int] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="CASCADE"), nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    side: Mapped[PositionSide] = mapped_column(SAEnum(PositionSide, native_enum=False), nullable=False)
    status: Mapped[PositionStatus] = mapped_column(SAEnum(PositionStatus, native_enum=False), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    entry_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    mark_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    liquidation_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    unrealized_pnl_usd: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    external_position_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    exchange_account = relationship("ExchangeAccount")
    token = relationship("TokenMaster")


class PositionSnapshot(TimestampMixin, Base):
    __tablename__ = "position_snapshots"
    __table_args__ = (
        Index("ix_position_snapshots_position_id", "position_id"),
        Index("ix_position_snapshots_snapshot_at", "snapshot_at"),
        Index("ix_position_snapshots_exchange_account_id", "exchange_account_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id", ondelete="CASCADE"), nullable=False)
    exchange_account_id: Mapped[int] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="CASCADE"), nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    side: Mapped[PositionSide] = mapped_column(SAEnum(PositionSide, native_enum=False), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    entry_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    mark_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    liquidation_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    unrealized_pnl_usd: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)

    position = relationship("Position")
    exchange_account = relationship("ExchangeAccount")
    token = relationship("TokenMaster")