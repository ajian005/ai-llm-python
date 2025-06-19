"""
Python 示例9： Openai whisper使用示例
"""
import json  # 添加 json 库的导入
import requests

def q_voice_to_text(file_path_wav):
    url = "https://www.dmxapi.cn/v1/audio/transcriptions"

    payload = {"model": "whisper-1"}
    files = {"file": ("audio.mp3", open(file_path_wav, "rb"))}

    # 直接使用 API 密钥
    gpt_key = "sk-*******************************************"  ## <------------------- 这里填你的 DMXAPI 令牌

    headers = {"Authorization": f"Bearer {gpt_key}"}

    # 发送请求
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # 处理响应
    data = json.loads(response.text)

    # 获取返回的文本内容
    voice_text = data["text"] if data["text"] is not None else ""

    return voice_text


print(q_voice_to_text("C:\\kywpy\\jay.mp3"))  ## <------------------- 这里改成你的音频文件