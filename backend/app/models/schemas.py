from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ComplaintCreate(BaseModel):
    text: str = Field(min_length=20, max_length=8000)
    locality: str = Field(min_length=2, max_length=160)
    category: str = Field(min_length=2, max_length=120)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Citation(BaseModel):
    complaint_id: str
    locality: str
    category: str
    score: float
    excerpt: str


class AgentReport(BaseModel):
    summary: str
    urgency: str
    severity_score: float
    escalation_priority: str
    duplicate_ids: list[str]
    citations: list[Citation]
    reasoning_trace: list[dict[str, Any]]


class ComplaintResponse(BaseModel):
    id: str
    raw_text: str
    cleaned_text: str
    locality: str
    category: str
    status: str
    severity_score: float | None
    escalation_priority: str | None
    created_at: datetime
    report: AgentReport | None = None


class ComplaintListResponse(BaseModel):
    complaints: list[ComplaintResponse]


class AnalyticsResponse(BaseModel):
    total_complaints: int
    open_complaints: int
    severity_distribution: dict[str, int]
    locality_counts: dict[str, int]
    trend_points: list[dict[str, Any]]


class EvaluationResponse(BaseModel):
    retrieval_precision: float
    hallucination_risk: float
    response_relevance: float
    latency_ms: int
    details: dict[str, Any]

