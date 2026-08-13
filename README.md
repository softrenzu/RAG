# RooomtechRAG

RooomtechRAG is a Python/FastAPI RAG engine built around **bvectorDB** as the vector storage and retrieval layer.

## v0.1

Current data path:

```text
Document
  -> parser
  -> chunker
  -> multilingual embedding
  -> bvectorDB

Question
  -> multilingual embedding
  -> bvectorDB search
  -> context construction
  -> LLM
  -> answer + citations
```

RooomtechRAG does **not** require bvectorDB to expose a Qdrant-compatible API. All bvectorDB-specific communication is isolated in `app/vectordb/bvector.py`.

## Supported input

- TXT
- Markdown
- PDF
- DOCX
- PPTX
- XLSX

## API

- `GET /health`
- `POST /v1/documents/text`
- `POST /v1/documents/file`
- `POST /v1/search`
- `POST /v1/chat`

OpenAPI / Swagger is available at `/docs` while the service is running.

## Setup

Create a Python 3.11 environment, then install the package and start FastAPI.

```text
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Copy `config.example` to `.env` and adjust the bvectorDB and LLM endpoints.

## bvectorDB contract

Default paths:

```text
POST /v1/collections/{collection}/upsert
POST /v1/collections/{collection}/search
DELETE /v1/collections/{collection}/documents/{document_id}
```

Default upsert body:

```json
{
  "records": [
    {
      "id": "document-id:0",
      "vector": [0.1, 0.2],
      "payload": {
        "document_id": "document-id",
        "title": "manual",
        "chunk_index": 0,
        "text": "...",
        "metadata": {}
      }
    }
  ]
}
```

Default search body:

```json
{
  "vector": [0.1, 0.2],
  "query": "search text",
  "top_k": 8,
  "mode": "hybrid",
  "filter": {}
}
```

The adapter accepts search results returned as a list or under `hits`, `results`, or `points`.

## Embedding

v0.1 uses `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` by default so Japanese and English documents can be embedded locally. The model is configurable with `EMBEDDING_MODEL`.

## LLM

The default configuration targets a local Ollama-style chat endpoint and uses `qwen3:8b`. The URL and model are configurable with `LLM_URL` and `LLM_MODEL`. `app/llm.py` is intentionally isolated so additional providers can be added without changing the RAG pipeline.

## Next milestones

- exact bvectorDB wire-contract integration once its final API is fixed
- query rewrite
- dense + sparse result fusion
- MMR diversity control
- reranking
- ACL / document permissions
- document versioning
- evaluation dataset support
- RAG AutoPilot for automatic chunk-size, retrieval, top-k and reranker optimization
