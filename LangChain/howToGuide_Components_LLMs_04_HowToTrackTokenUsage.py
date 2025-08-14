"""
   How to track token usage for LLMs  https://python.langchain.com/docs/how_to/llm_token_usage_tracking/
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

""" # Single call """
from langchain_community.callbacks import get_openai_callback
from langchain_openai import OpenAI

llm = OpenAI(model_name="gpt-3.5-turbo-instruct")

with get_openai_callback() as cb:
    result = llm.invoke("Tell me a joke")
    print(result)
    print("---")
print()

print(f"Total Tokens: {cb.total_tokens}")
print(f"Prompt Tokens: {cb.prompt_tokens}")
print(f"Completion Tokens: {cb.completion_tokens}")
print(f"Total Cost (USD): ${cb.total_cost}")

""" Multiple calls """
from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
template = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = template | llm

with get_openai_callback() as cb:
    response = chain.invoke({"topic": "birds"})
    print(response)
    response = chain.invoke({"topic": "fish"})
    print("--")
    print(response)

print()
print("---")
print(f"Total Tokens: {cb.total_tokens}")
print(f"Prompt Tokens: {cb.prompt_tokens}")
print(f"Completion Tokens: {cb.completion_tokens}")
print(f"Total Cost (USD): ${cb.total_cost}")

""" Streaming """
from langchain_community.callbacks import get_openai_callback
from langchain_openai import OpenAI

llm = OpenAI(model_name="gpt-3.5-turbo-instruct")

with get_openai_callback() as cb:
    for chunk in llm.stream("Tell me a joke"):
        print(chunk, end="", flush=True)
    print(result)
    print("---")
print()

print(f"Total Tokens: {cb.total_tokens}")
print(f"Prompt Tokens: {cb.prompt_tokens}")
print(f"Completion Tokens: {cb.completion_tokens}")
print(f"Total Cost (USD): ${cb.total_cost}")