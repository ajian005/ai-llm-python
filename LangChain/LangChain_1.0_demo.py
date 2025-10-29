"""
    LangChain overview  https://docs.langchain.com/oss/python/langchain/overview
"""

# pip install -qU "langchain[anthropic]" to call the model

# pip install -qU "langchain[anthropic]" to call the model

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import os

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
out = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
print(out)
