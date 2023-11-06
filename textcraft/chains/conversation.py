import textwrap
import time

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

from textcraft.models.llms.llm_creator import LLMCreator

memory = ConversationBufferWindowMemory(k=3)


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
    def chatForText(self, text):
        llm = LLMCreator.create_llm()
        conversation = ConversationChain(llm=llm, verbose=True, memory=memory)
        result = conversation.run(text)
        return result


if __name__ == "__main__":
    chat = Conversation()

    while True:
        try:
            user_input = input("请输入您的问题：")
            response = chat.chatForText(user_input)
            output_response(response)
        except KeyboardInterrupt:
            break
