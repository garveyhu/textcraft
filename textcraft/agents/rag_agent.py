from langchain import hub
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description

from textcraft.models.llms.llm_creator import LLMCreator
from textcraft.utils.complex import init_config_develop
from textcraft.vectors.es.connection import get_es_connection_resource
from textcraft.vectors.es.es_memory import ESMemory

class RAGAgent:
    def rag_chat(self, text: str):
        db = get_es_connection_resource()
        retriever = db.as_retriever()
        memory = ESMemory().buffer_window_memory(k=5, memory_key= "chat_history")

        tool = create_retriever_tool(
            retriever,
            "search_files_uploaded_by_users",
            "Searches and returns documents from files uploaded by users.",
        )
        tools = [tool]


        prompt = hub.pull("hwchase17/react-chat")

        prompt = prompt.partial(
            tools=render_text_description(tools),
            tool_names=", ".join([t.name for t in tools]),
        )
        
        llm = LLMCreator.create_llm()
        
        llm_with_stop = llm.bind(stop=["\nObservation"])
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
                "chat_history": lambda x: x["chat_history"],
            }
            | prompt
            | llm_with_stop
            | ReActSingleInputOutputParser()
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)

        # agent_executor = initialize_agent(
        #     tools,
        #     llm.bind(stop=["Observation"]),
        #     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        #     verbose=True,
        #     memory=memory,
        # )

        return agent_executor.invoke({"input": text})["output"]

if __name__ == "__main__":
    init_config_develop(dialog_id="0")
    rag_agent = RAGAgent()

    while True:
        try:
            user_input = input("请输入您的问题：")
            response = rag_agent.rag_chat(user_input)
            print(response)
        except KeyboardInterrupt:
            break
