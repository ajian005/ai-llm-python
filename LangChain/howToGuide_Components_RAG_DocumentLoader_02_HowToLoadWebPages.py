"""
How to load web pages: https://python.langchain.com/docs/how_to/document_loader_web/
"""

""" Simple and fast text extraction """
import bs4
from langchain_community.document_loaders import WebBaseLoader
import asyncio

page_url = "https://python.langchain.com/docs/how_to/chatbots_memory/"
loader = WebBaseLoader(web_paths=[page_url])
docs = []
for doc in loader.lazy_load():
    docs.append(doc)

assert len(docs) == 1
doc = docs[0]

print(f"{doc.metadata}\n")
print(doc.page_content[:500].strip())


loader = WebBaseLoader(
    web_paths=[page_url],
    bs_kwargs={
        "parse_only": bs4.SoupStrainer(class_="theme-doc-markdown markdown"),
    },
    bs_get_text_kwargs={"separator": " | ", "strip": True},
)

docs = []
async def load_docs():
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)
    return docs

docs = asyncio.run(load_docs())

assert len(docs) == 1
doc = docs[0]

""" Advanced parsing """
from langchain_unstructured import UnstructuredLoader

page_url = "https://python.langchain.com/docs/how_to/chatbots_memory/"
loader = UnstructuredLoader(web_url=page_url)

docs = []
async def load_docs():
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)

docs = asyncio.run(load_docs())
for doc in docs[:5]:
    print(doc.page_content)

""" Extracting content from specific sections """
for doc in docs[:5]:
    print(f"{doc.metadata['category']}: {doc.page_content}")

from typing import List

from langchain_core.documents import Document


async def _get_setup_docs_from_url(url: str) -> List[Document]:
    loader = UnstructuredLoader(web_url=url)

    setup_docs = []
    parent_id = -1
    async for doc in loader.alazy_load():
        if doc.metadata["category"] == "Title" and doc.page_content.startswith("Setup"):
            parent_id = doc.metadata["element_id"]
        if doc.metadata.get("parent_id") == parent_id:
            setup_docs.append(doc)

    return setup_docs


page_urls = [
    "https://python.langchain.com/docs/how_to/chatbots_memory/",
    "https://python.langchain.com/docs/how_to/chatbots_tools/",
]
setup_docs = []
for url in page_urls:
    page_setup_docs = asyncio.run(_get_setup_docs_from_url(url))
    setup_docs.extend(page_setup_docs)

from collections import defaultdict

setup_text = defaultdict(str)

for doc in setup_docs:
    url = doc.metadata["url"]
    setup_text[url] += f"{doc.page_content}\n"
dict(setup_text)

## Vector search over page content
import getpass
import os

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

vector_store = InMemoryVectorStore.from_documents(setup_docs, OpenAIEmbeddings())
retrieved_docs = vector_store.similarity_search("Install Tavily", k=2)
for doc in retrieved_docs:
    print(f"Page {doc.metadata['url']}: {doc.page_content[:300]}\n")

