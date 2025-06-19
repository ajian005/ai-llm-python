'''
    langchain 入门指南 - 让 AI 从互联网获取信息 https://developer.aliyun.com/article/1586872?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.22.62b72f3dt8keK5
'''
from langchain.chains.llm import LLMChain
from langchain_community.chains.llm_requests import LLMRequestsChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os


llm = ChatOpenAI(
    model="qwen-plus",     # model="yi-large",
    temperature=0.3,
    max_tokens=200,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
def query_baidu(question):
    template = """
    在 >>> 和 <<< 之间是从百度搜索结果中提取的原始文本。
    提取问题 '{query}' 的答案或者说 "not found" 如果信息不包含在内。
    >>> {requests_result} <<<
    """
    prompt = PromptTemplate(
        input_variables=["query", "requests_result"],
        template=template
    )
    inputs = {
        'query': question,
        'url': "https://www.baidu.com/s?wd=" + question.replace(" ", "+"),
    }
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    request_chain = LLMRequestsChain(llm_chain=llm_chain, output_key="query_info")
    return request_chain.invoke(inputs)
print(query_baidu("今天北京天气？"))