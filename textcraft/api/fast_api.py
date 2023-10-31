import uvicorn
from fastapi import FastAPI

from textcraft.api.complex import complex_router
from textcraft.api.config import config_router
from textcraft.api.langserve_api import langserve_router
from textcraft.api.test import test_router

app = FastAPI(title="TextCraft API", version="0.0.2")

app.include_router(test_router, prefix="/test", tags=["test"])
app.include_router(config_router, prefix="/config", tags=["config"])
app.include_router(complex_router, prefix="/complex", tags=["complex"])
langserve_router(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
