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
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.spark_appid = os.getenv("SPARK_APPID")
        self.spark_api_key = os.getenv("SPARK_API_KEY")
        self.spark_api_secret = os.getenv("SPARK_API_SECRET")
        self.ernie_api_key = os.getenv("ERNIE_API_KEY")
        self.ernie_api_secret = os.getenv("ERNIE_API_SECRET")
        self.qwen_api_key = os.getenv("QWEN_API_KEY")
        self.pinecone_env = os.getenv("PINECONE_ENV")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
