from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory

from textcraft.models.llms.llm_creator import LLMCreator
from textcraft.vectors.es.connection import get_es_connection_history


class ESMemory:
    """Elasticsearch作向量库操作，存储聊天历史（只存储作为上下文，不向量化）."""

    def __init__(self):
        self.history = get_es_connection_history()

    def summarize_memory(self, **kwargs):
        """`ConversationSummaryMemory` memory.
        对历史进行LLM总结，生成新的历史上下文

        Example:
            .. code-block:: python

                from langchain.chains import ConversationChain
                from textcraft.vectors.es.es_memory import ESMemory

                memory = ESMemory().summarize_memory()
                conversation_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
                result = conversation_chain.predict(input=text)

        Args:
            buffer: str = ""
            memory_key: str = "history"
        """
        memory = ConversationSummaryMemory.from_messages(
            llm=LLMCreator.create_llm(),
            chat_memory=self.history,
            return_messages=True,
            **kwargs,
        )
        return memory

    def buffer_window_memory(self, **kwargs):
        """`ConversationBufferWindowMemory` memory.
        对历史进行滑动窗口设置，生成窗口大小的历史上下文

        Example:
            .. code-block:: python

                from langchain.chains import ConversationChain
                from textcraft.vectors.es.es_memory import ESMemory

                memory = ESMemory().buffer_window_memory(k=3)
                conversation_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
                result = conversation_chain.predict(input=text)

        Args:
            human_prefix: str = "Human"
            ai_prefix: str = "AI"
            memory_key: str = "history"
            k: int = 5
        """

        memory = ConversationBufferWindowMemory(
            chat_memory=self.history, return_messages=True, **kwargs
        )
        return memory
