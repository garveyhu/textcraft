import pinecone
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from textcraft.model.spark.spark_chat import Spark
from textcraft.config import Config

cfg = Config()

def vector_qa(question: str) -> str:
    PINECONE_API_KEY = cfg.pinecone_api_key
    PINECONE_ENV = cfg.pinecone_env

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    embeddings = OpenAIEmbeddings()
    llm = Spark()
    # llm = OpenAI(temperature=0.5)
    docsearch = Pinecone.from_existing_index("langchain", embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True
    )
    result = qa({"query": question})
    
    return result.get("result", "")

if __name__ == "__main__":
    print(vector_qa("..."))