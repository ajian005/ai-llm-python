"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->领域模型-->长上下文（Qwen-Long） : https://help.aliyun.com/zh/model-studio/long-context-qwen-long?spm=a2c4g.11186623.help-menu-2400256.d_0_1_6_0.6c005b77yKIBxY

长上下文（Qwen-Long）
    处理超长文本文档时，标准大型语言模型会因上下文窗口限制而失败。Qwen-Long 模型提供 1000 万 Token 的上下文长度，通过文件上传和引用机制处理大规模数据。

    使用方式
    Qwen-Long 处理长文档分为以下两个步骤：文件上传与 API 调用。

    文件上传与解析：

    通过 API 上传文件，文件格式与大小限制请参考支持格式。

    上传并成功后，系统返回一个当前账号下的唯一 file-id并开始解析。文件上传、存储以及解析本身不产生费用。

    API 调用与计费：

    在调用模型时，通过在 system 消息中引用一个或多个 file-id。

    模型根据 file-id 关联的文本内容进行推理。

    每次API 调用都会将所引用文件内容 Token 数计入该次请求的输入Token。

此机制避免了在每次请求中传输庞大的文件内容，但需留意其计费方式。


"""

import os
from pathlib import Path
from openai import OpenAI
from openai import OpenAI, BadRequestError


def upload_file():
    """"文档上传"""
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务base_url
    )

    file_object = client.files.create(file=Path(".//test_file.docx"), purpose="file-extract")
    print(file_object.id)


def call_model():
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务base_url
    )
    try:
        # 初始化messages列表
        completion = client.chat.completions.create(
            model="qwen-long",
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                # 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
                {'role': 'system', 'content': f'fileid://file-fe-f9d8dbd2911b4735a6470f01'},
                {'role': 'user', 'content': '这篇文章讲了什么?'}
            ],
            # 所有代码示例均采用流式输出，以清晰和直观地展示模型输出过程。如果您希望查看非流式输出的案例，请参见https://help.aliyun.com/zh/model-studio/text-generation
            stream=True,
            stream_options={"include_usage": True}
        )

        full_content = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                # 拼接输出内容
                full_content += chunk.choices[0].delta.content
                print(chunk.model_dump())

        print(full_content)

    except BadRequestError as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == "__main__":
    #upload_file()
     call_model()
