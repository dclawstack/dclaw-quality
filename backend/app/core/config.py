from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "DClaw Quality"
    app_env: str = "dev"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_quality"

    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Add strict field definitions

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
