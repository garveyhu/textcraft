from fastapi import APIRouter, Body

from textcraft.chains.generalize import Generalize

generalize_router = APIRouter(prefix="/generalize", tags=["信息泛化"])


"""信息泛化"""


@generalize_router.post("/chat", description="聊天泛化")
async def generalize(text: str = Body(..., embed=True)):
    return Generalize().question_generalize(text=text)
