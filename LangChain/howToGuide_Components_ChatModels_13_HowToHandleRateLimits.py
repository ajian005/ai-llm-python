"""
  How to handle rate limits : https://python.langchain.com/docs/how_to/chat_model_rate_limiting/
"""

""" Initialize a rate limiter """
from langchain_core.rate_limiters import InMemoryRateLimiter
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

""" Choose a model """
import os
import time


from langchain.chat_models import init_chat_model
import asyncio

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    rate_limiter=rate_limiter, 
)


for _ in range(5):
    tic = time.time()
    llm.invoke("hello")
    toc = time.time()
    print(toc - tic)