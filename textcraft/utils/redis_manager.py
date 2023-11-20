import json

import redis

from textcraft.core.settings import settings


class RedisManager:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
        )

    def sync_configs_to_redis(self):
        pass

    def update_config(self, config_data):
        app_id = config_data["app"]["id"]
        key = f"app:{app_id}"
        result = self.client.set(key, json.dumps(config_data))
        return result

    def update_model_temperature(self, app_id, model_name, temperature):
        key = f"app:{app_id}"
        print(f"update model temperature: {key} {model_name} {temperature}")
        config_data = self.client.get(key)
        if config_data:
            config_data = json.loads(config_data)
            for chat in config_data["settings"]["models"]["chat"]:
                if chat["name"] == model_name:
                    chat["temperature"] = temperature
                    break
            result = self.update_config(config_data)
            return result
        else:
            return None

    def update_dialog_model(self, dialog_id, model):
        key = f"dialog:{dialog_id}"
        print(f"update dialog model: {key} {model}")
        result = self.client.set(key, model)
        return result

    def delete_config(self, app_id):
        key = f"app:{app_id}"
        result = self.client.delete(key)
        return result

    def get_config(self, app_id):
        key = f"app:{app_id}"
        config_data = self.client.get(key)
        if config_data:
            return json.loads(config_data)
        else:
            return None

    def get_dialog_model(self, dialog_id):
        key = f"dialog:{dialog_id}"
        model = self.client.get(key)
        if model:
            return model.decode()
        else:
            return None

    def close_connection(self):
        self.client.connection_pool.disconnect()


if __name__ == "__main__":
    redis_manager = RedisManager()
    redis_manager.sync_configs_to_redis()
    # print(redis_manager.get_config(0))
