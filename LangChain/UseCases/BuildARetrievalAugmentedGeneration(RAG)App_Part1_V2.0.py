"""
  Build a Retrieval Augmented Generation (RAG) App: Part 1: https://python.langchain.com/docs/tutorials/rag/
"""

"""  Setup LangSmith """

"""  Setup ----> LangSmith """
'''
配置文档设置
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
'''
import os

os.environ["LANGSMITH_PROJECT"]  =  "pr-indelible-mill-79"
os.environ["LANGSMITH_TRACING"]  =  "true"
os.environ["LANGSMITH_API_KEY"]  =  "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" # getpass.getpass()
os.environ["LANGSMITH_ENDPOINT"] =  "https://api.smith.langchain.com"

"""  Components  """

"""  Components ---> Select OpenAI chat model """
from langchain.chat_models import init_chat_model

from typing import Annotated
from typing import Literal



# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

"""  Components ---> Select OpenAI embeddings model """
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ["DMXAPI_API_KEY"],
    openai_api_base="https://www.dmxapi.cn/v1",  # 第三方平台地址
    model="text-embedding-3-large",
)

"""  Components ---> Select In-memory vector store """
from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)


""" Preview """
import bs4
from  langchain  import hub
from  langchain_community.document_loaders  import WebBaseLoader
from  langchain_core.documents import Document
from  langchain_text_splitters import RecursiveCharacterTextSplitter
from  langgraph.graph import START, StateGraph
from  typing_extensions import List, TypedDict

# Load and chunk contents of the blog
# Only keep post title, headers, and content from the full HTML.

# Loading documents
bs4_strainer = bs4.SoupStrainer(
    class_=("post-content", "post-title", "post-header")
)
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
)
docs = loader.load()
assert len(docs) == 1
print(f"Total characters: {len(docs[0].page_content)}")
print(docs[0].page_content[:500])

# Splitting documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,    # chunk size (characters)
                                               chunk_overlap=200,  # chunk overlap (characters)
                                               add_start_index=True,  # track index in original document
                                               )
all_splits = text_splitter.split_documents(docs)
print(f"Split blog post into {len(all_splits)} sub-documents.")


# Update metadata (illustration purposes)
total_documents = len(all_splits)
third = total_documents // 3

for i, document in enumerate(all_splits):
    if i < third:
        document.metadata["section"] = "beginning"
    elif i < 2 * third:
        document.metadata["section"] = "middle"
    else:
        document.metadata["section"] = "end"


# Index chunks
# Storing documents
document_ids = vector_store.add_documents(documents=all_splits)
print(document_ids[:3])



# Define prompt for question-answering
# N.B. for non-US LangSmith endpoints, you may need to specify
# api_url="https://api.smith.langchain.com" in hub.pull.
prompt = hub.pull("rlm/rag-prompt")
example_messages = prompt.invoke({"context": "(context goes here)", "question": "(question goes here)"}).to_messages()

assert len(example_messages) == 1
print(example_messages[0].content)


# Define schema for search
class Search(TypedDict):
    """Search query."""

    query: Annotated[str, "Search query to run."]
    section: Annotated[
        Literal["beginning", "middle", "end"],
        ...,
        "Section to query.",
    ]

# Define state for application
class State(TypedDict):
    question: str
    query: Search
    context: List[Document]
    answer: str

def analyze_query(state: State):
    structured_llm = llm.with_structured_output(Search)
    query = structured_llm.invoke(state["question"])
    return {"query": query}

# Define application steps
def retrieve(state: State):
    query = state["query"]
    retrieved_docs = vector_store.similarity_search(state["question"],
        filter=lambda doc: doc.metadata.get("section")  == query["section"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# LangGraph:Compile application and test
graph_builder = StateGraph(State).add_sequence([analyze_query, retrieve, generate])
graph_builder.add_edge(START, "analyze_query")
graph = graph_builder.compile()

from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

response = graph.invoke({"question": "What is Task Decomposition?"})
print(response["answer"])

print(f"Context: {response['context']}\n\n")
print(f"Answer: {response['answer']}")

# Stream steps:
for step in graph.stream(
    {"question": "What is Task Decomposition?"}, stream_mode="updates"
):
    print(f"{step}\n\n----------------\n")

# Stream tokens:
for message, metadata in graph.stream(
    {"question": "What is Task Decomposition?"}, stream_mode="messages"
):
    print(message.content, end="|")

