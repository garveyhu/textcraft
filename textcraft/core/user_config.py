import threading


class UserConfig:
    def __init__(self, data=None):
        if data is None:
            self.data = {}
        else:
            self.data = data

    def __getitem__(self, key):
        return self.get(key)

    def get_config(self, key):
        keys = key.split(".")
        result = self.data
        for k in keys:
            result = result.get(k, {})
        return result

    def __setitem__(self, key, value):
        self.set(key, value)

    def set_config(self, key, value):
        keys = key.split(".")
        current = self.data
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value

    def to_dict(self):
        return self.data


settings = threading.local()
settings.config = UserConfig()


def set_config(key, value):
    settings.config.set_config(key, value)


def get_config(key):
    return settings.config.get_config(key)


def get_config_dict():
    return settings.config.data


def init_config(data):
    settings.config = UserConfig(data)
