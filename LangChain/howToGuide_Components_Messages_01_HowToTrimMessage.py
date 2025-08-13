"""
  How to trim messages : https://python.langchain.com/docs/how_to/trim_messages/
"""

""" Trimming based on token count """
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    trim_messages,
)
from langchain_core.messages.utils import count_tokens_approximately

messages = [
    SystemMessage("you're a good assistant, you always respond with a joke."),
    HumanMessage("i wonder why it's called langchain"),
    AIMessage(
        'Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!'
    ),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        "Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!"
    ),
    HumanMessage("what do you call a speechless parrot"),
]


resultTrimeMessage = trim_messages(
    messages,
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    # Remember to adjust based on your model
    # or else pass a custom token_counter
    token_counter=count_tokens_approximately,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    # Remember to adjust based on the desired conversation
    # length
    max_tokens=45,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Most chat models expect that chat history ends with either:
    # (1) a HumanMessage or
    # (2) a ToolMessage
    end_on=("human", "tool"),
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
    allow_partial=False,
)

""" Trimming based on message count """
resultTrimeMessage2 = trim_messages(
    messages,
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    token_counter=len,
    # When token_counter=len, each message
    # will be counted as a single token.
    # Remember to adjust for your use case
    max_tokens=5,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Most chat models expect that chat history ends with either:
    # (1) a HumanMessage or
    # (2) a ToolMessage
    end_on=("human", "tool"),
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
)

print(resultTrimeMessage2)

""" Advanced Usage """
#  allow_partial=True
resultTrimeMessage3 = trim_messages(
    messages,
    max_tokens=56,
    strategy="last",
    token_counter=count_tokens_approximately,
    include_system=True,
    allow_partial=True,
)

#
trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    token_counter=count_tokens_approximately,
)

# 
trim_messages(
    messages,
    max_tokens=45,
    strategy="first",
    token_counter=count_tokens_approximately,
)