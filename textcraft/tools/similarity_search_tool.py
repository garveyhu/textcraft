import pinecone
from langchain.tools import BaseTool
from langchain.vectorstores import Pinecone

from textcraft.model.qwen.qwen_embedding import QwenEmbedding
from textcraft.config import Config

cfg = Config()
PINECONE_API_KEY = cfg.pinecone_api_key
PINECONE_ENV = cfg.pinecone_env
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
embeddings = QwenEmbedding()

class SimilaritySearchTool(BaseTool):
    name = "向量存储工具"
    description = (
        "文档存储pinecone"
    )

    def _run(self, text: str, run_manager=None) -> str:
        return self.run_for_similarity_search(text)
    
    async def _arun(
            self,
            text: str,
            run_manager=None,
    ) -> str:
        pass

    def run_for_similarity_search(self, text):
        docsearch = Pinecone.from_existing_index("langchain", embeddings)
        docs = docsearch.similarity_search_with_score(text, 2)
        return docs