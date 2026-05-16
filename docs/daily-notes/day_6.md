# Day 6

## Features Built

- **Continuous Integration:** Implemented a GitHub Actions workflow (`ci.yml`) to automatically test the backend and verify the frontend build on every push and pull request to the `main` branch.
- **Automated Testing Suite:** Created a robust `pytest` suite for the FastAPI backend, utilizing `pytest-asyncio` and `httpx.AsyncClient` to test asynchronous API endpoints.
- **Agent Logic Testing:** Implemented unit tests for the deterministic routing and escalation logic of the LangGraph agents.
- **Mocking Strategy:** Leveraged `pytest` fixtures in `conftest.py` to mock OpenAI embedding models and LLM generations, allowing the test suite to run quickly and cost-effectively without requiring live API keys.

## Concepts Learned

- **Asynchronous Testing:** Testing FastAPI requires an async HTTP client (`httpx.ASGITransport`) because standard HTTP clients cannot resolve the event loop correctly in tests.
- **Mocking Non-Deterministic AI:** True end-to-end tests for generative AI are brittle. The best practice is to mock the LLM output for logic unit tests, and rely on the LLM-as-a-judge evaluators (built in Phase 4) for qualitative assessments on production data.
- **CI/CD Pipelines:** How to define discrete jobs in GitHub Actions to test full-stack repositories efficiently.

## Problems Faced

- The agent workflow requires API keys for OpenAI and a connection to a vector database (ChromaDB) which are not available or are expensive to run in a CI environment.

## Solutions Implemented

- Used Python classes to mock the `embed_documents` and `embed_query` interfaces expected by LangChain.
- Replaced actual LLM inference calls with deterministic mock responses within the test runner context.

## Interview Questions (Testing & CI Focus)

1. How do you test a system that relies on a non-deterministic LLM?
2. What is the difference between testing the API and testing the LangGraph workflow?
3. Why did we use an `AsyncClient` for our pytest setup instead of the standard `TestClient` from FastAPI?

## Best Answers

1. You should separate logic tests from quality tests. For unit testing business logic (e.g., routing based on severity), mock the LLM's structured JSON output to ensure the system behaves correctly under specific edge cases. For quality testing (hallucinations, relevance), use an offline Evaluation pipeline (LLM-as-a-judge) over a dataset of hundreds of queries.
2. API tests verify HTTP status codes, payload validation (Pydantic), and middleware integration. LangGraph workflow tests verify the transition logic between nodes (e.g., does node A go to node B if variable X is True?) independently of the web framework.
3. FastAPI's standard `TestClient` is synchronous (using `requests`). For complex applications utilizing asynchronous databases (`asyncpg`) and async external calls, a synchronous client can cause event loop conflicts. Using `httpx.AsyncClient` ensures the entire test executes within a single, cleanly managed asyncio event loop.
