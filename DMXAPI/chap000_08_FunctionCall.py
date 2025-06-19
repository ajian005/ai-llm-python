"""
    Python 示例8： gpt-4o 函数调用FunctionCall示例
"""
import http.client
import json

# 创建一个 HTTPS 连接对象，连接到指定的域名
conn = http.client.HTTPSConnection("www.dmxapi.cn")

# 定义请求体，包含了 GPT-4 模型的参数设置
payload = json.dumps(
    {
        "model": "gpt-4o",  # <--------------------------------------------------- 这类填模型全称
        "max_tokens": 100,
        "temperature": 0.8,
        "stream": False,  # 是否启用流式响应，这里设置为 False，表示不使用流式输出
        "messages": [{"role": "user", "content": "上海今天几度？"}],
        "tools": [  # 定义可用工具，这里定义了一个用于获取天气信息的函数
            {
                "type": "function",  # 工具类型为函数
                "function": {
                    "name": "get_current_weather",  # 函数名称
                    "description": "获得天气信息",  # 函数描述
                    "parameters": {
                        "type": "object",  # 参数类型为对象
                        "properties": {  # 参数属性
                            "location": {
                                "type": "string",  # 地点参数的类型为字符串
                                "description": "城市和州名，例如：上海, 中国",  # 地点参数的描述
                            },
                            "unit": {
                                "type": "string",  # 温度单位类型为字符串
                                "enum": [
                                    "celsius",
                                    "fahrenheit",
                                ],  # 支持的单位有摄氏度和华氏度
                            },
                        },
                        "required": ["location"],  # 必须提供地点参数
                    },
                },
            }
        ],
    }
)

# 设置请求头部信息，指定接受和发送的数据格式
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer sk--***********************************************', # ",  ## <------------------- 这里填DMXAPI令牌
    "Content-Type": "application/json",
}

# 发送 POST 请求到 API
conn.request("POST", "/v1/chat/completions", payload, headers)

# 获取服务器响应
res = conn.getresponse()

# 读取响应数据
data = res.read()

# 打印解码后的响应数据
print(data.decode("utf-8"))
