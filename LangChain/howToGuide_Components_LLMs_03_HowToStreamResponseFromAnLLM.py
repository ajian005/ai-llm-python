"""
   How to stream responses from an LLM  https://python.langchain.com/docs/how_to/streaming_llm/
"""

import os
from langchain.chat_models import init_chat_model
from langchain_core.globals import set_llm_cache
import asyncio

llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  
    temperature=0, max_tokens=512,  # 使用 OpenAI 模型提供者)
)

# Sync stream 
for chunk in llm.stream("Write me a 1 verse song about sparkling water."):
    print(chunk, end="|", flush=True)

# Async streaming
async def async_stream():
    async for chunk in llm.astream("Write me a 1 verse song about sparkling water."):
        print(chunk, end="|", flush=True)
asyncio.run(async_stream())

# Async event streaming
async def async_stream_events():
    idx = 0
    async for event in llm.astream_events(
        "Write me a 1 verse song about goldfish on the moon", version="v1"
    ):
        idx += 1
        if idx >= 5:  # Truncate the output
            print("...Truncated")
            break
        print(event)
asyncio.run(async_stream_events())