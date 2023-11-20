from textcraft.core.user_config import get_config, set_config

"""用户、会话、应用"""


def user_id():
    """获取用户id"""
    return get_config("user.id")


def dialog_id():
    """获取会话id"""
    return get_config("dialog.id")


def dialog_model():
    """获取会话模型"""
    return get_config("dialog.model")


def app_id():
    """获取app id"""
    return get_config("app.id")


"""默认配置"""


def default_model():
    """获取默认模型名称"""
    return get_config("settings.config.default_chat")


def default_embedding():
    """获取默认模型嵌入"""
    return get_config("settings.config.default_embedding")


def default_vector():
    """获取默认向量库"""
    return get_config("settings.config.default_vector")


"""model配置"""


def chat_list():
    """获取chat模型列表"""
    return get_config("settings.models.chat")


def embedding_list():
    """获取embedding模型列表"""
    return get_config("settings.models.embedding")


def model_temperature():
    """获取默认模型温度"""
    list = chat_list()
    for chat in list:
        if chat["name"] == dialog_model():
            return float(chat["temperature"])
    return None


def keys_openai():
    """获取openai keys"""
    config = get_config("settings.models.keys.openai")
    return config["OPENAI_API_KEY"]


def keys_spark():
    """获取spark keys"""
    config = get_config("settings.models.keys.spark")
    return (config["SPARK_APPID"], config["SPARK_API_KEY"], config["SPARK_API_SECRET"])


def keys_qwen():
    """获取qwen keys"""
    config = get_config("settings.models.keys.qwen")
    return config["QWEN_API_KEY"]


def keys_ernie():
    """获取ernie keys"""
    config = get_config("settings.models.keys.ernie")
    return (config["ERNIE_API_KEY"], config["ERNIE_API_SECRET"])


"""memory配置"""


def vector_list():
    """获取向量库列表"""
    return get_config("settings.models.vector")


def keys_pinecone():
    """获取pinecone keys"""
    config = get_config("settings.memory.keys.pinecone")
    return (config["PINECONE_ENV"], config["PINECONE_API_KEY"])


"""修改配置"""


def set_dialog_model(model):
    """修改会话模型"""
    return set_config("dialog.model", model)


def set_model_temperature(temperature):
    """修改温度"""
    list = chat_list()
    for chat in list:
        if chat["name"] == dialog_model():
            chat["temperature"] = temperature
