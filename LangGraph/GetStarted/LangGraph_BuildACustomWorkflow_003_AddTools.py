"""
    Build a custom workflow : https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
    workflow下面: Add tools : https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/
"""

'''
    Prerequisites
      An API key for the Tavily Search Engine
'''

'''
    1. Install the search engine
      pip install -U langchain-tavily
'''

'''
    2. Configure your environment
      Configure your environment with your search engine API key
'''
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

'''
    3. Define the tool
      Define the web search tool
'''
from langchain_tavily import TavilySearch

try:
    # 创建TavilySearch实例
    tool = TavilySearch(max_results=2)
    tools = [tool]
    
    # 使用工具进行搜索
    result = tool.invoke("What's a 'node' in LangGraph?")
    print("搜索结果:", result)
except Exception as e:
    print(f"使用Tavily搜索时出错: {e}")

'''
    4. Define the graph
      For the StateGraph you created in the first tutorial, add bind_tools on the LLM. 
'''
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
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Modification: tell the LLM which tools it can call
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

'''
    5. Create a function to run the tools
'''
import json
from langchain_core.messages import ToolMessage

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

tool_node = BasicToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

'''
    6. Define the conditional_edges
'''
def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


graph_builder.add_edge(START, "chatbot")
# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile()

'''
    7. Visualize the graph (optional)
'''
# 导入并配置日志模块
import logging

# 配置基本日志格式和级别
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[
        logging.FileHandler("langgraph_workflow.log"),  # 写入文件
        logging.StreamHandler()  # 输出到控制台
    ]
)

# 创建一个日志记录器
logger = logging.getLogger("LangGraphWorkflow")

import os
from IPython.display import Image, display
"""
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass
    """
filePath = "LangGraph/GetStarted/LangGraph_BuildACustomWorkflow_003_AddTools.png"

try:
    # display(Image(graph.get_graph().draw_mermaid_png()))
    graph_image = graph.get_graph().draw_mermaid_png()
    # 相对路径设置：
    # 1. 保存到当前目录()：
    with open(filePath, "wb") as f:
        f.write(graph_image)
    print("图形已保存到当前目录下的 " + filePath + " 文件")
    logger.info(f"图形已成功保存到文件: {filePath}")
except FileNotFoundError as e:
    logger.error(f"无法创建或访问文件: {filePath}，错误信息: {str(e)}")
    print(f"错误: 文件夹路径不存在，请确保 {os.path.dirname(filePath)} 目录已创建")
except PermissionError as e:
    logger.error(f"没有写入权限: {filePath}，错误信息: {str(e)}")
    print(f"错误: 没有权限写入文件 {filePath}")
except Exception as e:
    logger.exception(f"保存图形时发生未知错误: {str(e)}")
    print(f"错误: 保存图形时发生异常: {str(e)}")

'''
    8. Ask the bot questions
'''
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break


'''
    9. Use prebuilts
    https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#9-use-prebuilts
'''