from textcraft.core.user_config import get_config
from textcraft.models.llms.baichuan import Baichuan
from textcraft.models.llms.ernie import Ernie
from textcraft.models.llms.openai import OpenAI
from textcraft.models.llms.qwen import Qwen
from textcraft.models.llms.spark import Spark


class LLMCreator:
    llms = {
        "openai": OpenAI,
        "qwen": Qwen,
        "spark": Spark,
        "ernie": Ernie,
        "baichuan": Baichuan,
    }

    @classmethod
    def create_llm(cls, llm_type=None, **kwargs):
        if llm_type is None:
            llm_type = get_config("settings.config.DEFAULT_LLM")
        llm_class = cls.llms.get(llm_type.lower())
        if not llm_class:
            raise ValueError(f"No LLM class found for type {llm_type}")

        if llm_class == OpenAI:
            return OpenAI(
                openai_api_key=get_config("settings.models.OPENAI_API_KEY"),
                temperature=float(get_config("settings.config.TEMPERATURE")),
            )

        return llm_class(**kwargs)
