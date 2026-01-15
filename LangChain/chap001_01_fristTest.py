'''
    langchain 入门指南（一）- 准备 API KEY    https://developer.aliyun.com/article/1586831?spm=a2c6h.24874632.expert-profile.150.1e375214WVEbY1
    langchain 入门指南（二）- 如何跟大模型对话  https://developer.aliyun.com/article/1586834?spm=a2c6h.24874632.expert-profile.149.1e375214WVEbY1
    langchain 入门指南（三）- token的计算     https://developer.aliyun.com/article/1586851?spm=a2c6h.24874632.expert-profile.146.1e375214WVEbY1
'''

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

chat = ChatOpenAI(
    model="qwen-plus",     # model="yi-large",
    temperature=0.3,
    max_tokens=200,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# BaseMessage 列表
messages = [
    SystemMessage(content="你是一名精通了 golang 的专家"),
    HumanMessage(content="写一个  golang 的 hello world 程序"),
]
response = chat.invoke(messages)
print(response.content)

# 元组列表
messages = [
    ('system', '你是一名精通了 golang 的专家'),
    ('human', '写一个  golang 的 hello world 程序')
]
response = chat.invoke(messages)
print(response.content)

# 字符串 这个字符串参数会被转换为 HumanMessage
response = chat.invoke('使用 golang 写一个 hello world 程序')
print(response.content)

# 字符串列表
messages = [
    "你是一名精通了 golang 的专家",
    "写一个  golang 的 hello world 程序",
]
response = chat.invoke(messages)
print(response.content)
print(response)



