from typing import Any
from app.models.schemas import Citation
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import ChromaVectorStore
from app.utils.text import excerpt


class ComplaintRetriever:
    def __init__(self, embeddings: EmbeddingService, vector_store: ChromaVectorStore) -> None:
        self.embeddings = embeddings
        self.vector_store = vector_store

    async def retrieve(
        self,
        query: str,
        locality: str | None = None,
        category: str | None = None,
        limit: int = 8,
    ) -> list[Citation]:
        vector = await self.embeddings.embed_query(query)
        filters = self._metadata_filter(locality, category)
        results = await self.vector_store.query(vector, limit=limit, metadata_filter=filters)
        reranked = sorted(results, key=lambda item: (item.score, item.metadata.get("created_at", "")), reverse=True)
        return [
            Citation(
                complaint_id=result.complaint_id,
                locality=str(result.metadata.get("locality", "")),
                category=str(result.metadata.get("category", "")),
                score=result.score,
                excerpt=excerpt(result.text),
            )
            for result in reranked
        ]

    def _metadata_filter(self, locality: str | None, category: str | None) -> dict[str, Any] | None:
        filters = [{key: value} for key, value in {"locality": locality, "category": category}.items() if value]
        if not filters:
            return None
        if len(filters) == 1:
            return filters[0]
        return {"$and": filters}

