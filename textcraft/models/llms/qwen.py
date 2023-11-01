from http import HTTPStatus
from typing import Any, List, Optional

import dashscope
from dashscope import Generation
from langchain.cache import InMemoryCache
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.globals import set_llm_cache
from langchain.llms.base import LLM

from textcraft.core.settings import settings

set_llm_cache(InMemoryCache())


class Qwen(LLM):
    @property
    def _llm_type(self) -> str:
        return "Qwen"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        temperature=settings.TEMPERATURE
        content = self._call_prompt(prompt, temperature=temperature)
        return content

    def _call_prompt(self, prompt, **kwargs: Any):
        dashscope.api_key = settings.QWEN_API_KEY
        # print("====_call_prompt====" + prompt)
        response = Generation.call(model="qwen-turbo", prompt=prompt, **kwargs)
        if response.status_code == HTTPStatus.OK:
            # print(response)
            if hasattr(response, "output"):
                output = response.output
                return output["text"]
        else:
            return (
                "Request id: %s, Status code: %s, error code: %s, error message: %s"
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                )
            )
     
def get_qwen():
    return Qwen()       
