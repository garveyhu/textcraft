from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseSettings


class Settings(BaseSettings):
    # GENERAL SETTINGS
    DEFAULT_LLM: str = None
    DEFAULT_EMBEDDING: str = None
    DEFAULT_VECTOR_STORE: str = None

    # LANGCHAIN
    LANGCHAIN_TRACING_V2: str = None
    LANGCHAIN_ENDPOINT: str = None
    LANGCHAIN_API_KEY: str = None
    LANGCHAIN_PROJECT: str = None

    # LLM PROVIDER
    OPENAI_API_KEY: str = None
    HUGGINGFACEHUB_API_TOKEN: str = None
    SPARK_APPID: str = None
    SPARK_API_KEY: str = None
    SPARK_API_SECRET: str = None
    ERNIE_API_KEY: str = None
    ERNIE_API_SECRET: str = None
    QWEN_API_KEY: str = None

    # MEMORY
    PINECONE_ENV: str = None
    PINECONE_API_KEY: str = None

    # CONFIG
    TEMPERATURE: float = 0.5
    
    # COMPLEX
    ASSEMBLYAI_API_KEY: str = None
    BEARLYAI_API_KEY: str = None


def refresh_settings():
    env_values = dotenv_values(env_file)
    for key, value in env_values.items():
        setattr(settings, key, value)


env_file = Path(__file__).parent.parent.parent / ".env"
settings = Settings(_env_file=env_file, _env_file_encoding="utf-8")
