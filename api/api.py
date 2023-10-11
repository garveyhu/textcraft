from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from summarize.openai_summarize import OpenAISummarizer
from io import StringIO

app = FastAPI()

@app.post("/summarize/file")
async def summarize_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode('utf-8')
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    summary = OpenAISummarizer().summarize_file(file_like_object)
    return {"summary": summary}

@app.post("/summarize/text")
async def summarize_text(long_text: str):
    summary = OpenAISummarizer().summarize_text(long_text)
    return {"summary": summary}
