from langchain.tools import BaseTool

class VectorStoreTool(BaseTool):
    name = "向量存储工具"
    description = (
        "文档存储pinecone"
    )

    def _run(self, text: str, run_manager=None) -> str:
        return self.run_for_vector_store(text)
    
    async def _arun(
            self,
            text: str,
            run_manager=None,
    ) -> str:
        pass

    def run_for_vector_store(self, text):
        return None
