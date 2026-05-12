from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Civic Governance Intelligence Platform"
    environment: str = "development"
    openai_api_key: str | None = None
    database_url: str = "postgresql+asyncpg://civic:civic@localhost:5432/civic_governance"
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4.1-mini"
    chunk_size: int = 900
    chunk_overlap: int = 120
    backend_cors_origins: str = Field(default="http://localhost:3000")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

