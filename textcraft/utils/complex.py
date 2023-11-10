from textcraft.core.user_config import init_config
from textcraft.utils.redis_manager import RedisManager


def init_config_develop(user_id="0", app_id="0", dialog_id="0"):
    """开发环境下初始化配置""" ""
    redis_manager = RedisManager()
    dic_data = redis_manager.get_config(app_id)
    dic_data.setdefault("user", {}).update({"id": user_id})
    dic_data.setdefault("dialog", {}).update({"id": dialog_id})

    init_config(dic_data)
