"""
  How to create custom callback handlers :  https://python.langchain.com/docs/how_to/custom_callbacks/
"""

""" ============================= Runnable Lambdas and Generators ============================= """
from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")


prompt = ChatPromptTemplate.from_messages(["Tell me a joke about {animal}"])

# To enable streaming, we pass in `streaming=True` to the ChatModel constructor
# Additionally, we pass in our custom handler as a list to the callbacks parameter
model = ChatAnthropic(
    model="claude-3-7-sonnet-20250219", streaming=True, callbacks=[MyCustomHandler()]
)

chain = prompt | model

response = chain.invoke({"animal": "bears"})

