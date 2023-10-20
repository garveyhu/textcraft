import pinecone 
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader

from textcraft.model.qwen.qwen_embedding import QwenEmbedding
from textcraft.config import Config

cfg = Config()
PINECONE_API_KEY = cfg.pinecone_api_key
PINECONE_ENV = cfg.pinecone_env

def store_document(document) -> Pinecone:
    print(f'document:{len(document)}')
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separator = "\n")
    docs = text_splitter.split_documents(document)
    print(f'split_documents:{len(docs)}')
    
    embeddings = QwenEmbedding()
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
    return docsearch

if __name__ == "__main__":
    loader = TextLoader('docs/zelda.txt', encoding='utf-8')
    document = loader.load()
    store_document(document)
    # query = "..."
    # docs = docsearch.similarity_search(query)
    # print(docs)