
"""
 Deep Agent Quickstart   https://docs.langchain.com/oss/python/deepagents/quickstart#step-4%3A-create-a-deep-agent
"""

'''
Step 1: Install dependencies
    pip install deepagents tavily-python
'''

'''
Step 2: Set up your API keys
    export ANTHROPIC_API_KEY="your-api-key"
    export TAVILY_API_KEY="your-tavily-api-key"
'''

'''
Step 3: Create a search tool

'''
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

'''
Step 4: Create a deep agent

'''
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

import os
from langchain.chat_models import init_chat_model


# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)


agent = create_deep_agent(
    model=llm,
    tools=[internet_search],
    system_prompt=research_instructions
)


'''
Step 5: Run the agent



'''
result = agent.invoke({"messages": [{"role": "user", "content": "What is spring ai alibaba ?"}]})

# Print the agent's response
print(result["messages"][-1].content)