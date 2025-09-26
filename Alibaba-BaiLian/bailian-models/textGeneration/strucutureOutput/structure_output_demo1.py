"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->结构化输出 : https://help.aliyun.com/zh/model-studio/json-mode?spm=a2c4g.11186623.help-menu-2400256.d_0_1_4.116c1062cCDMZ1

JSON Mode
    执行信息抽取或结构化数据生成任务时，大模型可能返回多余文本（如 ```json）导致下游解析失败。开启结构化输出可以确保大模型输出标准格式的 JSON 字符串。

    使用方式
        设置response_format参数：在请求体中，将 response_format 参数设置为 {"type": "json_object"}。
        提示词包含"JSON"关键词：System Message 或 User Message 中需要包含 "JSON" 关键词（不区分大小写），否则会报错：'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.

    以从个人简介中抽取信息的简单场景为例，介绍快速使用结构化输出的方法。
"""
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-flash",
    messages=[
        {
            "role": "system",
            "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
        },
        {
            "role": "user",
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
        },
    ],
    response_format={"type": "json_object"}
)

json_string = completion.choices[0].message.content
print(json_string)