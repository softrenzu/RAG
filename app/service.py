from uuid import uuid4

from app.config import Settings
from app.embeddings import EmbeddingClient
from app.ingestion.chunker import chunk_text
from app.vectordb.bvector import BVectorDBClient


class RAGService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.embeddings = EmbeddingClient(settings.embedding_model)
        self.db = BVectorDBClient(settings)

    async def ingest_text(self, collection: str, title: str, text: str, document_id: str | None = None, metadata: dict | None = None) -> tuple[str, int]:
        doc_id = document_id or str(uuid4())
        chunks = chunk_text(text, self.settings.chunk_size, self.settings.chunk_overlap)
        vectors = await self.embeddings.embed(chunks)
        records = []
        for index, chunk in enumerate(chunks):
            records.append({
                "id": f"{doc_id}:{index}",
                "vector": vectors[index],
                "payload": {
                    "document_id": doc_id,
                    "title": title,
                    "chunk_index": index,
                    "text": chunk,
                    "metadata": metadata or {},
                },
            })
        await self.db.upsert(collection, records)
        return doc_id, len(records)

    async def search(self, collection: str, query: str, top_k: int, mode: str, filters: dict | None = None):
        vector = (await self.embeddings.embed([query]))[0]
        return await self.db.search(collection, vector, query, top_k, mode, filters or {})
