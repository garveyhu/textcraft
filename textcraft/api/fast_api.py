from io import StringIO
from typing import Dict, List, Union

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from langserve import add_routes

from textcraft.summarize.openai_summarize import OpenAISummarizer
from textcraft.summarize.spark_summarize import SparkSummarizer
from textcraft.tools.classify_tool import ClassifyTool
from textcraft.tools.label_tool import LabelTool
from textcraft.tools.qa_tool import QATool
from textcraft.tools.similarity_search_tool import SimilaritySearchTool
from textcraft.tools.title_tool import TitleTool
from textcraft.tools.vector_store_tool import VectorStoreTool
from textcraft.chains.joketeller import get_chain

app = FastAPI(title="TextCraft API", version="0.0.2")

tag_custom = "custom"
tag_langserve = "langserve"

add_routes(app, get_chain(), path="/langserve")


@app.post("/summarize/openai/file", tags=[tag_custom])
async def summarize_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    return OpenAISummarizer().summarize_file(file_like_object)


@app.post("/summarize/openai/text", tags=[tag_custom])
async def summarize_text(long_text: str):
    return OpenAISummarizer().summarize_text(long_text)


@app.post("/summarize/spark/file", tags=[tag_custom])
async def summarize_spark_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    return SparkSummarizer().summarize_file(file_like_object)


@app.post("/summarize/spark/text", tags=[tag_custom])
async def summarize_spark_text(long_text: str):
    return SparkSummarizer().summarize_text(long_text)


@app.get("/tools/title", tags=[tag_custom])
async def title_tool(text: str):
    return TitleTool().run(text)


@app.get("/tools/classify", tags=[tag_custom])
async def classify_tool(text: str, labels: str):
    classify_tool = ClassifyTool()
    classify_tool.labels = labels
    return classify_tool.run(text)


@app.get("/tools/label", tags=[tag_custom])
async def label_tool(text: str, labels: str):
    label_tool = LabelTool()
    label_tool.labels = labels
    return label_tool.run(text)


@app.get("/tools/qa", tags=[tag_custom])
async def qa_tool(text: str):
    return QATool().run(text)


@app.post("/tools/vector_store", tags=[tag_custom])
async def vector_store_tool(paragraphs: List[Dict[str, Union[str, Dict[str, str]]]]):
    vector_store_tool = VectorStoreTool()
    vector_store_tool.paragraphs = paragraphs
    result = vector_store_tool.run("")
    if result is None:
        return JSONResponse(content={"error": "Invalid file format"}, status_code=400)
    return JSONResponse(content="success", status_code=200)


@app.get("/tools/similarity_search", tags=[tag_custom])
async def similarity_search_tool(text: str):
    return SimilaritySearchTool().run(text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
