from langchain import VectorDBQA, OpenAI
from model.spark.SparkChat import Spark
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
embeddings = OpenAIEmbeddings()
llm = Spark()
# llm = OpenAI(temperature=0.5)
docsearch = Pinecone.from_existing_index("langchain", embeddings)
qa = VectorDBQA.from_chain_type(
    llm=llm, chain_type="stuff", vectorstore=docsearch, return_source_documents=True
)
# 进行问答
result = qa({"query": "这篇文章的作者是谁"})
print(result.get("result", ""))
