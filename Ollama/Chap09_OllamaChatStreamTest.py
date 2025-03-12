from ollama import chat
from ollama import ChatResponse

stream = chat(
    model='deepseek-r1:1.5b', 
    messages=[{ 'role': 'user','content': '你是谁？',}],
    stream=True,
)

# 逐块打印响应内容
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)