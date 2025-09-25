"""
   使用FastAPI与aiohttp进行SSE响应开发 https://zhuanlan.zhihu.com/p/651676361

   # 使用 requests 库调用接口得到SSE响应。
"""

import requests  

def test():  
    url = r"http://127.0.0.1:8003/sse"  
    headers = {'Content-Type': 'text/event-stream'}  
    response = requests.get(url, headers=headers, stream=True)  
    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True): 
        print(chunk)  

if __name__ == '__main__':  
    test()
