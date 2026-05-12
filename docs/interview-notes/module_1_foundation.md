# Module 1 Interview Preparation

1. What is the core architecture of this platform?
   Answer: A Next.js dashboard sends complaints to FastAPI, which stores structured records in PostgreSQL, embeds text into ChromaDB, retrieves similar records, runs a LangGraph workflow, and persists reports, memory, and evaluation logs.

2. Why is this not a chatbot?
   Answer: The system has structured ingestion, retrieval, persisted memory, multi-agent workflow state, citations, analytics, and evaluation logs. Chat is not the primary abstraction.

3. Why choose FastAPI?
   Answer: Async support, type-driven validation, dependency injection, automatic OpenAPI, and strong fit with Python AI tooling.

4. Why choose Next.js?
   Answer: It supports production routing, server-rendered analytics pages, client-side intake, and Vercel deployment.

5. Why use PostgreSQL and a vector DB?
   Answer: PostgreSQL stores durable transactional records. The vector DB indexes high-dimensional embeddings for semantic similarity.

6. What is RAG?
   Answer: Retrieval-Augmented Generation retrieves relevant external context before generation so outputs can be grounded in known data.

7. How do embeddings work here?
   Answer: Complaint text is converted into dense vectors where semantically similar complaints are closer in vector space.

8. Why `text-embedding-3-small`?
   Answer: It balances cost, quality, latency, and integration simplicity.

9. What is metadata filtering?
   Answer: Retrieval can restrict candidates by fields like locality or category before ranking semantic similarity.

10. What is reranking?
    Answer: It reorders retrieved candidates using additional signals such as similarity score, recency, metadata match, or a cross-encoder.

11. Why use chunk overlap?
    Answer: Overlap keeps details near chunk boundaries available during retrieval.

12. How is duplicate detection implemented?
    Answer: The workflow marks high-scoring retrieved complaints as likely duplicates.

13. How would you improve duplicate detection?
    Answer: Add thresholds tuned on labeled pairs, locality constraints, temporal windows, and a cross-encoder verifier.

14. What is persistent memory?
    Answer: Memory records are stored between sessions and retrieved later to contextualize recurring locality issues.

15. What is short-term memory?
    Answer: The current workflow state and reasoning trace during one complaint processing run.

16. Why use LangGraph?
    Answer: It turns agents into explicit workflow nodes with typed state and inspectable transitions.

17. What are the agent responsibilities?
    Answer: Planner routes work, severity scores risk, duplicate agent checks similarity, summarizer writes grounded output, escalation agent selects authority.

18. How do citations reduce hallucination?
    Answer: They force summaries to reference retrieved records and make unsupported claims easier to detect.

19. What metrics are logged?
    Answer: Retrieval precision, hallucination risk, response relevance, and latency.

20. How would you evaluate retrieval precision?
    Answer: Use labeled relevant complaint sets and compute precision@k, recall@k, and MRR.

21. How would you scale ingestion?
    Answer: Move embedding and agent execution to workers, batch embeddings, and make API submission return accepted jobs.

22. How would auth be added?
    Answer: Clerk/Auth.js on the frontend and verified JWT claims on FastAPI routes with role-based access control.

23. What are production risks?
    Answer: LLM cost, latency spikes, vector drift, hallucinations, privacy, and accidental cross-tenant retrieval.

24. How would you debug a bad summary?
    Answer: Inspect retrieved citations, agent trace, prompt/context, model output, and evaluation logs.

25. What would you build next?
    Answer: Alembic migrations, real LLM summarization with guarded prompts, background jobs, auth, and labeled evaluation datasets.

