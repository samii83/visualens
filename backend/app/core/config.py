# backend/app/core/config.py
"""
Configuration management using Pydantic's BaseSettings.
Loads environment variables from a .env file.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Defines application settings."""
    HUGGING_FACE_API_KEY: str
    HUGGING_FACE_IMAGE_CAPTION_MODEL: str = "nlpconnect/vit-gpt2-image-captioning"
    HUGGING_FACE_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"] # Default for Vite

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Returns a cached instance of the settings."""
    return Settings()
