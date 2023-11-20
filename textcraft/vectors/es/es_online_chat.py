from typing import Dict, List, Optional, Union

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from textcraft.utils.complex import init_config_develop
from textcraft.utils.convert_util import docs_to_json
from textcraft.vectors.es.connection import es_connection


class ESOnline:
    """Elasticsearch作向量库操作，存储聊天数据（向量化）."""

    def __init__(self):
        self.index_name = "online_chat"
        self.db = es_connection(self.index_name)

    def online_content(self, content: List[Document]):
        self.db.add_documents(content)
        self.db.client.indices.refresh(index=self.index_name)

    def online_chat(self, chat: List[Dict[str, Union[str, Dict[str, str]]]]):
        """存储聊天记录

                Example:
                    input:
                        [
                            {
                              "metadata": {
                                 "logintime": "1700184326000",
                                 "loginid": "2023111709252100052",
                                 "logouttime": "1700184339000",
                                 "receiver": "ROBOT",
                                 "sender": "游客915203",
                                 "sourceType": "0",
                                 "msgid": "1725324284868747266",
                                 "time": "1700184319000"
                              }
                              "page_content": "转人工"
                            },
                            {
                              "metadata": {
                                "logintime": "1700114152305",
                                "loginid": "111613392800038",
                                "logouttime": "1700117589605",
                                "receiver": "AI",
                                "sender": "Human",
                                "sourceType": "message",
                                "msgid": "1725324284868748566",
                                "time": "1540113168305"
                              },
                              "page_content": "游戏基本上没有设计固定的线路让你前进，要如何选择前进的道路完全取决于你的选择。"
                            }
                        ]
                    .. code-block:: python

                        from textcraft.vectors.es.es_store import ESStore

                        ESStore().store_chat(input)

                Args:
                    chat: 文本内容段落集

                """

        input_docs = [
            Document(
                page_content=paragraph["page_content"], metadata=paragraph["metadata"]
            )
            for paragraph in chat
        ]
        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, separator="\n"
        )
        docs = text_splitter.split_documents(input_docs)
        self.online_content(docs)

    def similarity_search_score(self, query: str):
        """按照得分排序返回结果"""
        docs = self.db.similarity_search_with_score(query, 2)
        return docs_to_json(docs)


if __name__ == "__main__":
    init_config_develop(dialog_id="0")
    es_store = ESOnline()

    print(es_store.similarity_search_score("人工"))

    # docs = get_docs("E:\\VSCode\\vscode-python\\AI\\textcraft\\docs\\探索的技巧.txt")
    # es_store.store_file_paragraphs(docs)

    # print(es_store.similarity_search_score("塞尔达有哪些探索技巧？"))
