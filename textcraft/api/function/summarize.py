from io import StringIO

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from textcraft.function.summarize.summarizer import Summarizer
from textcraft.tools.classify_tool import ClassifyTool
from textcraft.tools.label_tool import LabelTool

summarize_router = APIRouter(prefix="/summarize", tags=["总结API"])


@summarize_router.post("/text", description="总结文字")
async def summarize_text(long_text: str):
    return Summarizer().summarize_text(long_text)


@summarize_router.post("/file", description="总结文件")
async def summarize_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    return Summarizer().summarize_file(file_like_object)


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
