import uvicorn
from fastapi import FastAPI, HTTPException, Request

from textcraft.api.config import config_router
from textcraft.api.functions import function_router
from textcraft.api.langserves import langserve_router
from textcraft.api.test import test_router
from textcraft.core.user_config import init_config
from textcraft.utils.redis_manager import RedisManager

app = FastAPI(title="TextCraft API", version="0.0.2")

app.include_router(config_router)
app.include_router(test_router)
app.include_router(function_router)
langserve_router(app)


@app.middleware("http")
async def set_config(request: Request, call_next):
    user_id = request.headers.get("User-Id")
    app_id = request.headers.get("App-Id")
    dialog_id = request.headers.get("Dialog-Id")
    
    if app_id is None:
        app_id = "0"
    if user_id is None:
        user_id = "0"
    if dialog_id is None:
        dialog_id = "0"
        
    redis_manager = RedisManager()
    dic_data = redis_manager.get_config(app_id)
    dic_data.setdefault("user", {}).update({"id": user_id})
    dic_data.setdefault("dialog", {}).update({"id": dialog_id})
    
    if dic_data is None:
        raise HTTPException(status_code=404, detail="User config not found.")

    init_config(dic_data)

    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
