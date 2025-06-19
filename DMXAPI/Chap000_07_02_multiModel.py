"""
    Python 示例7-2： gpt-4o 多模态本地图片解析示例 
"""
import base64

import requests


def encode_image(image_path):
    """
    读取本地图片并编码为Base64字符串。
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


# 将 URL 和 API key 提取为独立变量，便于管理和修改
域名 = "https://www.dmxapi.cn/"  # 定义API的基础域名
API_URL = 域名 + "v1/chat/completions"  # 完整的API请求URL
API_KEY = "sk-************************************************"  # <--------------------------------------------- 请替换为你的 DMXAPI 令牌

# 本地图片路径
image_path = "33.png"  # <--------------------------------------------- 本地图片路径
base64_image = encode_image(image_path)  # 编码本地图片

# 创建请求数据payload，包括所需的模型和消息内容
payload = {
    "model": "chatgpt-4o-latest",  # 指定使用的多模态AI模型，除了gpt-4o 也推荐使用 claude-3-5-sonnet系列
    "messages": [
        {
            "role": "system",  # 系统角色信息，可以为空
            "content": "",
        },
        {
            "role": "user",  # 用户角色的消息内容
            "content": [
                {"type": "text", "text": "请解释图片里说了哪些内容"},  # 发送文本消息
                {
                    "type": "image_url",  # 发送图片URL
                    "image_url": {
                        # 使用Base64编码的本地图片
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
            ],
        },
    ],
    "temperature": 0.1,  # 设置生成文本的随机性，越低输出越有确定性
    "user": "DMXAPI",  # 发送请求的用户标识
}

# 定义HTTP请求头，包括内容类型和身份验证信息
headers = {
    "Content-Type": "application/json",  # 设置内容类型为JSON
    "Authorization": f"Bearer {API_KEY}",  # 使用 f-string 动态插入 API_KEY，进行身份验证
    "User-Agent": f"DMXAPI/1.0.0 ({域名})",  # 自定义的User-Agent，用于识别客户端信息
}

# 发送POST请求，将请求数据和头信息传入API，获取响应
response = requests.post(API_URL, headers=headers, json=payload)

# 输出API的响应内容
print(response.text)

