from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


class Summarizer:
    """ 
    总结器
    提炼文本标题
    """

    def __init__(self, llm):
        self.llm = llm
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.prompt_template = """为以下内容取标题，标题字数简短控制10字之内:\n{text}\n标题:"""
        self.PROMPT = PromptTemplate(
            template=self.prompt_template, input_variables=["text"]
        )

    def summarize_text(self, long_text):
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

    def summarize_file(self, file_obj):
        return self.summarize_text(file_obj.read())
