"""
   How to filter messages  https://python.langchain.com/docs/how_to/filter_messages/
"""

""" Basic usage """
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    filter_messages,
)

messages = [
    SystemMessage("you are a good assistant", id="1"),
    HumanMessage("example input", id="2", name="example_user"),
    AIMessage("example output", id="3", name="example_assistant"),
    HumanMessage("real input", id="4", name="bob"),
    AIMessage("real output", id="5", name="alice"),
]

result = filter_messages(messages, include_types=["human"])
print(result)

result2 = filter_messages(messages, exclude_names=["example_user", "example_assistant"])
print(result2)


result3 = filter_messages(messages, include_types=[HumanMessage, AIMessage], exclude_ids=["3"])
print(result3)


""" Chaining """
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=0)
# Notice we don't pass in messages. This creates
# a RunnableLambda that takes messages as input
filter_ = filter_messages(exclude_names=["example_user", "example_assistant"])
chain = filter_ | llm
chain.invoke(messages)


