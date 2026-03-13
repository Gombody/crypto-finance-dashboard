from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.enums import CategoryType, ChainType, ExchangeType, WalletType
from backend.models.mixins import TimestampMixin

from decimal import Decimal

class TokenMaster(TimestampMixin, Base):
    __tablename__ = "token_master"
    __table_args__ = (
        UniqueConstraint("chain_type", "contract_address", name="uq_token_master_chain_contract"),
        UniqueConstraint("chain_type", "token_symbol", "is_native", name="uq_token_master_chain_symbol_native"),
        CheckConstraint("decimals >= 0 AND decimals <= 36", name="ck_token_master_decimals"),
        Index("ix_token_master_symbol", "token_symbol"),
        Index("ix_token_master_chain_type", "chain_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token_symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    token_name: Mapped[str] = mapped_column(String(128), nullable=False)
    chain_type: Mapped[ChainType] = mapped_column(SAEnum(ChainType, native_enum=False), nullable=False)
    contract_address: Mapped[str | None] = mapped_column(String(128), nullable=True)
    decimals: Mapped[int] = mapped_column(Integer, nullable=False, default=18)
    is_native: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    cmc_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    coingecko_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class ExchangeAccount(TimestampMixin, Base):
    __tablename__ = "exchange_accounts"
    __table_args__ = (
        UniqueConstraint("exchange_type", "account_name", name="uq_exchange_accounts_exchange_name"),
        Index("ix_exchange_accounts_exchange_type", "exchange_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_type: Mapped[ExchangeType] = mapped_column(SAEnum(ExchangeType, native_enum=False), nullable=False)
    account_name: Mapped[str] = mapped_column(String(128), nullable=False)
    account_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    api_key_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class Wallet(TimestampMixin, Base):
    __tablename__ = "wallets"
    __table_args__ = (
        UniqueConstraint("chain_type", "address", name="uq_wallets_chain_address"),
        Index("ix_wallets_wallet_name", "wallet_name"),
        Index("ix_wallets_chain_type", "chain_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_name: Mapped[str] = mapped_column(String(128), nullable=False)
    chain_type: Mapped[ChainType] = mapped_column(SAEnum(ChainType, native_enum=False), nullable=False)
    wallet_type: Mapped[WalletType] = mapped_column(SAEnum(WalletType, native_enum=False), nullable=False)
    address: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    custodian_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class WalletTokenConfig(TimestampMixin, Base):
    __tablename__ = "wallet_token_configs"
    __table_args__ = (
        UniqueConstraint("wallet_id", "token_id", name="uq_wallet_token_configs_wallet_token"),
        Index("ix_wallet_token_configs_wallet_id", "wallet_id"),
        Index("ix_wallet_token_configs_token_id", "token_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("token_master.id", ondelete="RESTRICT"), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    min_alert_threshold: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    max_alert_threshold: Mapped[Decimal | None] = mapped_column(Numeric(38, 18), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    wallet = relationship("Wallet")
    token = relationship("TokenMaster")


class CategoryMaster(TimestampMixin, Base):
    __tablename__ = "category_master"
    __table_args__ = (
        UniqueConstraint("category_code", name="uq_category_master_code"),
        Index("ix_category_master_category_type", "category_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_code: Mapped[str] = mapped_column(String(64), nullable=False)
    category_name: Mapped[str] = mapped_column(String(128), nullable=False)
    category_type: Mapped[CategoryType] = mapped_column(SAEnum(CategoryType, native_enum=False), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class ProjectMaster(TimestampMixin, Base):
    __tablename__ = "project_master"
    __table_args__ = (
        UniqueConstraint("project_code", name="uq_project_master_code"),
        Index("ix_project_master_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_code: Mapped[str] = mapped_column(String(64), nullable=False)
    project_name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class KRWCategoryMaster(TimestampMixin, Base):
    __tablename__ = "krw_category_master"
    __table_args__ = (
        UniqueConstraint("category_code", name="uq_krw_category_master_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_code: Mapped[str] = mapped_column(String(64), nullable=False)
    category_name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_income: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)