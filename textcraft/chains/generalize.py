from langchain.schema.output_parser import StrOutputParser

from textcraft.models.llms.llm_creator import LLMCreator
from textcraft.prompts.generalize import GENERALIZATION_PROMPT


class Generalize():
    def question_generalize(self, text):
        llm = LLMCreator.create_llm()
        runnable = GENERALIZATION_PROMPT | llm | StrOutputParser()
        result = runnable.invoke({"input": text})
        return result

    