from pathlib import Path

from dotenv import dotenv_values
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # CONFIG
    REDIS_HOST: str = None
    REDIS_PORT: str = None
    REDIS_DB: str = None
    REDIS_PASSWORD: str = None

    ELASTICSEARCH_URL: str = None
    ES_SCHEME: str = None
    ES_HOSTS: str = None
    ES_PORT: int = None

    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_ENDPOINT: str = None
    LANGCHAIN_API_KEY: str = None
    LANGCHAIN_PROJECT: str = None


def refresh_settings():
    env_values = dotenv_values(env_file)
    for key, value in env_values.items():
        setattr(settings, key, value)


config_file = Path(__file__).parent.parent.parent / "config.json"
env_file = Path(__file__).parent.parent.parent / ".env"
settings = Settings(_env_file=env_file, _env_file_encoding="utf-8")
