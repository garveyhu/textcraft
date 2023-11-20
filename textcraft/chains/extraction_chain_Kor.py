import json

from kor.extraction import create_extraction_chain
from kor.nodes import Number, Object, Text
from langchain.prompts import PromptTemplate

from textcraft.models.llms.llm_creator import LLMCreator
from textcraft.utils.complex import init_config_develop


class ExtractionChain:
    attributes: {}
    def extraction(self, text: str, schema: str, prompt: str):
        llm = LLMCreator.create_llm()
        schema2 = self.parsetext(schema, prompt)
        DEFAULT_INSTRUCTION_TEMPLATE = PromptTemplate(
            input_variables=["type_description", "format_instructions"],
            template=(
                f"{prompt}"
                "。"
                "您的目标是从输入中提取与下面描述的表单匹配的结构化信息,"
                "提取信息时，请确保它与类型信息完全匹配,"
                "不要添加任何未显示在下面显示的架构中的属性\n\n"
                "{type_description}\n\n"
                "{format_instructions}\n\n"
            ),
        )
        chain = create_extraction_chain(llm, schema2, encoder_or_encoder_class="JSON",
                                        instruction_template=DEFAULT_INSTRUCTION_TEMPLATE,
                                        input_formatter="triple_quotes")
        response = chain.run(text)["raw"]
        resultStr = json.dumps(response, ensure_ascii=False)
        resultStr = resultStr.replace("\\n", "")
        if "json{" in resultStr:
            resultStr = resultStr[(resultStr.index("json") + 4):(resultStr.index("}```") + 1)]
        if "<json>{" in resultStr:
            resultStr = resultStr[(resultStr.index("<json>{") + 6):(resultStr.index("}</json>") + 1)]
        for key, value in self.attributes.items():
            resultStr = resultStr.replace(value, key)
        return resultStr

    def parsetext(self, text: str, prompt: str):
        jsonobj = json.loads(text)
        self.attributes = jsonobj["attributes"]
        attributes2 = []
        for key, value in self.attributes.items():
            attributes2.append(
                Text(
                    id=value,
                    description=value
                ))
        # examples_text = jsonobj["examples"]["text"]
        # examples_result = jsonobj["examples"]["result"]
        schema2 = Object(
            id="Information",
            description=prompt,
            attributes=attributes2,
            # examples=[(
            #     examples_text,
            #     examples_result
            # )
            # ]
        )
        return schema2


if __name__ == "__main__":
    init_config_develop(dialog_id="2")
    inp = """[
                {
                    "text": {
                        "content": "您好，有什么可以帮助您的？"
                    },
                    "fromName": "陈江南"
                },
                {
                    "text": {
                        "content": "我要预约办理取款业务"
                    },
                    "fromName": "周意"
                },
                   {
                    "text": {
                        "content": "请问预约地点、时间、额度是多少呢？"
                    },
                    "fromName": "陈江南"
                },
                {
                    "text": {
                        "content": "时间是明天下午2点",
                    },
                    "fromName": "周意"
                },
                {
                    "text": {
                        "content": "取款20万",
                    },
                    "fromName": "周意"
                },
                {
                    "text": {
                        "content": "取款地点是彩虹支行"
                    },
                    "fromName": "周意"
                },
                      {
                    "text": {
                        "content": "请提供您的姓名、手机号、身份证号及住址"
                    },
                    "fromName": "陈江南"
                },
                {
                    "text": {
                        "content": "17681810472"
                    },
                    "fromName": "周意"
                },
                {
                    "text": {
                        "content": "331023198711111421"
                    },
                    "fromName": "周意"
                },
                {
                    "text": {
                        "content": "周意"
                    }
                    "fromName": "周意"
                },
                  {
                    "text": {
                        "content": "杭州市滨江区江南大道3000号"
                    }
                    "fromName": "周意"
                }
            ]"""
    schema = '{"attributes":{"001":"姓名","002":"手机号","003":"身份证号","004":"住址","005":"卡号"},"examples": {"text":" 客服:您好！有什么可以帮您? 客户:我要预约一下上门办卡业务, 客服:好的，请提供您的姓名、电话、身份证号、住址,  客户:韦小宝，17681810472，331024197812231512，622229292929123，杭州市滨江区江南大道3888号 客服:好的，已帮您预约","result":{"姓名":"韦小宝","手机号": "17681810472","身份证号":"331024197812231512","卡号":"622229292929123","住址": "杭州市滨江区江南大道3888号"}}}'

    # prompt = "Understand and summarize this conversation.and extracting customer information from customer service and customer conversations.and n the returned results, the name dictionary key is displayed as 789789789789789789, and the phone number dictionary key is displayed as 456456456456456456456456"
    prompt="以下是客服和客户的对话,请理解和总结这段对话并提取出客户的相关信息"
    chain = ExtractionChain()
    response = chain.extraction(inp, schema, prompt)
    print(response)
