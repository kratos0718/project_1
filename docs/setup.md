# Setup Guide

## Prerequisites

- Docker and Docker Compose
- Node.js 22+
- Python 3.12+
- OpenAI API key for production embeddings and LLM-backed agents

## Environment

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` for real embeddings. Without it, the backend uses a deterministic local embedding fallback so the architecture can be exercised offline.

## Docker

```bash
docker compose up --build
```

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

