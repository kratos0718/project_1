# Day 5

## Features Built

- **Production-Ready Docker Images:** Replaced the development startup commands with production WSGI/ASGI configurations.
  - Backend: Uses `gunicorn` with `uvicorn` worker classes for resilient process management.
  - Frontend: Re-written Dockerfile utilizing a multi-stage Next.js `standalone` build for extremely optimized and secure container sizes.
- **Observability:** Centralized standard JSON logging in the backend.
- **Traceability:** Added a `CorrelationIdMiddleware` that assigns an `X-Request-ID` to all inbound requests, appending it automatically to all logs via context variables, allowing trace stitching across API calls and LangGraph agent loops.

## Concepts Learned

- **Multi-Stage Docker Builds:** How to segregate dependency installation, building, and runner stages to reduce attack surface and image size (e.g. from >1GB to ~100MB).
- **WSGI vs ASGI Process Management:** Why Gunicorn is still beneficial as a process manager for Uvicorn in production, as it manages worker restarts and buffering.
- **Context Variables:** How `contextvars` in Python provides thread-safe and async-safe global state, perfect for passing Correlation IDs deep into synchronous and asynchronous service layers without polluting function signatures.

## Problems Faced

- Deploying Next.js naively results in massive images containing all `node_modules`. 
- Tracking the flow of a single user's request across complex LangGraph workflows is impossible without a trace ID.

## Solutions Implemented

- Set `output: "standalone"` in `next.config.ts` to enable Next.js to trace specific dependencies.
- Integrated `python-json-logger` for structured ELK/Datadog friendly logs.

## Interview Questions (Deployment & Ops Focus)

1. Why use Gunicorn to run an async Uvicorn application?
2. What are the benefits of a multi-stage Docker build?
3. How do you trace a request across a multi-agent AI pipeline?

## Best Answers

1. Uvicorn is excellent at handling asynchronous connections (ASGI) but lacks robust process management. Gunicorn handles starting, monitoring, and restarting Uvicorn worker processes to maximize CPU utilization and resilience.
2. It dramatically reduces the final image size by discarding build tools and intermediate dependencies, which also improves security by minimizing the attack surface.
3. Inject a unique Correlation ID (e.g., UUID) at the API gateway or middleware level. Use thread-safe context variables (like Python's `contextvars`) to implicitly pass this ID to the logging formatter so every log emitted by any agent or sub-routine is stamped with the same ID.
