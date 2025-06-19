# 这是一个 DMXAPI 调用 API 的 Python 例子
import requests
import json
import os

api_key_temp = os.getenv("DMXAPI_API_KEY")
print("DMXAPI Key:", api_key_temp)

# ------------------------------------------------------------------------------------
# 这里不要用 openai base url，需要改成DMXAPI的中转 https://www.dmxapi.cn ，下面是已经改好的。
# ------------------------------------------------------------------------------------
url = "https://www.dmxapi.cn/v1/chat/completions"

payload = json.dumps({
   "model": "o1-mini-2024-09-12",  # 01系列模型包括：o1-preview、o1-preview-2024-09-12、o1-mini、o1-mini-2024-09-12
   "messages": [
      # ================== 下面 2个参数，在使用 o1-preview 系列模型时，不需要填写 ==================
      #{ 
      #   "role": "system",
      #   "content": "You are a helpful assistant."
      #}, ================== 上面 2个参数，在使用 o1-preview 系列模型时，不需要填写 ==================
      {
         "role": "user",
         "content": "周树人和鲁迅是兄弟吗？"
      }
   ]
})
headers = {
   'Accept': 'application/json',
   'Authorization': api_key_temp, # 这里放你的 DMXapi key
   'User-Agent': 'DMXAPI/1.0.0 (https://www.dmxapi.cn)',  # 这里也改成 DMXAPI 的中转URL https://www.dmxapi.cn，已经改好
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload,timeout=(10.0, 300.0))  # 01系列模型不支持流式输出，所以要设置 timeout，避免太长回答造成的超时。
print(response.text)
