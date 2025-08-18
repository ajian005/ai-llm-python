"""
 How to use the LangChain indexing API : https://python.langchain.com/docs/how_to/indexing/

 The indexing API lets you load and keep in sync documents from any source into a vector store. Specifically, it helps:
    Avoid writing duplicated content into the vector store
    Avoid re-writing unchanged content
    Avoid re-computing embeddings over unchanged content
"""

from langchain.indexes import SQLRecordManager, index
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

collection_name = "test_index"

embedding = OpenAIEmbeddings()

vectorstore = ElasticsearchStore(
    es_url="http://localhost:9200", index_name="test_index", embedding=embedding
)

namespace = f"elasticsearch/{collection_name}"
record_manager = SQLRecordManager(
    namespace, db_url="sqlite:///record_manager_cache.sql"
)
record_manager.create_schema()

doc1 = Document(page_content="kitty", metadata={"source": "kitty.txt"})
doc2 = Document(page_content="doggy", metadata={"source": "doggy.txt"})

def _clear():
    """Hacky helper method to clear content. See the `full` mode section to understand why it works."""
    index([], record_manager, vectorstore, cleanup="full", source_id_key="source")

""""Source"""
