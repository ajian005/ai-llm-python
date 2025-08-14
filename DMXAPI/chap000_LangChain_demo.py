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

llm = ChatOpenAI(
    openai_api_key=os.environ["DMXAPI_API_KEY"],
    openai_api_base="https://www.dmxapi.cn/v1",  # 第三方平台地址
    model_name="gpt-3.5-turbo"  # 确认第三方平台支持的模型名称
)

text = "周树人和鲁迅是兄弟吗？"
print(model.invoke(text))
print("======================================")
print(llm.invoke(text))