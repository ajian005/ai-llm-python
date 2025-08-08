"""
How to: init any model in one line : https://python.langchain.com/docs/how_to/chat_models_universal_init/

    There are three main methods for debugging:
    Verbose Mode: This adds print statements for "important" events in your chain.
    Debug Mode: This add logging statements for ALL events in your chain.
    LangSmith Tracing: This logs events to LangSmith to allow for visualization there.
"""
'''
Tracing
'''

import getpass
import os

#os.environ["LANGSMITH_TRACING"] = "true"
#os.environ["LANGSMITH_API_KEY"] = getpass.getpass()

import getpass
import os

# 获取 DMXAPI API 密钥
if not os.environ.get("DMXAPI_API_KEY"):
  os.environ["DMXAPI_API_KEY"] = getpass.getpass("Enter API key for DMXAPI: ")

# 获取 Tavily API 密钥
if not os.environ.get("TAVILY_API_KEY"):
  os.environ["TAVILY_API_KEY"] = getpass.getpass("Enter API key for Tavily: ")

from langchain.chat_models import init_chat_model

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)


from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch

tools = [TavilySearch(max_results=5, topic="general", tavily_api_key=os.environ["TAVILY_API_KEY"])]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke(
    {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
)

# set_verbose(True)
from langchain.globals import set_verbose

set_verbose(True)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke(
    {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
)


# set_debug(True)
from langchain.globals import set_debug

set_debug(True)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke(
    {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
)
