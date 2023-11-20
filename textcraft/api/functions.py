from fastapi import APIRouter

from textcraft.api.function.chat import chat_router
from textcraft.api.function.es import es_router
from textcraft.api.function.extraction import extraction_router
from textcraft.api.function.summarize import summarize_router
from textcraft.api.function.generalize import generalize_router

function_router = APIRouter(tags=["功能API集"])

function_router.include_router(chat_router)
function_router.include_router(summarize_router)
function_router.include_router(extraction_router)
function_router.include_router(generalize_router)
function_router.include_router(es_router)
