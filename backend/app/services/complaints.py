from time import perf_counter

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.workflow import ComplaintAgentWorkflow
from app.config.settings import Settings
from app.evaluation.metrics import EvaluationService
from app.memory.store import MemoryStore
from app.models.database import AgentReportRecord, ComplaintRecord
from app.models.schemas import AnalyticsResponse, ComplaintCreate, ComplaintResponse
from app.rag.chunking import ComplaintChunker
from app.rag.embeddings import EmbeddingService
from app.rag.retriever import ComplaintRetriever
from app.rag.vector_store import ChromaVectorStore
from app.utils.text import clean_complaint_text


class ComplaintService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.chunker = ComplaintChunker(settings.chunk_size, settings.chunk_overlap)
        self._embeddings: EmbeddingService | None = None
        self._vector_store: ChromaVectorStore | None = None
        self._retriever: ComplaintRetriever | None = None
        self.workflow = ComplaintAgentWorkflow()
        self.memory = MemoryStore(session)
        self.evaluator = EvaluationService(session)

    @property
    def embeddings(self) -> EmbeddingService:
        if self._embeddings is None:
            self._embeddings = EmbeddingService(self.settings)
        return self._embeddings

    @property
    def vector_store(self) -> ChromaVectorStore:
        if self._vector_store is None:
            self._vector_store = ChromaVectorStore(self.settings)
        return self._vector_store

    @property
    def retriever(self) -> ComplaintRetriever:
        if self._retriever is None:
            self._retriever = ComplaintRetriever(self.embeddings, self.vector_store)
        return self._retriever

    async def submit(self, payload: ComplaintCreate) -> ComplaintResponse:
        started = perf_counter()
        cleaned = clean_complaint_text(payload.text)
        complaint = ComplaintRecord(
            raw_text=payload.text,
            cleaned_text=cleaned,
            locality=payload.locality,
            category=payload.category,
            extra_metadata=payload.metadata,
        )
        self.session.add(complaint)
        await self.session.flush()

        citations = await self.retriever.retrieve(cleaned, locality=payload.locality, category=payload.category)
        report = await self.workflow.run(
            {
                "complaint_id": complaint.id,
                "text": cleaned,
                "locality": payload.locality,
                "category": payload.category,
                "citations": citations,
            }
        )

        complaint.severity_score = report.severity_score
        complaint.escalation_priority = report.escalation_priority
        self.session.add(
            AgentReportRecord(
                complaint_id=complaint.id,
                summary=report.summary,
                urgency=report.urgency,
                duplicate_ids=report.duplicate_ids,
                citations=[citation.model_dump() for citation in report.citations],
                reasoning_trace=report.reasoning_trace,
            )
        )

        chunks = self.chunker.split(cleaned)
        vectors = await self.embeddings.embed_documents([chunk.text for chunk in chunks])
        await self.vector_store.upsert(
            complaint_id=complaint.id,
            chunks=[chunk.text for chunk in chunks],
            embeddings=vectors,
            metadata={"locality": payload.locality, "category": payload.category, "created_at": complaint.created_at.isoformat()},
        )
        await self.memory.remember("issue", report.summary, locality=payload.locality, source_complaint_id=complaint.id, importance=max(1, int(report.severity_score * 5)))
        await self.evaluator.log_submission(
            complaint_id=complaint.id,
            citations=citations,
            report_summary=report.summary,
            latency_ms=int((perf_counter() - started) * 1000),
        )
        await self.session.commit()
        return ComplaintResponse(
            id=complaint.id,
            raw_text=complaint.raw_text,
            cleaned_text=complaint.cleaned_text,
            locality=complaint.locality,
            category=complaint.category,
            status=complaint.status,
            severity_score=complaint.severity_score,
            escalation_priority=complaint.escalation_priority,
            created_at=complaint.created_at,
            report=report,
        )

    async def list_recent(self, limit: int = 25) -> list[ComplaintResponse]:
        result = await self.session.execute(select(ComplaintRecord).order_by(ComplaintRecord.created_at.desc()).limit(limit))
        return [
            ComplaintResponse(
                id=item.id,
                raw_text=item.raw_text,
                cleaned_text=item.cleaned_text,
                locality=item.locality,
                category=item.category,
                status=item.status,
                severity_score=item.severity_score,
                escalation_priority=item.escalation_priority,
                created_at=item.created_at,
            )
            for item in result.scalars().all()
        ]

    async def analytics(self) -> AnalyticsResponse:
        total = await self.session.scalar(select(func.count(ComplaintRecord.id))) or 0
        open_count = await self.session.scalar(select(func.count(ComplaintRecord.id)).where(ComplaintRecord.status == "open")) or 0
        rows = await self.session.execute(select(ComplaintRecord.locality, func.count(ComplaintRecord.id)).group_by(ComplaintRecord.locality))
        locality_counts = {locality: count for locality, count in rows.all()}
        severity_rows = await self.session.execute(select(ComplaintRecord.escalation_priority, func.count(ComplaintRecord.id)).group_by(ComplaintRecord.escalation_priority))
        severity_distribution = {priority or "unscored": count for priority, count in severity_rows.all()}
        return AnalyticsResponse(
            total_complaints=total,
            open_complaints=open_count,
            severity_distribution=severity_distribution,
            locality_counts=locality_counts,
            trend_points=[],
        )
