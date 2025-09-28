"""
    大模型服务平台-->百炼用户指南（模型）-->多模态 --> 文字提取 :  https://help.aliyun.com/zh/model-studio/qwen-vl-ocr

    文字提取（Qwen-OCR）: 通义千问OCR 是专用于文字提取的视觉理解模型，可从各类图像（如扫描文档、表格、票据等）中提取文本或解析结构化数据，支持识别多种语言，并能通过特定任务指令实现信息抽取、表格解析、公式识别等高级功能。
"""

import os
from openai import OpenAI
import dashscope

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def text_extraction():

    PROMPT_TICKET_EXTRACTION = """
    请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。
    要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。
    返回数据格式以json方式输出，格式为：{'发票号码'：'xxx', '车次'：'xxx', '起始站'：'xxx', '终点站'：'xxx', '发车日期和时间点'：'xxx', '座位号'：'xxx', '席别类型'：'xxx','票价':'xxx', '身份证号码'：'xxx', '购票人姓名'：'xxx'"},
    """
    completion = client.chat.completions.create(
        model="qwen-vl-ocr-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg",
                        # 输入图像的最小像素阈值，小于该值图像会按原比例放大，直到总像素大于min_pixels
                        "min_pixels": 28 * 28 * 4,
                        # 输入图像的最大像素阈值，超过该值图像会按原比例缩小，直到总像素低于max_pixels
                        "max_pixels": 28 * 28 * 8192
                    },
                    # qwen-vl-ocr、qwen-vl-ocr-latest、qwen-vl-ocr-2025-04-13及以后的快照模型支持在以下text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.    
                    # 如调用qwen-vl-ocr-1028，模型会使用固定Prompt：Read all the text in the image.不支持用户在text中传入自定义Prompt
                    {"type": "text",
                     "text": PROMPT_TICKET_EXTRACTION}
                ]
            }
        ])
    print(completion.choices[0].message.content)



if __name__ == "__main__":
    text_extraction()