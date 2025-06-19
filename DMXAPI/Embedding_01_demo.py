import json
import requests
import os

api_key_temp = os.getenv("DMXAPI_API_KEY")
print("DMXAPI Key:", api_key_temp)

# API endpoint
url = "https://www.dmxapi.cn/v1/embeddings"  # <---------------- 仅限 cn人民币站使用

# API key (假设需要认证)
api_key = api_key_temp  # <----------------  填入 DMXAPI 后台令牌

# Headers
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Body parameters
data = {
    "input": "你好，把这句话变向量吧。",
    "model": "text-embedding-ada-002",  # 假设使用的模型
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check the response
if response.status_code == 200:
    embedding = response.json()
    print("Embedding created successfully:")
    print(embedding)
else:
    print(f"Failed to create embedding. Status code: {response.status_code}")
    print(response.text)
