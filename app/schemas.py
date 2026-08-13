from typing import Any, Literal

from pydantic import BaseModel, Field


RetrievalMode = Literal["dense", "sparse", "hybrid"]


class TextDocumentIn(BaseModel):
    collection: str = "default"
    title: str
    text: str
    document_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    document_id: str
    chunks: int
    collection: str


class SearchRequest(BaseModel):
    collection: str = "default"
    query: str
    top_k: int = Field(default=8, ge=1, le=100)
    mode: RetrievalMode = "hybrid"
    filters: dict[str, Any] = Field(default_factory=dict)


class SearchHit(BaseModel):
    id: str
    score: float
    text: str
    document_id: str = ""
    title: str = ""
    chunk_index: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    mode: RetrievalMode
    hits: list[SearchHit]
    trace: dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    collection: str = "default"
    question: str
    top_k: int = Field(default=8, ge=1, le=50)
    mode: RetrievalMode = "hybrid"
    filters: dict[str, Any] = Field(default_factory=dict)
    rewrite_query: bool = True


class Citation(BaseModel):
    source_id: str
    document_id: str
    title: str
    chunk_index: int
    text: str


class ChatResponse(BaseModel):
    question: str
    search_query: str
    answer: str
    citations: list[Citation]
    trace: dict[str, Any] = Field(default_factory=dict)
