from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "RooomtechRAG"
    app_env: str = "development"

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"

    bvectordb_url: str = "http://localhost:8081"
    bvectordb_api_key: str = ""
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
