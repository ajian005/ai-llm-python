'''
    异步客户端
    如果你希望异步执行请求，可以使用 AsyncClient 类，适用于需要并发的场景。
    异步客户端支持与传统的同步请求一样的功能，唯一的区别是请求是异步执行的，可以提高性能，尤其是在高并发场景下。
'''

import asyncio
from ollama import AsyncClient

async def chat():
    message = {'role': 'user', 'content': '你是谁?'}
    response = await AsyncClient().chat(model='deepseek-r1:1.5b', messages=[message])
    print(response['message']['content'])

asyncio.run(chat())