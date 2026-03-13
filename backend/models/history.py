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
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.enums import BalanceOwnerType, TxDirection, TxStatus
from backend.models.mixins import TimestampMixin

from decimal import Decimal

class BalanceSnapshot(TimestampMixin, Base):
    __tablename__ = "balance_snapshots"
    __table_args__ = (
        Index("ix_balance_snapshots_snapshot_at", "snapshot_at"),
        Index("ix_balance_snapshots_wallet_snapshot_at", "wallet_id", "snapshot_at"),
        Index("ix_balance_snapshots_exchange_snapshot_at", "exchange_account_id", "snapshot_at"),
        Index("ix_balance_snapshots_token_snapshot_at", "token_id", "snapshot_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    owner_type: Mapped[BalanceOwnerType] = mapped_column(SAEnum(BalanceOwnerType, native_enum=False), nullable=False)
    exchange_account_id: Mapped[int | None] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="CASCADE"), nullable=True)
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), nullable=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    balance_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    usd_price: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    usd_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    source_run_id: Mapped[int | None] = mapped_column(ForeignKey("sync_job_runs.id", ondelete="SET NULL"), nullable=True)

    exchange_account = relationship("ExchangeAccount")
    wallet = relationship("Wallet")
    token = relationship("TokenMaster")
    source_run = relationship("SyncJobRun")


class WalletTxHistory(TimestampMixin, Base):
    __tablename__ = "wallet_tx_history"
    __table_args__ = (
        UniqueConstraint("chain_type", "tx_hash", "token_id", name="uq_wallet_tx_history_chain_tx_token"),
        Index("ix_wallet_tx_history_wallet_id", "wallet_id"),
        Index("ix_wallet_tx_history_token_id", "token_id"),
        Index("ix_wallet_tx_history_confirmed_at", "confirmed_at"),
        Index("ix_wallet_tx_history_from_address", "from_address"),
        Index("ix_wallet_tx_history_to_address", "to_address"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    chain_type: Mapped[str] = mapped_column(String(32), nullable=False)
    tx_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    block_number: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tx_direction: Mapped[TxDirection] = mapped_column(SAEnum(TxDirection, native_enum=False), nullable=False)
    tx_status: Mapped[TxStatus] = mapped_column(SAEnum(TxStatus, native_enum=False), nullable=False)
    from_address: Mapped[str | None] = mapped_column(String(128), nullable=True)
    to_address: Mapped[str | None] = mapped_column(String(128), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    fee_amount: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    fee_token_symbol: Mapped[str | None] = mapped_column(String(32), nullable=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)

    wallet = relationship("Wallet")
    token = relationship("TokenMaster")


class BalanceChange(TimestampMixin, Base):
    __tablename__ = "balance_changes"
    __table_args__ = (
        Index("ix_balance_changes_detected_at", "detected_at"),
        Index("ix_balance_changes_wallet_id", "wallet_id"),
        Index("ix_balance_changes_exchange_account_id", "exchange_account_id"),
        Index("ix_balance_changes_token_id", "token_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    owner_type: Mapped[BalanceOwnerType] = mapped_column(SAEnum(BalanceOwnerType, native_enum=False), nullable=False)
    exchange_account_id: Mapped[int | None] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="CASCADE"), nullable=True)
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), nullable=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    previous_amount: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    delta_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    delta_usd_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    source_run_id: Mapped[int | None] = mapped_column(ForeignKey("sync_job_runs.id", ondelete="SET NULL"), nullable=True)
    reason_hint: Mapped[str | None] = mapped_column(String(255), nullable=True)

    exchange_account = relationship("ExchangeAccount")
    wallet = relationship("Wallet")
    token = relationship("TokenMaster")
    source_run = relationship("SyncJobRun")