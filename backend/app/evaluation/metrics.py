from app.models.database import EvaluationLogRecord
from app.models.schemas import Citation, EvaluationResponse


class EvaluationService:
    def __init__(self, session) -> None:
        self.session = session

    async def log_submission(
        self,
        complaint_id: str,
        citations: list[Citation],
        report_summary: str,
        latency_ms: int,
    ) -> EvaluationResponse:
        precision = sum(1 for citation in citations if citation.score >= 0.7) / max(1, len(citations))
        hallucination_risk = 0.15 if citations else 0.45
        relevance = min(1.0, 0.45 + precision * 0.4 + min(len(report_summary), 500) / 2500)
        response = EvaluationResponse(
            retrieval_precision=round(precision, 3),
            hallucination_risk=round(hallucination_risk, 3),
            response_relevance=round(relevance, 3),
            latency_ms=latency_ms,
            details={"citation_count": len(citations), "method": "heuristic_baseline"},
        )
        self.session.add(EvaluationLogRecord(complaint_id=complaint_id, **response.model_dump()))
        return response

