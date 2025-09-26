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

from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""  # 定义完整回复
is_answering = False  # 判断是否结束思考过程并开始回复

# 创建聊天完成请求
completion = client.chat.completions.create(
    # 此处以qwen-plus-2025-04-28为例，可更换为其它支持联网搜索的深度思考模型
    model="qwen-plus-2025-04-28",
    messages=[{"role": "user", "content": "哪吒2的票房"}],
    extra_body={
        # 开启深度思考的参数，对 qwen3-30b-a3b-thinking-2507 、qwen3-235b-a22b-thinking-2507、QwQ、DeepSeek-R1 模型无效
        "enable_thinking": True,
        "enable_search": True,  # 开启联网搜索的参数
        "search_options": {
            "forced_search": True,  # 强制联网搜索的参数
            "search_strategy": "pro",  # 模型将搜索10条互联网信息
        },
    },
    # QwQ 模型仅支持流式输出方式调用
    stream=True,
    # 解除以下注释会在最后一个chunk返回Token使用量
    stream_options={"include_usage": True},
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\n" + "=" * 20 + "Usage" + "=" * 20)
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, "reasoning_content") and delta.reasoning_content != None:
            print(delta.reasoning_content, end="", flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end="", flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)