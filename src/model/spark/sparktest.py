import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import ssl
import websocket
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
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import LLMChain
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory

# We'll make a temporary directory to avoid clutter
working_directory = TemporaryDirectory()

logging.basicConfig(level=logging.INFO)
# 启动llm的缓存
langchain.llm_cache = InMemoryCache()
result_list = []
shell_tool = ShellTool()

def _construct_query(prompt, temperature, max_tokens):
    data = {
        "header": {
            "app_id": SPARK_APPID,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": "generalv2",
                "random_threshold": temperature,
                "max_tokens": max_tokens,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "user", "content": prompt}
                ]
            }
        }
    }
    return data


def _run(ws, *args):
    data = json.dumps(
        _construct_query(prompt=ws.question, temperature=ws.temperature, max_tokens=ws.max_tokens))
    print (data)
    ws.send(data)


def on_error(ws, error):
    print("error:", error)


def on_close(ws):
    print("closed...")


def on_open(ws):
    thread.start_new_thread(_run, (ws,))


def on_message(ws, message):
    data = json.loads(message)
    print('====data=====')
    print(data)
    code = data['header']['code']
    # print(data)
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        result_list.append(content)
        if status == 2:
            ws.close()
            setattr(ws, "content", "".join(result_list))
            print('====result_list=====')
            print(result_list)
            result_list.clear()


class Spark(LLM):
    '''
    根据源码解析在通过LLMS包装的时候主要重构两个部分的代码
    _call 模型调用主要逻辑,输入问题，输出模型相应结果
    _identifying_params 返回模型描述信息，通常返回一个字典，字典中包括模型的主要参数
    '''

    gpt_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # spark官方模型提供api接口
    host = urlparse(gpt_url).netloc  # host目标机器解析
    path = urlparse(gpt_url).path  # 路径目标解析
    max_tokens = 1024
    temperature = 0.5

    # ws = websocket.WebSocketApp(url='')

    @property
    def _llm_type(self) -> str:
        # 模型简介
        return "Spark"

    def _get_url(self):
        # 获取请求路径
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        signature_sha = hmac.new(SPARK_API_SECRET.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{SPARK_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.gpt_url + '?' + urlencode(v)
        return url

    def _post(self, prompt):
        # 模型请求响应
        websocket.enableTrace(False)
        wsUrl = self._get_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error,
                                    on_close=on_close, on_open=on_open)
        ws.question = prompt
        setattr(ws, "temperature", self.temperature)
        setattr(ws, "max_tokens", self.max_tokens)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return ws.content if hasattr(ws, "content") else ""

    def _call(self, prompt: str,
              stop: Optional[List[str]] = None) -> str:
        # 启动关键的函数
        content = self._post(prompt)
        print('======content======')
        print(content)
        # content = "这是一个测试"
        return content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """
        Get the identifying parameters.
        """
        _param_dict = {
            "url": self.gpt_url
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
    llm = Spark(temperature=0.9)
    tools = load_tools(["llm-math", "wikipedia", "human"], llm=llm)
    prefix = """Have a conversation with a human, answering the following questions as best you can. 
              You have access to the following tools:"""
    suffix = """Begin!"
    {chat_history}
    Question: {input}
    {agent_scratchpad}"""
    prompt = ZeroShotAgent.create_prompt(
     tools=tools,
     prefix=prefix,
     suffix=suffix,
     input_variables=["input", "chat_history", "agent_scratchpad"]
    )
    memory = ConversationBufferMemory(memory_key="chat_history")
    output_parser = CustomOutputParser()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True, output_parser=output_parser)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory,handle_parsing_errors=True)


    # shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace("{", "{{").replace("}", "}}")
    # toolsfile = FileManagementToolkit(root_dir=str(working_directory.name),
    #                               selected_tools=["read_file", "write_file", "list_directory"]).get_tools()

    # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #                          handle_parsing_errors=True,verbose=True)
    # print(agent.agent.llm_chain.prompt.template)
    # print(SPARK_APPID)
    # data =json.dumps(llm._construct_query(prompt="你好啊", temperature=llm.temperature, max_tokens=llm.max_tokens))
    # print (data)
    # print (type(data))
    # result = llm("13除以3等于几？精确到小数点后两位", stop=["you"])
    agent_chain.run(input="富春山居图的作者是谁?")
    # print(result)

    # print(shell_tool.run({"commands": ["curl -s https://langchain.com | grep -o 'http[s]*://[^\" ]*' | sort"]}))
# read_tool, write_tool, list_tool = toolsfile
# write_tool.run({"file_path": "example.txt", "text": "Hello World!"})
# list_tool.run({})

# while (1):
#     Input = input("\n" + "我:")
#     agent_chain.run(input=Input)
