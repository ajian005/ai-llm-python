"""
    大模型服务平台-->百炼用户指南（模型）--> 工具调用 --> MCP : https://help.aliyun.com/zh/model-studio/mcp

 MCP
    模型上下文协议（Model Context Protocol, MCP）可帮助大模型使用外部工具与数据，相比 Function Calling，MCP 更灵活且易于使用。本文介绍通过阿里云百炼模型服务接入 MCP 的方法。

"""

import os
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

# LLM 配置
llm_cfg = {
    "model": "qwen-plus-latest",
    "model_server": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    "api_key": os.getenv("DASHSCOPE_API_KEY"),
}

# 系统消息
system = "你是会天气查询、地图查询、网页部署的助手"

# 工具列表
tools = [
    {
        "mcpServers": {
            "amap-maps": {
                "type": "sse",
                # 替换为您的 URL
                "url": "https://mcp.api-inference.modelscope.net/f03f60966fe148/sse",
            },
            "edgeone-pages-mcp": {
                "type": "sse",
                # 替换为您的 URL
                "url": "https://mcp.api-inference.modelscope.net/c9bd5615732542/sse",
            },
        }
    }
]

# 创建助手实例
bot = Assistant(
    llm=llm_cfg,
    name="助手",
    description="高德地图、天气查询、公网链接部署",
    system_message=system,
    function_list=tools,
)
WebUI(bot).run()

