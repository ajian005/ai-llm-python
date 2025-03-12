'''
    多轮对话
    Python 使用 requests 库与 Ollama API 交互
    运行前提条件 部署Ollama
'''


import requests

# 生成文本
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "deepseek-r1:1.5b",
        "messages": [
                {
                    "role": "user",
                    "content": "你好，你能帮我写一段 Python 代码吗？"
                }
            ],
        "stream": False
    }
)
print(response.json())