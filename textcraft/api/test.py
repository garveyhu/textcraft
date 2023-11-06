from fastapi import APIRouter

from textcraft.chains.conversation import Conversation

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.get("/conversation")
async def conversation(text: str):
    return Conversation().chatForText(text)
