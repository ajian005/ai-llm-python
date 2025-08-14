"""
How to load documents from a directory: https://python.langchain.com/docs/how_to/document_loader_directory/
"""

from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("../", glob="**/*.md")
docs = loader.load()
len(docs)

print(docs[0].page_content[:100])

# Show a progress bar
loader = DirectoryLoader("../", glob="**/*.md", show_progress=True)
docs = loader.load()

# Use multithreading
loader = DirectoryLoader("../", glob="**/*.md", use_multithreading=True)
docs = loader.load()

# Change loader class
from langchain_community.document_loaders import TextLoader
loader = DirectoryLoader("../", glob="**/*.md", loader_cls=TextLoader)
docs = loader.load()

print(docs[0].page_content[:100])

from langchain_community.document_loaders import PythonLoader
loader = DirectoryLoader("../../../../../", glob="**/*.py", loader_cls=PythonLoader)

# Auto-detect file encodings with TextLoader
path = "../../../libs/langchain/tests/unit_tests/examples/"

loader = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader)

