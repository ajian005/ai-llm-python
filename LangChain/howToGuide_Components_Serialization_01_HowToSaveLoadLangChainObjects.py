"""
  How to save and load LangChain objects :  https://python.langchain.com/docs/how_to/serialization/
"""

from langchain_core.load import dumpd, dumps, load, loads
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Translate the following into {language}:"),
        ("user", "{text}"),
    ],
)

# llm = ChatOpenAI(model="gpt-4o-mini", api_key="llm-api-key")
# 导入阿里云模型模块
from langchain.chat_models import init_chat_model

# 初始化 Qwen-Plus 模型
llm = init_chat_model(
    model="qwen-plus", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)


chain = prompt | llm

""" ============================= Saving objects -->  To json ============================= """
string_representation = dumps(chain, pretty=True)
print(string_representation[:500])

""" ============================= Saving objects -->  To a json-serializable Python dict ============================= """
dict_representation = dumpd(chain)
print(type(dict_representation))

""" ============================= Saving objects -->  To disk ============================= """
import json
with open("./tmp/chain.json", "w") as fp:
    json.dump(string_representation, fp)


""" ============================= Loading objects -->  From string ============================= """
chain = loads(string_representation, secrets_map={"OPENAI_API_KEY": "llm-api-key"})

""" ============================= Loading objects -->  From dict ============================= """
chain = load(dict_representation, secrets_map={"OPENAI_API_KEY": "llm-api-key"})

""" ============================= Loading objects -->  From disk ============================= """
with open("/tmp/chain.json", "r") as fp:
    chain = loads(json.load(fp), secrets_map={"OPENAI_API_KEY": "llm-api-key"})
