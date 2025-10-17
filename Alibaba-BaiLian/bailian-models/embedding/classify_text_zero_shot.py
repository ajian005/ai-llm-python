"""
    大模型服务平台-->百炼用户指南（模型）--> 向量化 --> 文本与多模态向量化 : https://help.aliyun.com/zh/model-studio/embedding

    向量化模型能够将文本、图像和视频数据转化为数值向量，并用于后续的语义搜索、推荐、聚类、分类、异常检测等任务。

模型选择
    选择合适的模型取决于您的输入数据类型和应用场景。

    处理纯文本或代码：推荐使用 text-embedding-v4。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。

    处理多模态内容：对于包含图像、文本或视频的混合内容，可以选择针对视觉能力进行优化提升的 tongyi-embedding-vision-plus 与 tongyi-embedding-vision-flash或通用多模态模型multimodal-embedding-v1。

    处理大规模数据：若您需要处理大规模、非实时的文本数据，建议使用 text-embedding-v4 并结合 OpenAI兼容-Batch调用，以显著降低成本。


    ====
    文本分类
        通过计算输入文本与预定义标签的向量相似度，实现在没有预先标记的示例的情况下，对新类别进行识别和分类。

"""

import dashscope
import numpy as np


def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def classify_text_zero_shot(text, labels):
    """零样本文本分类"""
    # 1. 获取输入文本和所有标签的向量
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v4",
        input=[text] + labels,
        dimension=1024
    )
    embeddings = resp.output['embeddings']
    text_embedding = embeddings[0]['embedding']
    label_embeddings = [emb['embedding'] for emb in embeddings[1:]]

    # 2. 计算与每个标签的相似度
    scores = [cosine_similarity(text_embedding, label_emb) for label_emb in label_embeddings]

    # 3. 返回相似度最高的标签
    best_match_index = np.argmax(scores)
    return labels[best_match_index], scores[best_match_index]


# 使用示例
text_to_classify = "这件衣服的料子很舒服，款式也好看"
possible_labels = ["数码产品", "服装配饰", "食品饮料", "家居生活"]

label, score = classify_text_zero_shot(text_to_classify, possible_labels)
print(f"输入文本: '{text_to_classify}'")
print(f"最匹配的分类是: '{label}' (相似度: {score:.3f})")