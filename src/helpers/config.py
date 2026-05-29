from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    FILE_ALLOWED_TYPES: List[str] = ["application/pdf", "text/plain"]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

def get_settings():
    return Settings()