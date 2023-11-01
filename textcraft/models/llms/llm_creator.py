from textcraft.core.settings import settings
from textcraft.models.llms.baichuan import get_baichuan
from textcraft.models.llms.ernie import get_ernie
from textcraft.models.llms.openai import get_openai
from textcraft.models.llms.qwen import get_qwen
from textcraft.models.llms.spark import get_spark


class LLMCreator:
    @classmethod
    def create_llm(cls, llm_type=None):
        llms = {
            "openai": get_openai(),
            "qwen": get_qwen(),
            "spark": get_spark(),
            "ernie": get_ernie(),
            "baichuan": get_baichuan(),
        }
        if llm_type is None:
            llm_type = settings.DEFAULT_LLM

        llm_class = llms.get(llm_type.lower())
        if not llm_class:
            raise ValueError(f"No LLM class found for type {llm_type}")

        return llm_class
