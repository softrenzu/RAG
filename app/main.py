import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.generation import AnswerGenerator
from app.ingestion.parser import parse_document
from app.llm import LLMClient
from app.schemas import ChatRequest, ChatResponse, IngestResponse, SearchRequest, SearchResponse, TextDocumentIn
from app.service import RAGService

settings = get_settings()
service = RAGService(settings)
generator = AnswerGenerator(LLMClient(settings))
app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "name": settings.app_name, "vector_db": "bvectorDB"}


@app.post("/v1/documents/text", response_model=IngestResponse)
async def ingest_text(document: TextDocumentIn) -> IngestResponse:
    try:
        doc_id, count = await service.ingest_text(
            document.collection,
            document.title,
            document.text,
            document.document_id,
            document.metadata,
        )
        return IngestResponse(document_id=doc_id, chunks=count, collection=document.collection)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/v1/documents/file", response_model=IngestResponse)
async def ingest_file(
    file: UploadFile = File(...),
    collection: str = Form("default"),
    title: str = Form(""),
    document_id: str | None = Form(None),
    metadata: str = Form("{}"),
) -> IngestResponse:
    try:
        data = await file.read()
        text = parse_document(file.filename or "document.txt", data)
        metadata_obj = json.loads(metadata)
        doc_id, count = await service.ingest_text(
            collection,
            title or file.filename or "document",
            text,
            document_id,
            metadata_obj,
        )
        return IngestResponse(document_id=doc_id, chunks=count, collection=collection)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/v1/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    try:
        hits = await service.search(request.collection, request.query, request.top_k, request.mode, request.filters)
        return SearchResponse(
            query=request.query,
            mode=request.mode,
            hits=hits,
            trace={"collection": request.collection, "top_k": request.top_k, "backend": "bvectorDB"},
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        hits = await service.search(request.collection, request.question, request.top_k, request.mode, request.filters)
        answer, citations = await generator.generate(request.question, hits)
        return ChatResponse(
            question=request.question,
            search_query=request.question,
            answer=answer,
            citations=citations,
            trace={"collection": request.collection, "top_k": request.top_k, "mode": request.mode, "backend": "bvectorDB"},
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
