from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.llms.openai import OpenAI

from textcraft.core.settings import settings

set_llm_cache(InMemoryCache())
openai_api_key = settings.OPENAI_API_KEY
openai = OpenAI(openai_api_key=openai_api_key)
