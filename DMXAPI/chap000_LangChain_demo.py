# ------------------------------------------------------------------------------------
# 在 LangChain 中使用 DMXAPI KEY 的例子
# ------------------------------------------------------------------------------------
from langchain_openai import ChatOpenAI
import os

api_key_temp = os.getenv("DMXAPI_API_KEY")
print("DMXAPI Key:", api_key_temp)

model = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://www.dmxapi.cn/v1",
    api_key=api_key_temp,  # 替换成你的 DMXapi 令牌key
)
text = "周树人和鲁迅是兄弟吗？"
print(model(text))