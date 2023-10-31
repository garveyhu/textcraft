import pinecone
from langchain.chains import RetrievalQA
from langchain.vectorstores.pinecone import Pinecone

from textcraft.core.settings import settings
from textcraft.models.embeddings.embedding_creator import EmbeddingCreator
from textcraft.models.llms.spark import Spark


def vector_qa(question: str) -> str:
    PINECONE_API_KEY = settings.PINECONE_API_KEY
    PINECONE_ENV = settings.PINECONE_ENV

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    embeddings = EmbeddingCreator.create_embedding()
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
