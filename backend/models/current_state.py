from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.enums import PriceSourceType
from backend.models.mixins import TimestampMixin

from decimal import Decimal

class PortfolioCurrentPrice(TimestampMixin, Base):
    __tablename__ = "portfolio_current_prices"
    __table_args__ = (
        UniqueConstraint("token_id", name="uq_portfolio_current_prices_token"),
        CheckConstraint("price_usd >= 0", name="ck_portfolio_current_prices_price_usd"),
        Index("ix_portfolio_current_prices_price_updated_at", "price_updated_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="CASCADE"), nullable=False)
    price_usd: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    price_source: Mapped[PriceSourceType] = mapped_column(SAEnum(PriceSourceType, native_enum=False), nullable=False)
    price_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)

    token = relationship("TokenMaster")


class ExchangeCurrentBalance(TimestampMixin, Base):
    __tablename__ = "exchange_current_balances"
    __table_args__ = (
        UniqueConstraint("exchange_account_id", "token_id", name="uq_exchange_current_balances_account_token"),
        CheckConstraint("available_amount >= 0", name="ck_exchange_current_balances_available_amount"),
        CheckConstraint("locked_amount >= 0", name="ck_exchange_current_balances_locked_amount"),
        CheckConstraint("total_amount >= 0", name="ck_exchange_current_balances_total_amount"),
        Index("ix_exchange_current_balances_exchange_account_id", "exchange_account_id"),
        Index("ix_exchange_current_balances_token_id", "token_id"),
        Index("ix_exchange_current_balances_last_synced_at", "last_synced_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_account_id: Mapped[int] = mapped_column(ForeignKey("exchange_accounts.id", ondelete="CASCADE"), nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    available_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False, default=0)
    locked_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False, default=0)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False, default=0)
    usd_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    exchange_account = relationship("ExchangeAccount")
    token = relationship("TokenMaster")


class WalletCurrentBalance(TimestampMixin, Base):
    __tablename__ = "wallet_current_balances"
    __table_args__ = (
        UniqueConstraint("wallet_id", "token_id", name="uq_wallet_current_balances_wallet_token"),
        CheckConstraint("balance_amount >= 0", name="ck_wallet_current_balances_balance_amount"),
        Index("ix_wallet_current_balances_wallet_id", "wallet_id"),
        Index("ix_wallet_current_balances_token_id", "token_id"),
        Index("ix_wallet_current_balances_last_synced_at", "last_synced_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    balance_amount: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False, default=0)
    usd_value: Mapped[Decimal | None] = mapped_column(Numeric(38, 8), nullable=True)
    last_block_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    wallet = relationship("Wallet")
    token = relationship("TokenMaster")