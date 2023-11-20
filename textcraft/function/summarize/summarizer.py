from typing import List
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import CharacterTextSplitter
from textcraft.vectors.es.es_store import ESStore

from textcraft.api.schema.chats import ChatList
from textcraft.prompts.summarize import (
    SUMMARIZE_TEXT_PROMPT,
    SUMMARIZE_CONVERSATION_PROMPT,
)
from textcraft.models.llms.llm_creator import LLMCreator
from textcraft.utils.convert_util import chatlist_to_chats, chats_to_chat_str


class Summarizer:
    """
    总结器
    提炼文本标题
    """

    def __init__(self):
        self.llm = LLMCreator.create_llm()
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.prompt_template = """为以下内容取标题，标题字数简短控制10字之内:\n{text}\n标题:"""
        self.PROMPT = PromptTemplate(
            template=self.prompt_template, input_variables=["text"]
        )

    def summarize_text(self, text: str):
        llm = LLMCreator.create_llm()
        runnable = SUMMARIZE_TEXT_PROMPT | llm | StrOutputParser()
        result = runnable.invoke({"text": text})
        return result

    def summarize_conversation(self, chats: List[dict]):
        chats_text = chats_to_chat_str(chats)
        llm = LLMCreator.create_llm()
        runnable = SUMMARIZE_CONVERSATION_PROMPT | llm | StrOutputParser()
        result = runnable.invoke({"conversation_text": chats_text})
        return result

    def summarize_conversation_chatlist(self, chats: ChatList):
        result = self.summarize_conversation(chatlist_to_chats(chats))
        return result

    def summarize_conversation_dialog_shot(self, size):
        chatting_records = ESStore().search_show(size)
        result = self.summarize_conversation(chatting_records)
        return result

    def summarize_text_map_reduce(self, long_text):
        texts = self.text_splitter.split_text(long_text)
        docs = [Document(page_content=t) for t in texts[:3]]
        chain = load_summarize_chain(
            self.llm,
            chain_type="map_reduce",
            return_intermediate_steps=True,
            map_prompt=self.PROMPT,
            combine_prompt=self.PROMPT,
        )
        result = chain({"input_documents": docs}, return_only_outputs=True)
        output_text = result.get("output_text", "")
        return output_text.strip("\n")
