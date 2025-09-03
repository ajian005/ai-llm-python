"""
    Build a custom workflow : https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
    workflow下面: Add memory  https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/
    This tutorial builds on Add tools.
"""

import os
from langchain.chat_models import init_chat_model

import os
import getpass

try:
    # 尝试从环境变量获取API密钥
    tavily_api_key = os.environ.get("TAVILY_API_KEY")
    # 如果环境变量中没有，提示用户输入
    if not tavily_api_key:
        tavily_api_key = getpass.getpass("请输入您的Tavily API密钥: ")
    # 设置环境变量
    os.environ["TAVILY_API_KEY"] = tavily_api_key
except Exception as e:
    print(f"获取Tavily API密钥失败: {e}")
    exit(1)

import os
from langchain.chat_models import init_chat_model
# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    temperature=0
)
from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

"""
  3. Interact with your chatbot¶
"""
config = {"configurable": {"thread_id": "1"}}
user_input = "Hi there! My name is Will."

# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

"""
  4. Ask a follow up question
"""
user_input = "Remember my name?"

# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

# The only difference is we change the `thread_id` here to "2" instead of "1"
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    {"configurable": {"thread_id": "2"}},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()


"""
  5. Inspect the state
"""
snapshot = graph.get_state(config)
print("snapshot:", snapshot)
print("snapshot.next:", snapshot.next)

