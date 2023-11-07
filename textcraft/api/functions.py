from fastapi import APIRouter

from textcraft.api.function.chat import chat_router
from textcraft.api.function.complex import complex_router
from textcraft.api.function.summarize import summarize_router

function_router = APIRouter(tags=["功能API集"])

function_router.include_router(summarize_router)
function_router.include_router(chat_router)
function_router.include_router(complex_router)
