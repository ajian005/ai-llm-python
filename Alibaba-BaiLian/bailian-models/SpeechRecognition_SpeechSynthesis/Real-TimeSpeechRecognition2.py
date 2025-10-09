"""
    大模型服务平台-->百炼用户指南（模型）-->语音识别/合成 -->实时语音识别 : https://help.aliyun.com/zh/model-studio/real-time-speech-recognition
    实时语音识别
      实时语音识别可以将音频流实时转换为文本，实现“边说边出文字”的效果。它适用于对麦克风语音进行实时识别，以及对本地音频文件进行实时转录。可广泛应用于会议实时记录，直播实时字幕，社交聊天等场景。
"""

"""
    一句话识别能够对一分钟内的语音数据流（无论是从外部设备如麦克风获取的音频流，还是从本地文件读取的音频流）进行识别并流式返回结果。
"""
import os
import requests
from http import HTTPStatus

import dashscope
from dashscope.audio.asr import *


# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开， 并将your-api-key替换为自己的API Key
# dashscope.api_key = "your-api-key"

class Callback(TranslationRecognizerCallback):
    def on_open(self) -> None:
        print("TranslationRecognizerCallback open.")

    def on_close(self) -> None:
        print("TranslationRecognizerCallback close.")

    def on_event(
            self,
            request_id,
            transcription_result: TranscriptionResult,
            translation_result: TranslationResult,
            usage,
    ) -> None:
        print("request id: ", request_id)
        print("usage: ", usage)
        if translation_result is not None:
            print(
                "translation_languages: ",
                translation_result.get_language_list(),
            )
            english_translation = translation_result.get_translation("en")
            print("sentence id: ", english_translation.sentence_id)
            print("translate to english: ", english_translation.text)
        if transcription_result is not None:
            print("sentence id: ", transcription_result.sentence_id)
            print("transcription: ", transcription_result.text)

    def on_error(self, message) -> None:
        print('error: {}'.format(message))

    def on_complete(self) -> None:
        print('TranslationRecognizerCallback complete')


    
# 识别传入麦克风的语音
def main1():
    # 若没有将API Key配置到环境变量中，需将your-api-key替换为自己的API Key
    # dashscope.api_key = "your-api-key"

    r = requests.get(
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
    )
    with open("asr_example.wav", "wb") as f:
        f.write(r.content)

    callback = Callback()

    translator = TranslationRecognizerChat(
        model="gummy-chat-v1",
        format="wav",
        sample_rate=16000,
        callback=callback,
    )

    translator.start()

    try:
        audio_data: bytes = None
        f = open("asr_example.wav", 'rb')
        if os.path.getsize("asr_example.wav"):
            while True:
                audio_data = f.read(12800)
                if not audio_data:
                    break
                else:
                    if translator.send_audio_frame(audio_data):
                        print("send audio frame success")
                    else:
                        print("sentence end, stop sending")
                        break
        else:
            raise Exception(
                'The supplied file was empty (zero bytes long)')
        f.close()
    except Exception as e:
        raise e

    translator.stop()

# 识别本地文件

if __name__ == "__main__":
    main1()