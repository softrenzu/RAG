# RooomRAG — Retrieval-Augmented Generation Engine

Version: `0.3.0`

RooomRAG is a source-available Python/FastAPI RAG engine for document ingestion, retrieval, context construction, and cited LLM answers. It is designed to work with RooomVector through a dedicated adapter rather than depending on a Qdrant-compatible API.

## Data path

```text
Document
  -> parser
  -> chunker
  -> multilingual embedding
  -> RooomVector adapter

Question
  -> multilingual embedding
  -> hybrid retrieval
  -> context construction
  -> LLM
  -> answer + citations
```

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

```bash
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Copy `config.example` to `.env` and configure the vector database and LLM endpoints.

The internal adapter filename and some environment variables may retain earlier `bvectorDB` naming during the `0.3.x` compatibility transition. The product integration target is RooomVector.

## Roadmap

- Query rewrite
- Dense + sparse result fusion
- MMR diversity control
- Reranking
- ACL/document permissions
- Document versioning
- Evaluation datasets
- Automatic retrieval and chunking optimization

## Licensing and enterprise support

Starting with version `0.3.0`, ROOOMTECH-authored code is offered under either the PolyForm Noncommercial License 1.0.0 for uses permitted by that license, or a separate paid ROOOMTECH Commercial Software License for business/commercial-purpose uses and other uses outside the PolyForm permission.

Commercial license agreements, maintenance, technical support, implementation, integration, upgrades, security support, SLA options, private builds, and custom development are available.

Contact: `support@rooomtech.com`

PolyForm Noncommercial License 1.0.0: https://polyformproject.org/licenses/noncommercial/1.0.0

Earlier releases retain their published license terms. Third-party software retains its own licenses. See `LICENSE`.
