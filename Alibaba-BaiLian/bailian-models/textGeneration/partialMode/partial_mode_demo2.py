"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->指定前缀续写（Partial Mode） : https://help.aliyun.com/zh/model-studio/partial-mode?spm=a2c4g.11186623.help-menu-2400256.d_0_1_5.76925b77IIRUnj&scm=20140722.H_2862210._.OR_help-T_cn~zh-V_1

  指定前缀续写（Partial Mode）
     在代码补全、文本续写等场景中，需要模型从已有的文本片段（前缀）开始继续生成。Partial Mode 可提供精确控制能力，确保模型输出的内容紧密衔接提供的前缀，提升生成结果的准确性与可控性。

  传入图片或视频
    qwen-vl-max系列与qwen-vl-plus系列模型支持在输入图像、视频数据时进行前缀续写，可应用于产品介绍、社交媒体内容创作、新闻稿生成、创意文案等场景
"""

import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-vl-max",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
                    },
                },
                {"type": "text", "text": "我要发社交媒体，请帮我想一下文案。"},
            ],
        },
        {
            "role": "assistant",
            "content": "今天发现了一家宝藏咖啡馆",
            "partial": True,
        },
    ],
)
print(completion.choices[0].message.content)