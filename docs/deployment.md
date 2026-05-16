# Deployment Guide

## Production Architecture

This platform consists of three main components:
1. **Frontend:** Next.js application, served as a multi-stage standalone Node.js image or deployed to Vercel.
2. **Backend:** FastAPI application, managed by Gunicorn with Uvicorn async workers.
3. **Database Layer:** PostgreSQL for persistent storage and ChromaDB (or Pinecone) for vector embeddings.

## Deploying to Production (Docker-based)

The `docker-compose.yml` supports end-to-end production testing, but for actual deployment, use container orchestrators (e.g. AWS ECS, Kubernetes).

1. Set up your environments with `.env`:
   - `DATABASE_URL` (PostgreSQL connection string)
   - `OPENAI_API_KEY` (Your API key for embeddings/LLMs)
   - `CHROMA_HOST` and `CHROMA_PORT`
   - `NEXT_PUBLIC_API_BASE_URL` (For frontend API calls)
2. Build the optimized images:
   - Backend: Uses Gunicorn with 4 workers. Ensure memory allocation is sufficient.
   - Frontend: Uses a multi-stage build emitting a Next.js `standalone` process for extremely small container footprints.
3. Apply database migrations:
   - Before starting the backend, run Alembic: `alembic upgrade head`

## Observability & Logging

- **Structured JSON Logging:** The backend outputs standard JSON logs using `python-json-logger`.
- **Correlation IDs:** Every request receives an `X-Request-ID` attached to the log records, allowing easy tracking across the API and the LangGraph agent workflows. Configure your log aggregator (e.g. Datadog, ELK) to index `correlation_id`.

## Managed Services Alternatives

- **Frontend:** Vercel (Add `NEXT_PUBLIC_API_BASE_URL` and Clerk keys).
- **Backend:** Railway or Render (Connect PostgreSQL plugin).
- **Vector DB:** Pinecone (Replaces ChromaDB local container).
