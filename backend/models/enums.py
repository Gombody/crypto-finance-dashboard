from enum import Enum


class ChainType(str, Enum):
    ETH = "ETH"
    BNB = "BNB"
    POLYGON = "POLYGON"
    ARBITRUM = "ARBITRUM"
    OPTIMISM = "OPTIMISM"
    SOLANA = "SOLANA"
    TRON = "TRON"
    OTHER = "OTHER"


class ExchangeType(str, Enum):
    BINANCE = "BINANCE"
    BYBIT = "BYBIT"
    BITGET = "BITGET"
    GATE = "GATE"
    MEXC = "MEXC"
    KUCOIN = "KUCOIN"
    OKX = "OKX"
    UPBIT = "UPBIT"
    BITHUMB = "BITHUMB"
    COINONE = "COINONE"
    OTHER = "OTHER"


class WalletType(str, Enum):
    EOA = "EOA"
    SAFE = "SAFE"
    CUSTODY = "CUSTODY"
    EXCHANGE_DEPOSIT = "EXCHANGE_DEPOSIT"
    OTHER = "OTHER"


class BalanceOwnerType(str, Enum):
    EXCHANGE = "EXCHANGE"
    WALLET = "WALLET"


class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"


class PriceSourceType(str, Enum):
    CMC = "CMC"
    COINGECKO = "COINGECKO"
    EXCHANGE = "EXCHANGE"
    MANUAL = "MANUAL"


class TxDirection(str, Enum):
    IN = "IN"
    OUT = "OUT"
    SELF = "SELF"


class TxStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"


class LedgerDirection(str, Enum):
    IN = "IN"
    OUT = "OUT"


class LedgerStatus(str, Enum):
    POSTED = "POSTED"
    VOIDED = "VOIDED"
    REPLACED = "REPLACED"


class PositionSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class PositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    LIQUIDATED = "LIQUIDATED"


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"


class SyncJobStatus(str, Enum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class AuditActionType(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    VOID = "VOID"
    REPLACE = "REPLACE"