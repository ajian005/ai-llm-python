"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->深度思考 : https://help.aliyun.com/zh/model-studio/deep-thinking?spm=a2c4g.11186623.help-menu-2400256.d_0_1_3.5cc425c8XqPlrq&scm=20140722.H_2870973._.OR_help-T_cn~zh-V_1

开启/关闭思考模式
混合思考模型通过enable_thinking参数控制是否开启思考模式：

true：开启思考模式

false：关闭思考模式
"""

from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen-plus-2025-04-28",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    # enable_thinking 参数开启思考过程，qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
    extra_body={"enable_thinking": True},
    stream=True,
    # stream_options={
    #     "include_usage": True
    # },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content

