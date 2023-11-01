from langchain.embeddings import OpenAIEmbeddings

from textcraft.core.settings import settings


def get_openai():
    openai_api_key = settings.OPENAI_API_KEY
    openai = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return openai
