from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    YOUTUBE_API_KEY: str
    GITHUB_TOKEN: str | None = None  # Optional — raises GitHub rate limit from 60 to 5000 req/h

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
