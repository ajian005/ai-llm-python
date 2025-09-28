"""
    大模型服务平台-->百炼用户指南（模型）-->多模态 --> 视觉理解 :  https://help.aliyun.com/zh/model-studio/vision

    视觉理解（Qwen-VL）: 通义千问VL模型可以根据您传入的图片来进行回答。
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

"""
    理解在线图像（通过URL指定，非本地图像）
"""
def understand_picture():
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest", # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=[
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                        },
                    },
                    {"type": "text", "text": "图中描绘的是什么景象?"},
                ],
            },
        ],
    )
    print(completion.choices[0].message.content)


"""
    开启/关闭思考模式 
    qwen3-vl-plus、qwen3-vl-plus-2025-09-23 模型属于混合思考模型，模型可以在思考后回复，也可直接回复；通过enable_thinking参数控制是否开启思考模式：
        true：         开启思考模式
        false（默认）： 关闭思考模式
"""
def understand_picture2():
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复
    enable_thinking = True
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="qwen3-vl-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                        },
                    },
                    {"type": "text", "text": "这道题怎么解答？"},
                ],
            },
        ],
        stream=True,
        # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
        # qwen-vl-plus、 qwen3-vl-plus-2025-09-23可通过enable_thinking开启或关闭思考、对于qwen3-vl-235b-a22b-thinking，enable_thinking开启，其他Qwen-VL模型均不适用
        extra_body={
            'enable_thinking': True,
            "thinking_budget": 500},

        # 解除以下注释会在最后一个chunk返回Token使用量
        # stream_options={
        #     "include_usage": True
        # }
    )

    if enable_thinking:
        print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                # 打印回复过程
                print(delta.content, end='', flush=True)
                answer_content += delta.content

    # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
    # print(reasoning_content)
    # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
    # print(answer_content)


"""
多轮对话（参考历史对话信息）
    通义千问VL模型可以参考历史对话信息实现多轮对话，您需要维护一个messages 数组，将每一轮的对话历史以及新的指令添加到 messages 数组中。
"""
def understand_picture3():
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}]},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ],
        }
    ]
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",  # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=messages,
        )
    print(f"第一轮输出：{completion.choices[0].message.content}")
    assistant_message = completion.choices[0].message
    messages.append(assistant_message.model_dump())
    messages.append({
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "做一首诗描述这个场景"
            }
            ]
        })
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=messages,
        )
    print(f"第二轮输出：{completion.choices[0].message.content}")


"""
流式输出
    大模型接收到输入后，会逐步生成中间结果，最终结果由这些中间结果拼接而成。这种一边生成一边输出中间结果的方式称为流式输出。采用流式输出时，您可以在模型进行输出的同时阅读，减少等待模型回复的时间。
"""
def understand_picture4():
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",  # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=[
        {"role": "system",
            "content": [{"type":"text","text": "You are a helpful assistant."}]},
            {"role": "user",
            "content": [{"type": "image_url",
                        "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
                        {"type": "text", "text": "图中描绘的是什么景象？"}]}],
        stream=True
    )
    full_content = ""
    print("流式输出内容为：")
    for chunk in completion:
        # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
        if chunk.choices and chunk.choices[0].delta.content != "":
            full_content += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content)
    print(f"完整内容为：{full_content}")


"""
高分辨率图像理解
    您可以通过设置vl_high_resolution_images参数为true，将通义千问VL模型的单图Token上限从1280提升至16384：

"""
def understand_picture5():
    # 若使用新加坡地域的模型，请释放下列注释
    # dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
    messages = [
        {
            "role": "user",
            "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
                {"text": "这张图表现了什么内容?"}
            ]
        }
    ]

    response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen-vl-max-latest',  # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=messages,
        vl_high_resolution_images=True
    )

    print("大模型的回复:\n ",response.output.choices[0].message.content[0]["text"])
    print("Token用量情况：","输入总Token：",response.usage["input_tokens"] , "，输入图像Token：" , response.usage["image_tokens"])


"""
多图像输入
    通义千问VL 模型支持单次请求传入多张图片进行综合分析，所有图像的总Token数需在模型的最大输入之内，可传入图像的最大数量请参考图像数量限制。

    以下是理解多张在线图像（通过URL指定，非本地图像）的示例代码。了解如何传入本地文件和图像限制。

"""
def understand_picture6():
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest", # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=[
        {"role":"system","content":[{"type": "text", "text": "You are a helpful assistant."}]},
        {"role": "user","content": [
            # 第一张图像url，如果传入本地文件，请将url的值替换为图像的Base64编码格式
            {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
            # 第二张图像url，如果传入本地文件，请将url的值替换为图像的Base64编码格式
            {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},},
            {"type": "text", "text": "这些图描绘了什么内容？"},
                ],
            }
        ],
    )

    print(completion.choices[0].message.content)


"""
视频理解
        部分通义千问VL模型支持对视频内容的理解，文件形式包括图像列表（视频帧）或视频文件。
视频文件限制

    视频大小：
        传入公网URL：Qwen2.5-VL系列模型支持传入的视频大小不超过1 GB；其他模型不超过150MB。
        传入本地文件时：
            使用OpenAI SDK方式，经Base64编码后的视频需小于10MB；
            使用DashScope SDK方式，视频本身需小于100MB。详情请参见传入本地文件。

    视频时长：
        Qwen2.5-VL系列模型：2秒至10分钟；
        其他模型：2秒至40秒。
    视频格式： MP4、AVI、MKV、MOV、FLV、WMV 等。
    视频尺寸：无特定限制，模型处理前会被调整到约60万像素数，更大尺寸的视频文件不会有更好的理解效果。
    暂时不支持对视频文件的音频进行理解。

    视频抽帧说明

        通义千问VL模型通过抽帧来分析视频，抽帧频率决定了模型分析的精细度，不同SDK的控制方式如下：
        使用 DashScope SDK：
        可通过设置 fps 参数来控制抽帧频率，表示每隔 
        fps
        1
        ​
    
        秒抽取一帧图像。建议为高速运动场景（如体育赛事、动作电影）设置较大的较大的fps值，为内容静态或较长的视频设置较小的fps值。
        使用 OpenAI SDK：
        抽帧频率固定为每隔0.5秒抽取一帧，无法通过参数修改。
"""
def understand_picture7():
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=[
            {"role": "system",
            "content": [{"type": "text","text": "You are a helpful assistant."}]},
            {"role": "user","content": [{
                # 直接传入视频文件时，请将type的值设置为video_url
                # 使用OpenAI SDK时，视频文件默认每间隔0.5秒抽取一帧，且不支持修改，如需自定义抽帧频率，请使用DashScope SDK.
                "type": "video_url",            
                "video_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"}},
                {"type": "text","text": "这段视频的内容是什么?"}]
            }]
    )
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    # understand_picture()
    # understand_picture2()
    # understand_picture3()
    # understand_picture4()
    #  understand_picture5()
    #  understand_picture6()
    understand_picture7()