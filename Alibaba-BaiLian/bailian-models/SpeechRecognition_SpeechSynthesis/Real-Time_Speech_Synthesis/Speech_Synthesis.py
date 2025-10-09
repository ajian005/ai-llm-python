"""
    大模型服务平台-->百炼用户指南（模型）-->语音识别/合成 -->语音合成-CosyVoice/Sambert : https://help.aliyun.com/zh/model-studio/text-to-speech
    语音合成-CosyVoice/Sambert
        语音合成，又称文本转语音（Text-to-Speech，TTS），是将文本转换为自然语音的技术。该技术基于机器学习算法，通过学习大量语音样本，掌握语言的韵律、语调和发音规则，从而在接收到文本输入时生成真人般自然的语音内容。
"""
# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *

# 若没有将API Key配置到环境变量中，需将your-api-key替换为自己的API Key
# dashscope.api_key = "your-api-key"

# 模型
model = "cosyvoice-v2"
# 音色
voice = "longxiaochun_v2"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("今天天气怎么样？")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)