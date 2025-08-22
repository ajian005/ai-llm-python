"""
  How to create a custom Output Parser :  https://python.langchain.com/docs/how_to/output_parser_custom/
"""

""" ============================= Runnable Lambdas and Generators ============================= """
from typing import Iterable

# from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.messages import AIMessage, AIMessageChunk

# model = ChatAnthropic(model_name="claude-2.1")
from langchain.chat_models import init_chat_model
import os
# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)


def parse(ai_message: AIMessage) -> str:
    """Parse the AI message."""
    return ai_message.content.swapcase()


chain = llm | parse
result = chain.invoke("hello")
print(result)

print("==========================================================")

for chunk in chain.stream("tell me about yourself in one sentence"):
    print(chunk, end="|", flush=True)


from langchain_core.runnables import RunnableGenerator
def streaming_parse(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    for chunk in chunks:
        yield chunk.content.swapcase()
streaming_parse = RunnableGenerator(streaming_parse)

chain = model | streaming_parse
chain.invoke("hello")

for chunk in chain.stream("tell me about yourself in one sentence"):
    print(chunk, end="|", flush=True)

"======================= Inheriting from Parsing Base Classes ====================="
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser
import asyncio


# The [bool] desribes a parameterization of a generic.
# It's basically indicating what the return type of parse is
# in this case the return type is either True or False
class BooleanOutputParser(BaseOutputParser[bool]):
    """Custom boolean parser."""

    true_val: str = "YES"
    false_val: str = "NO"

    def parse(self, text: str) -> bool:
        cleaned_text = text.strip().upper()
        if cleaned_text not in (self.true_val.upper(), self.false_val.upper()):
            raise OutputParserException(
                f"BooleanOutputParser expected output value to either be "
                f"{self.true_val} or {self.false_val} (case-insensitive). "
                f"Received {cleaned_text}."
            )
        return cleaned_text == self.true_val.upper()

    @property
    def _type(self) -> str:
        return "boolean_output_parser"

parser = BooleanOutputParser()
parser.invoke("YES")

try:
    parser.invoke("MEOW")
except Exception as e:
    print(f"Triggered an exception of type: {type(e)}")

parser = BooleanOutputParser(true_val="OKAY")
parser.invoke("OKAY")

parser.batch(["OKAY", "NO"])

async def run_abatch():
    return await parser.abatch(["OKAY", "NO"])
result = asyncio.run(run_abatch())

from langchain_anthropic.chat_models import ChatAnthropic

anthropic = ChatAnthropic(model_name="claude-2.1")
anthropic.invoke("say OKAY or NO")

chain = anthropic | parser
chain.invoke("say OKAY or NO")

from typing import List

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import BaseGenerationOutputParser
from langchain_core.outputs import ChatGeneration, Generation


class StrInvertCase(BaseGenerationOutputParser[str]):
    """An example parser that inverts the case of the characters in the message.

    This is an example parse shown just for demonstration purposes and to keep
    the example as simple as possible.
    """

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> str:
        """Parse a list of model Generations into a specific format.

        Args:
            result: A list of Generations to be parsed. The Generations are assumed
                to be different candidate outputs for a single model input.
                Many parsers assume that only a single generation is passed it in.
                We will assert for that
            partial: Whether to allow partial results. This is used for parsers
                     that support streaming
        """
        if len(result) != 1:
            raise NotImplementedError(
                "This output parser can only be used with a single generation."
            )
        generation = result[0]
        if not isinstance(generation, ChatGeneration):
            # Say that this one only works with chat generations
            raise OutputParserException(
                "This output parser can only be used with a chat generation."
            )
        return generation.message.content.swapcase()


chain = anthropic | StrInvertCase()

chain.invoke("Tell me a short sentence about yourself")


