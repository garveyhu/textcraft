import pinecone
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone

from textcraft.config import Config
from textcraft.model.qwen.qwen_embedding import QwenEmbedding
from textcraft.model.spark.spark_chat import Spark

cfg = Config()


def vector_qa(question: str) -> str:
    PINECONE_API_KEY = cfg.pinecone_api_key
    PINECONE_ENV = cfg.pinecone_env

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    embeddings = QwenEmbedding()
    llm = Spark()
    docsearch = Pinecone.from_existing_index("langchain", embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    result = qa({"query": question})

    return result.get("result", "")


if __name__ == "__main__":
    print(vector_qa("..."))
