"""
    大模型服务平台-->百炼用户指南（模型）--> 向量化 --> 文本与多模态向量化 : https://help.aliyun.com/zh/model-studio/embedding

    向量化模型能够将文本、图像和视频数据转化为数值向量，并用于后续的语义搜索、推荐、聚类、分类、异常检测等任务。

模型选择
    选择合适的模型取决于您的输入数据类型和应用场景。

    处理纯文本或代码：推荐使用 text-embedding-v4。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。

    处理多模态内容：对于包含图像、文本或视频的混合内容，可以选择针对视觉能力进行优化提升的 tongyi-embedding-vision-plus 与 tongyi-embedding-vision-flash或通用多模态模型multimodal-embedding-v1。

    处理大规模数据：若您需要处理大规模、非实时的文本数据，建议使用 text-embedding-v4 并结合 OpenAI兼容-Batch调用，以显著降低成本。


    ====
    文本聚类
        通过分析向量间的距离，将相似的文本自动分组。
"""
# 需要安装 scikit-learn: pip install scikit-learn
import dashscope
import numpy as np
from sklearn.cluster import KMeans


def cluster_texts(texts, n_clusters=2):
    """将一组文本进行聚类"""
    # 1. 获取所有文本的向量
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v4",
        input=texts,
        dimension=1024
    )
    embeddings = np.array([item['embedding'] for item in resp.output['embeddings']])

    # 2. 使用KMeans算法进行聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(embeddings)

    # 3. 整理并返回结果
    clusters = {i: [] for i in range(n_clusters)}
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(texts[i])
    return clusters


# 使用示例
documents_to_cluster = [
    "手机公司A发售新款手机",
    "搜索引擎公司B推出新款系统",
    "世界杯决赛阿根廷对阵法国",
    "奥运会中国队再添一金",
    "某公司发布最新AI芯片",
    "欧洲杯赛事报道"
]
clusters = cluster_texts(documents_to_cluster, n_clusters=2)
for cluster_id, docs in clusters.items():
    print(f"--- 类别 {cluster_id} ---")
    for doc in docs:
        print(f"- {doc}")