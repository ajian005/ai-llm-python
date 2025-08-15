"""
  How to create and query vector stores: https://python.langchain.com/docs/how_to/vectorstores/
"""

""" Get started """
import os
import getpass

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Load the document, split it into chunks, embed each chunk and load it into the vector store.
raw_documents = TextLoader('state_of_the_union.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

""" Chroma """
# pip install langchain-chroma
from langchain_chroma import Chroma
db = Chroma.from_documents(documents, OpenAIEmbeddings())

""" pip install faiss-cpu """
# pip install faiss-cpu
from langchain_community.vectorstores import FAISS
db = FAISS.from_documents(documents, OpenAIEmbeddings())

""" lancedb """
# pip install lancedb
from langchain_community.vectorstores import LanceDB
import lancedb
import asyncio
db = lancedb.connect("/tmp/lancedb")
table = db.create_table(
    "my_table",
    data=[
        {
            "vector": embeddings.embed_query("Hello World"),
            "text": "Hello World",
            "id": "1",
        }
    ],
    mode="overwrite",
)
db = LanceDB.from_documents(documents, OpenAIEmbeddings())

""" Similarity search """
# All vectorstores expose a similarity_search method. This will take incoming documents, create an embedding of them, and then find all documents with the most similar embedding.
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
print(docs[0].page_content)


""" Similarity search by vector """
# It is also possible to do a search for documents similar to a given embedding vector using similarity_search_by_vector which accepts an embedding vector as a parameter instead of a string.
embedding_vector = OpenAIEmbeddings().embed_query(query)
docs = db.similarity_search_by_vector(embedding_vector)
print(docs[0].page_content)


""" Async Operations """
async def perform_async_search():
    global docs
    docs = await db.asimilarity_search(query)
asyncio.run(perform_async_search())
