from textcraft.core.config import default_embedding, keys_openai
from textcraft.models.embeddings.openai import OpenAIEmbeddings
from textcraft.models.embeddings.qwen import QwenEmbedding


class EmbeddingCreator:
    embeddings = {
        "text-embedding-ada-002": OpenAIEmbeddings,
        "text-embedding-v1": QwenEmbedding,
    }

    @classmethod
    def create_embedding(cls, embedding_type=None):
        if embedding_type is None:
            embedding_type = default_embedding()

        embedding_class = cls.embeddings.get(embedding_type.lower())
        if not embedding_class:
            raise ValueError(f"No embedding class found for type {embedding_type}")

        if embedding_class == OpenAIEmbeddings:
            return OpenAIEmbeddings(openai_api_key=keys_openai)

        return embedding_class()


def get_embedding():
    return EmbeddingCreator().create_embedding()
