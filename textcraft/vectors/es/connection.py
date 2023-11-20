from langchain.memory import ElasticsearchChatMessageHistory
from langchain.vectorstores.elasticsearch import ElasticsearchStore

from textcraft.core.config import dialog_id
from textcraft.core.settings import settings
from textcraft.models.embeddings.embedding_creator import get_embedding

ES_URL = settings.ELASTICSEARCH_URL
ELASTIC_USERNAME = None
ELASTIC_PASSWORD = None

if ES_URL and ELASTIC_USERNAME and ELASTIC_PASSWORD:
    es_connection_details = {
        "es_url": ES_URL,
        "es_user": ELASTIC_USERNAME,
        "es_password": ELASTIC_PASSWORD,
    }
else:
    es_connection_details = {"es_url": ES_URL}


def es_connection(index_name: str):
    return ElasticsearchStore(
        **es_connection_details,
        embedding=get_embedding(),
        index_name=index_name,
    )


def es_connection_history(index_name: str, session_id: str):
    return ElasticsearchChatMessageHistory(
        **es_connection_details,
        index=index_name,
        session_id=session_id,
    )


def get_es_connection_dialog():
    index_name = "dialog_" + dialog_id()
    return es_connection(index_name)


def get_es_connection_resource():
    index_name = "resource_" + dialog_id()
    return es_connection(index_name)


def get_es_connection_history():
    return es_connection_history("history", dialog_id())
