import json

import redis

from textcraft.core.settings import settings
from textcraft.utils.mongo_manager import MongoDBManager


class RedisManager:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
        )

    def sync_configs_to_redis(self):
        mongo_manager = MongoDBManager()
        all_config_data = mongo_manager.all_config()

        if all_config_data:
            for config_data in all_config_data:
                self.update_config(config_data)

    def update_config(self, config_data):
        user_id = config_data["user"]["id"]
        key = f"user:{user_id}"
        result = self.client.set(key, json.dumps(config_data))
        return result

    def delete_config(self, user_id):
        key = f"user:{user_id}"
        result = self.client.delete(key)
        return result

    def get_config(self, user_id):
        key = f"user:{user_id}"
        config_data = self.client.get(key)
        if config_data:
            return json.loads(config_data)
        else:
            return None

    def close_connection(self):
        self.client.connection_pool.disconnect()


if __name__ == "__main__":
    redis_manager = RedisManager()
    # redis_manager.sync_configs_to_redis()
    # print(redis_manager.get_config("030317"))
