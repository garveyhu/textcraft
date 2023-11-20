from typing import Dict, List, Optional, Union

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from textcraft.api.schema.chats import ChatList
from textcraft.core.config import dialog_id, dialog_model
from textcraft.utils.complex import init_config_develop
from textcraft.utils.convert_util import (
    chats_to_docs,
    docs_to_json_score,
    hit_to_json_score,
)
from textcraft.vectors.es.connection import es_connection
from textcraft.vectors.es.ElasticsearchConnection import ElasticsearchConnection


class ESStore:
    """Elasticsearch作向量库操作，存储聊天数据（向量化）."""

    def __init__(self, index_suffix: str = "dialog_"):
        self.dialog_id = dialog_id()
        self.index_name = index_suffix + self.dialog_id
        self.db = es_connection(self.index_name)

    def store_content(self, content: List[Document]):
        """存储文本内容段落集"""
        for paragraph in content:
            paragraph.metadata["llm_type"] = dialog_model()
        self.db.add_documents(content)
        self.db.client.indices.refresh(index=self.index_name)

    def store_messages(self, messages: List[Document]):
        for message in messages:
            message.metadata["type"] = "message"
        self.store_content(messages)

    def store_file_paragraphs(self, paragraphs: List[Document]):
        for paragraph in paragraphs:
            paragraph.metadata["type"] = "file"
        self.store_content(paragraphs)

    def store_chat(self, chats: ChatList):
        """存储聊天记录

        Example:
            input:
                [
                    {
                        "page_content": "塞尔达有哪些探索技巧？",
                        "metadata": {
                            "sender": "Human",
                            "receiver": "AI",
                            "timestamp": "2023-11-07T12:05:00",
                            "type": "message"
                        }
                    },
                    {
                        "page_content": "游戏基本上没有设计固定的线路让你前进，要如何选择前进的道路完全取决于你的选择。",
                        "metadata": {
                            "sender": "AI",
                            "receiver": "Human",
                            "timestamp": "2023-11-07T12:05:03",
                            "type": "message"
                        }
                    }
                ]
            .. code-block:: python

                from textcraft.vectors.es.es_store import ESStore

                ESStore().store_chat(input)

        Args:
            chat: 文本内容段落集

        """

        chat_dicts = [chat.model_dump() for chat in chats.chats]
        docs = chats_to_docs(chat_dicts)
        # text_splitter = CharacterTextSplitter(
        #     chunk_size=1000, chunk_overlap=0, separator="\n"
        # )
        # docs = text_splitter.split_documents(docs)
        self.store_content(docs)
        
    def store_file(self, file_like_object):
        file_content = file_like_object.read()
        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, separator="\n"
        )
        docs = text_splitter.create_documents([file_content])
        self.store_file_paragraphs(docs)

    def similarity_search_score(self, query: str):
        """按照得分排序返回结果"""
        docs = self.db.similarity_search_with_score(query, 2)
        return docs_to_json_score(docs)

    def search_show(self, size: int = 10):
        """搜索指定size文档"""
        body = {
            "query": {"match_all": {}},
            "sort": [{"metadata.timestamp": {"order": "desc"}}],
            "_source": ["text", "metadata"],
            "size": size,
        }
        hits = ElasticsearchConnection().search_index(self.index_name, body)
        hits_reversed = hits[::-1]
        return hit_to_json_score(hits_reversed)


if __name__ == "__main__":
    init_config_develop(dialog_id="0")
    es_store = ESStore()

    # docs = get_docs("E:\\VSCode\\vscode-python\\AI\\textcraft\\docs\\探索的技巧.txt")
    # es_store.store_file_paragraphs(docs)

    # print(es_store.similarity_search_score("塞尔达有哪些探索技巧？"))
