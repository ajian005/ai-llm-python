"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->领域模型-->角色扮演（Qwen-Character） : https://help.aliyun.com/zh/model-studio/role-play?spm=a2c4g.11186623.help-menu-2400256.d_0_1_6_3.7a8577e9YCwe4c

  通义千问的角色扮演模型，适合拟人化的对话场景（如虚拟社交、游戏NPC、IP复刻、硬件/玩具/车机等）。相比于其它通义千问模型，提升了人设还原、话题推进、倾听共情等能力。

  对话调用
    人物设定
        您在使用 Character 模型进行角色扮演时，可以对 System Message 的以下方面进行配置：

        通过优化 Prompt 模板，可以使大模型更准确、可靠地执行特定任务。详情请参考Prompt自动优化。
        角色的详细信息

        包括姓名、年龄、性格、职业、简介、人物关系等。

        角色的其他介绍

        对于角色的经历、关注的事情进行一些更丰富的描述。可用标签隔开不同类别的内容，用文字描述。

        补充对话场景

        尽量明确产出场景的背景，以及人物关系，给角色提出明确的指令和要求，让角色按照指令要求进行对话。

        补充语言风格

        提示角色需要表现出的风格以及说话的长短；如果需要角色有一些特殊的表现，比如动作、表情等，也可以提示。
"""


import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def call_character():
    completion = client.chat.completions.create(
        model="qwen-plus-character",
        messages=[
            {
                "role": "system",
                "content": "你是江让，男性，一个围棋天才，拿过很多围棋的奖项。你现在在读高中，是高中校草，用户是你的班长。一开始你看用户在奶茶店打工，你很好奇，后来慢慢喜欢上用户了。\n\n你的性格特点：\n\n热情，聪明，顽皮\n\n你的行事风格：\n\n机制，果断\n\n你的语言特点：\n\n说话幽默，爱开玩笑\n\n你可以将动作、神情语气、心理活动、故事背景放在（）中来表示，为对话提供补充信息。",
            },
            {"role": "assistant", "content": "班长你在干嘛呢"},
            {"role": "user", "content": "我在看书"},
        ],
    )

    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main = call_character()
    
