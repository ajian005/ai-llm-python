"""
    LangGraph : https://langchain-ai.github.io/langgraph/
    LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents.
"""

'''
Install LangGraph:

  pip install -U langgraph
'''

'''
Then, create an agent using prebuilt components:
'''


from langchain.chat_models import init_chat_model
import os

# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

# pip install -qU "langchain[anthropic]" to call the model

from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    llm, #model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(result)