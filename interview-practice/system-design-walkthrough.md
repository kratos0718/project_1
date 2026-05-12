# System Design Walkthrough

## One-Minute Pitch

This project is an AI civic governance intelligence platform. It ingests public complaints, cleans and embeds the text, stores vectors in ChromaDB, retrieves semantically similar complaints, runs a LangGraph multi-agent workflow, persists memory in PostgreSQL, and exposes analytics in a Next.js dashboard.

## Core Flow

1. User submits a complaint from the dashboard.
2. FastAPI validates and cleans the complaint.
3. PostgreSQL stores raw and cleaned complaint data.
4. The RAG layer retrieves similar historical complaints from ChromaDB.
5. LangGraph agents analyze severity, duplicates, summary, and escalation.
6. The platform stores the agent report, memory, and evaluation metrics.
7. The dashboard displays complaint feed, analytics, citations, and reasoning traces.

## Why This Architecture

FastAPI was chosen for async Python APIs and AI ecosystem compatibility. Next.js was chosen for a production dashboard and Vercel deployment. PostgreSQL handles durable transactional data. ChromaDB handles semantic similarity search. LangGraph makes the agent workflow explicit, inspectable, and extensible.

## Scalability Plan

- Move embedding and agent execution to background workers.
- Batch embeddings for throughput and cost control.
- Add Alembic migrations for schema evolution.
- Add tenant-aware auth filters before retrieval.
- Add observability across API latency, vector search, LLM calls, and agent state transitions.
- Replace ChromaDB with Pinecone if managed vector scale is required.

## Reliability Plan

- Store raw complaint data before AI processing.
- Retry embedding/vector writes.
- Record evaluation logs for every generated report.
- Use citations to make summaries auditable.
- Add human review queues for critical or high-risk escalations.

## Security Plan

- Add Clerk/Auth.js authentication.
- Verify JWTs in FastAPI.
- Scope complaints by tenant, department, and role.
- Avoid cross-tenant vector retrieval by enforcing metadata filters.
- Redact personally identifiable information before embedding where required.

