from textcraft.core.settings import settings
from textcraft.models.embeddings.openai import get_openai
from textcraft.models.embeddings.qwen import get_qwen


class EmbeddingCreator:
    @classmethod
    def create_embedding(cls, embedding_type=None):
        embeddings = {
            "openai": get_openai(),
            "qwen": get_qwen(),
        }
        if embedding_type is None:
            embedding_type = settings.DEFAULT_EMBEDDING


        embedding_class = embeddings.get(embedding_type.lower())
        if not embedding_class:
            raise ValueError(f"No embedding class found for type {embedding_type}")

        return embedding_class
