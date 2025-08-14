"""
  How to load Markdown : https://python.langchain.com/docs/how_to/document_loader_markdown/
"""

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document

markdown_path = "../../../README.md"
loader = UnstructuredMarkdownLoader(markdown_path)

data = loader.load()
assert len(data) == 1
assert isinstance(data[0], Document)
readme_content = data[0].page_content
print(readme_content[:250])

# Retain Elements
loader = UnstructuredMarkdownLoader(markdown_path, mode="elements")
data = loader.load()
print(f"Number of documents: {len(data)}\n")
for document in data[:2]:
    print(f"{document}\n")

print(set(document.metadata["category"] for document in data))


