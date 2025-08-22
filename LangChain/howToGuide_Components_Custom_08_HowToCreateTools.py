"""
  How to create tools :  https://python.langchain.com/docs/how_to/custom_tools/
"""

""" ============================= Creating tools from functions ============================= """
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)


from langchain_core.tools import tool


@tool
async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


from typing import Annotated, List


@tool
def multiply_by_max(
    a: Annotated[int, "scale factor"],
    b: Annotated[List[int], "list of ints over which to take maximum"],
) -> int:
    """Multiply a by the maximum of b."""
    return a * max(b)


print(multiply_by_max.args_schema.model_json_schema())



from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)


@tool(parse_docstring=True)
def foo(bar: str, baz: int) -> str:
    """The foo.

    Args:
        bar: The bar.
        baz: The baz.
    """
    return bar


print(foo.args_schema.model_json_schema())


from langchain_core.tools import StructuredTool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

print(calculator.invoke({"a": 2, "b": 3}))
# print(await calculator.ainvoke({"a": 2, "b": 5}))

class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

print(calculator.invoke({"a": 2, "b": 3}))
print(calculator.name)
print(calculator.description)
print(calculator.args)

""" ============================= Creating tools from Runnables ============================= """
from langchain_core.language_models import GenericFakeChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [("human", "Hello. Please respond in the style of {answer_style}.")]
)

# Placeholder LLM
llm = GenericFakeChatModel(messages=iter(["hello matey"]))

chain = prompt | llm | StrOutputParser()

as_tool = chain.as_tool(
    name="Style responder", description="Description of when to use tool."
)
as_tool.args

""" ============================= Subclass BaseTool ============================= """
from typing import Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


# Note: It's important that every field has type hints. BaseTool is a
# Pydantic class and not having type hints can lead to unexpected behavior.
class CustomCalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "useful for when you need to answer questions about math"
    args_schema: Optional[ArgsSchema] = CalculatorInput
    return_direct: bool = True

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> int:
        """Use the tool."""
        return a * b

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> int:
        """Use the tool asynchronously."""
        # If the calculation is cheap, you can just delegate to the sync implementation
        # as shown below.
        # If the sync calculation is expensive, you should delete the entire _arun method.
        # LangChain will automatically provide a better implementation that will
        # kick off the task in a thread to make sure it doesn't block other async code.
        return self._run(a, b, run_manager=run_manager.get_sync())

multiply = CustomCalculatorTool()
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)

print(multiply.invoke({"a": 2, "b": 3}))
# print(await multiply.ainvoke({"a": 2, "b": 3}))


""" ============================= How to create async tools ============================= """
from langchain_core.tools import StructuredTool
import asyncio

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

calculator = StructuredTool.from_function(func=multiply)

print(calculator.invoke({"a": 2, "b": 3}))
print(
print(asyncio.run(calculator.ainvoke({"a": 2, "b": 5})))
)  # Uses default LangChain async implementation incurs small overhead

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

print(calculator.invoke({"a": 2, "b": 3}))

print(asyncio.run(calculator.ainvoke({"a": 2, "b": 5})))
  # Uses default LangChain async implementation incurs small overhead

@tool
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

try:
    multiply.invoke({"a": 2, "b": 3})
except NotImplementedError:
    print("Raised not implemented error. You should not be doing this.")

""" ============================= Handling Tool Errors ============================= """
from langchain_core.tools import ToolException


def get_weather(city: str) -> int:
    """Get weather for the given city."""
    raise ToolException(f"Error: There is no city by the name of {city}.")


get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_errors=True,
)
get_weather_tool.invoke({"city": "foobar"})


get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_errors="There is no such city, but it's probably above 0K there!",
)

get_weather_tool.invoke({"city": "foobar"})


def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_errors=_handle_error,
)

get_weather_tool.invoke({"city": "foobar"})


""" ============================= HReturning artifacts of Tool execution ============================= """
import random
from typing import List, Tuple

from langchain_core.tools import tool


@tool(response_format="content_and_artifact")
def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
    """Generate size random ints in the range [min, max]."""
    array = [random.randint(min, max) for _ in range(size)]
    content = f"Successfully generated array of {size} random ints in [{min}, {max}]."
    return content, array

generate_random_ints.invoke({"min": 0, "max": 9, "size": 10})

generate_random_ints.invoke(
    {
        "name": "generate_random_ints",
        "args": {"min": 0, "max": 9, "size": 10},
        "id": "123",  # required
        "type": "tool_call",  # required
    }
)


from langchain_core.tools import BaseTool


class GenerateRandomFloats(BaseTool):
    name: str = "generate_random_floats"
    description: str = "Generate size random floats in the range [min, max]."
    response_format: str = "content_and_artifact"

    ndigits: int = 2

    def _run(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
        range_ = max - min
        array = [
            round(min + (range_ * random.random()), ndigits=self.ndigits)
            for _ in range(size)
        ]
        content = f"Generated {size} floats in [{min}, {max}], rounded to {self.ndigits} decimals."
        return content, array

    # Optionally define an equivalent async method

    # async def _arun(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
    #     ...


rand_gen = GenerateRandomFloats(ndigits=4)
rand_gen.invoke(
    {
        "name": "generate_random_floats",
        "args": {"min": 0.1, "max": 3.3333, "size": 3},
        "id": "123",
        "type": "tool_call",
    } )

