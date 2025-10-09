"""
    大模型服务平台-->百炼用户指南（模型）-->语音识别/合成 -->实时语音合成-通义千问 : https://help.aliyun.com/zh/model-studio/qwen-tts
       
       实时语音合成-通义千问提供低延迟、流式文本输入与流式音频输出能力，提供多种拟人音色，支持多语种/方言合成，可在同一音色下输出多语种，并能自适应调节语气，流畅处理复杂文本。

       通过以下代码与 Qwen-TTS Realtime API 建立 WebSocket 连接。
"""

# pip install websocket-client
import json
import websocket
import os

# 若没有配置环境变量，请用百炼API Key将下行替换为：API_KEY="sk-xxx",
API_KEY=os.getenv("DASHSCOPE_API_KEY")
API_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime"

headers = [
    "Authorization: Bearer " + API_KEY
]

def on_open(ws):
    print(f"Connected to server: {API_URL}")
def on_message(ws, message):
    data = json.loads(message)
    print("Received event:", json.dumps(data, indent=2))
def on_error(ws, error):
    print("Error:", error)

ws = websocket.WebSocketApp(
    API_URL,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error
)

ws.run_forever()