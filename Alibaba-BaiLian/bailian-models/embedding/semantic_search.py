"""
    大模型服务平台-->百炼用户指南（模型）--> 向量化 --> 文本与多模态向量化 : https://help.aliyun.com/zh/model-studio/embedding

    向量化模型能够将文本、图像和视频数据转化为数值向量，并用于后续的语义搜索、推荐、聚类、分类、异常检测等任务。

模型选择
    选择合适的模型取决于您的输入数据类型和应用场景。

    处理纯文本或代码：推荐使用 text-embedding-v4。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。

    处理多模态内容：对于包含图像、文本或视频的混合内容，可以选择针对视觉能力进行优化提升的 tongyi-embedding-vision-plus 与 tongyi-embedding-vision-flash或通用多模态模型multimodal-embedding-v1。

    处理大规模数据：若您需要处理大规模、非实时的文本数据，建议使用 text-embedding-v4 并结合 OpenAI兼容-Batch调用，以显著降低成本。


    ====
    语义搜索: 通过计算查询与文档之间的向量相似度，实现精准的语义匹配。

"""
import dashscope
import numpy as np
from dashscope import TextEmbedding

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_search(query, documents, top_k=5):
    """语义搜索"""
    # 生成查询向量
    query_resp = TextEmbedding.call(
        model="text-embedding-v4",
        input=query,
        dimension=1024
    )
    query_embedding = query_resp.output['embeddings'][0]['embedding']

    # 生成文档向量
    doc_resp = TextEmbedding.call(
        model="text-embedding-v4",
        input=documents,
        dimension=1024
    )

    # 计算相似度
    similarities = []
    for i, doc_emb in enumerate(doc_resp.output['embeddings']):
        similarity = cosine_similarity(query_embedding, doc_emb['embedding'])
        similarities.append((i, similarity))

    # 排序并返回top_k结果
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [(documents[i], sim) for i, sim in similarities[:top_k]]

# 使用示例
documents = [
    "人工智能是计算机科学的一个分支",
    "机器学习是实现人工智能的重要方法",
    "深度学习是机器学习的一个子领域"
]
query = "什么是AI？"
results = semantic_search(query, documents, top_k=2)
for doc, sim in results:
    print(f"相似度: {sim:.3f}, 文档: {doc}")
    