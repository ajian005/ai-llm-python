"""
  How to track token usage in ChatModels : https://python.langchain.com/docs/how_to/chat_token_usage_tracking/
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
openai_response = llm.invoke("hello")
result = openai_response.usage_metadata
print(result)


aggregate = None
for chunk in llm.stream("hello", stream_usage=True):
    print(chunk)
    aggregate = chunk if aggregate is None else aggregate + chunk
print(aggregate.content)
print(aggregate.usage_metadata)


aggregate = None
for chunk in llm.stream("hello"):
    print(chunk)

from pydantic import BaseModel, Field
import asyncio


class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


# Under the hood, .with_structured_output binds tools to the
# chat model and appends a parser.
structured_llm = llm.with_structured_output(Joke)

async def process_astream_events():
    async for event in structured_llm.astream_events("Tell me a joke"):
      if event["event"] == "on_chat_model_end":
          print(f"Token usage: {event['data']['output'].usage_metadata}\n")
      elif event["event"] == "on_chain_end" and event["name"] == "RunnableSequence":
          print(event["data"]["output"])
      else:
          pass

asyncio.run(process_astream_events())


#  Tracking token usage through configuration
from langchain_core.callbacks import UsageMetadataCallbackHandler
callback = UsageMetadataCallbackHandler()
result_1 = llm.invoke("Hello", config={"callbacks": [callback]})
print("callback.usage_metadata",callback.usage_metadata)

from langchain_core.callbacks import get_usage_metadata_callback

with get_usage_metadata_callback() as cb:
    llm.invoke("Hello")
    print("cb.usage_metadata:\r\n", cb.usage_metadata)

from langgraph.prebuilt import create_react_agent


# Create a tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return "It's sunny."


#  %pip install -qU langgraph

callback = UsageMetadataCallbackHandler()

tools = [get_weather]
agent = create_react_agent("openai:gpt-4o-mini", tools)
for step in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in Boston?"}]},
    stream_mode="values",
    config={"callbacks": [callback]},
):
    step["messages"][-1].pretty_print()


print(f"\nTotal usage: {callback.usage_metadata}")    


from langgraph.prebuilt import create_react_agent

# Create a tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return "It's sunny."

callback = UsageMetadataCallbackHandler()

callback = UsageMetadataCallbackHandler()

tools = [get_weather]
agent = create_react_agent("openai:gpt-4o-mini", tools)
for step in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in Boston?"}]},
    stream_mode="values",
    config={"callbacks": [callback]},
):
    step["messages"][-1].pretty_print()


print(f"\nTotal usage: {callback.usage_metadata}")
