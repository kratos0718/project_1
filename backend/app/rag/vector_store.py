from dataclasses import dataclass
from typing import Any

import chromadb

from app.config.settings import Settings


@dataclass(frozen=True)
class RetrievalResult:
    complaint_id: str
    text: str
    score: float
    metadata: dict[str, Any]


class ChromaVectorStore:
    def __init__(self, settings: Settings) -> None:
        self.client = chromadb.PersistentClient(path="./chroma_data")
        self.collection = self.client.get_or_create_collection("civic_complaints")

    async def upsert(
        self,
        complaint_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: dict[str, Any],
    ) -> None:
        ids = [f"{complaint_id}:{index}" for index in range(len(chunks))]
        metadatas = [{**metadata, "complaint_id": complaint_id, "chunk_index": index} for index in range(len(chunks))]
        self.collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)

    async def query(
        self,
        embedding: list[float],
        limit: int = 8,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        response = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit,
            where=metadata_filter,
            include=["documents", "metadatas", "distances"],
        )
        results: list[RetrievalResult] = []
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]
        for document, metadata, distance in zip(documents, metadatas, distances, strict=False):
            results.append(
                RetrievalResult(
                    complaint_id=str(metadata.get("complaint_id")),
                    text=document,
                    score=max(0.0, 1.0 - float(distance)),
                    metadata=dict(metadata),
                )
            )
        return results

