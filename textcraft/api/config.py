from dotenv import dotenv_values, set_key
from fastapi import APIRouter, HTTPException, Request

from textcraft.core.settings import env_file, refresh_settings, settings
from textcraft.core.user_config import get_config_dict
from textcraft.utils.mongo_manager import MongoDBManager
from textcraft.utils.redis_manager import RedisManager

config_router = APIRouter(prefix="/settings", tags=["settings"])


@config_router.post("/system/update")
async def system_config_update(config_param: dict):
    key = config_param.get("key")
    value = config_param.get("value")

    if key is None:
        raise HTTPException(status_code=400, detail="Key is required in the request.")

    success = set_key(env_file, key, value)

    if not success:
        raise HTTPException(
            status_code=404, detail=f"Key '{key}' not found in .env file."
        )

    refresh_settings()

    return "System configuration updated successfully."


@config_router.get("/system/list")
async def system_config_list():
    config_list = []
    env_values = dotenv_values(env_file)

    for key, value in env_values.items():
        config_list.append({"key": key, "value": value})

    return config_list


@config_router.get("/system/runtime/list")
async def system_runtime_config():
    config_list = []
    for key, value in settings:
        config_list.append({"key": key, "value": value})

    return config_list


@config_router.post("/user/create")
async def user_config_create(request: Request):
    try:
        json_data = await request.json()
        mongo_manager = MongoDBManager()
        redis_manager = RedisManager()

        mongo_manager.insert_config(json_data)
        redis_manager.update_config(json_data)

        return "User configuration created successfully"
    except Exception as e:
        return {"error": str(e)}


@config_router.post("/user/update")
async def user_config_update(request: Request):
    try:
        json_data = await request.json()
        mongo_manager = MongoDBManager()
        redis_manager = RedisManager()

        mongo_manager.update_config(json_data)
        redis_manager.update_config(json_data)

        return "User configuration updated successfully"
    except Exception as e:
        return {"error": str(e)}


@config_router.get("/user/list")
async def user_config_list(user_id: str):
    mongo_manager = MongoDBManager()
    redis_manager = RedisManager()

    mongo_config_list = mongo_manager.get_config(user_id)
    redis_config_list = redis_manager.get_config(user_id)

    return {"mongo": mongo_config_list, "redis": redis_config_list}


@config_router.get("/user/thread")
async def user_config_thread():
    return get_config_dict()


@config_router.get("/user/async")
async def user_config_async():
    redis_manager = RedisManager()

    redis_manager.sync_configs_to_redis()

    return "User configuration asynced successfully"
