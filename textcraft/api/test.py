from fastapi import APIRouter

from textcraft.core.settings import settings

test_router = APIRouter()


@test_router.get("/default_model")
async def get_config():
    return settings.DEFAULT_MODEL
