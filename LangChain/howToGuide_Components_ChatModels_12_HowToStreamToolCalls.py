"""
  How to stream tool calls : https://python.langchain.com/docs/how_to/tool_streaming/
"""

from langchain_core.tools import tool
import getpass
import os

from langchain.chat_models import init_chat_model
import asyncio

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

tools = [add, multiply]
llm_with_tools = llm.bind_tools(tools)
query = "What is 3 * 12? Also, what is 11 + 49?"

async def main2():
    async for chunk in llm_with_tools.astream(query):
      print(chunk.tool_call_chunks)
 
asyncio.run(main2())


async def astream():
    first = True
    async for chunk in llm_with_tools.astream(query):
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk

    print(gathered.tool_call_chunks)
    print(type(gathered.tool_call_chunks[0]["args"]))

asyncio.run(astream())


async def astream2():
  first = True
  async for chunk in llm_with_tools.astream(query):
      if first:
          gathered = chunk
          first = False
      else:
          gathered = gathered + chunk
      print(gathered.tool_calls)
      print(type(gathered.tool_calls[0]["args"]))

asyncio.run(astream2())

