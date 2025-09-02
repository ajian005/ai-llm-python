"""
    Start with a prebuilt agent : https://langchain-ai.github.io/langgraph/agents/agents/
"""

''' 
 Prerequisites
 需要大模型的API Key , 如: An Anthropic API key
'''

''' 
  1. Install dependencies
  If you haven't already, install LangGraph and LangChain:
    pip install langgraph langchain
    pip install -U langgraph "langchain[anthropic]"
'''

'''
  2. Create an agent
  To create an agent, use create_react_agent
'''

from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
import os

# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    temperature=0
)

def get_weather(city : str) -> str :
    """ Get the weather for a city """
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    llm,
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

'''
   3. Configure an LLM
   To configure an LLM with specific parameters, such as temperature, use init_chat_model:
'''  
from langchain.chat_models import init_chat_model
from langgraph.prebuilt    import create_react_agent

'''
    llm = init_chat_model(
        "anthropic:claude-3-7-sonnet-latest",
        temperature=0
    )
'''

from langchain.chat_models import init_chat_model
import os



agent = create_react_agent(
    llm,
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

''' 
4. Add a custom prompt

'''
'''
        Prompts : Static: A string is interpreted as a system message.
'''
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    llm,
    tools=[get_weather],
    # A static prompt that never changes
    prompt="Never answer questions about the weather."
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

'''
        Prompts : Dynamic: A list of messages generated at runtime, based on input or configuration.
'''
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:  
    user_name = config["configurable"].get("user_name")
    system_msg = f"You are a helpful assistant. Address the user as {user_name}."
    return [{"role": "system", "content": system_msg}] + state["messages"]

agent = create_react_agent(
    llm,
    tools=[get_weather],
    prompt=prompt
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
      config={"configurable": {"user_name": "John Smith"}}
)


''' 
5. Add memory
'''
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_react_agent(
    llm,
    tools=[get_weather],
    checkpointer=checkpointer  
)

# Run the agent
config = {"configurable": {"thread_id": "1"}}
sf_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config  
)
ny_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what about new york?"}]},
    config
)


''' 
6. Configure structured output¶
'''

from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent

class WeatherResponse(BaseModel):
    conditions: str

agent = create_react_agent(
    llm,
    tools=[get_weather],
    response_format=WeatherResponse  
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(response["structured_response"])