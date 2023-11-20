import json

import uvicorn
from fastapi import FastAPI, Request

from textcraft.api.config import config_router
from textcraft.api.functions import function_router
from textcraft.api.langserves import langserve_router
from textcraft.core.user_config import init_config
from textcraft.utils.redis_manager import RedisManager

app = FastAPI(title="TextCraft API", version="0.0.2")

app.include_router(function_router)
app.include_router(config_router)
langserve_router(app)


@app.middleware("http")
async def set_config(request: Request, call_next):
    settings = request.headers.get("settings")
    if settings is None:
        # raise HTTPException(status_code=404, detail="Config header not found.")
        redis_manager = RedisManager()
        dic_data = redis_manager.get_config(app_id="0")
        dialog_model = redis_manager.get_dialog_model(dialog_id="0")
        dic_data.setdefault("user", {}).update({"id": "0"})
        dic_data.setdefault("dialog", {}).update({"id": "0", "model": dialog_model})
    else:
        dic_data = json.loads(json.loads(settings))

    init_config(dic_data)

    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
