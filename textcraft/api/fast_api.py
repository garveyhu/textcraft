import json

import uvicorn
from fastapi import FastAPI, HTTPException, Request

from textcraft.api.complex import complex_router
from textcraft.api.config import config_router
from textcraft.api.langserve_api import langserve_router
from textcraft.api.test import test_router
from textcraft.core.user_config import init_config
from textcraft.utils.redis_manager import RedisManager

app = FastAPI(title="TextCraft API", version="0.0.2")

app.include_router(test_router, prefix="/test", tags=["test"])
app.include_router(config_router, prefix="/config", tags=["config"])
app.include_router(complex_router, tags=["complex"])
langserve_router(app)


@app.middleware("http")
async def set_config(request: Request, call_next):
    user_id = request.headers.get("User-Id")
    if user_id is None:
        user_id = "030317"
        # raise HTTPException(status_code=400, detail="userId header is missing")
    redis_manager = RedisManager()
    json_data = redis_manager.get_config(user_id)
    if json_data is None:
        raise HTTPException(status_code=404, detail="User config not found.")

    init_config(json_data)

    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
