import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import ssl
import requests
import langchain
import logging
from myconfig import SPARK_APPID, SPARK_API_KEY, SPARK_API_SECRET
from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from typing import Optional, List, Dict, Mapping, Any
from langchain.llms.base import LLM
from langchain.cache import InMemoryCache
from langchain.agents import load_tools,AgentOutputParser
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import ShellTool
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re

logging.basicConfig(level=logging.INFO)
# 启动llm的缓存
langchain.llm_cache = InMemoryCache()
result_list = []
shell_tool = ShellTool()

class SydBaichuan(LLM):
    '''
    根据源码解析在通过LLMS包装的时候主要重构两个部分的代码
    _call 模型调用主要逻辑,输入问题，输出模型相应结果
    _identifying_params 返回模型描述信息，通常返回一个字典，字典中包括模型的主要参数
    '''

    url = "http://172.16.0.112:8000/"  # spark官方模型提供api接口
    temperature = 0.5

    # ws = websocket.WebSocketApp(url='')

    @property
    def _llm_type(self) -> str:
        # 模型简介
        return "SydBaichuan"

    def _post(self, prompt):

        param_dict = {
            'prompt':  prompt
        }
        response = requests.post(url=self.url, json=param_dict)
        content = ""
        if hasattr(response, "content"):
            content = response.content
        # result = json.loads(content.decode('utf-8'))
        print( "---=--->"+ content.decode('utf-8'))
        return content

    def _call(self, prompt: str,
              stop: Optional[List[str]] = None) -> str:
        # 启动关键的函数
        content = self._post(prompt)
        # content = "这是一个测试"
        return content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """
        Get the identifying parameters.
        """
        _param_dict = {
            "url": self.url
        }
        return _param_dict


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


if __name__ == "__main__":
    llm = SydBaichuan(temperature=0.9)
    tools = load_tools(["llm-math","wikipedia"], llm=llm)
    output_parser = CustomOutputParser()
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                             handle_parsing_errors=True,verbose=True,output_parser=output_parser)
    print(agent.agent.llm_chain.prompt.template)
    # print(SPARK_APPID)
    # data =json.dumps(llm._construct_query(prompt="你好啊", temperature=llm.temperature, max_tokens=llm.max_tokens))
    # print (data)
    # print (type(data))
    # result = llm("13除以3等于几？精确到小数点后两位", stop=["you"])
    agent.run("13除以3等于几？精确到小数点后两位")
    # print(result)
