from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base
from backend.models.enums import AuditActionType, SyncJobStatus
from backend.models.mixins import TimestampMixin


class SyncJobRun(TimestampMixin, Base):
    __tablename__ = "sync_job_runs"
    __table_args__ = (
        Index("ix_sync_job_runs_job_name", "job_name"),
        Index("ix_sync_job_runs_started_at", "started_at"),
        Index("ix_sync_job_runs_status", "status"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_name: Mapped[str] = mapped_column(String(128), nullable=False)
    job_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[SyncJobStatus] = mapped_column(SAEnum(SyncJobStatus, native_enum=False), nullable=False)
    records_processed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class EntityAuditLog(TimestampMixin, Base):
    __tablename__ = "entity_audit_logs"
    __table_args__ = (
        Index("ix_entity_audit_logs_entity_type_entity_id", "entity_type", "entity_id"),
        Index("ix_entity_audit_logs_action_type", "action_type"),
        Index("ix_entity_audit_logs_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action_type: Mapped[AuditActionType] = mapped_column(SAEnum(AuditActionType, native_enum=False), nullable=False)
    actor: Mapped[str | None] = mapped_column(String(128), nullable=True)
    before_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    after_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)