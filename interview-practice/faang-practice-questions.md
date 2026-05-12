# FAANG-Style Practice Questions

1. Design a system to process one million civic complaints per day.
   Strong answer: Use API ingestion, durable queue, worker pool, batched embeddings, vector sharding, PostgreSQL partitioning, and cached analytics.

2. How would you prevent hallucinations?
   Strong answer: Require citations, constrain generation to retrieved context, run groundedness checks, log hallucination risk, and route high-risk reports to human review.

3. Why use LangGraph?
   Strong answer: It gives explicit state, inspectable transitions, modular nodes, retries, branching, and a cleaner path to durable workflows than prompt chaining.

4. How would you tune retrieval quality?
   Strong answer: Build a labeled dataset, measure precision@k and recall@k, tune chunking, metadata filters, embedding model, reranking, and similarity thresholds.

5. How would you detect duplicate complaints?
   Strong answer: Combine vector similarity, locality/category filters, temporal windows, and a verification model or cross-encoder.

6. What happens if ChromaDB is unavailable?
   Strong answer: Store the complaint in PostgreSQL, mark vector indexing as pending, retry asynchronously, and degrade agent output with lower confidence.

7. How would you reduce latency?
   Strong answer: Parallelize retrieval and memory lookup, batch embeddings, cache frequent queries, move heavy analysis to workers, and stream status updates.

8. How would you handle multi-tenancy?
   Strong answer: Add tenant IDs to SQL rows and vector metadata, verify auth claims, enforce filters server-side, and isolate sensitive indexes if required.

9. What database indexes matter?
   Strong answer: Index locality, category, status, created time, source complaint IDs, and tenant IDs. For analytics, consider materialized views.

10. How would you evaluate summaries?
    Strong answer: Use human labels, citation coverage, groundedness checks, relevance scoring, and regression tests across known complaint scenarios.

11. Why not only use SQL search?
    Strong answer: SQL keyword search misses semantic similarity. Vector search can match "garbage pile" with "solid waste accumulation".

12. Why keep raw and cleaned text?
    Strong answer: Raw text preserves auditability. Cleaned text improves downstream retrieval and processing consistency.

13. How would you handle PII?
    Strong answer: Detect and redact sensitive fields before embeddings, encrypt storage, restrict access, and define retention policies.

14. How would you make the dashboard useful for operators?
    Strong answer: Prioritize unresolved issues, severity distribution, locality trends, duplicate clusters, and escalation queues.

15. What is the biggest production risk?
    Strong answer: Untrusted AI output. The mitigation is citations, evaluation, traceability, human review, and explicit confidence scoring.

