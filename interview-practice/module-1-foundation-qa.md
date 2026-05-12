# Module 1 Foundation Q&A

## 1. What did you build first?

I built the foundation: FastAPI backend, Next.js frontend, PostgreSQL models, ChromaDB integration path, LangGraph workflow, Docker Compose, and documentation.

## 2. Why start with architecture instead of model prompts?

AI systems fail when orchestration, persistence, evaluation, and observability are afterthoughts. Starting with architecture makes the platform extensible.

## 3. What makes this portfolio-grade?

It demonstrates real system boundaries: API layer, service layer, RAG layer, vector store, agent graph, memory store, evaluation logs, deployment docs, and interview-ready architecture decisions.

## 4. What would you improve next?

I would add Alembic migrations, real LLM-based summarization, background jobs, authentication enforcement, labeled evaluation data, and richer analytics.

## 5. How do you explain the tradeoff of local embedding fallback?

The fallback allows offline development and testing of control flow. Production should use real embedding models for semantic quality.

## 6. Why persist memory in PostgreSQL?

PostgreSQL provides durable, queryable, auditable records. It is appropriate for long-term issue memory and locality patterns.

## 7. How would this evolve into production?

The synchronous complaint submission path would become an asynchronous job pipeline. The API would store the complaint quickly, workers would process embeddings and agents, and the UI would show job status.

