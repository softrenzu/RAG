from typing import Any

import httpx

from app.config import Settings
from app.schemas import SearchHit


class BVectorDBClient:
    """Thin adapter between RooomtechRAG and bvectorDB.

    bvectorDB is intentionally treated as its own database API rather than a
    Qdrant-compatible endpoint. If its wire contract changes, edit this file;
    the rest of RooomtechRAG remains unchanged.
    """

    def __init__(self, settings: Settings):
        self.base_url = settings.bvectordb_url.rstrip("/")
        self.upsert_path = settings.bvectordb_upsert_path
        self.search_path = settings.bvectordb_search_path
        self.delete_path = settings.bvectordb_delete_path
        self.timeout = settings.request_timeout

    def _url(self, path: str, **values: str) -> str:
        return self.base_url + path.format(**values)

    async def upsert(self, collection: str, records: list[dict[str, Any]]) -> None:
        url = self._url(self.upsert_path, collection=collection)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json={"records": records})
            response.raise_for_status()

    async def search(
        self,
        collection: str,
        vector: list[float],
        query_text: str,
        top_k: int,
        mode: str,
        filters: dict[str, Any] | None = None,
    ) -> list[SearchHit]:
        url = self._url(self.search_path, collection=collection)
        body = {
            "vector": vector,
            "query": query_text,
            "top_k": top_k,
            "mode": mode,
            "filter": filters or {},
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=body)
            response.raise_for_status()
            raw = response.json()

        items = raw if isinstance(raw, list) else raw.get("hits", raw.get("results", raw.get("points", [])))
        hits: list[SearchHit] = []
        for item in items:
            payload = item.get("payload", item.get("metadata", {})) or {}
            text = item.get("text") or payload.get("text", "")
            hits.append(
                SearchHit(
                    id=str(item.get("id", payload.get("chunk_id", ""))),
                    score=float(item.get("score", item.get("similarity", 0.0))),
                    text=text,
                    document_id=str(payload.get("document_id", item.get("document_id", ""))),
                    title=str(payload.get("title", item.get("title", ""))),
                    chunk_index=int(payload.get("chunk_index", item.get("chunk_index", 0))),
                    metadata=payload.get("metadata", payload),
                )
            )
        return hits

    async def delete_document(self, collection: str, document_id: str) -> None:
        url = self._url(self.delete_path, collection=collection, document_id=document_id)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(url)
            response.raise_for_status()
