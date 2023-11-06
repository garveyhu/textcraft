from tkinter import Text
from typing import Any

from git import Object
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

from MExtraction import create_extraction_chain

from testdemo.AliTyqwChat import TongYiQianWen
from testdemo.BDWxyyChat import WenXinYiYan
from testdemo.SparkChat import Spark
from langchain.schema.output_parser import T
llm = WenXinYiYan(temperature=0.9)

# # Schema
# schema = {
#     "properties": {
#         "name": {"type": "string"},
#         "height": {"type": "integer"},
#         "hair_color": {"type": "string"},
#     },
#     "required": ["name", "height"],
# }
# # Input
# inp = """Alex is 5 feet tall. Claudia is 1 feet taller Alex and jumps higher than him. Claudia is a brunette and Alex is blonde."""
 #
schema = {
     "properties":{
         "name":{"type":"string"},
         "ID":{"type":"string"},
         "Phone":{"type":"string"},
         "Business": {"type": "string"},
         "Time": {"type": "string"},
         "Location": {"type": "string"}
     },
     "required": ["name", "ID","Phone","Business","Time","Location"],
}
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
                    "content": "请提供您的姓名、手机号、身份证号"
                },
                "fromName": "陈江南"
            },
            {
                "text": {
                    "content": "我的手机号是17681810472"
                },
                "fromName": "周意"
            },
            {
                "text": {
                    "content": "身份证号是331023198711111421"
                },
                "fromName": "周意"
            },
            {
                "text": {
                    "content": "名字叫周意"
                }
                "fromName": "周意"
            }
        ]"""
_EXTRACTION_TEMPLATE = """Here is a conversation between customer service and the customer,only extract the customer's information and save the relevant entities mentioned above\
in the following passage together with their properties.

Only extract the properties mentioned in the 'information_extraction' function.and output in json format

If a property is not present and is not required in the function parameters, do not include it in the output.

Passage:
{input}
"""
promots= PromptTemplate(
    template=_EXTRACTION_TEMPLATE,
    input_variables=["input"]
)
class CustomerOutparser(BaseOutputParser[Any]):

    def parse(self, text: str) -> T:
        text1 = text.replace('\n', '')
        print("======>" + text1)
        text2 = text1[text1.index("json") + 4: text1.index("}]```") + 1]
        print("====2==>" + text2)
        return text2

chain = create_extraction_chain(schema, llm,promots, CustomerOutparser())

response=chain.run(inp)
print(response)