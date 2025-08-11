"""
  How to return structured data from a model : https://python.langchain.com/docs/how_to/structured_output/
"""

import getpass
import os

from langchain.chat_models import init_chat_model

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

from langchain_core.globals import set_llm_cache  

# In Memory Cache
# %%time
from langchain_core.caches import InMemoryCache

set_llm_cache(InMemoryCache())

# The first time, it is not yet in cache, so it should take longer
result = llm.invoke("Tell me a joke")
print(result.content)

"""  SQLite Cache """
# !rm .langchain.db

# We can do the same thing with a SQLite cache
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# %%time
# The first time, it is not yet in cache, so it should take longer
llm.invoke("Tell me a joke")

# %%time
# The second time it is, so it goes faster
result2 = llm.invoke("Tell me a joke")
print(result2.content)


