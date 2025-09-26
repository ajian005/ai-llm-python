"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->指定前缀续写（Partial Mode） : https://help.aliyun.com/zh/model-studio/partial-mode?spm=a2c4g.11186623.help-menu-2400256.d_0_1_5.76925b77IIRUnj&scm=20140722.H_2862210._.OR_help-T_cn~zh-V_1

  指定前缀续写（Partial Mode）
     在代码补全、文本续写等场景中，需要模型从已有的文本片段（前缀）开始继续生成。Partial Mode 可提供精确控制能力，确保模型输出的内容紧密衔接提供的前缀，提升生成结果的准确性与可控性。

"""

import os
from openai import OpenAI

# 1. 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 定义需要补全的代码前缀
prefix = """def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
"""

# 3. 发起 Partial Mode 请求
# 注意：messages 数组的最后一条消息 role 为 "assistant"，并包含 "partial": True
completion = client.chat.completions.create(
    model="qwen3-coder-plus",
    messages=[
        {"role": "user", "content": "请补全这个斐波那契函数，勿添加其它内容"},
        {"role": "assistant", "content": prefix, "partial": True},
    ],
)

# 4. 手动拼接前缀和模型生成的内容
generated_code = completion.choices[0].message.content
complete_code = prefix + generated_code

print(complete_code)