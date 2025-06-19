"""
Python 示例6：豆包即梦seedream-3.0 & Openai dall-e-3 & flux系列绘图模型 复制代码
>>>>>>>>>>>>>>>>> gpt-image-1 更详细教程《DMXAPI 画图模型使用说明》
"""

import http.client
import json
import os

api_key_temp = os.getenv("DMXAPI_API_KEY")
print("DMXAPI Key:", api_key_temp)

# 定义 API 密钥和基本 URL
API_KEY = api_key_temp  # 请替换为你的 DMXAPI 令牌
API_HOST = "www.dmxapi.cn"  # API 主机地址
API_ENDPOINT = "/v1/images/generations"  # API 请求路径

# 请求参数
prompt_text = "科技感的店铺门口，店铺名称是DMXAPI"  # 描述生成图像的提示词
model_name = "seedream-3.0"  # 可选：dall-e-3,seedream-3.0,flux-schnell,flux-dev,flux.1.1-pro
image_size = "1024x1024"  # 图像尺寸 参考值：1792x1024, 1024 × 1792, 1024x1024

# 构建请求的 JSON 数据
payload = json.dumps(
    {
        "prompt": prompt_text,
        "n": 1,  # 生产图片数量，修改会报错，默认1就可以。
        "model": model_name,
        "size": image_size,
    }
)

# 定义请求头信息
headers = {
    "Authorization": f"Bearer {API_KEY}",  # 使用变量 API_KEY
    "Accept": "application/json",
    "User-Agent": "DMXAPI/1.0.0 (https://www.dmxapi.cn)",
    "Content-Type": "application/json",
}

# 建立 HTTPS 连接
conn = http.client.HTTPSConnection(API_HOST)

# 发送 POST 请求
conn.request("POST", API_ENDPOINT, payload, headers)

# 获取响应并读取数据
res = conn.getresponse()
data = res.read()

# 输出结果
print(data.decode("utf-8"))
