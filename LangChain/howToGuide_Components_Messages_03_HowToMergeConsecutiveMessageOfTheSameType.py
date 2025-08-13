"""
   How to merge consecutive messages of the same type  https://python.langchain.com/docs/how_to/merge_message_runs/
"""

""" Basic usage """
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    merge_message_runs,
)

messages = [
    SystemMessage("you're a good assistant."),
    SystemMessage("you always respond with a joke."),
    HumanMessage([{"type": "text", "text": "i wonder why it's called langchain"}]),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        'Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!'
    ),
    AIMessage("Why, he's probably chasing after the last cup of coffee in the office!"),
]

merged = merge_message_runs(messages)
print("\n\n".join([repr(x) for x in merged]))

# Chaining
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=0)
# Notice we don't pass in messages. This creates
# a RunnableLambda that takes messages as input
merger = merge_message_runs()
chain = merger | llm
chain.invoke(messages)


# merge_message_runs can also be placed after a prompt:
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate(
    [
        ("system", "You're great a {skill}"),
        ("system", "You're also great at explaining things"),
        ("human", "{query}"),
    ]
)
chain = prompt | merger | llm
chain.invoke({"skill": "math", "query": "what's the definition of a convergent series"})

