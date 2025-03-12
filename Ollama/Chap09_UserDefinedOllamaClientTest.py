'''
创建Ollama自定义客户端
通过 Client，你可以自定义请求的设置（如请求头、URL 等），并发送请求
'''

from ollama import Client

client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)

response = client.chat(model='deepseek-r1:1.5b', messages=[
    {
        'role': 'user',
        'content': '你是谁?',
    },
])
print(response['message']['content'])