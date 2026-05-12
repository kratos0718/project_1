from typing import Any, TypedDict

from app.models.schemas import Citation


class ComplaintWorkflowState(TypedDict, total=False):
    complaint_id: str
    text: str
    locality: str
    category: str
    citations: list[Citation]
    severity_score: float
    urgency: str
    duplicate_ids: list[str]
    summary: str
    escalation_priority: str
    reasoning_trace: list[dict[str, Any]]

