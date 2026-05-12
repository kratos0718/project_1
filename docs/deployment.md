# Deployment Guide

## Frontend: Vercel

1. Set project root to `frontend`.
2. Add `NEXT_PUBLIC_API_BASE_URL`.
3. Add Clerk publishable key when auth is enabled.
4. Deploy with the default Next.js build command.

## Backend: Railway or Render

1. Set project root to `backend`.
2. Build from `backend/Dockerfile`.
3. Add `DATABASE_URL`, `OPENAI_API_KEY`, `CHROMA_HOST`, and `CHROMA_PORT`.
4. Provision PostgreSQL.
5. Provision ChromaDB or replace `ChromaVectorStore` with Pinecone for managed vector search.

## Production Notes

- Move long-running complaint analysis into a queue worker.
- Use Alembic migrations instead of startup `create_all`.
- Add auth middleware and tenant-aware metadata filtering.
- Enable structured logs and trace IDs across API, vector search, and agent workflow.

