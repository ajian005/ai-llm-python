"""
    使用FastAPI与aiohttp进行SSE响应开发  https://zhuanlan.zhihu.com/p/651676361
"""

import asyncio
from fastapi import FastAPI, Request
from sse_starlette import EventSourceResponse
import uvicorn  

app = FastAPI()  


@app.get("/")  
async def root():  
    return {"message": "Hello World"}

@app.get("/sse")  
async def sse_endpoint(request: Request):
    async def event_generator(request: Request):
        res_str = "七夕情人节即将来临，我们为您准备了精美的鲜花和美味的蛋糕"
        for i in res_str:
            if await request.is_disconnected():
                print("client disconnected")
                break
            yield {  
                "event": "message",  
                "retry": 15000,  
                "data": i  
            } 
            await asyncio.sleep(0.1)
    g = event_generator(request)
    return EventSourceResponse(g, media_type="text/event-stream")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)