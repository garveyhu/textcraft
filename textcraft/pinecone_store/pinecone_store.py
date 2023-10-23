from typing import List, Dict, Union
    
import pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader

from textcraft.model.qwen.qwen_embedding import QwenEmbedding
from textcraft.config import Config

cfg = Config()
PINECONE_API_KEY = cfg.pinecone_api_key
PINECONE_ENV = cfg.pinecone_env
embeddings = QwenEmbedding()
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)


def store_document(document) -> Pinecone:
    print(f"document:{len(document)}")
    text_splitter = CharacterTextSplitter(
        chunk_size=2000, chunk_overlap=0, separator="\n"
    )
    docs = text_splitter.split_documents(document)
    print(f"split_documents:{len(docs)}")

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

def store_paragraphs(paragraphs: List[Dict[str, Union[str, Dict[str, str]]]]) -> Pinecone:
    input_docs = [Document(page_content=paragraph['page_content'], metadata=paragraph['metadata']) for paragraph in paragraphs]

    text_splitter = CharacterTextSplitter(
        chunk_size=2000, chunk_overlap=0, separator="\n"
    )
    docs = text_splitter.split_documents(input_docs)

    index_name = "langchain"

    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    return docsearch

def similarity_search(query):
    docsearch = Pinecone.from_existing_index("langchain", embeddings)
    docs = docsearch.similarity_search_with_score(query, 2)
    return docs_json(docs)

def docs_json(data):
    json_data = []

    for item in data:
        doc, score = item
        doc_dict = {
            "page_content": doc.page_content,
            "metadata": doc.metadata,
            "score": score
        }
        json_data.append(doc_dict)
        
    return json_data

if __name__ == "__main__":
#     docsearch = store_text("""背影·朱自清
# 我与父亲不相见已二年余了，我最不能忘记的是他的背影。
# """, name="Alice", age=30, city="New York")
    loader = TextLoader("docs/yxzx.txt", encoding="utf-8")
    document = loader.load()
    store_document(document)
#     embeddings = QwenEmbedding()
#     pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
#     docsearch = Pinecone.from_existing_index("langchain", embeddings)
#     query = """近几年来，父亲和我都是东奔西走，家中光景是一日不如一日。他少年出外谋生，独力支持，做了许多大事。哪知老境却如此颓唐！他触目伤怀，自然情不能自已。情郁于中，自然要发之于
# 外；家庭琐屑便往往触他之怒。他待我渐渐不同往日。但最近两年的不见，他终于忘却我的不好，只是惦记着我，惦记着我的儿子。我北来后，他写了一信给我，信中说道：“我身体平安，惟膀子疼痛厉害，举箸提笔， 诸多不便，大约大去之期不远矣。”我读到此处，在晶莹的泪光中，又看见那肥胖的、青布棉袍黑布马褂的背影。唉！我不知何时再能与他相见！"""
#     # docs = docsearch
#     # docs = docsearch.similarity_search_with_relevance_scores(query)
#     docs = docsearch.similarity_search_with_score(query, 2)
#     print(docs_json(docs))
