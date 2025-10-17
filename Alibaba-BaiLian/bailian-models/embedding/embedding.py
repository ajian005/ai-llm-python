"""
    大模型服务平台-->百炼用户指南（模型）--> 向量化 --> 文本与多模态向量化 : https://help.aliyun.com/zh/model-studio/embedding

    向量化模型能够将文本、图像和视频数据转化为数值向量，并用于后续的语义搜索、推荐、聚类、分类、异常检测等任务。

模型选择
    选择合适的模型取决于您的输入数据类型和应用场景。

    处理纯文本或代码：推荐使用 text-embedding-v4。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。

    处理多模态内容：对于包含图像、文本或视频的混合内容，可以选择针对视觉能力进行优化提升的 tongyi-embedding-vision-plus 与 tongyi-embedding-vision-flash或通用多模态模型multimodal-embedding-v1。

    处理大规模数据：若您需要处理大规模、非实时的文本数据，建议使用 text-embedding-v4 并结合 OpenAI兼容-Batch调用，以显著降低成本。

"""

import os
from openai import OpenAI


client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),  
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 百炼服务的base_url
)


def get_embedding_text(text: str) -> str:
    completion = client.embeddings.create(
        model="text-embedding-v4",
        input=text
    )
    print(completion.model_dump_json())



import dashscope
import json
from http import HTTPStatus

def get_embedding_multiModal(image: str) -> str:

    # 输入可以是视频
    # video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"
    # input = [{'video': video}]
    # 或图片
    input = [{'image': image}]
    resp = dashscope.MultiModalEmbedding.call(
        model="tongyi-embedding-vision-plus",
        input=input
    )

    print(json.dumps(resp.output, indent=4))




if __name__ == "__main__":
    image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
    input_texts = "衣服的质量杠杠的"
    get_embedding_text(input_texts)
    get_embedding_multiModal(image)
    # get_embedding(image)

