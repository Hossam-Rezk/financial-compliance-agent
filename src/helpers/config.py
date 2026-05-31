from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    FILE_ALLOWED_TYPES: List[str] = ["application/pdf", "text/plain"]
    FILE_MAX_SIZE: int

    # Upload streaming chunk (bytes)
    FILE_UPLOAD_CHUNK_SIZE: int = 524288

    # Text splitter settings (characters)
    FILE_DEFAULT_CHUNK_SIZE: int = 512
    FILE_DEFAULT_OVERLAP_SIZE: int = 50
    MONGO_DB_URL: str
    MONGO_DATABASE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

@lru_cache
def get_settings():
    return Settings()