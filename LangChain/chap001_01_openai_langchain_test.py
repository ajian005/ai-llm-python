import getpass
import os

# 设置 DashScope API Key
if not os.environ.get("DMXAPI_API_KEY"):
    os.environ["DMXAPI_API_KEY"] = getpass.getpass("Enter API key for DMXAPI_API_KEY: ")

# 导入阿里云模型模块
from langchain.chat_models import init_chat_model

# 初始化 Qwen-Plus 模型
llm = init_chat_model(
    model="qwen-plus", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

# 示例：调用模型生成响应
from langchain_core.messages import HumanMessage

response = llm.invoke([HumanMessage(content="你好，Qwen Plus！")])
print(response.content)