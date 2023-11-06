from textcraft.core.user_config import get_config
from textcraft.models.embeddings.openai import OpenAIEmbeddings
from textcraft.models.embeddings.qwen import QwenEmbedding


class EmbeddingCreator:
    embeddings = {
        "openai": OpenAIEmbeddings,
        "qwen": QwenEmbedding,
    }

    @classmethod
    def create_embedding(cls, embedding_type=None, **kwargs):
        if embedding_type is None:
            embedding_type = get_config("settings.config.DEFAULT_EMBEDDING")
        embedding_class = cls.embeddings.get(embedding_type.lower())
        if not embedding_class:
            raise ValueError(f"No embedding class found for type {embedding_type}")

        if embedding_class == OpenAIEmbeddings:
            return OpenAIEmbeddings(
                openai_api_key=get_config("settings.models.OPENAI_API_KEY")
            )

        return embedding_class(**kwargs)
