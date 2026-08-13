from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "RooomtechRAG"
    app_env: str = "development"

    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    llm_url: str = "http://localhost:11434/api/chat"
    llm_model: str = "qwen3:8b"

    bvectordb_url: str = "http://localhost:8081"
    bvectordb_upsert_path: str = "/v1/collections/{collection}/upsert"
    bvectordb_search_path: str = "/v1/collections/{collection}/search"
    bvectordb_delete_path: str = "/v1/collections/{collection}/documents/{document_id}"

    default_collection: str = "default"
    default_top_k: int = 8
    chunk_size: int = 900
    chunk_overlap: int = 150
    request_timeout: float = 60.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
