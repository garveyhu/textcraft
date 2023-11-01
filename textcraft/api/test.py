from cgi import test
from fastapi import APIRouter

from textcraft.core.settings import settings
from textcraft.chains.conversation import Conversation

test_router = APIRouter()


@test_router.get("/default_model")
async def get_config():
    return settings.DEFAULT_LLM

@test_router.get("/conversation")
async def conversation(text: str):
    return Conversation().chatForText(text)
