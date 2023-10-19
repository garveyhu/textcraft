from io import StringIO

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from textcraft.summarize.openai_summarize import OpenAISummarizer
from textcraft.summarize.spark_summarize import SparkSummarizer
from textcraft.pinecone_store.pinecone_qa import vector_qa
from textcraft.tools.title_tool import TitleTool
from textcraft.tools.label_tool import AliUnderstand
from textcraft.tools.qa_tool import QATool

app = FastAPI()


@app.post("/summarize/file")
async def summarize_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    summary = OpenAISummarizer().summarize_file(file_like_object)
    return {"summary": summary}


@app.post("/summarize/text")
async def summarize_text(long_text: str):
    summary = OpenAISummarizer().summarize_text(long_text)
    return {"summary": summary}


@app.post("/summarize/spark/file")
async def summarize_spark_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    summary = SparkSummarizer().summarize_file(file_like_object)
    return {"summary": summary}


@app.post("/summarize/spark/text")
async def summarize_spark_text(long_text: str):
    summary = SparkSummarizer().summarize_text(long_text)
    return {"summary": summary}


@app.post("/pinecone_store/qa")
async def pinecone_store_qa(question: str):
    return vector_qa(question)


@app.get("/tools/title")
async def title_tool(text: str):
    return TitleTool().run(text)


@app.get("/tools/label")
async def label_tool(text: str):
    return AliUnderstand().run(text)


@app.get("/tools/qa")
async def qa_tool(text: str):
    return QATool().run(text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
