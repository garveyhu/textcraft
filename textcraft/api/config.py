from dotenv import set_key, dotenv_values
from fastapi import APIRouter, HTTPException

from textcraft.core.settings import env_file, refresh_settings, settings

config_router = APIRouter()


@config_router.post("/env/update")
async def update_config(config_param: dict):
    key = config_param.get("key")
    value = config_param.get("value")

    if key is None:
        raise HTTPException(status_code=400, detail="Key is required in the request.")

    # 更新配置
    success = set_key(env_file, key, value)

    if not success:
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found in .env file.")

    # 刷新配置
    refresh_settings()

    return "Configuration updated successfully."

@config_router.get("/env/list")
async def env_list():
    config_list = []
    env_values = dotenv_values(env_file)

    for key, value in env_values.items():
        config_list.append({"key": key, "value": value})

    return config_list


@config_router.get("/settings/list")
async def settings_list():
    config_list = []
    for key, value in settings:
        config_list.append({"key": key, "value": value})

    return config_list
