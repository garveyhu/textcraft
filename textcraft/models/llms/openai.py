from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.llms.openai import OpenAI

set_llm_cache(InMemoryCache())
