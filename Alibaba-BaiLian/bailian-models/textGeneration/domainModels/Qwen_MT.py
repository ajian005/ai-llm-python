"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->领域模型-->翻译能力（Qwen-MT） : https://help.aliyun.com/zh/model-studio/machine-translation?spm=a2c4g.11186623.help-menu-2400256.d_0_1_6_2.5893535d3KiivA

  Qwen-MT模型是基于Qwen3模型优化的机器翻译大语言模型，支持92个语种（包括中、英、日、韩、法、西、德、泰、印尼、越、阿等）互译，且提供了术语干预、领域提示、记忆库等能力，提升模型在复杂应用场景下的翻译效果。

工作方式
    传入待翻译内容：messages 数组中有且仅有一个 role 为 user 的消息，其 content 为待翻译文本。
    设置语种：参考支持的语言，在 translation_options 中设置源语种 (source_lang) 和目标语种 (target_lang)。若需自动检测源语种，可将 source_lang 设为 auto。
    指明源语种有利于提升翻译准确率。
    Qwen-MT 模型也支持通过自定义提示词设置语种。  
"""


import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def call_translation():
    """ 翻译为英文的简单场景 """
    messages = [
        {
            "role": "user",
            "content": "我看到这个视频后没有笑"
        }
    ]
    translation_options = {
        "source_lang": "auto",
        "target_lang": "English"
    }

    completion = client.chat.completions.create(
        model="qwen-mt-turbo",
        messages=messages,
        extra_body={
            "translation_options": translation_options
        }
    )
    print(completion.choices[0].message.content)

def call_translation_stream():
    """ 翻译为英文的简单场景 流式输出 """

    messages = [{"role": "user", "content": "我看到这个视频后没有笑"}]
    translation_options = {"source_lang": "Chinese", "target_lang": "English"}

    completion = client.chat.completions.create(
        model="qwen-mt-turbo",
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
        extra_body={"translation_options": translation_options},
    )
    for chunk in completion:
        if chunk.choices:
            print(chunk.choices[0].delta.content)
        else:
            print("="*20+"usage 消耗"+"="*20)
            print(chunk.usage)

if __name__ == "__main__":
    # call_translation()
    call_translation_stream()

