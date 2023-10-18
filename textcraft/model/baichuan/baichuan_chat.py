import requests
from typing import List
import logging
from typing import Optional, Mapping, Any
import json

import langchain
from langchain.llms.base import LLM
from langchain.cache import InMemoryCache

logging.basicConfig(level=logging.INFO)
langchain.llm_cache = InMemoryCache()
result_list = []

class Baichuan(LLM):
    """
    根据源码解析在通过LLMS包装的时候主要重构两个部分的代码
    _call 模型调用主要逻辑,输入问题，输出模型相应结果
    _identifying_params 返回模型描述信息，通常返回一个字典，字典中包括模型的主要参数
    """

    url = "http://172.16.0.112:8000/"  # spark官方模型提供api接口
    temperature = 0.5

    @property
    def _llm_type(self) -> str:
        return "baichuan"

    def _post(self, prompt):
        param_dict = {"prompt": prompt}
        response = requests.post(url=self.url, json=param_dict)
        content = ""
        if hasattr(response, "content"):
            content = response.content
        # result = json.loads(content.decode('utf-8'))
        print(json.loads(content.decode("utf-8")))
        return json.loads(content.decode("utf-8"))["response"]

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        content = self._post(prompt)
        return content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """
        Get the identifying parameters.
        """
        _param_dict = {"url": self.url}
        return _param_dict
