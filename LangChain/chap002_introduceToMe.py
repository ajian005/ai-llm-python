import getpass
import os

if not os.environ.get("ALIYUN_API_KEY"):  # 修改环境变量名称
    os.environ["ALIYUN_API_KEY"] = getpass.getpass("Enter API key for Tongyi Qianwen: ")

from langchain_community.llms import Tongyi  # 修改导入语句

# 初始化通义千问LLM
llm = Tongyi(
    model='qwen-turbo',  # 使用阿里云通义千问模型
    api_key=os.environ.get("ALIYUN_API_KEY"),
    temperature=0.9,
)


from typing import Optional

from pydantic import BaseModel, Field


# Pydantic
class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )


structured_llm = llm.with_structured_output(Joke)

structured_llm.invoke("Tell me a joke about cats")