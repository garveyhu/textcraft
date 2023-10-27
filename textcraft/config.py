import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Config:
    """
    Configuration class to store the variables for different env access.
    """

    def __init__(self):
        # TextCraft - GENERAL SETTINGS
        self.default_model = os.getenv("DEFAULT_MODEL")
        
        # langchain
        self.langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
        self.langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")
        self.langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
        self.langchain_project = os.getenv("LANGCHAIN_PROJECT")
        
        # LLM PROVIDER
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.spark_appid = os.getenv("SPARK_APPID")
        self.spark_api_key = os.getenv("SPARK_API_KEY")
        self.spark_api_secret = os.getenv("SPARK_API_SECRET")
        self.ernie_api_key = os.getenv("ERNIE_API_KEY")
        self.ernie_api_secret = os.getenv("ERNIE_API_SECRET")
        self.qwen_api_key = os.getenv("QWEN_API_KEY")
        
        # MEMORY
        self.pinecone_env = os.getenv("PINECONE_ENV")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        # COMPLEX
        self.assemblyAI_api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.bearlyAi_api_key = os.getenv("BEARLYAI_API_KEY")
