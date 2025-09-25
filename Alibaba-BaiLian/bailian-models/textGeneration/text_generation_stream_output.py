"""
    大模型服务平台-->百炼用户指南（模型）-->文本生成-->流式输出 : https://help.aliyun.com/zh/model-studio/stream?spm=a2c4g.11186623.help-menu-2400256.d_0_1_2.72b3453aId5el8
    在实时聊天或长文本生成应用中，长时间的等待会损害用户体验。请求处理时间过长也容易触发服务端超时，导致任务失败。流式输出通过持续返回模型生成的文本片段，解决了这两个核心问题。

    工作原理:
    流式输出基于 Server-Sent Events (SSE) 协议。发起流式请求后，服务端与客户端建立持久化 HTTP 连接。模型每生成一个文本块（称为 chunk），立即通过连接推送。全部内容生成后，服务端发送结束信号。
    客户端监听事件流，实时接收并处理文本块，例如逐字渲染界面。这与非流式调用（一次性返回所有内容）形成对比。    
"""

import os
from openai import OpenAI, APIError

# 1. 准备工作：初始化客户端
# 建议通过环境变量配置API Key，避免硬编码。
try:
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.environ["DASHSCOPE_API_KEY"],
        # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
except KeyError:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

# 2. 发起流式请求
try:
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请介绍一下自己"}
        ],
        stream=True,
        # 目的：在最后一个chunk中获取本次请求的Token用量。
        stream_options={"include_usage": True}
    )

    # 3. 处理流式响应
    # 使用列表推导式和join()是处理大量文本片段时最高效的方式。
    content_parts = []
    print("AI: ", end="", flush=True)
    
    for chunk in completion:
        # 最后一个chunk不包含choices，但包含usage信息。
        if chunk.choices:
            # 关键：delta.content可能为None，使用`or ""`避免拼接时出错。
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            content_parts.append(content)
        elif chunk.usage:
            # 请求结束，打印Token用量。
            print("\n--- 请求用量 ---")
            print(f"输入 Tokens: {chunk.usage.prompt_tokens}")
            print(f"输出 Tokens: {chunk.usage.completion_tokens}")
            print(f"总计 Tokens: {chunk.usage.total_tokens}")

    full_response = "".join(content_parts)
    # print(f"\n--- 完整回复 ---\n{full_response}")

except APIError as e:
    print(f"API 请求失败: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")
