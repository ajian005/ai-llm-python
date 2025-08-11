"""
  How to use chat models to call tools : https://python.langchain.com/docs/how_to/tool_calling/
"""

"""
Defining tool schemas
"""
''' Python functions'''
# The function name, type hints, and docstring are all part of the tool
# schema that's passed to the model. Defining good, descriptive schemas
# is an extension of prompt engineering and is an important part of
# getting models to perform well.
def add(a: int, b: int) -> int:
    """Add two integers.
    Args:
        a: First integer
        b: Second integer
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two integers.
    Args:
        a: First integer
        b: Second integer
    """
    return a * b

''' LangChain Tool'''




''' TypedDict class'''
from typing_extensions import Annotated, TypedDict


class add2(TypedDict):
    """Add two integers."""

    # Annotations must have the type and can optionally include a default value and description (in that order).
    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]


class multiply2(TypedDict):
    """Multiply two integers."""

    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]


tools = [add2, multiply2]


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

llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12?"

llm_with_tools.invoke(query)

query = "What is 3 * 12? Also, what is 11 + 49?"

# Tool calls
result = llm_with_tools.invoke(query).tool_calls

# Parsing
from langchain_core.output_parsers import PydanticToolsParser
chain = llm_with_tools | PydanticToolsParser(tools=[add2, multiply2])
result = chain.invoke(query)
print("result=", result)
