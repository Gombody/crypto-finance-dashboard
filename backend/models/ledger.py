from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
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
from backend.models.enums import LedgerDirection, LedgerStatus
from backend.models.mixins import TimestampMixin

from decimal import Decimal

class CryptoLedger(TimestampMixin, Base):
    __tablename__ = "crypto_ledger"
    __table_args__ = (
        Index("ix_crypto_ledger_occurred_at", "occurred_at"),
        Index("ix_crypto_ledger_project_id", "project_id"),
        Index("ix_crypto_ledger_category_id", "category_id"),
        Index("ix_crypto_ledger_token_id", "token_id"),
        Index("ix_crypto_ledger_status", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("project_master.id", ondelete="SET NULL"), nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category_master.id", ondelete="SET NULL"), nullable=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    exchange_account_id: Mapped[int | None] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="SET NULL"), nullable=True)
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id", ondelete="SET NULL"), nullable=True)
    direction: Mapped[LedgerDirection] = mapped_column(SAEnum(LedgerDirection, native_enum=False), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    unit_price_usd: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    total_value_usd: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    tx_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    external_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[LedgerStatus] = mapped_column(
        SAEnum(LedgerStatus, native_enum=False),
        nullable=False,
        default=LedgerStatus.POSTED,
    )
    voided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    void_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    replaced_by_id: Mapped[int | None] = mapped_column(ForeignKey("crypto_ledger.id", ondelete="SET NULL"), nullable=True)

    project = relationship("ProjectMaster")
    category = relationship("CategoryMaster")
    token = relationship("TokenMaster")
    exchange_account = relationship("ExchangeAccount")
    wallet = relationship("Wallet")
    replacement_entry = relationship("CryptoLedger", remote_side=[id], uselist=False)


class KRWLedger(TimestampMixin, Base):
    __tablename__ = "krw_ledger"
    __table_args__ = (
        Index("ix_krw_ledger_occurred_on", "occurred_on"),
        Index("ix_krw_ledger_project_id", "project_id"),
        Index("ix_krw_ledger_krw_category_id", "krw_category_id"),
        Index("ix_krw_ledger_status", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    occurred_on: Mapped[date] = mapped_column(Date, nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("project_master.id", ondelete="SET NULL"), nullable=True)
    krw_category_id: Mapped[int | None] = mapped_column(ForeignKey("krw_category_master.id", ondelete="SET NULL"), nullable=True)
    direction: Mapped[LedgerDirection] = mapped_column(SAEnum(LedgerDirection, native_enum=False), nullable=False)
    amount_krw: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    vendor_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    external_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)

    status: Mapped[LedgerStatus] = mapped_column(
        SAEnum(LedgerStatus, native_enum=False),
        nullable=False,
        default=LedgerStatus.POSTED,
    )
    voided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    void_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    replaced_by_id: Mapped[int | None] = mapped_column(ForeignKey("krw_ledger.id", ondelete="SET NULL"), nullable=True)

    project = relationship("ProjectMaster")
    krw_category = relationship("KRWCategoryMaster")
    replacement_entry = relationship("KRWLedger", remote_side=[id], uselist=False)


class MonthlyAssetBaseline(TimestampMixin, Base):
    __tablename__ = "monthly_asset_baselines"
    __table_args__ = (
        UniqueConstraint("baseline_month", "token_id", name="uq_monthly_asset_baselines_month_token"),
        CheckConstraint("baseline_amount >= 0", name="ck_monthly_asset_baselines_amount"),
        Index("ix_monthly_asset_baselines_baseline_month", "baseline_month"),
        Index("ix_monthly_asset_baselines_token_id", "token_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    baseline_month: Mapped[date] = mapped_column(Date, nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    baseline_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    baseline_price_usd: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    baseline_value_usd: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    is_manual_override: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    token = relationship("TokenMaster")