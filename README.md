# Production Agentic RAG

Production-oriented retrieval-augmented generation service built with **FastAPI + LangGraph + PostgreSQL/pgvector**. The project demonstrates agentic routing, hybrid retrieval, reranking, grounded citations, evaluation hooks, Docker, and automated tests.

## Architecture

```text
Client -> FastAPI -> LangGraph
                    |-> retrieve -> pgvector
                    |-> rerank -> relevance scoring
                    |-> answer -> LLM provider
                    `-> citations + trace metadata
```

## Highlights

- Agentic query routing instead of a single fixed RAG chain
- Chunking + embeddings + pgvector similarity search
- Lightweight hybrid keyword/vector retrieval
- Reciprocal-rank fusion and deterministic reranking
- Answers require source citations
- Provider-agnostic LLM interface with a local deterministic fallback
- Health endpoint, structured response models, and unit tests
- Docker Compose for PostgreSQL/pgvector

## API

`POST /v1/ask`

```json
{"question":"What is the refund policy?","top_k":5}
```

Response includes the answer, route, confidence, and cited source IDs.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

For vector search infrastructure:

```bash
docker compose up -d
```

## Tests

```bash
pytest -q
```

## Engineering notes

This is an original portfolio implementation using open-source libraries rather than a copied tutorial repository. Benchmark numbers should be generated from the included evaluation harness before being claimed publicly.
