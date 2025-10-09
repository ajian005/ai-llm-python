"""
    大模型服务平台-->百炼用户指南（模型）-->语音识别/合成 -->实时语音识别 : https://help.aliyun.com/zh/model-studio/real-time-speech-recognition
    实时语音识别
      实时语音识别可以将音频流实时转换为文本，实现“边说边出文字”的效果。它适用于对麦克风语音进行实时识别，以及对本地音频文件进行实时转录。可广泛应用于会议实时记录，直播实时字幕，社交聊天等场景。
"""

"""
    一句话识别能够对一分钟内的语音数据流（无论是从外部设备如麦克风获取的音频流，还是从本地文件读取的音频流）进行识别并流式返回结果。
"""
import pyaudio
import dashscope
from dashscope.audio.asr import *


# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开， 并将your-api-key替换为自己的API Key
# dashscope.api_key = "your-api-key"

mic = None
stream = None

class Callback(TranslationRecognizerCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print("TranslationRecognizerCallback open.")
        mic = pyaudio.PyAudio()
        stream = mic.open(
            format=pyaudio.paInt16, channels=1, rate=16000, input=True
        )

    def on_close(self) -> None:
        global mic
        global stream
        print("TranslationRecognizerCallback close.")
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

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
            if english_translation.vad_pre_end:
                print("vad pre end {}, {}, {}".format(transcription_result.pre_end_start_time, transcription_result.pre_end_end_time, transcription_result.pre_end_timemillis))
        if transcription_result is not None:
            print("sentence id: ", transcription_result.sentence_id)
            print("transcription: ", transcription_result.text)

    
# 识别传入麦克风的语音
def main1():
    callback = Callback()
    translator = TranslationRecognizerChat(
                        model="gummy-chat-v1",
                        format="pcm",
                        sample_rate=16000,
                        transcription_enabled=True,
                        translation_enabled=True,
                        translation_target_languages=["en"],
                        callback=callback,
                    )
    translator.start()
    print("请您通过麦克风讲话体验一句话语音识别和翻译功能")
    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            if not translator.send_audio_frame(data):
                print("sentence end, stop sending")
                break
        else:
            break
    translator.stop()


# 识别本地文件

if __name__ == "__main__":
    main1()