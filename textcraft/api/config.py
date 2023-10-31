from pathlib import Path

from fastapi import APIRouter, HTTPException

from textcraft.core.settings import refresh_settings, settings

config_router = APIRouter()
env_file_path = Path(__file__).parent.parent.parent / ".env"


@config_router.post("/update")
async def update_config(config_param: dict):
    key = config_param.get("key")
    value = config_param.get("value")

    if key is None:
        raise HTTPException(status_code=400, detail="Key is required in the request.")

    with open(env_file_path, "r", encoding="utf-8") as env_file:
        lines = env_file.readlines()

    updated_lines = []
    key_found = False
    for line in lines:
        if line.strip().startswith(key + "="):
            updated_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            updated_lines.append(line)

    if not key_found:
        raise HTTPException(
            status_code=404, detail=f"Key '{key}' not found in .env file."
        )

    with open(env_file_path, "w", encoding="utf-8") as env_file:
        env_file.writelines(updated_lines)

    refresh_settings()

    return "Configuration updated successfully."


@config_router.get("/list/env")
async def env_list():
    config_list = []
    with open(env_file_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            if line.strip() and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                value = value.strip('"')
                config_list.append({"key": key, "value": value})

    return config_list


@config_router.get("/list/settings")
async def settings_list():
    config_list = []
    for key, value in settings:
        config_list.append({"key": key, "value": value})

    return config_list
