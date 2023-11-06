from typing import Dict, List, Union

from langchain.tools import BaseTool

from textcraft.vectors.pinecone_store import store_paragraphs


class VectorStoreTool(BaseTool):
    name = "向量存储工具"
    description = "文档存储pinecone"
    paragraphs = []

    def _run(self, text: str, run_manager=None) -> str:
        return self.run_for_vector_store(self.paragraphs)

    async def _arun(
        self,
        text: str,
        run_manager=None,
    ) -> str:
        pass

    def run_for_vector_store(
        self, paragraphs: List[Dict[str, Union[str, Dict[str, str]]]]
    ):
        return store_paragraphs(paragraphs)
