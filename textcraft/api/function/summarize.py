from fastapi import APIRouter, Body

from textcraft.api.schema.chats import ChatList
from textcraft.function.summarize.summarizer import Summarizer
from textcraft.tools.classify_tool import ClassifyTool
from textcraft.tools.label_tool import LabelTool

summarize_router = APIRouter(prefix="/summarize", tags=["总结API"])


"""摘要总结"""


@summarize_router.post("/text", description="总结文本")
async def summarize_text(text: str = Body(..., embed=True)):
    return Summarizer().summarize_text(text)


@summarize_router.post("/conversation", description="总结对话")
async def summarize_conversation(chats: ChatList):
    return Summarizer().summarize_conversation_chatlist(chats)


@summarize_router.get("/conversation/shot", description="总结会话指定size对话")
async def summarize_conversation_dialog_shot(size: int = 10):
    return Summarizer().summarize_conversation_dialog_shot(size)


"""OpenNLU"""


@summarize_router.get("/classify", description="段落分类")
async def classify(text: str, labels: str):
    classify_tool = ClassifyTool()
    classify_tool.labels = labels
    return classify_tool.run(text)


@summarize_router.get("/label", description="段落标签")
async def label(text: str, labels: str):
    label_tool = LabelTool()
    label_tool.labels = labels
    return label_tool.run(text)
