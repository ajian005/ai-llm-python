"""
  Build an Agent with AgentExecutor (Legacy): https://python.langchain.com/docs/how_to/agent_executor/
"""

""" ====================== Basic Usage ====================== """
model = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    )

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

tools = [magic_function]

query = "what is the value of magic_function(3)?"


from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke({"input": query})


# LangGraph's react agent executor manages a state that is defined by a list of messages.
from langgraph.prebuilt import create_react_agent
langgraph_agent_executor = create_react_agent(model, tools)
messages = langgraph_agent_executor.invoke({"messages": [("human", query)]})
{
    "input": query,
    "output": messages["messages"][-1].content,
}

message_history = messages["messages"]

new_query = "Pardon?"

messages = langgraph_agent_executor.invoke(
    {"messages": message_history + [("human", new_query)]}
)
{
    "input": new_query,
    "output": messages["messages"][-1].content,
}

""" ====================== Prompt Templates ====================== """
# First up, using AgentExecutor
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Respond only in Spanish."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke({"input": query})

""" ====================== Memory In LangChain ====================== """
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langchain.chat_models import init_chat_model
import os

# model = ChatOpenAI(model="gpt-4o")
model = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    )

memory = InMemoryChatMessageHistory(session_id="test-session")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        # First put the history
        ("placeholder", "{chat_history}"),
        # Then the new input
        ("human", "{input}"),
        # Finally the scratchpad
        ("placeholder", "{agent_scratchpad}"),
    ])

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

tools = [magic_function]
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "test-session"}}

print(
    agent_with_chat_history.invoke({"input": "Hi, I'm polly! What's the output of magic_function of 3?"}, config)["output"]
)
print("---")

print(agent_with_chat_history.invoke({"input": "Remember my name?"}, config)["output"])
print("---")

print(agent_with_chat_history.invoke({"input": "what was that output again?"}, config)["output"])


""" ====================== Memory In LangGraph ====================== """
from langgraph.checkpoint.memory import MemorySaver  # an in-memory checkpointer
from langgraph.prebuilt import create_react_agent

system_message = "You are a helpful assistant."
# This could also be a SystemMessage object
# system_message = SystemMessage(content="You are a helpful assistant. Respond only in Spanish.")

memory = MemorySaver()
langgraph_agent_executor = create_react_agent(
    model, tools, prompt=system_message, checkpointer=memory
)

config = {"configurable": {"thread_id": "test-thread"}}
print(
    langgraph_agent_executor.invoke(
        {"messages": [
                ("user", "Hi, I'm polly! What's the output of magic_function of 3?")
            ]},
        config,
    )["messages"][-1].content
)
print("---")
print(
    langgraph_agent_executor.invoke(
        {"messages": [("user", "Remember my name?")]}, config
    )["messages"][-1].content
)
print("---")
print(
    langgraph_agent_executor.invoke(
        {"messages": [("user", "what was that output again?")]}, config
    )["messages"][-1].content
)

""" ======================== Iterating through steps  In LangChain ======================== """
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages(
    [   ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ])

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

tools = [magic_function]
agent = create_tool_calling_agent(model, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

for step in agent_executor.stream({"input": query}):
    print(step)


""" ======================== Iterating through steps  In LangGraph ======================== """
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("placeholder", "{messages}"),
    ])
langgraph_agent_executor = create_react_agent(model, tools, prompt=prompt)
for step in langgraph_agent_executor.stream(
    {"messages": [("human", query)]}, stream_mode="updates"
):
    print(step)


""" ======================== return_intermediate_steps  In LangChain ======================== """
agent_executor = AgentExecutor(agent=agent, tools=tools, return_intermediate_steps=True)
result = agent_executor.invoke({"input": query})
print(result["intermediate_steps"])


""" ======================== return_intermediate_steps  In LangGraph ======================== """
from langgraph.prebuilt import create_react_agent
langgraph_agent_executor = create_react_agent(model, tools=tools)
messages = langgraph_agent_executor.invoke({"messages": [("human", query)]})


""" ======================== max_iterations  In LangChain ======================== """
@tool
def magic_function(input: str) -> str:
    """Applies a magic function to an input."""
    return "Sorry, there was an error. Please try again."

tools = [magic_function]
prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Respond only in Spanish."),
            ("human", "{input}"),
            # Placeholders fill up a **list** of messages
            ("placeholder", "{agent_scratchpad}"),
        ])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,)

agent_executor.invoke({"input": query})

""" ======================== max_iterations  In LangGraph ======================== """
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

RECURSION_LIMIT = 2 * 3 + 1

langgraph_agent_executor = create_react_agent(model, tools=tools)
try:
    for chunk in langgraph_agent_executor.stream(
        {"messages": [("human", query)]},
        {"recursion_limit": RECURSION_LIMIT},
        stream_mode="values",
    ):
        print(chunk["messages"][-1])
except GraphRecursionError:
    print({"input": query, "output": "Agent stopped due to max iterations."})

""" ======================== max_execution_time  In LangChain ======================== """
import time

@tool
def magic_function(input: str) -> str:
    """Applies a magic function to an input."""
    time.sleep(2.5)
    return "Sorry, there was an error. Please try again."

tools = [magic_function]
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_execution_time=2,
    verbose=True,
)
agent_executor.invoke({"input": query})


""" ======================== max_execution_time  In LangGraph ======================== """
from langgraph.prebuilt import create_react_agent

langgraph_agent_executor = create_react_agent(model, tools=tools)
# Set the max timeout for each step here
langgraph_agent_executor.step_timeout = 2

try:
    for chunk in langgraph_agent_executor.stream({"messages": [("human", query)]}):
        print(chunk)
        print("------")
except TimeoutError:
    print({"input": query, "output": "Agent stopped due to a step timeout."})

import asyncio

from langgraph.prebuilt import create_react_agent

langgraph_agent_executor = create_react_agent(model, tools=tools)


async def stream(langgraph_agent_executor, inputs):
    async for chunk in langgraph_agent_executor.astream(
        {"messages": [("human", query)]}
    ):
        print(chunk)
        print("------")


try:
    task = asyncio.create_task(
        stream(langgraph_agent_executor, {"messages": [("human", query)]})
    )
    asyncio.get_event_loop().run_until_complete(asyncio.wait_for(task, timeout=3))
except asyncio.TimeoutError:
    print("Task Cancelled.")


""" ======================== early_stopping_method  In LangChain ======================== """
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return "Sorry there was an error, please try again."


tools = [magic_function]

agent = create_tool_calling_agent(model, tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, early_stopping_method="force", max_iterations=1
)

result = agent_executor.invoke({"input": query})
print("Output with early_stopping_method='force':")
print(result["output"])


""" ======================== early_stopping_method  In LangGraph ======================== """
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

RECURSION_LIMIT = 2 * 1 + 1

langgraph_agent_executor = create_react_agent(model, tools=tools)

try:
    for chunk in langgraph_agent_executor.stream(
        {"messages": [("human", query)]},
        {"recursion_limit": RECURSION_LIMIT},
        stream_mode="values",
    ):
        print(chunk["messages"][-1])
except GraphRecursionError:
    print({"input": query, "output": "Agent stopped due to max iterations."})

""" ======================== trim_intermediate_steps  In LangChain ======================== """
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ])

magic_step_num = 1

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    global magic_step_num
    print(f"Call number: {magic_step_num}")
    magic_step_num += 1
    return input + magic_step_num

tools = [magic_function]

agent = create_tool_calling_agent(model, tools, prompt=prompt)

def trim_steps(steps: list):
    # Let's give the agent amnesia
    return []

agent_executor = AgentExecutor(
    agent=agent, tools=tools, trim_intermediate_steps=trim_steps
)

query = "Call the magic function 4 times in sequence with the value 3. You cannot call it multiple times at once."

for step in agent_executor.stream({"input": query}):
    pass


""" ======================== trim_intermediate_steps  In LangGraph ======================== """
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

magic_step_num = 1


@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    global magic_step_num
    print(f"Call number: {magic_step_num}")
    magic_step_num += 1
    return input + magic_step_num


tools = [magic_function]


def _modify_state_messages(state: AgentState):
    # Give the agent amnesia, only keeping the original user query
    return [("system", "You are a helpful assistant"), state["messages"][0]]


langgraph_agent_executor = create_react_agent(
    model, tools, prompt=_modify_state_messages
)

try:
    for step in langgraph_agent_executor.stream(
        {"messages": [("human", query)]}, stream_mode="updates"
    ):
        pass
except GraphRecursionError as e:
    print("Stopping agent prematurely due to triggering stop condition")

