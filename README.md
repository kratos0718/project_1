# AI Civic Governance Intelligence Platform

Enterprise-grade multi-agent AI platform for retrieving, clustering, prioritizing, and summarizing civic complaints with RAG, vector search, persistent memory, and workflow orchestration.

## What Is Included

- FastAPI backend with clean service boundaries for complaints, RAG, agents, memory, and evaluation.
- Next.js 15 frontend shell with dashboard, complaint intake, analytics, retrieval visualization, and reasoning traces.
- ChromaDB vector database integration path using real embeddings.
- PostgreSQL persistence model for complaints, agent reports, memory records, and evaluation logs.
- LangGraph orchestration design for planner, severity, duplicate, summarization, and escalation agents.
- Docker Compose for local full-stack execution.
- Architecture, setup, deployment, API, diagrams, daily notes, and interview preparation docs.

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Frontend: `http://localhost:3000`

Backend API: `http://localhost:8000/docs`

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Architecture Decisions

See [docs/architecture.md](docs/architecture.md) for decisions, alternatives, tradeoffs, and scalability notes.

## Interview Practice

Readable interview prep is separated under [interview-practice](interview-practice) for quick GitHub access. It includes a system design walkthrough, RAG/agents/memory cheatsheet, FAANG-style questions, and module-specific Q&A.

## Project Phases

1. Architecture, backend, frontend skeleton.
2. Embeddings, vector DB, RAG.
3. LangGraph agents and persistent memory.
4. Evaluation, optimization, analytics.
5. Deployment, documentation, interview preparation.
