"""
大模型服务平台-->百炼用户指南（模型）-->文本生成-->深度思考 : https://help.aliyun.com/zh/model-studio/deep-thinking?spm=a2c4g.11186623.help-menu-2400256.d_0_1_3.5cc425c8XqPlrq&scm=20140722.H_2870973._.OR_help-T_cn~zh-V_1

联网搜索
    由于训练数据的时效性，大模型无法准确回答如股票价格、今日资讯等时效性问题。
    您可以通过设置enable_search参数为true以启用联网检索功能，使大模型可以基于实时检索数据进行回复。

    开启enable_search后，模型会先判断是否需要使用联网搜索能力来回答您的问题：

    需要联网搜索
        当问题被模型判断需要使用联网搜索能力，模型会根据联网搜索的结果进行回复。
        联网搜索功能当前免费，但搜索到的信息会增加 Token 消耗。

    不需要联网搜索
        模型本身已经可以回答如“你是谁”、“一年有多少天”等简单或常识性的问题。此时模型不会去联网搜索，而是直接进行回答。
        如果您希望强制开启联网搜索功能，请参见下文的forced_search参数。

    在设置enable_search参数为true后，您可以通过search_options参数来配置联网搜索策略，包括以下方面：

    是否强制联网搜索：
        通过forced_search配置，可选值：
            true 强制开启。
            false（默认值）不强制开启。

    是否返回搜索来源:
        该策略仅支持 DashScope 方式。通过enable_source配置，可选值：
        true 返回数据中包含搜索来源的信息。搜索来源信息通过search_info参数返回。
        false（默认值）  返回数据中不包含搜索来源的信息

    开启角标标注
        该策略仅支持 DashScope 方式。
        就像在写论文时在右上角用[i] 来标注引用的文献，角标标注可以在大模型的回复内容中标注引用来源。
        如果返回数据包含搜索来源的信息（enable_source为true），您可以通过enable_citation来配置是否开启角标标注功能。可选值：

        true  开启角标标注。
                角标标注的样式可以通过下方的citation_format参数设置。
        false（默认值） 不开启角标标注。

        在开启角标标注功能后，您可以通过citation_format配置角标样式。可选值：
        "[<number>]"（默认值）  角标形式为[i]。
        "[ref_<number>]"       角标形式为[ref_i]。

        搜索数量
        
"""

import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
    {'role': 'user', 'content': '哪吒2的票房'}
]

response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    # 此处以qwen-plus-2025-04-28为例，可按需更换为支持联网搜索的模型
    model="qwen-plus-2025-04-28",  
    messages=messages,
    # 开启深度思考的参数，对 qwen3-30b-a3b-thinking-2507 、qwen3-235b-a22b-thinking-2507、QwQ 、DeepSeek-R1 模型无效
    enable_thinking = True,
    enable_search = True, # 开启联网搜索的参数
    search_options = {
        "forced_search": True, # 强制开启联网搜索
        "enable_source": True, # 使返回结果包含搜索来源的信息，OpenAI 兼容方式暂不支持返回
        "enable_citation": True, # 开启角标标注功能
        "citation_format": "[ref_<number>]", # 角标形式为[ref_i]
        "search_strategy": "pro" # 模型将搜索10条互联网信息
    },
    stream=True,
    incremental_output=True,
    result_format="message",
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
# 判断是否为第一个chunk，便于打印搜索信息
is_first_chunk = True

print("=" * 20 + "搜索信息" + "=" * 20)

for chunk in response:
    if is_first_chunk:
        search_results = chunk.output.search_info["search_results"]
        for web in search_results:
            print(f"[{web['index']}]: [{web['title']}]({web['url']})")
        print("=" * 20 + "思考过程" + "=" * 20)
        reasoning_content += chunk.output.choices[0].message.reasoning_content
        print(chunk.output.choices[0].message.reasoning_content,end="",flush=True)
        is_first_chunk = False
    else:
        # 如果思考过程与回复皆为空，则忽略
        if (chunk.output.choices[0].message.content == "" and 
            chunk.output.choices[0].message.reasoning_content == ""):
            pass
        else:
            # 如果当前为思考过程
            if (chunk.output.choices[0].message.reasoning_content != "" and 
                chunk.output.choices[0].message.content == ""):
                print(chunk.output.choices[0].message.reasoning_content, end="",flush=True)
                reasoning_content += chunk.output.choices[0].message.reasoning_content
            # 如果当前为回复
            elif chunk.output.choices[0].message.content != "":
                if not is_answering:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                    is_answering = True
                print(chunk.output.choices[0].message.content, end="",flush=True)
                answer_content += chunk.output.choices[0].message.content

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
# 如果您需要打印本次请求的 Token 消耗，请将以下代码解除注释后运行
# print("\n"+"="*20+"Token 消耗"+"="*20)
# print(chunk.usage)