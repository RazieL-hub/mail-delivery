from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_async_url: str
    database_sync_url: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
