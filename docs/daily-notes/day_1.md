# Day 1

## Features Built

- Monorepo scaffold with FastAPI backend and Next.js frontend.
- Complaint intake API.
- RAG chunking, embedding, ChromaDB vector storage, and semantic retrieval interfaces.
- LangGraph workflow with planner, severity, duplicate detection, summarization, and escalation nodes.
- PostgreSQL persistence models for complaints, reports, memory, and evaluation logs.
- Dashboard, complaint intake page, analytics page, loading states, and error boundary.

## Concepts Learned

- How RAG combines embeddings, vector search, metadata filtering, reranking, and citations.
- Why multi-agent workflows benefit from explicit graph state.
- How persistent memory differs from a chat transcript.

## Problems Faced

- The empty workspace required creating architecture, code, and docs from scratch.
- Full production AI integrations need external services and credentials.

## Solutions Implemented

- Added Docker Compose for PostgreSQL, ChromaDB, backend, and frontend.
- Added deterministic embedding fallback for offline development while preserving real OpenAI embedding support.
- Added documentation for production hardening steps.

## Tradeoffs

- Startup table creation is useful for MVP speed but should become Alembic migrations.
- Heuristic evaluation establishes the data pipeline but should be replaced by labeled datasets and judge models.

## Interview Questions

1. Why use a vector database instead of SQL full-text search?
2. How do chunk size and overlap affect retrieval?
3. Why use LangGraph instead of prompt chaining?
4. How would you detect hallucinations in generated civic reports?
5. How would you scale this platform to millions of complaints?

## Best Answers

1. Vector search captures semantic similarity, while full-text search mainly captures lexical overlap.
2. Larger chunks preserve context but reduce retrieval precision; overlap prevents important details from being split apart.
3. LangGraph makes workflow state explicit, testable, inspectable, and easier to extend with retries or branching.
4. Require citations, compare claims against retrieved context, and log groundedness scores with human review on high-risk cases.
5. Use queues, batched embeddings, vector sharding, read replicas, caching, and tenant-aware metadata indexes.

