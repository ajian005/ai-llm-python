"""
   How to cache LLM responses  https://python.langchain.com/docs/how_to/llm_caching/
"""

import os
from langchain.chat_models import init_chat_model
from langchain_core.globals import set_llm_cache

llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

from langchain_core.caches import InMemoryCache

set_llm_cache(InMemoryCache())

# The first time, it is not yet in cache, so it should take longer
response = llm.invoke("Tell me a joke")
# print(response)

""" SQLite Cache """
# We can do the same thing with a SQLite cache
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# The first time, it is not yet in cache, so it should take longer
response2 = llm.invoke("Tell me a joke2")
print(response2)