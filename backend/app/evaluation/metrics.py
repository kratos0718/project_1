from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.database import EvaluationLogRecord
from app.models.schemas import Citation, EvaluationResponse
from app.config.settings import get_settings

class EvaluationScores(BaseModel):
    hallucination_risk: float = Field(description="Score from 0.0 to 1.0 indicating likelihood of hallucination (1.0 = high risk, 0.0 = completely grounded in citations)")
    response_relevance: float = Field(description="Score from 0.0 to 1.0 indicating how relevant the summary is to the citations and core complaint")
    reasoning: str = Field(description="Brief reasoning for the assigned scores")


class EvaluationService:
    def __init__(self, session) -> None:
        self.session = session
        settings = get_settings()
        if settings.openai_api_key:
            self.llm = ChatOpenAI(model=settings.llm_model, api_key=settings.openai_api_key, temperature=0.0)
        else:
            self.llm = None

    async def log_submission(
        self,
        complaint_id: str,
        citations: list[Citation],
        report_summary: str,
        latency_ms: int,
    ) -> EvaluationResponse:
        precision = sum(1 for citation in citations if citation.score >= 0.7) / max(1, len(citations))
        
        if self.llm:
            cited_text = "\n".join(f"- {c.excerpt}" for c in citations) or "No citations."
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert evaluator. Grade the provided summary based on its hallucination risk and response relevance to the provided citations. Hallucination risk should be 1.0 if the summary invents details not in the citations, and 0.0 if perfectly grounded."),
                ("human", "Summary:\n{summary}\n\nCitations:\n{citations}")
            ])
            chain = prompt | self.llm.with_structured_output(EvaluationScores)
            try:
                result = await chain.ainvoke({"summary": report_summary, "citations": cited_text})
                hallucination_risk = result.hallucination_risk
                relevance = result.response_relevance
                method = "llm_judge"
            except Exception:
                hallucination_risk = 0.15 if citations else 0.45
                relevance = min(1.0, 0.45 + precision * 0.4 + min(len(report_summary), 500) / 2500)
                method = "heuristic_fallback"
        else:
            hallucination_risk = 0.15 if citations else 0.45
            relevance = min(1.0, 0.45 + precision * 0.4 + min(len(report_summary), 500) / 2500)
            method = "heuristic_baseline"

        response = EvaluationResponse(
            retrieval_precision=round(precision, 3),
            hallucination_risk=round(hallucination_risk, 3),
            response_relevance=round(relevance, 3),
            latency_ms=latency_ms,
            details={"citation_count": len(citations), "method": method},
        )
        self.session.add(EvaluationLogRecord(complaint_id=complaint_id, **response.model_dump()))
        return response

