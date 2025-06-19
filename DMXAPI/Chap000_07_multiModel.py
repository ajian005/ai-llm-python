"""
  Python 示例7-1： gpt、claude、gemini 多模态网络图片解析示例
"""
import requests
import os

api_key_temp = os.getenv("DMXAPI_API_KEY")
print("DMXAPI Key:", api_key_temp)

# 将 URL 和 API key 提取为独立变量，便于管理和修改
域名 = "https://www.dmxapi.cn/"  # 定义API的基础域名
API_URL = 域名 + "v1/chat/completions"  # 完整的API请求URL
API_KEY = api_key_temp  ## <--------------------------------------------- 请替换为你的 DMXAPI 令牌

# 图片URL（使用代码B中的图片URL）
IMAGE_URL = "https://pic.rmb.bdstatic.com/bjh/down/9bfc5b8f8f725467a1e3ccc4d7adc160.png"


def analyze_image(api_url, api_key, image_url, prompt):
    """
    使用指定的API对图片进行分析。

    :param api_url: API端点URL
    :param api_key: API密钥
    :param image_url: 需要分析的图片URL
    :param prompt: 分析提示词
    :return: 分析结果文本
    """
    # 构建请求数据payload，包括所需的模型和消息内容
    payload = {
        "model": "gemini-2.0-flash-thinking-exp-1219",  # 指定使用的多模态AI模型  推荐 gemini-2.0-flash-thinking-exp-1219    gpt-4o-2024-08-06
        "messages": [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": "你是一个图片分析助手。"}
                ],  # 提供系统指令
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url  # 使用代码B中的图片URL
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,  # 使用用户指定的提示词
                    },
                ],
            },
        ],
        "temperature": 0.1,  # 设置生成文本的随机性
        "user": "DMXAPI",  # 发送请求的用户标识
    }

    # 定义HTTP请求头，包括内容类型和身份验证信息
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "DMXAPI/1.0.0 (https://www.dmxapi.cn/)",
    }

    try:
        # 发送POST请求，将请求数据和头信息传入API，获取响应
        response = requests.post(api_url, headers=headers, json=payload)

        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            # 提取并返回分析结果
            return result["choices"][0]["message"]["content"]
        else:
            # 如果请求失败，打印错误信息
            print(f"请求失败，状态码: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"请求过程中发生异常: {e}")
        return None


if __name__ == "__main__":
    # 定义你的提示词
    prompt = "请详细描述这张图片的内容。"

    # 调用函数进行图片分析
    analysis_result = analyze_image(API_URL, API_KEY, IMAGE_URL, prompt)

    if analysis_result:
        print("图片分析结果:")
        print(analysis_result)


