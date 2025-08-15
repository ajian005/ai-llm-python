"""
  Caching (caching_embeddings) : https://python.langchain.com/docs/how_to/caching_embeddings/
"""

import getpass
import os
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


# 2. 配置第三方平台的API基础URL和密钥
embeddings_model = OpenAIEmbeddings(
                        openai_api_key=os.environ["DMXAPI_API_KEY"],
                        openai_api_base="https://www.dmxapi.cn/v1",  # 第三方平台地址
                        model="text-embedding-3-large",
                    )

store = LocalFileStore("./cache/")

cached_embedder = embeddings_model.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)

list(store.yield_keys())

raw_documents = TextLoader("state_of_the_union.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

db = FAISS.from_documents(documents, cached_embedder)

list(store.yield_keys())[:5]

from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import InMemoryByteStore

store = InMemoryByteStore()

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)