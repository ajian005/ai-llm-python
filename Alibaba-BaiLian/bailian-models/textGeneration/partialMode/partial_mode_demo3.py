"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->指定前缀续写（Partial Mode） : https://help.aliyun.com/zh/model-studio/partial-mode?spm=a2c4g.11186623.help-menu-2400256.d_0_1_5.76925b77IIRUnj&scm=20140722.H_2862210._.OR_help-T_cn~zh-V_1

  指定前缀续写（Partial Mode）
     在代码补全、文本续写等场景中，需要模型从已有的文本片段（前缀）开始继续生成。Partial Mode 可提供精确控制能力，确保模型输出的内容紧密衔接提供的前缀，提升生成结果的准确性与可控性。

  基于不完整输出进行续写
    如果大模型返回不完整的内容，可使用 Partial Mode 对不完整的内容续写，使其语义完整。大模型可能返回不完整内容的情况：

    max_tokens参数设置过小，使模型返回被截断的内容。

    非流式输出触发超时，已生成的内容不完整。
"""

import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def chat_completion(messages,max_tokens=None):
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        max_tokens=max_tokens
    )
    print(f"###停止生成原因：{response.choices[0].finish_reason}")
    
    return response.choices[0].message.content

# 使用示例
messages = [{"role": "user", "content": "请写一个短篇科幻故事"}]

# 第一轮调用，设置max_tokens为40
first_content = chat_completion(messages, max_tokens=40)
print(first_content)
# 将第一轮的响应加入到assistant message，并设置partial=True
messages.append({"role": "assistant", "content": first_content, "partial": True})

# 第二轮调用
second_content = chat_completion(messages)
print("###完整内容：")
print(first_content+second_content)