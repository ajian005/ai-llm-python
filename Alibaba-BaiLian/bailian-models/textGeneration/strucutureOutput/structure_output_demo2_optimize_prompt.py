"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->结构化输出 : https://help.aliyun.com/zh/model-studio/json-mode?spm=a2c4g.11186623.help-menu-2400256.d_0_1_4.116c1062cCDMZ1

优化提示词
    模糊的提示词（如“返回用户信息”）会使模型生成非预期结果。
    建议在提示词中准确描述预期 Schema，包括字段类型、必需性、格式要求（如日期格式），并提供示例。

    
应用于生产环境
    有效性校验
       当前暂不支持根据给定的 JSON Schema 生成 JSON 字符串。传递给下游业务前，建议使用工具对其进行有效性校验，
       如 jsonschema (Python)、Ajv (JavaScript)、Everit (Java)等，确保其符合指定的 JSON Schema 要求，
       避免因字段缺失、类型错误或格式不规范导致下游系统解析失败、数据丢失或业务逻辑中断。失败时可通过重试、大模型改写等策略进行修复。

    禁用 max_tokens
       请勿在开启结构化输出时指定 max_tokens（控制模型输出 Token 数的参数，默认值为模型最大输出 Token 数），
       否则返回的 JSON 字符串可能不完整，导致下游业务解析失败。

"""

from openai import OpenAI
import os
import json
import textwrap  # 用于处理多行字符串的缩进，提高代码可读性

# 预定义示例响应，用于向模型展示期望的输出格式
# 示例1：包含所有字段的完整响应
example1_response = json.dumps(
    {
        "info": {"name": "张三", "age": "25岁", "email": "zhangsan@example.com"},
        "hobby": ["唱歌"]
    },
    ensure_ascii=False
)
# 示例2：包含多个hobby的响应
example2_response = json.dumps(
    {
        "info": {"name": "李四", "age": "30岁", "email": "lisi@example.com"},
        "hobby": ["跳舞", "游泳"]
    },
    ensure_ascii=False
)
# 示例3：不包含hobby字段的响应（hobby非必需）
example3_response = json.dumps(
    {
        "info": {"name": "赵六", "age": "28岁", "email": "zhaoliu@example.com"}
    },
    ensure_ascii=False
)
# 示例4：另一个不包含hobby字段的响应
example4_response = json.dumps(
    {
        "info": {"name": "孙七", "age": "35岁", "email": "sunqi@example.com"}
    },
    ensure_ascii=False
)

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# dedent的作用是去除每行开头的公共缩进，使字符串在代码中可以美观地缩进，但在运行时不会包含这些额外的空格
system_prompt = textwrap.dedent(f"""\
    请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

    【输出格式要求】
    输出必须严格遵循以下JSON结构：
    {{
      "info": {{
        "name": "字符串类型，必需字段，用户姓名",
        "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
        "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
      }},
      "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
    }}

    【字段提取规则】
    1. name: 从文本中识别用户姓名，必需提取
    2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
    3. email: 识别邮箱地址，保持原始格式，必需提取
    4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

    【参考示例】
    示例1（包含爱好）：
    Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
    A：{example1_response}

    示例2（包含多个爱好）：
    Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
    A：{example2_response}

    示例3（不包含爱好）：
    Q：我叫赵六，今年28岁，我的邮箱是zhaoliu@example.com
    A：{example3_response}

    示例4（不包含爱好）：
    Q：我是孙七，35岁，邮箱sunqi@example.com
    A：{example4_response}

    请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。\
""")

# 调用大模型API进行信息提取
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
        },
    ],
    response_format={"type": "json_object"},  # 指定返回JSON格式
)

# 提取并打印模型生成的JSON结果
json_string = completion.choices[0].message.content
print(json_string)