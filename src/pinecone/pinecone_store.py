from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone 
from langchain.document_loaders import TextLoader
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

loader = TextLoader('docs/back.txt', encoding='utf-8')
documents = loader.load()
print(f'documents:{len(documents)}')
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separator = "\n")
docs = text_splitter.split_documents(documents)
print(f'documents:{len(docs)}')
 
embeddings = OpenAIEmbeddings()
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

index_name = "langchain"
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(
#         name=index_name,
#         dimension=1536,
#         metric='cosine'
#     )

# openAi将内容转成向量之后的长度是1536
docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

query = "我最不能忘记的是他的背影"
docs = docsearch.similarity_search(query)
print(docs)