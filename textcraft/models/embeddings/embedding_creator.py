from inspect import isclass

from textcraft.core.settings import settings
from textcraft.models.embeddings.openai import openai
from textcraft.models.embeddings.qwen import QwenEmbedding


class EmbeddingCreator:
    embeddings = {
        "openai": openai,
        "qwen": QwenEmbedding,
    }

    @classmethod
    def create_embedding(cls, embedding_type=None, *args, **kwargs):
        if embedding_type is None:
            embedding_type = settings.DEFAULT_EMBEDDING

        embedding_class = cls.embeddings.get(embedding_type.lower())
        if not embedding_class:
            raise ValueError(f"No embedding class found for type {embedding_type}")

        if isclass(embedding_class):
            return embedding_class(*args, **kwargs)

        return embedding_class
