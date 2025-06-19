"""
    How to stream runnables   https://python.langchain.com/docs/how_to/streaming/
"""
import getpass
import os

# 设置 DashScope API Key
if not os.environ.get("DMXAPI_API_KEY"):
    os.environ["DMXAPI_API_KEY"] = getpass.getpass("Enter API key for DMXAPI_API_KEY: ")

# 导入阿里云模型模块
from langchain.chat_models import init_chat_model

# 初始化 Qwen-Plus 模型
llm = init_chat_model(
    model="qwen-plus", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

# Let's start with the sync stream API:
chunks = []
for chunk in llm.stream("what color is the sky?"):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)

# Alternatively, if you're working in an async environment, 
# you may consider using the async astream API:
# Alternatively, if you're working in an async environment, 
# you may consider using the async astream API:
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
chain = prompt | llm | parser

async for chunk in chain.astream({"topic": "parrot"}):
    print(chunk, end="|", flush=True)


# Non-streaming components
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho", "harrison likes spicy food"],
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

chunks = [chunk for chunk in retriever.stream("where did harrison work?")]
chunks


