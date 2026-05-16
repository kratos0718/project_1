# Module 2: Production Readiness & Observability Q&A

This module contains practice questions focused on scaling, deploying, and operating complex AI applications in a production environment.

## 1. How would you scale the backend to handle 10,000 requests per minute?

**Answer:**
- **Load Balancing:** Deploy multiple instances of the FastAPI backend behind a load balancer (like AWS ALB or NGINX).
- **Process Management:** Use Gunicorn with Uvicorn workers on each instance to maximize CPU core utilization.
- **Async DB Drivers:** Ensure all database calls (PostgreSQL and Vector DB) use asynchronous drivers (`asyncpg`) to prevent blocking the event loop.
- **Queueing:** For long-running LangGraph agents, move the computation off the synchronous API request into an asynchronous message queue (e.g., Celery, AWS SQS) and return a Job ID to the client for polling.
- **Caching:** Cache frequent identical embedding lookups or static configuration data using Redis.

## 2. Why use a Multi-Stage Docker build for Next.js?

**Answer:**
- **Reduced Image Size:** Next.js can produce a `standalone` folder containing only the precise Node.js runtime files necessary for the app, rather than the entire `node_modules` folder (which includes dev dependencies).
- **Security:** Excluding build tools and compilers from the final image drastically reduces the attack surface if a vulnerability is exploited.
- **Caching:** Segregating the `npm install` layer from the application code layer means the dependencies layer can be cached heavily by Docker, speeding up CI/CD pipelines.

## 3. How do you implement tracing in a multi-agent workflow where functions call each other deeply?

**Answer:**
- We implement **Correlation IDs**. 
- At the API boundary, a middleware generates a unique `X-Request-ID` (UUID) or reads one from the incoming HTTP headers.
- Instead of passing this ID as an argument through every LangGraph node (which pollutes the function signatures), we use Python's `contextvars` to store the ID.
- The global structured logger (using `python-json-logger`) intercepts every log message and injects the Correlation ID from the `contextvars` context.
- When shipped to a central log aggregator like Datadog or ELK, we can filter by the Correlation ID to see the exact sequence of events, agent decisions, and DB queries triggered by that specific user request.

## 4. Why use structured JSON logging instead of plain text logs?

**Answer:**
- Plain text logs require brittle regular expressions (Regex) to parse metadata (like timestamps, log levels, or request IDs) on the log aggregator side.
- JSON logging outputs a predefined schema. Log aggregators can natively index JSON keys (e.g., `level: "ERROR"`, `correlation_id: "123"`), making searches instantly fast, reliable, and enabling the creation of automated alerts and dashboards based on specific keys.
