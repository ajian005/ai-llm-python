"""
    大模型服务平台-->百炼用户指南（模型）--> 向量化 --> 文本与多模态向量化 : https://help.aliyun.com/zh/model-studio/embedding

    向量化模型能够将文本、图像和视频数据转化为数值向量，并用于后续的语义搜索、推荐、聚类、分类、异常检测等任务。

模型选择
    选择合适的模型取决于您的输入数据类型和应用场景。

    处理纯文本或代码：推荐使用 text-embedding-v4。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。

    处理多模态内容：对于包含图像、文本或视频的混合内容，可以选择针对视觉能力进行优化提升的 tongyi-embedding-vision-plus 与 tongyi-embedding-vision-flash或通用多模态模型multimodal-embedding-v1。

    处理大规模数据：若您需要处理大规模、非实时的文本数据，建议使用 text-embedding-v4 并结合 OpenAI兼容-Batch调用，以显著降低成本。


    ====
    推荐系统 ： 通过分析用户历史行为向量，发现用户的兴趣偏好并推荐相似物品。。
    需要埋点数据，  如用户ID、物品ID、行为类型、行为时间等。
    关键点: 前端传用户标识，根据用户标识找到用户历史行为记录，将历史行为记录转换为向量表示，计算用户偏好向量（很多策略:如取平均），生成所有物品向量，计算推荐分数（余弦相似度），排序并返回推荐结果。

"""
import dashscope
import numpy as np
from dashscope import TextEmbedding

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def build_recommendation_system(user_history, all_items, top_k=10):
    """构建推荐系统"""
    # 生成用户历史向量
    history_resp = TextEmbedding.call(
        model="text-embedding-v4",
        input=user_history,
        dimension=1024
    )

    # 计算用户偏好向量（取平均）
    user_embedding = np.mean([
        emb['embedding'] for emb in history_resp.output['embeddings']
    ], axis=0)

    # 生成所有物品向量
    items_resp = TextEmbedding.call(
        model="text-embedding-v4",
        input=all_items,
        dimension=1024
    )

    # 计算推荐分数
    recommendations = []
    for i, item_emb in enumerate(items_resp.output['embeddings']):
        score = cosine_similarity(user_embedding, item_emb['embedding'])
        recommendations.append((all_items[i], score))

    # 排序并返回推荐结果
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_k]

# 使用示例 
#  (user_action_history: 用户历史行为是用户访问的电影信息)
user_history = ["科幻类", "动作类", "悬疑类"]
all_movies = ["未来世界", "太空探险", "古代战争", "浪漫之旅", "超级英雄"]
recommendations = build_recommendation_system(user_history, all_movies)
for movie, score in recommendations:
    print(f"推荐分数: {score:.3f}, 电影: {movie}")