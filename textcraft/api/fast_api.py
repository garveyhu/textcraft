from io import StringIO
from typing import List, Dict, Union

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from textcraft.summarize.openai_summarize import OpenAISummarizer
from textcraft.summarize.spark_summarize import SparkSummarizer
from textcraft.tools.title_tool import TitleTool
from textcraft.tools.label_tool import LabelTool
from textcraft.tools.classify_tool import ClassifyTool
from textcraft.tools.qa_tool import QATool
from textcraft.tools.similarity_search_tool import SimilaritySearchTool
from textcraft.tools.vector_store_tool import VectorStoreTool

app = FastAPI()


@app.post("/summarize/openai/file")
async def summarize_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    return OpenAISummarizer().summarize_file(file_like_object)


@app.post("/summarize/openai/text")
async def summarize_text(long_text: str):
    return OpenAISummarizer().summarize_text(long_text)


@app.post("/summarize/spark/file")
async def summarize_spark_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    return SparkSummarizer().summarize_file(file_like_object)


@app.post("/summarize/spark/text")
async def summarize_spark_text(long_text: str):
    return SparkSummarizer().summarize_text(long_text)


@app.get("/tools/title")
async def title_tool(text: str):
    return TitleTool().run(text)


@app.get("/tools/classify")
async def classify_tool(text: str, labels: str):
    classify_tool = ClassifyTool()
    classify_tool.labels = labels
    return classify_tool.run(text)


@app.get("/tools/label")
async def label_tool(text: str, labels: str):
    label_tool = LabelTool()
    label_tool.labels = labels
    return label_tool.run(text)


@app.get("/tools/qa")
async def qa_tool(text: str):
    return QATool().run(text)


@app.post("/tools/vector_store")
async def vector_store_tool(paragraphs: List[Dict[str, Union[str, Dict[str, str]]]]):
    vector_store_tool = VectorStoreTool()
    vector_store_tool.paragraphs = paragraphs
    result = vector_store_tool.run('')
    if result is None:
        return JSONResponse(content={"error": "Invalid file format"}, status_code=400)
    return JSONResponse(content="success", status_code=200)


@app.get("/tools/similarity_search")
async def similarity_search_tool(text: str):
    return SimilaritySearchTool().run(text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
