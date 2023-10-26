from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

llm = OpenAI()
chat_model = ChatOpenAI()

llm.predict("hi!")
chat_model.predict("hi!")
print("done")
