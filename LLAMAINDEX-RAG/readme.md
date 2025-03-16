# RAG项目实战(使用llamaindex构建自己的知识库) 
- 1.环境配置
- 2.下载Sentence Transformer 模型 
- 3.下载InternLM2 1.8B/qwen2.5_0.5B 模型 
- 4.创建知识库
- 5.创建web应用


# 1.环境配置
使用 conda 配置项目python环境

```shell
# 创建环境
conda create -n rag python=3.10
# 激活环境
conda activate rag
# 安装一些必要的库(requirements.txt在项目代码包中) 
pip install -r requirements.txt
```

# 2.下载Sentence Transformer 模型 

在进行RAG之前，需要使用词向量模型进行Embedding，将文本进行向量化处理，此处选择 Sentence
Transformer 模型。

执行 llamindex_demo/download_hf.py下载。



# 3.下载InternLM2 1.8B/qwen2.5_0.5B 模型 

 执行llamindex_demo/download_internlm1.8_chat.py下载。


 执行llamindex_demo/llamaindex_internlm.py进行提问测试，得到结果如下。
 可以看出模型本身并不 具备关于 xtuner 的相关知识，回复也比较杂乱。


# 4.创建知识库
在 llamindex_demo 文件夹下，创建 data 文件夹，用于构建知识库。

 执行llamindex_demo/llamaindex_RAG.py，运行次测试后，可以看到可以正确回答，并且可以给出回 答的出处:


# 5.创建web应用

 执行llamindex_demo/app.py
```shell
streamlit run app.py
```

运行后可以打开网页端，可以进行提问:
http://localhost:8501/

