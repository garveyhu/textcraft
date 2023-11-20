from typing import Any

from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain.schema.output_parser import T

from textcraft.chains.MExtraction import create_extraction_chain
from textcraft.models.llms.llm_creator import LLMCreator


class ExtractionChain:
    def extraction(self, text: str, schema: str, prompt: str):
        llm = LLMCreator.create_llm()
        prompts = PromptTemplate(template=prompt, input_variables=["input"])
        chain = create_extraction_chain(schema, llm, prompts, CustomerOutparser())
        response = chain.run(text)
        return response


class CustomerOutparser(BaseOutputParser[Any]):
    def parse(self, text: str) -> T:
        text1 = text.replace("\n", "")
        print("======>" + text1)
        text3 = text1.split("```")
        print(text3[1])
        text2 = text3[1][4:]
        print("====2==>" + text2)
        return text2
