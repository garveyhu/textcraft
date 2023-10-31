class Inventory:
    vector_store = ["pinecone", "faiss"]
    llm = [
        "gpt4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "qwen-turbo",
        "ernie",
        "spark",
        "baichuan",
    ]
    embeddings = ["openai-text-embedding-ada-002", "qwen-text-embedding-v1"]


inventory = Inventory()
