import json

import pymongo
from bson import json_util

from textcraft.core.settings import config_file, settings


class MongoDBManager:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB]
        self.collection = self.db[settings.MONGODB_COLLECTION]

    def insert_config(self, config_data):
        result = self.collection.insert_one(config_data)
        return result.inserted_id

    def update_config(self, config_data):
        app_id = config_data["app"]["id"]
        filter_query = {"app.id": app_id}
        update_data = {"$set": config_data}
        result = self.collection.update_one(filter_query, update_data)
        return result.modified_count

    def delete_config(self, app_id):
        filter_query = {"app.id": app_id}
        result = self.collection.delete_one(filter_query)
        return result.deleted_count

    def get_config(self, app_id):
        filter_query = {"app.id": app_id}
        config_data = json_util.loads(
            json_util.dumps(self.collection.find_one(filter_query))
        )
        if "_id" in config_data:
            del config_data["_id"]

        return config_data

    def all_config(self):
        all_config_data = list(self.collection.find())
        json_config_data = []

        if all_config_data:
            for config_data in all_config_data:
                if "_id" in config_data:
                    del config_data["_id"]
                json_config_data.append(json_util.loads(json_util.dumps(config_data)))

        return json_config_data

    def close_connection(self):
        self.client.close()

    def load_json(self):
        with open(config_file, "r") as file:
            config_data = json.load(file)
        return config_data


if __name__ == "__main__":
    collection = MongoDBManager()
    # print(collection.load_json())
    print(collection.insert_config(collection.load_json()))
    # print(collection.update_config(collection.load_json()))
    # print(collection.delete_config("030317"))
    # print(collection.get_config("030317"))
    # print(collection.all_config())
