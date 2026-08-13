# RooomtechRAG

RooomtechRAG is a Python/FastAPI RAG engine designed to use **bvectorDB** as its vector storage and retrieval layer.

## v0.1 scope

- Document ingestion: TXT, Markdown, PDF, DOCX, PPTX, XLSX
- Adaptive text chunking
- Embeddings through an OpenAI-compatible API
- bvectorDB adapter isolated from the RAG engine
- Dense / hybrid retrieval request modes
- Reciprocal Rank Fusion (RRF)
- Maximal Marginal Relevance (MMR)
- Optional reranking hook
- Context construction with source citations
- OpenAI-compatible LLM generation
- FastAPI endpoints for ingest, search and chat
- Retrieval trace in API responses

## Architecture

```text
Documents
   |
Parser -> Chunker -> Embedding
   |                  |
   +-------------> bvectorDB
                        |
Question -> Query Rewrite -> Retrieval -> RRF/MMR -> Context -> LLM -> Answer + citations
```

## API

- `GET /health`
- `POST /v1/documents/text`
- `POST /v1/documents/file`
- `POST /v1/search`
- `POST /v1/chat`

## Setup

```bash
cp .env.example .env
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Swagger UI: `http://localhost:8000/docs`

## bvectorDB connection

RooomtechRAG deliberately does not assume Qdrant compatibility. The bvectorDB integration is contained in `app/vectordb/bvector.py`.

The default HTTP adapter expects JSON APIs for upsert and search. Endpoint paths are configurable so bvectorDB can keep its own API design.

```env
BVECTORDB_URL=http://localhost:8081
BVECTORDB_UPSERT_PATH=/v1/collections/{collection}/upsert
BVECTORDB_SEARCH_PATH=/v1/collections/{collection}/search
BVECTORDB_DELETE_PATH=/v1/collections/{collection}/documents/{document_id}
```

If bvectorDB uses different request/response bodies, only `app/vectordb/bvector.py` needs modification.

## Example

```bash
curl -X POST http://localhost:8000/v1/documents/text \
  -H 'Content-Type: application/json' \
  -d '{"collection":"manuals","title":"sample","text":"RooomtechRAG uses bvectorDB."}'

curl -X POST http://localhost:8000/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"collection":"manuals","question":"What database does RooomtechRAG use?"}'
```

## Next milestones

v0.2 will add automated RAG evaluation and AutoPilot optimization across chunk size, embedding model, top-k, retrieval strategy and reranker settings.
