from fastapi import APIRouter, Body

from textcraft.chains.conversation import Conversation

chat_router = APIRouter(prefix="/chat", tags=["聊天API"])


"""LLM对话"""


@chat_router.post("/call", description="通用会话(非记忆)")
async def chat(text: str = Body(... , embed=True)):
    return Conversation().chat_without_memory(text)


@chat_router.post("/conversation", description="通用会话(记忆)")
async def chat(text: str = Body(... , embed=True)):
    return Conversation().chat_with_memory(text)
