from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    YOUTUBE_API_KEY: str
    APP_API_KEY: str
    CORS_ORIGINS: str = "*" # Comma-separated list or *
    RATE_LIMIT_PER_MINUTE: int = 100
    GITHUB_TOKEN: str | None = None  # Optional — raises GitHub rate limit from 60 to 5000 req/h
    GEMINI_API_KEY: str | None = None  # Required for the marketing ML pipeline (Stage 4 content generation)
    GEMINI_MODEL: str = "gemini-3.8-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
