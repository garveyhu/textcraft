from langchain.chains import RetrievalQA
from model.spark.SparkChat import Spark
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os

def vector_qa(question: str) -> str:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    embeddings = OpenAIEmbeddings()
    llm = Spark()
    # llm = OpenAI(temperature=0.5)
    docsearch = Pinecone.from_existing_index("langchain", embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True
    )
    # 进行问答
    result = qa({"query": question})
    return result.get("result", "")

if __name__ == "__main__":
    print(vector_qa("..."))