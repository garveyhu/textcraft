from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from summarize.OpenAISummarize import summarize_file
import uvicorn
from io import StringIO

app = FastAPI()

@app.post("/summarize/")
async def summarize(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode('utf-8')
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    
    # 创建一个 StringIO 对象，模仿文件对象
    file_like_object = StringIO(decoded_content)
    
    # 传递给 summarize_file 函数
    summary = summarize_file(file_like_object)
    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
