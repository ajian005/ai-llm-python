"""
    Build a custom workflow : https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
    workflow下面: Add human-in-the-loop controls  https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/
    This tutorial builds on Add memory.
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
from langchain_core.tools import tool

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")

"""
  2. Compile the graph
"""
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

"""
  3. Visualize the graph (optional) ==========================
"""
import os
from IPython.display import Image, display
filePath = "LangGraph/GetStarted/LangGraph_BuildACustomWorkflow_003_AddHumanInTheLoopControls.png"
try:
    graph_image = graph.get_graph().draw_mermaid_png()
    # 相对路径设置：
    # 1. 保存到当前目录()：
    with open(filePath, "wb") as f:
        f.write(graph_image)
    print("图形已保存到当前目录下的 " + filePath + " 文件")
except FileNotFoundError as e:
    print(f"错误: 文件夹路径不存在，请确保 {os.path.dirname(filePath)} 目录已创建")
except PermissionError as e:
    print(f"错误: 没有权限写入文件 {filePath}")
except Exception as e:
    print(f"错误: 保存图形时发生异常: {str(e)}")

"""
  4. Prompt the chatbot 
"""
user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

"""
  5. Resume execution
"""
human_response = (
    "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
    " It's much more reliable and extensible than simple autonomous agents."
)

human_command = Command(resume={"data": human_response})
events = graph.stream(human_command, config, stream_mode="values")

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

"""
6.  Inspect the state
    snapshot = graph.get_state(config)
    print("snapshot:", snapshot)
    print("snapshot.next:", snapshot.next)
"""
