"""
   How to parse text from message objects  https://python.langchain.com/docs/how_to/output_parser_string/
"""

import os
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

response = llm.invoke("Hello")
response.content
print("response.content:", response.content)

from langchain_core.tools import tool
@tool
def get_weather(location: str) -> str:
    """Get the weather from a location."""

    return "Sunny."


llm_with_tools = llm.bind_tools([get_weather])

response = llm_with_tools.invoke("What's the weather in San Francisco, CA?")
result = response.content
print("result:", response)

# To automatically parse text from message objects irrespective of the format of the underlying content, we can use StrOutputParser. We can compose it with a chat model as follows:
from langchain_core.output_parsers import StrOutputParser
chain = llm_with_tools | StrOutputParser()

# StrOutputParser simplifies the extraction of text from message objects:
response = chain.invoke("What's the weather in San Francisco, CA?")
print(response)

for chunk in chain.stream("What's the weather in San Francisco, CA?"):
    print(chunk, end="|")

    