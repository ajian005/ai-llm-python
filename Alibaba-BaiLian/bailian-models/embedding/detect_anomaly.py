"""
    大模型服务平台-->百炼用户指南（模型）--> 向量化 --> 文本与多模态向量化 : https://help.aliyun.com/zh/model-studio/embedding

    向量化模型能够将文本、图像和视频数据转化为数值向量，并用于后续的语义搜索、推荐、聚类、分类、异常检测等任务。

模型选择
    选择合适的模型取决于您的输入数据类型和应用场景。

    处理纯文本或代码：推荐使用 text-embedding-v4。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。

    处理多模态内容：对于包含图像、文本或视频的混合内容，可以选择针对视觉能力进行优化提升的 tongyi-embedding-vision-plus 与 tongyi-embedding-vision-flash或通用多模态模型multimodal-embedding-v1。

    处理大规模数据：若您需要处理大规模、非实时的文本数据，建议使用 text-embedding-v4 并结合 OpenAI兼容-Batch调用，以显著降低成本。


    =======
    异常检测
        通过计算文本向量与正常样本中心的向量相似度，识别出与常规模式显著不同的异常数据。

"""

import dashscope
import numpy as np


def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def detect_anomaly(new_comment, normal_comments, threshold=0.6):
    # 1. 向量化所有正常评论和新评论
    all_texts = normal_comments + [new_comment]
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v4",
        input=all_texts,
        dimension=1024
    )
    embeddings = [item['embedding'] for item in resp.output['embeddings']]

    # 2. 计算正常评论的中心向量（平均值）
    normal_embeddings = np.array(embeddings[:-1])
    normal_center_vector = np.mean(normal_embeddings, axis=0)

    # 3. 计算新评论与中心向量的相似度
    new_comment_embedding = np.array(embeddings[-1])
    similarity = cosine_similarity(new_comment_embedding, normal_center_vector)

    # 4. 判断是否为异常
    is_anomaly = similarity < threshold
    return is_anomaly, similarity


# 使用示例
normal_user_comments = [
    "今天的会议很有成效",
    "项目进展顺利",
    "下周发布新版本",
    "用户反馈良好"
]

test_comments = {
    "正常评论": "功能符合预期",
    "异常-无意义乱码": "asdfghjkl zxcvbnm",
    "异常-不相关": "某人骑车从甲地前往乙地, 前三分之一的路程平均速度是12km/h, 中间三分之一路程的平均速度是18km/h, 后三分之一路程的平均速度为  12 km/h ，此人全程的平均速度是",
    "异常-不相关":"100件商品中有两件次品，将其打包成10箱，每箱10件，则两件次品同一箱的概率为"
 
}



print("--- 异常检测示例 ---")
for desc, comment in test_comments.items():
    is_anomaly, score = detect_anomaly(comment, normal_user_comments)
    result = "是" if is_anomaly else "否"
    print(f"评论: '{comment}'")
    print(f"是否为异常: {result} (与正常样本相似度: {score:.3f})\n")