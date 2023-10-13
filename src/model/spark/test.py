# 导入LLM包装器
from langchain import OpenAI, ConversationChain
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# 初始化包装器，temperature越高结果越随机
llm = OpenAI(temperature=0.9)
# 进行调用
text = "What would be a good company name for a company that makes colorful socks?"
print("input text: ", text)
print(llm(text))

prompt = PromptTemplate(
input_variables=["product"],
template="What is a good name for a company that makes {product}?",
)
print("input text: product")
print(prompt.format(product="colorful socks"))

chain = LLMChain(llm=llm, prompt=prompt)
chain.run("colorful socks")

# 导入一些tools，比如llm-math
# llm-math是langchain里面的能做数学计算的模块
tools = load_tools(["llm-math"], llm=llm)
# 初始化tools，models 和使用的agent
agent = initialize_agent(tools,
 llm,
 agent="zero-shot-react-description",
 verbose=True)
text = "12 raised to the 3 power and result raised to 2 power?"
print("input text: ", text)
agent.run(text)

# ConversationChain用法
llm = OpenAI(temperature=0)
# 将verbose设置为True，以便我们可以看到提示
conversation = ConversationChain(llm=llm, verbose=True)
print("input text: conversation")
conversation.predict(input="Hi there!")
conversation.predict(
input="I'm doing well! Just having a conversation with an AI.")
