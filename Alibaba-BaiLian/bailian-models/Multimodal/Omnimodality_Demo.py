"""
    大模型服务平台-->百炼用户指南（模型）-->多模态 --> 全模态 :  https://help.aliyun.com/zh/model-studio/qwen-omni

    音频理解（Qwen-Audio）: Qwen-Omni 模型能够接收文本、图片、音频、视频等多种模态的组合输入，并生成文本或语音形式的回复， 提供多种拟人音色，支持多语言和方言的语音输出，可应用于文本创作、视觉识别、语音助手等场景。
"""

import os
from openai import OpenAI
import dashscope
import base64
import io
import wave
import soundfile as sf
import numpy as np


client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


def Omnimodality():
    # 2. 发起请求
    try:
        completion = client.chat.completions.create(
            model="qwen3-omni-flash",
            messages=[{"role": "user", "content": "你是谁"}],
            modalities=["text", "audio"],  # 指定输出文本和音频
            audio={"voice": "Cherry", "format": "wav"},
            stream=True,  # 必须设置为 True
            stream_options={"include_usage": True},
        )

        # 3. 处理流式响应并解码音频
        print("模型回复：")
        audio_base64_string = ""
        for chunk in completion:
            # 处理文本部分
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")

            # 收集音频部分
            if chunk.choices and hasattr(chunk.choices[0].delta, "audio") and chunk.choices[0].delta.audio:
                audio_base64_string += chunk.choices[0].delta.audio.get("data", "")

        # 4. 保存音频文件
        if audio_base64_string:
            wav_bytes = base64.b64decode(audio_base64_string)
            audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
            sf.write("./Alibaba-BaiLian/bailian-models/Multimodal/audio_assistant.wav", audio_np, samplerate=24000)
            print("\n音频文件已保存至：audio_assistant.wav")

    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    Omnimodality()