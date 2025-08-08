"""
How to stream runnables https://python.langchain.com/docs/how_to/streaming/
"""

"""
  Using Stream
"""
'''
   LLMs and Chat Models
'''
import getpass 
import os

if not os.environ.get("DMXAPI_API_KEY"):
  os.environ["DMXAPI_API_KEY"] = getpass.getpass("Enter API key for DMXAPI: ")

from langchain.chat_models import init_chat_model
import asyncio

# model = init_chat_model("gpt-4o-mini", model_provider="openai")

model = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

# Let's start with the sync stream API:
chunks = []
for chunk in model.stream("what color is the sky?"):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)



# Alternatively, if you're working in an async environment, you may consider using the async astream API:
print("====   async stream ====")
chunks = []
async def stream_async():
    chunks = []
    async for chunk in model.astream("what color is the sky?"):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)

asyncio.run(stream_async())
print("====   async stream2 ====")

'''
    Chains
'''
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
chain  = prompt | model | parser

async def stream_async_chain():
    async for chunk in chain.astream({"topic": "parrot"}):
        print(chunk, end="|", flush=True)

asyncio.run(stream_async_chain())

print("====   async stream3 ====")
# Working with Input Streams
from langchain_core.output_parsers import JsonOutputParser

chain = (
    model | JsonOutputParser()
)  # Due to a bug in older versions of Langchain, JsonOutputParser did not stream results from some models
async def stream_async_json():
    async for text in chain.astream(
    "output a list of the countries france, spain and japan and their populations in JSON format. "
    'Use a dict with an outer key of "countries" which contains a list of countries. '
    "Each country should have the key `name` and `population`"):
        print(text, flush=True)

asyncio.run(stream_async_json())



from langchain_core.output_parsers import (
    JsonOutputParser,
)


# A function that operates on finalized inputs
# rather than on an input_stream
def _extract_country_names(inputs):
    """A function that does not operates on input streams and breaks streaming."""
    if not isinstance(inputs, dict):
        return ""

    if "countries" not in inputs:
        return ""

    countries = inputs["countries"]

    if not isinstance(countries, list):
        return ""

    country_names = [
        country.get("name") for country in countries if isinstance(country, dict)
    ]
    return country_names


chain = model | JsonOutputParser() | _extract_country_names

async def stream_async_country_names():
    async for text in chain.astream(
    "output a list of the countries france, spain and japan and their populations in JSON format. "
    'Use a dict with an outer key of "countries" which contains a list of countries. '
    "Each country should have the key `name` and `population`"):
        print(text, end="|", flush=True)
asyncio.run(stream_async_country_names())

# xxx yyy
from langchain_core.output_parsers import JsonOutputParser

async def _extract_country_names_streaming(input_stream):
    """A function that operates on input streams."""
    country_names_so_far = set()

    async for input in input_stream:
        if not isinstance(input, dict):
            continue

        if "countries" not in input:
            continue

        countries = input["countries"]

        if not isinstance(countries, list):
            continue

        for country in countries:
            name = country.get("name")
            if not name:
                continue
            if name not in country_names_so_far:
                yield name
                country_names_so_far.add(name)


chain = model | JsonOutputParser() | _extract_country_names_streaming

async def stream_async_country_names_streaming():
    async for text in chain.astream(
    "output a list of the countries france, spain and japan and their populations in JSON format. "
    'Use a dict with an outer key of "countries" which contains a list of countries. '
    "Each country should have the key `name` and `population`",):
        print(text, end="|", flush=True)
asyncio.run(stream_async_country_names_streaming())

"""
   Non-streaming components
"""
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
import asyncio

template = """Answer the question based only on the following context:
            {context}

            Question: {question}
            """
prompt = ChatPromptTemplate.from_template(template)

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho", "harrison likes spicy food"],
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

chunks = [chunk for chunk in retriever.stream("where did harrison work?")]
chunks

retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

for chunk in retrieval_chain.stream(
    "Where did harrison work? Write 3 made up sentences about this place."
):
    print(chunk, end="|", flush=True)


"""
    Using Stream Events
"""
'''
    Chat Model
'''
events = []
async def collect_events():
    events = []
    async for event in model.astream_events("hello"):
        events.append(event)
    return events
events = asyncio.run(collect_events())


'''
    Chain
'''


'''
    Propagating Callbacks
'''
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool


def reverse_word(word: str):
    return word[::-1]


reverse_word = RunnableLambda(reverse_word)


@tool
def bad_tool(word: str):
    """Custom tool that doesn't propagate callbacks."""
    return reverse_word.invoke(word)


async def print_events():
    async for event in bad_tool.astream_events("hello"):
        print(event)

asyncio.run(print_events())


@tool
def correct_tool(word: str, callbacks):
    """A tool that correctly propagates callbacks."""
    return reverse_word.invoke(word, {"callbacks": callbacks})


async def print_correct_tool_events():
    async for event in correct_tool.astream_events("hello"):
        print(event)

asyncio.run(print_correct_tool_events())

from langchain_core.runnables import RunnableLambda


async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


reverse_and_double = RunnableLambda(reverse_and_double)


async def print_reverse_and_double_events():
    await reverse_and_double.ainvoke("1234")
    async for event in reverse_and_double.astream_events("1234"):
        print(event)

asyncio.run(print_reverse_and_double_events())


from langchain_core.runnables import chain

@chain
async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


async def run_reverse_and_double():
    await reverse_and_double.ainvoke("1234")
    async for event in reverse_and_double.astream_events("1234"):
        print(event)

asyncio.run(run_reverse_and_double())


