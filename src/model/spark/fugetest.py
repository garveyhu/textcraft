
import re
from typing import List, Union
import textwrap
import time

from langchain.agents import (
    Tool,
    AgentExecutor,
    LLMSingleActionAgent,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import PromptTemplate

from langchain.llms.base import BaseLLM
from SparkChat import Spark
from SydBCChat import SydBaichuan
CONTEXT_QA_TMPL = """
根据以下提供的信息，回答用户的问题
信息：{context}

问题：{query}
"""
CONTEXT_QA_PROMPT = PromptTemplate(
    input_variables=["query", "context"],
    template=CONTEXT_QA_TMPL,
)


def output_response(response: str) -> None:
    if not response:
        exit(0)
    for line in textwrap.wrap(response, width=60):
        for word in line.split():
            for char in word:
                print(char, end="", flush=True)
                time.sleep(0.1)  # Add a delay of 0.1 seconds between each character
            print(" ", end="", flush=True)  # Add a space between each word
        print()  # Move to the next line after each line is printed
    print("----------------------------------------------------------------")


class FugeDataSource:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def find_product_description(self, product_name: str) -> str:
        """模拟公司产品的数据库"""
        product_info = {
            "好快活": "好快活是一个营销人才平台，以社群+公众号+小程序结合的运营模式展开，帮助企业客户连接并匹配充满才华的营销人才。",
            "Rimix": """Rimix通过采购流程数字化、完备的项目数据存储记录及标准的供应商管理体系，帮助企业实现采购流程, 透明合规可追溯，大幅节约采购成本。Rimix已为包括联合利华，滴滴出行等多家广告主提供服务，平均可为客户节约采购成本30%。""",
            "Bid Agent": "Bid Agent是一款专为中国市场设计的搜索引擎优化管理工具，支持5大搜索引擎。Bid Agent平均为广告主提升18%的投放效果，同时平均提升47%的管理效率。目前已为阳狮广告、GroupM等知名4A公司提供服务与支持。",
        }
        return product_info.get(product_name, "没有找到这个产品")

    def find_company_info(self, query: str) -> str:
        """模拟公司介绍文档数据库，让llm根据抓取信息回答问题"""
        context = """
        关于产品："让广告技术美而温暖"是复歌的产品理念。在努力为企业客户创造价值的同时，也希望让使用复歌产品的每个人都能感受到技术的温度。
        我们关注用户的体验和建议，我们期待我们的产品能够给每个使用者的工作和生活带来正面的改变。
        我们崇尚技术，用科技的力量使工作变得简单，使生活变得更加美好而优雅，是我们的愿景。
        企业文化：复歌是一个非常年轻的团队，公司大部分成员是90后。
        工作上，专业、注重细节、拥抱创新、快速试错。
        协作中，开放、坦诚、包容、还有一点点举重若轻的幽默感。
        以上这些都是复歌团队的重要特质。
        在复歌，每个人可以平等地表达自己的观点和意见，每个人的想法和意愿都会被尊重。
        如果你有理想，并拥有被理想所驱使的自我驱动力，我们期待你的加入。
        """
        prompt = CONTEXT_QA_PROMPT.format(query=query, context=context)
        return self.llm(prompt)


AGENT_TMPL = """按照给定的格式回答以下问题。你可以使用下面这些工具：

{tools}

回答时需要遵循以下用---括起来的格式：

---
Question: 我需要回答的问题
Thought: 回答这个上述我需要做些什么
Action: ”{tool_names}“ 中的其中一个工具名
Action Input: 选择工具所需要的输入
Observation: 选择工具返回的结果
...（这个思考/行动/行动输入/观察可以重复N次）
Thought: 我现在知道最终答案
Final Answer: 原始输入问题的最终答案
---

现在开始回答，记得在给出最终答案前多按照指定格式进行一步一步的推理。

Question: {input}
{agent_scratchpad}
"""


class CustomPromptTemplate(StringPromptTemplate):
    template: str  # 标准模板
    tools: List[Tool]  # 可使用工具集合

    def format(self, **kwargs) -> str:
        """
        按照定义的 template，将需要的值都填写进去。

        Returns:
            str: 填充好后的 template。
        """
        intermediate_steps = kwargs.pop("intermediate_steps")  # 取出中间步骤并进行执行
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts  # 记录下当前想法
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )  # 枚举所有可使用的工具名+工具描述
        kwargs["tool_names"] = ", ".join(
            [tool.name for tool in self.tools]
        )  # 枚举所有的工具名称
        cur_prompt = self.template.format(**kwargs)
        print(cur_prompt)
        return cur_prompt


class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        """
        解析 llm 的输出，根据输出文本找到需要执行的决策。

        Args:
            llm_output (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            Union[AgentAction, AgentFinish]: _description_
        """
        if "Final Answer:" in llm_output:  # 如果句子中包含 Final Answer 则代表已经完成
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )

        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"  # 解析 action_input 和 action
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)

        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )


if __name__ == "__main__":
    ## set api token in terminal
    llm = SydBaichuan(temperature=0.9)

    fuge_data_source = FugeDataSource(llm)
    tools = [
        Tool(
            name="查询产品名称",
            func=fuge_data_source.find_product_description,
            description="通过产品名称找到产品描述时用的工具，输入应该是产品名称",
        ),
        Tool(
            name="复歌科技公司相关信息",
            func=fuge_data_source.find_company_info,
            description="当用户询问公司相关的问题，可以通过这个工具了解相关信息",
        ),
    ]
    agent_prompt = CustomPromptTemplate(
        template=AGENT_TMPL,
        tools=tools,
        input_variables=["input", "intermediate_steps"],
    )
    output_parser = CustomOutputParser()

    llm_chain = LLMChain(llm=llm, prompt=agent_prompt)

    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names,
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )

    while True:
        try:
            user_input = input("请输入您的问题：")
            response = agent_executor.run(user_input)
            output_response(response)
        except KeyboardInterrupt:
            break