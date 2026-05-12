from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ComplaintRecord(Base):
    __tablename__ = "complaints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    raw_text: Mapped[str] = mapped_column(Text)
    cleaned_text: Mapped[str] = mapped_column(Text)
    locality: Mapped[str] = mapped_column(String(160), index=True)
    category: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(40), default="open", index=True)
    severity_score: Mapped[float | None] = mapped_column(Float)
    escalation_priority: Mapped[str | None] = mapped_column(String(40))
    extra_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    reports: Mapped[list["AgentReportRecord"]] = relationship(back_populates="complaint")


class AgentReportRecord(Base):
    __tablename__ = "agent_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    complaint_id: Mapped[str] = mapped_column(ForeignKey("complaints.id"))
    summary: Mapped[str] = mapped_column(Text)
    urgency: Mapped[str] = mapped_column(String(40))
    duplicate_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    citations: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    reasoning_trace: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    complaint: Mapped[ComplaintRecord] = relationship(back_populates="reports")


class MemoryRecord(Base):
    __tablename__ = "memory_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    memory_type: Mapped[str] = mapped_column(String(60), index=True)
    locality: Mapped[str | None] = mapped_column(String(160), index=True)
    content: Mapped[str] = mapped_column(Text)
    importance: Mapped[int] = mapped_column(Integer, default=1)
    source_complaint_id: Mapped[str | None] = mapped_column(String(36), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class EvaluationLogRecord(Base):
    __tablename__ = "evaluation_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    complaint_id: Mapped[str | None] = mapped_column(String(36), index=True)
    retrieval_precision: Mapped[float | None] = mapped_column(Float)
    hallucination_risk: Mapped[float | None] = mapped_column(Float)
    response_relevance: Mapped[float | None] = mapped_column(Float)
    latency_ms: Mapped[int] = mapped_column(Integer)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

