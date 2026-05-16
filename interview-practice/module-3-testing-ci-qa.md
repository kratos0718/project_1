# Module 3: Testing & CI/CD Pipeline Q&A

This module explores the complexities of testing generative AI systems and ensuring continuous integration without breaking builds or incurring massive API costs.

## 1. How do you design a CI/CD pipeline for a repository containing both a Next.js frontend and a FastAPI backend?

**Answer:**
- We use a platform like GitHub Actions to orchestrate the pipeline.
- We separate the tests into distinct, parallel jobs (e.g., `backend-test` and `frontend-build`) to reduce the total pipeline runtime.
- For the backend, we setup a Python environment, cache `pip` dependencies, install test requirements (`pytest`), and execute the test suite against the backend directory.
- For the frontend, we setup Node.js, cache `npm`, run `npm run lint` for code quality, and trigger a `next build` to guarantee the production asset compilation succeeds.

## 2. Testing AI models in CI/CD is notoriously flaky. How did you resolve this?

**Answer:**
- By heavily utilizing Mocking for unit tests. 
- Calling real OpenAI APIs in a CI pipeline is slow, expensive, and non-deterministic (an LLM might format the exact same prompt differently on Tuesday than it did on Monday, breaking strict assertions).
- We use `pytest` fixtures to intercept calls to the LangChain wrappers. We return static, pre-defined JSON payloads that mimic the structure the LLM would output. This allows us to rapidly and deterministically test the **routing and business logic** of our multi-agent system.

## 3. What is the difference between Pytest fixtures and standard setup/teardown methods?

**Answer:**
- Standard `setUp` and `tearDown` methods (like those in `unittest`) run for every test in a class, which can lead to redundant execution and a rigid hierarchy.
- `pytest` fixtures use Dependency Injection. You simply declare the fixture name in the test function's arguments (e.g., `def test_api(async_client):`), and pytest automatically resolves and injects it.
- Fixtures also support highly granular scoping (function, class, module, session). For example, we can spin up an in-memory SQLite test database once for the entire session, rather than recreating it 500 times for 500 tests.

## 4. How do you test asynchronous code in Python?

**Answer:**
- Python's standard `unittest` framework was built for synchronous code. For async code, we use `pytest-asyncio`.
- We decorate test functions with `@pytest.mark.asyncio`, allowing us to use `await` inside the test body.
- When testing a FastAPI application that utilizes an async database, we replace the standard synchronous `TestClient` with `httpx.AsyncClient` paired with an `ASGITransport`. This ensures no `EventLoop is already running` errors occur by keeping everything within a single async context.
