"""
   使用FastAPI与aiohttp进行SSE响应开发 https://zhuanlan.zhihu.com/p/651676361

   https://blog.csdn.net/kris__lee/article/details/145162257https://blog.csdn.net/kris__lee/article/details/145162257

"""

from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import Generator, Any
import uvicorn



app = FastAPI()

async def event_generator():
    while True:
        await asyncio.sleep(1)
        yield {"data": "Hello, World!"}

@app.get("/events")
async def sse_endpoint():
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)