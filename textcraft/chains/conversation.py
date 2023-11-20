import textwrap
import time
from operator import itemgetter

from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

from textcraft.models.llms.llm_creator import LLMCreator, get_llm
from textcraft.prompts.complex import HISTORY_PROMPT
from textcraft.utils.complex import init_config_develop
from textcraft.vectors.es.es_memory import ESMemory


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


class Conversation:
    def chat_with_memory(self, text):
        llm = LLMCreator.create_llm()
        memory = ESMemory().buffer_window_memory(k=5)
        conversation_chain = ConversationChain(
            llm=llm, prompt=HISTORY_PROMPT, memory=memory
        )
        result = conversation_chain.invoke({"input": text})["response"]
        return result

    def chat_without_memory(self, text):
        llm = LLMCreator.create_llm()
        runnable = llm | StrOutputParser()
        result = runnable.invoke(text)
        return result


def test_general_chat_chain():
    input_store = {
        "input": RunnablePassthrough(),
    }
    chain = input_store | StrOutputParser()
    return chain


def general_chat_chain():
    memory = ESMemory().buffer_window_memory(k=3)
    input_store = {
        "input": itemgetter("input"),
    }
    loaded_memory = {
        "input": itemgetter("input"),
        "test": lambda x: print(x),
        "history": RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
    }
    standalone_question = HISTORY_PROMPT | get_llm() | StrOutputParser()
    output_store = {"output": itemgetter("standalone_question")}
    store_memory = RunnableLambda(memory.save_context(input_store, output_store))

    final_chain = (
        input_store | loaded_memory | standalone_question | output_store | store_memory
    )

    return final_chain


if __name__ == "__main__":
    init_config_develop(dialog_id="3")
    chat = Conversation()

    while True:
        try:
            user_input = input("请输入您的问题：")
            # response = general_chat_chain().invoke({"input": user_input})
            # response = test_general_chat_chain().invoke({"input": user_input})
            response = chat.chat_without_memory(user_input)
            output_response(response)
        except KeyboardInterrupt:
            break
