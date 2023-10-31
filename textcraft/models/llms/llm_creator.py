from inspect import isclass

from textcraft.core.settings import settings
from textcraft.models.llms.baichuan import Baichuan
from textcraft.models.llms.ernie import Ernie
from textcraft.models.llms.openai import openai
from textcraft.models.llms.qwen import Qwen
from textcraft.models.llms.spark import Spark


class LLMCreator:
    llms = {
        "openai": openai,
        "qwen": Qwen,
        "spark": Spark,
        "ernie": Ernie,
        "baichuan": Baichuan,
    }

    @classmethod
    def create_llm(cls, llm_type=None, *args, **kwargs):
        if llm_type is None:
            llm_type = settings.DEFAULT_LLM

        llm_class = cls.llms.get(llm_type.lower())
        if not llm_class:
            raise ValueError(f"No LLM class found for type {llm_type}")

        if isclass(llm_class):
            return llm_class(*args, **kwargs)

        return llm_class
