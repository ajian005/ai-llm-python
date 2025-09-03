"""
    Build a custom workflow : https://langchain-ai.github.io/langgraph/concepts/why-langgraph/

    workflow下面: Build a basic chatbot https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#build-a-basic-chatbot
"""

'''
    1 Build a basic chatbot
'''
# 1. Install packages¶
# pip install -U langgraph langsmith

# 2. Create a StateGraph
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph = StateGraph(State)


# 3. Add a node
import os
from langchain.chat_models import init_chat_model

''' 
    os.environ["OPENAI_API_KEY"] = "sk-..."
    llm = init_chat_model("openai:gpt-4.1")
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


# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    temperature=0
)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder = StateGraph(State)


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

# 4. Add an entry point¶
graph_builder.add_edge(START, "chatbot")

# 5. Add an exit point
graph_builder.add_edge("chatbot", END)

# 6. Compile the graph
graph = graph_builder.compile()

# 7. Visualize the graph (optional)
from IPython.display import Image, display

filePath = "LangGraph/GetStarted/LangGraph_BuildACustomWorkflow_003.png"

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


# 8. Run the chatbot
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            logger.info("用户退出程序")
            print("Goodbye!")
            break
        logger.info(f"收到用户输入: {user_input}")
        stream_graph_updates(user_input)
    except EOFError:
        # 处理EOF错误（如Ctrl+D）
        logger.info("检测到EOF信号，程序退出")
        print("\nGoodbye!")
        break
    except KeyboardInterrupt:
        # 处理键盘中断（如Ctrl+C）
        logger.info("检测到键盘中断，程序退出")
        print("\n程序已中断")
        break
    except Exception as e:
        # 捕获其他所有异常并记录详细信息
        logger.exception(f"处理用户输入时发生错误: {str(e)}")
        # 提供fallback选项
        user_input = "What do you know about LangGraph?"
        logger.info(f"使用fallback输入: {user_input}")
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
