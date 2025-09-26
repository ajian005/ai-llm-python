"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->领域模型-->代码能力（Qwen-Coder） : https://help.aliyun.com/zh/model-studio/qwen-coder?spm=a2c4g.11186623.help-menu-2400256.d_0_1_6_1.1360407dzJw0nY#d6f57ecc9dgev

代码能力（Qwen-Coder）
    Qwen3-Coder 模型具有强大的代码能力，可通过 API 将其集成到业务中。

"""

import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def find_prime_numbers():
    """ 
     使用通义千问代码模型编写一个寻找质数的Python函数
    """
    completion = client.chat.completions.create(
        model="qwen3-coder-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。质数是指仅能被1和其自身整除的正整数，如2, 3, 5, 7等。不要输出非代码的内容。'}],
        )
    print("="*20+"回复内容"+"="*20)
    print(completion.choices[0].message.content)
    print("="*20+"Token消耗"+"="*20)
    print(completion.usage)

def tool_call():
    """ 
     Qwen3-Coder 模型具有强大的 Coding Agent 能力。您可以为模型配置读写文件、列举文件等工具，使其可以直接修改代码文件。
    """
    tools = [
        # 工具1 读取文件内容
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取指定路径的文件内容。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目标文件的相对或绝对路径"
                        }
                    },
                    "required": ["path"]
                }
            }
        },
        # 工具2 写入文件内容
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "将内容写入指定文件，若文件不存在则创建。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目标文件的相对或绝对路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "写入文件的字符串内容"
                        }
                    },
                    "required": ["path", "content"]
                }
            }
        },
        # 工具3 列出目录内容
        {
            "type": "function",
            "function": {
                "name": "list_directory",
                "description": "列出指定目录中的文件和子目录。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目标目录的相对或绝对路径"
                        }
                    },
                    "required": ["path"]
                }
            }
        }
    ]

    messages = [{"role": "user", "content": "写一个python代码，快速排序，命名为quick_sort.py"}]

    completion = client.chat.completions.create(
        model="qwen3-coder-plus",
        messages=messages,
        tools=tools
    )

    print("="*20+"工具调用信息"+"="*20)
    print(completion.choices[0].message.tool_calls)
    print("="*20+"Token消耗"+"="*20)
    print(completion.usage)

 
def code_completion():
    """ 
    代码补全
    基于前缀进行代码补全
    阿里云百炼提供了 OpenAI 兼容的 Completions 接口，适合代码补全场景。
    """
    completion = client.completions.create(
    model="qwen2.5-coder-32b-instruct",
    prompt="<|fim_prefix|>写一个python的快速排序函数，def quick_sort(arr):<|fim_suffix|>",
    )

    print(completion.choices[0].text)


if __name__ == "__main__":
    # find_prime_numbers()
    # tool_call() 
    code_completion()