"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->领域模型-->数据挖掘（Qwen-Doc） : https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc?spm=a2c4g.11186623.help-menu-2400256.d_0_1_6_4.2a1930330Qyq55&scm=20140722.H_2948885._.OR_help-T_cn~zh-V_1

    数据挖掘模型专门针对信息抽取、内容审核、分类打标和摘要生成任务进行设计。相比通用对话模型，该模型能够快速且精确地输出规范的结构化数据（如JSON格式），解决通用对话模型返回不规范回复结构或提取信息不够准确的问题。
使用方式
    Qwen-Doc-Turbo 支持通过以下三种方式从文件中提取信息：

    通过文件URL传入 (推荐):

        直接在API请求中提供文件的公开URL，模型即可访问并解析内容。此方法最多支持单次传入10个文件，并可通过 file_parsing_strategy 参数指定解析策略（auto 或 text_only），是处理多文件的唯一方式。

        SDK: 文件URL方式当前仅支持DashScope协议，可以选择使用DashScope Python SDK或者HTTP方式调用（如curl）。

    通过文件ID传入:

        先将本地文件上传至百炼平台，生成一个当前阿里云账号下唯一的 file-id并开始解析，然后在后续的API请求中引用此id。此方法兼容 OpenAI SDK，适合需要重复使用同一份文件或处理本地文件的场景。

        SDK: 文件上传与管理使用 OpenAI SDK，模型调用兼容 OpenAI SDK 和 DashScope SDK。

    通过纯文本传入:

        对于较短或临时的文本内容，可以直接将其作为 system 消息的一部分传入。

        SDK: 兼容 OpenAI SDK 和 DashScope SDK。
"""

import os
import dashscope

def call_generation():

    response = dashscope.Generation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'), # 如果您没有配置环境变量，请在此处替换您的API-KEY
        model='qwen-doc-turbo',
        messages=[
        {"role": "system","content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "从这份客户反馈报告中，提取所有反馈信息，并整理成一个标准的JSON数组。每个对象需要包含：feedback_id (字符串)、product_name (字符串)、user_name (字符串)、rating_score (1-5的整数)、feedback_type (字符串) 和 summary (不超过30字的中文摘要)。"
                },
                {
                    "type": "doc_url",
                    "doc_url": [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250910/gokhyx/%E5%AE%A2%E6%88%B7%E5%8F%8D%E9%A6%88%E6%8A%A5%E5%91%8A.txt"
                    ],
                    "file_parsing_strategy": "auto"
                }
            ]
        }]
    )
    try:
        if response.status_code == 200:
            print(response.output.choices[0].message.content)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误代码: {response.code}")
            print(f"错误信息: {response.message}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
    except Exception as e:
        print(f"发生错误: {e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
    

if __name__ == "__main__":
    call_generation()
