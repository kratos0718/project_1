# RAG, Agents, Memory Cheatsheet

## RAG

Retrieval-Augmented Generation means the system retrieves relevant context before generating an answer. In this platform, complaints are embedded, stored in ChromaDB, retrieved by semantic similarity, and attached as citations to the AI report.

## Embeddings

Embeddings convert complaint text into dense numeric vectors. Similar complaints should have nearby vectors even if they use different words.

## Chunking

Chunking splits long complaints into smaller searchable units. This project uses a `900` character chunk size and `120` character overlap to preserve context around boundaries.

## Metadata Filtering

Metadata filtering narrows vector search by fields like locality or category. This improves relevance and prevents unrelated complaints from polluting retrieval.

## Reranking

Reranking reorders retrieved candidates using additional signals. The current baseline sorts by vector score and recency metadata. A production version could add a cross-encoder reranker.

## Agents

The platform uses LangGraph agents:

- Planner Agent: chooses workflow path.
- Severity Agent: scores risk and urgency.
- Duplicate Detection Agent: identifies semantically similar complaints.
- Summarization Agent: creates an executive report grounded in citations.
- Escalation Agent: recommends the right authority.

## Memory

Short-term memory is the current workflow state. Long-term memory is persisted in PostgreSQL. Locality memory tracks recurring issues in a specific area.

## Evaluation

Important metrics:

- Retrieval precision
- Hallucination risk
- Response relevance
- Latency
- Citation coverage

## Strong Interview Line

The system is designed so AI output is not treated as magic text. Every report is connected to retrieval evidence, workflow traces, persistent memory, and evaluation logs.

