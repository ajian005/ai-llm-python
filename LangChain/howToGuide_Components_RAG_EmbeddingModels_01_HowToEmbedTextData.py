"""
  Text embedding models : https://python.langchain.com/docs/how_to/embed_text/
"""

import getpass
import os
from langchain_openai import OpenAIEmbeddings

# 2. 配置第三方平台的API基础URL和密钥
embeddings_model = OpenAIEmbeddings(
                        openai_api_key=os.environ["DMXAPI_API_KEY"],
                        openai_api_base="https://www.dmxapi.cn/v1",  # 第三方平台地址
                        model="text-embedding-3-large",
                    )

"""embed_documents"""
embeddings = embeddings_model.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ]
)
print("len(embeddings)", len(embeddings))
print("len(embeddings)",len(embeddings[0]))

"""embed_query"""
embedded_query = embeddings_model.embed_query("What was the name mentioned in the conversation?")
result = embedded_query[:5]
print(result)

