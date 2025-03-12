'''
错误处理
    Ollama SDK 会在请求失败或响应流式传输出现问题时抛出错误。
    我们可以使用 try-except 语句来捕获这些错误，并根据需要进行处理。
    在上述例子中，如果模型 does-not-yet-exist 不存在，抛出 ResponseError 错误，捕获后你可以选择拉取该模型或进行其他处理。
'''
from ollama import Client
from ollama import chat
from ollama import ChatResponse
# from ollama import ollama


model = 'does-not-yet-exist'

try:
    response = ollama.chat(model)
except ollama.ResponseError as e:
    print('Error:', e.error)
    if e.status_code == 404:
        ollama.pull(model)