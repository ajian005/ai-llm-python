"""
  How to get log probabilities : hhttps://python.langchain.com/docs/how_to/logprobs/
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

llm = ChatOpenAI(
    model="qwen-plus",     # model="yi-large",
    temperature=0.3,
    max_tokens=200,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1").bind(logprobs=True)
msg = llm.invoke(("human", "how are you today"))
result = msg.response_metadata["logprobs"]["content"][:5] 
print(result)


ct = 0
full = None
for chunk in llm.stream(("human", "how are you today")):
    if ct < 5:
        full = chunk if full is None else full + chunk
        if "logprobs" in full.response_metadata:
            print(full.response_metadata["logprobs"]["content"])
    else:
        break
    ct += 1