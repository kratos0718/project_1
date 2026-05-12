# Architecture

## System Overview

The platform is a full-stack civic intelligence system. Complaints enter through the Next.js UI, are persisted in PostgreSQL, embedded into ChromaDB, retrieved semantically for grounding, analyzed by a LangGraph multi-agent workflow, and stored as memory/evaluation records for later sessions.

## Decision: FastAPI Backend

Why chosen: FastAPI provides async request handling, OpenAPI generation, dependency injection, and strong Python typing that fits AI service orchestration.

Alternatives rejected: Django was heavier for this API-first service. Flask required more manual typing, validation, and OpenAPI work.

Tradeoffs: FastAPI gives speed and clarity, but large teams must be disciplined about module boundaries because it is less opinionated than Django.

Scalability: Services can be moved behind queues for async processing, and API workers can scale horizontally behind a load balancer.

## Decision: Next.js 15 Frontend

Why chosen: Next.js supports server-rendered dashboards, client-side forms, deployment to Vercel, and strong TypeScript ergonomics.

Alternatives rejected: Vite SPA would be simpler but weaker for production routing and deployment conventions. Remix is excellent but less aligned with the requested stack.

Tradeoffs: Server components introduce mental overhead, but they reduce client bundle size for read-heavy analytics pages.

Scalability: Dashboard pages can move to cached server data while complaint intake remains interactive client code.

## Decision: ChromaDB Vector Store

Why chosen: ChromaDB is easy to run locally through Docker and supports metadata-filtered semantic search.

Alternatives rejected: Pinecone is more operationally mature for managed production but adds external account setup and cost.

Tradeoffs: ChromaDB is developer-friendly, while Pinecone would be preferred for high-volume managed vector search.

Scalability: The vector store is isolated behind `ChromaVectorStore`, so Pinecone can replace it without changing API or agent code.

## Decision: OpenAI `text-embedding-3-small`

Why chosen: It is cost-efficient, high quality for semantic retrieval, and available through the same provider as the LLM layer.

Alternatives rejected: `BAAI/bge-small-en-v1.5` is strong and self-hostable, but it adds model serving complexity.

Tradeoffs: OpenAI embeddings reduce infra burden but introduce external dependency and per-token cost.

Scalability: Embeddings can be cached and batch-generated. The `EmbeddingService` currently includes a deterministic fallback only for local development without an API key.

## Decision: LangGraph Multi-Agent Workflow

Why chosen: LangGraph models the civic workflow as an explicit state machine with inspectable agent transitions.

Alternatives rejected: Plain prompt chaining hides workflow state and is harder to test. A custom orchestrator would duplicate LangGraph concepts.

Tradeoffs: LangGraph adds a dependency, but provides durable structure for branching, retries, memory, and evaluation.

Scalability: Agents can become independent nodes with tool calls, queue boundaries, and persisted graph checkpoints.

## RAG Design

Chunk size is `900` characters with `120` character overlap. Civic complaints are usually short, but longer submissions may contain multiple location and urgency details. The overlap keeps cross-boundary context like street names and consequences available to retrieval.

Retrieval performs embedding search with optional locality/category metadata filters, then reranks by vector score and recency metadata. Reports include citations from retrieved complaints so generated summaries are grounded in stored records.

## Memory Design

Short-term memory is represented by each workflow state and reasoning trace. Long-term issue memory is persisted in PostgreSQL through `memory_records`. Locality history memory is queried by locality and ordered by importance and recency.

## Evaluation Design

The baseline evaluation pipeline logs retrieval precision, hallucination risk, response relevance, and latency. Current scoring is heuristic so the pipeline exists before LLM judges are introduced. Later phases should add labeled test sets and model-graded groundedness checks.

