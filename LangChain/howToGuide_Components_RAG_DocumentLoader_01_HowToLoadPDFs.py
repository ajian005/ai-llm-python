"""
How to load PDFs: https://python.langchain.com/docs/how_to/document_loader_pdf/
"""
from langchain_community.document_loaders import PyPDFLoader
import asyncio

import getpass
import os


file_path = (
    "/Users/lijianquan/Downloads/LayoutParser.pdf"
)


loader = PyPDFLoader(file_path)
pages = []
async def load_pdf():
    async for page in loader.alazy_load():
        pages.append(page)
asyncio.run(load_pdf())

print(f"{pages[0].metadata}\n")
print(pages[0].page_content)

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# 2. 配置第三方平台的API基础URL和密钥
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ["DMXAPI_API_KEY"],
    openai_api_base="https://www.dmxapi.cn/v1",  # 第三方平台地址
)

vector_store = InMemoryVectorStore.from_documents(pages, embeddings)
docs = vector_store.similarity_search("What is LayoutParser?", k=2)
print("=======================================================")
for doc in docs:
    print(f"Page {doc.metadata['page']}: {doc.page_content[:300]}\n")