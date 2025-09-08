"""
    Running agents : https://langchain-ai.github.io/langgraph/agents/run_agents/

    Agents support both synchronous and asynchronous execution using either 
    .invoke() / await .ainvoke() for full responses, or .stream() / .astream() for incremental streaming output. 
    This section explains how to provide input, interpret output, enable streaming, and control execution limits.
"""

"""
Basic usage
   Agents can be executed in two primary modes:
     - Synchronous  using .invoke()  or .stream()
     - Asynchronous using .ainvoke() or .astream()
"""
# Sync invocation
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(...)
response = agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})

# Async invocation
import asyncio
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(...)
async def async_invoke_agent(agent):
    return await agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})
# 调用异步函数需要使用以下方式
response = asyncio.run(async_invoke_agent(agent))

"""
Inputs and outputs
    Agents use a language model that expects a list of messages as an input. 
    Therefore, agent inputs and outputs are stored as a list of messages under the messages key in the agent state.
"""

"""
 Input format
    Agent input must be a dictionary with a messages key. Supported formats are:
    Format	            Example
    String	            {"messages": "Hello"}                                                      — Interpreted as a HumanMessage
    Message dictionary	{"messages": {"role": "user", "content": "Hello"}}
    List of messages	{"messages": [{"role": "user", "content": "Hello"}]}
    With custom state	{"messages": [{"role": "user", "content": "Hello"}], "user_name": "Alice"} — If using a custom state_schema
"""

"""
 Output format
    Agent output is a dictionary containing:
    messages: A list of all messages exchanged during execution (user input, assistant replies, tool invocations).
    Optionally, structured_response if structured output is configured.
    If using a custom state_schema, additional keys corresponding to your defined fields may also be present in the output. These can hold updated state values from tool execution or prompt logic.
    See the context guide for more details on working with custom state schemas and accessing context.
"""

"""
 Streaming output
    Agents support streaming responses for more responsive applications. This includes:
      Progress updates after each step
      LLM tokens as they're generated
      Custom tool messages during execution

  Streaming is available in both sync and async modes:
"""
# Sync streaming
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    stream_mode="updates"):
    print(chunk)


# Async streaming
async def async_stream_agent(agent):
    async for chunk in agent.astream(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    stream_mode="updates"):
        print(chunk)
response = asyncio.run(async_invoke_agent(agent))


"""
    Max iterations
    To control agent execution and avoid infinite loops, set a recursion limit. 
    This defines the maximum number of steps the agent can take before raising a GraphRecursionError. 
    You can configure recursion_limit at runtime or when defining agent via .with_config():
"""
# Runtime
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

max_iterations  =  3
recursion_limit =  2 * max_iterations + 1
agent = create_react_agent(
    model="anthropic:claude-3-5-haiku-latest",
    tools=[get_weather]
)
try:
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "what's the weather in sf"}]},
        {"recursion_limit": recursion_limit},
    )
except GraphRecursionError:
    print("Agent stopped due to max iterations.")