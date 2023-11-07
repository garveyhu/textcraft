from fastapi import APIRouter

from textcraft.chains.conversation import Conversation

test_router = APIRouter(prefix="/test", tags=["测试API"])


@test_router.get("/conversation", description="历史会话")
async def conversation(text: str):
    return Conversation().chatForText(text)
