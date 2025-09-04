"""
    Build a custom workflow : https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
    workflow下面: Time travel  https://langchain-ai.github.io/langgraph/tutorials/get-started/6-time-travel/
    This tutorial builds on Customize state.
"""

"""
    1. Rewind your graph
"""

import os
from langchain.chat_models import init_chat_model
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

from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
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
graph_builder.add_edge(START, "chatbot")

memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

"""
    2. Add steps
"""
config = {"configurable": {"thread_id": "1"}}
events = graph.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "I'm learning LangGraph. "
                    "Could you do some research on it for me?"
                ),
            },
        ],
    },
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()


events = graph.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Ya that's helpful. Maybe I'll "
                    "build an autonomous agent with it!"
                ),
            },
        ],
    },
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()



"""
    3. Replay the full state history
"""
to_replay = None
for state in graph.get_state_history(config):
    print("Num Messages: ", len(state.values["messages"]), "Next: ", state.next)
    print("-" * 80)
    if len(state.values["messages"]) == 6:
        # We are somewhat arbitrarily selecting a specific state based on the number of chat messages in the state.
        to_replay = state


print(to_replay.next)
print(to_replay.config)


"""
    4. Load a state from a moment-in-time
"""
# The `checkpoint_id` in the `to_replay.config` corresponds to a state we've persisted to our checkpointer.
for event in graph.stream(None, to_replay.config, stream_mode="values"):
    if "messages" in event:
        event["messages"][-1].pretty_print()
