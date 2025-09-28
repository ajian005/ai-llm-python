"""
    大模型服务平台-->百炼用户指南（模型）-->多模态 --> 音频理解 :  https://help.aliyun.com/zh/model-studio/audio-understanding

    音频理解（Qwen-Audio）: 通义千问Audio是阿里云研发的大规模音频语言模型，能够接受多种音频（包括说话人语音、自然声音、音乐、歌声）和文本作为输入，并输出文本。通义千问Audio不仅能对输入的音频进行转录，还具备更深层次的语义理解、情感分析、音频事件检测、语音聊天等能力。
"""

import os
from openai import OpenAI
import dashscope


client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def audio_understanding():
    messages = [
        {
            "role": "user",
            "content": [
                {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"},
                {"text": "这段音频在说什么?"}
            ]
        }
    ]

    response = dashscope.MultiModalConversation.call(
        model="qwen-audio-turbo-latest", 
        messages=messages,
        result_format="message"
        )
    print("输出结果为：")
    print(response["output"]["choices"][0]["message"].content[0]["text"])


    if __name__ == "__main__":
        audio_understanding()