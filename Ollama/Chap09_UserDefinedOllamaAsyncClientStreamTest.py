'''
    异步客户端
        异步流式响应
        如果你需要异步地处理流式响应，可以通过将 stream=True 设置为异步生成器来实现。
        这里，响应将逐部分地异步返回，每部分都可以即时处理。
'''

import asyncio
from ollama import AsyncClient

async def chat():
    message = {'role': 'user', 'content': '你是谁?'}
    async for part in await AsyncClient().chat(model='deepseek-r1:1.5b', messages=[message], stream=True):
        print(part['message']['content'], end='', flush=True)

asyncio.run(chat())