"""
  How to stream chat model responses : https://python.langchain.com/docs/how_to/chat_streaming/
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import asyncio

llm = ChatOpenAI(
    model="qwen-plus",     # model="yi-large",
    temperature=0.3,
    max_tokens=200,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1").bind(logprobs=True)

# Sync streaming    
for chunk in llm.stream("Write me a 1 verse song about goldfish on the moon"):
    print(chunk.content, end="|", flush=True)

# Async Streaming
async def async_stream():
    async for chunk in llm.astream("Write me a 1 verse song about goldfish on the moon"):
        print(chunk.content, end="|", flush=True)


# Astream events        
async def async_stream_events():
    global idx
    idx = 0
    async for event in chat.astream_events(
    "Write me a 1 verse song about goldfish on the moon"):
        idx += 1
        if idx >= 5:  # Truncate the output
            print("...Truncated")
            break
        print(event)