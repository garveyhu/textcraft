from typing import Dict, List, Union

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    page_content: str
    metadata: Dict[str, Union[str, Dict[str, str]]] = Field(...)


class ChatList(BaseModel):
    chats: List[ChatMessage] = Field(
        ...,
        example=[
            {
                "page_content": "塞尔达有哪些探索技巧？",
                "metadata": {
                    "sender": "Human",
                    "receiver": "AI",
                    "timestamp": "2023-11-07T12:05:00",
                    "type": "message",
                },
            },
            {
                "page_content": "游戏基本上没有设计固定的线路让你前进，要如何选择前进的道路完全取决于你的选择。",
                "metadata": {
                    "sender": "AI",
                    "receiver": "Human",
                    "timestamp": "2023-11-07T12:05:03",
                    "type": "message",
                },
            },
        ],
    )
