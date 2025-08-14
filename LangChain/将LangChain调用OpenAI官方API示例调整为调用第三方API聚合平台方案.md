#  LangChain 调用 OpenAI 官方 API

##  要将 LangChain 调用 OpenAI 官方 API 的示例调整为调用第三方 API 聚合平台，主要需要修改 API 的基础 URL（endpoint）和对应的 API 密钥，具体操作如下：
  - 1. 首先获取第三方平台提供的 API 基础 URL（通常与 OpenAI 官方不同）
  - 2. 使用第三方平台提供的 API 密钥替换原有的 OpenAI 密钥
  - 3. 在初始化模型 / 嵌入时指定新的基础 URL

## OpenAIEmbeddings 调整后的示例代码如下：
```python
    import getpass
    import os

    # 1. 替换为第三方平台的API密钥环境变量
    if "THIRD_PARTY_API_KEY" not in os.environ:
        os.environ["THIRD_PARTY_API_KEY"] = getpass.getpass("第三方平台API Key:")

    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_openai import OpenAIEmbeddings

    # 2. 配置第三方平台的API基础URL和密钥
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.environ["THIRD_PARTY_API_KEY"],
        openai_api_base="https://第三方平台API基础地址/v1"  # 替换为实际的第三方API地址
    )

    # 3. 后续使用方式保持不变
    vector_store = InMemoryVectorStore.from_documents(pages, embeddings)
    docs = vector_store.similarity_search("What is LayoutParser?", k=2)
    for doc in docs:
        print(f"Page {doc.metadata['page']}: {doc.page_content[:300]}\n")
```

## 如果使用的是 LLM 模型（如 ChatOpenAI），修改方式类似：  
```python  
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        openai_api_key=os.environ["DMXAPI_API_KEY"],
        openai_api_base="https://www.dmxapi.cn/v1",  # 第三方平台地址
        model_name="gpt-3.5-turbo"  # 确认第三方平台支持的模型名称
    )
```

```python 
    from langchain_openai import ChatOpenAI
    import os

    api_key_temp = os.getenv("DMXAPI_API_KEY")
    print("DMXAPI Key:", api_key_temp)

    model = ChatOpenAI(
        model="gpt-4o-mini",
        base_url="https://www.dmxapi.cn/v1",
        api_key=api_key_temp,  # 替换成你的 DMXapi 令牌key
    )
    text = "周树人和鲁迅是兄弟吗？"
    print(model.invoke(text))
```

或另一种方式
```python  
    from langchain.chat_models import init_chat_model

    llm = init_chat_model(
        model="gpt-4o-mini", 
        api_key =os.environ["DMXAPI_API_KEY"],
        base_url="https://www.dmxapi.cn/v1",
        model_provider="openai",  # 使用 OpenAI 模型提供者)
        )
```

## 注意事项：
不同第三方平台的 API 基础 URL 格式可能不同，需按照平台提供的文档填写
确认第三方平台支持的模型名称，可能与官方名称一致或有差异
部分平台可能需要额外的认证参数，需根据其文档进行补充配置
建议先通过简单的 API 调用测试第三方平台的连通性，再集成到 LangChain 中    