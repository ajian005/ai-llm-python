"""
    大模型服务平台-->百炼用户指南（模型）-->文本生成-->领域模型-->数学能力（Qwen-Math） : https://help.aliyun.com/zh/model-studio/math-language-model

    阿里云百炼提供的 Qwen-Math 系列模型具备强大的数学推理和计算能力，模型提供详细的解题步骤，便于理解和验证。
"""

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"), # 请勿在代码中硬编码凭证，应始终使用环境变量或密钥管理服务
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-math-plus",
    messages=[{'role': 'user', 'content': 'Derive a universal solution for the quadratic equation $ Ax^2+Bx+C=0 $'}])
print(completion.choices[0].message.content)