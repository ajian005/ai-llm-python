"""
    大模型服务平台-->百炼用户指南（模型）-->语音识别/合成 -->录音文件识别-Paraformer/Fun-ASR/SenseVoice : https://help.aliyun.com/zh/model-studio/recording-file-recognition
"""

from http import HTTPStatus
from dashscope.audio.asr import Transcription
import dashscope
import os
import json

# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

task_response = Transcription.async_call(
    model='fun-asr',
    file_urls=['https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
               'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav']
)

transcribe_response = Transcription.wait(task=task_response.output.task_id)
if transcribe_response.status_code == HTTPStatus.OK:
    print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
    print('transcription done!')