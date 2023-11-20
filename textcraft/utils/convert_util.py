from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

from textcraft.api.schema.chats import ChatList


def chats_to_docs(chats):
    """聊天记录chats转换为langchain文档Document格式

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

            output:
                [
                    Document(
                        page_content="塞尔达有哪些探索技巧？",
                        metadata={
                            "sender": "Human",
                            "receiver": "AI",
                            "timestamp": "2023-11-07T12:05:00",
                            "type": "message"
                        }
                    ),
                    Document(
                        page_content="游戏基本上没有设计固定的线路让你前进，要如何选择前进的道路完全取决于你的选择。",
                        metadata={
                            "sender": "AI",
                            "receiver": "Human",
                            "timestamp": "2023-11-07T12:05:03",
                            "type": "message"
                        }
                    )
                ]

    """

    docs = [
        Document(page_content=chat["page_content"], metadata=chat["metadata"])
        for chat in chats
    ]
    return docs


def chatlist_to_chats(chats: ChatList):
    return [chat.model_dump() for chat in chats.chats]


def chats_to_chat_str(chats: List[dict]):
    chats_text = "\n".join(
        [f"{chat['metadata']['sender']}: {chat['page_content']}" for chat in chats]
    )
    return chats_text


def docs_to_json_score(data):
    json_data = []

    for item in data:
        doc, score = item
        doc_dict = {
            "page_content": doc.page_content,
            "metadata": doc.metadata,
            "score": score,
        }
        json_data.append(doc_dict)

    return json_data


def get_docs(path: str):
    """获取文件路径文档内容"""
    loader = TextLoader(
        path=path,
        encoding="utf-8",
    )
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=500, chunk_overlap=0, separator="\n"
    )
    docs = text_splitter.split_documents(documents)
    return docs


def hit_to_json_score(data):
    """将es查询结果hits转换为json格式"""
    json_data = []

    for item in data:
        doc = item["_source"]
        score = item["_score"]
        doc_dict = {
            "page_content": doc["text"],
            "metadata": doc["metadata"],
            "score": score,
        }
        json_data.append(doc_dict)

    return json_data


def docs_to_json(data):
    json_data = []

    for item in data:
        doc, score = item
        doc_dict = {
            "body": doc.page_content,
            "sourceType": doc.metadata["sourceType"],
            "fromjid": doc.metadata["sender"],
            "tojid": doc.metadata["receiver"],
            "loginid": doc.metadata["loginid"],
            "time": doc.metadata["time"],
            "id": doc.metadata["msgid"],
            "logintime": doc.metadata["logintime"],
            "logouttime": doc.metadata["logouttime"],
            "score": score
        }
        json_data.append(doc_dict)

    return json_data

def hit_to_json(data):
    json_data = []

    for item in data:
        doc, score = item
        doc_dict = {
            "body": doc.page_content,
            "sourceType": doc.metadata["sourceType"],
            "fromjid": doc.metadata["sender"],
            "tojid": doc.metadata["receiver"],
            "loginid": doc.metadata["loginid"],
            "time": doc.metadata["time"],
            "id": doc.metadata["msgid"],
            "logintime": doc.metadata["logintime"],
            "logouttime": doc.metadata["logouttime"],
            "score": score
        }
        json_data.append(doc_dict)

    return json_data