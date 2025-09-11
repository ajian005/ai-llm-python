"""
    Stream outputs : https://langchain-ai.github.io/langgraph/how-tos/streaming/

    You can stream outputs from a LangGraph agent or workflow.
"""

"""
   ==== Supported stream modes =======================================

    Mode	Description
    values	Streams the full value of the state after each step of the graph.
    updates	Streams the updates to the state after each step of the graph. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately.
    custom	Streams custom data from inside your graph nodes.
    messages	Streams 2-tuples (LLM token, metadata) from any graph nodes where an LLM is invoked.
    debug	Streams as much information as possible throughout the execution of the graph.
"""

"""
   ==== Stream from an agent --> Agent progress =======================================
   To stream agent progress, use the stream() or astream() methods with stream_mode="updates". This emits an event after every agent step.
   For example, if you have an agent that calls a tool once, you should see the following updates:
        LLM node: AI message with tool call requests
        Tool node: Tool message with execution result
        LLM node: Final AI response

    ---- Sync -------------------
    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode="updates"
    ):
        print(chunk)
        print("\n")

    ---- Async -------------------
    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode="updates"
    ):
        print(chunk)
        print("\n")

"""

"""
   ==== Stream from an agent --> LLM tokens =======================================
   To stream tokens as they are produced by the LLM, use stream_mode="messages":
   
    ---- Sync --------------------
    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )
    for token, metadata in agent.stream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode="messages"
    ):
        print("Token", token)
        print("Metadata", metadata)
        print("\n")

    ---- Async -------------------
    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )
    async for token, metadata in agent.astream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode="messages"
    ):
        print("Token", token)
        print("Metadata", metadata)
        print("\n")

"""

"""
   ==== Stream from an agent --> Tool updates =======================================
   To stream updates from tools as they are executed, you can use get_stream_writer.
    ---- Sync -------------------
    from langgraph.config import get_stream_writer

    def get_weather(city: str) -> str:
        ''' Get weather for a given city. ''' 
        writer = get_stream_writer()
        # stream any arbitrary data
        writer(f"Looking up data for city: {city}")
        return f"It's always sunny in {city}!"

    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )

    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode="custom"
    ):
        print(chunk)
        print("\n")

    ---- Async -------------------
    from langgraph.config import get_stream_writer

    def get_weather(city: str) -> str:
        ''' Get weather for a given city. ''' 
        writer = get_stream_writer()
        # stream any arbitrary data
        writer(f"Looking up data for city: {city}")
        return f"It's always sunny in {city}!"

    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )

    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode="custom"
    ):
        print(chunk)
        print("\n")
"""

"""
   ==== Stream from an agent --> Stream multiple modes =======================================
     You can specify multiple streaming modes by passing stream mode as a list: stream_mode=["updates", "messages", "custom"]:

    ---- Sync -------------------
    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )

    for stream_mode, chunk in agent.stream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode=["updates", "messages", "custom"]
    ):
        print(chunk)
        print("\n")

    ---- Async -------------------
    agent = create_react_agent(
        model="anthropic:claude-3-7-sonnet-latest",
        tools=[get_weather],
    )

    async for stream_mode, chunk in agent.astream(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        stream_mode=["updates", "messages", "custom"]
    ):
        print(chunk)
        print("\n")

"""

"""
   ==== Stream from an agent --> Disable streaming =======================================
    In some applications you might need to disable streaming of individual tokens for a given model. This is useful in multi-agent systems to control which agents stream their output.

    See the Models guide to learn how to disable streaming.
"""


"""
   ==== Stream from a workflow --> Basic usage example =======================================

   LangGraph graphs expose the .stream() (sync) and .astream() (async) methods to yield streamed outputs as iterators.
    ---- Sync -------------------
    for chunk in graph.stream(inputs, stream_mode="updates"):
        print(chunk)

    ---- Async -------------------
    async for chunk in graph.astream(inputs, stream_mode="updates"):
        print(chunk)

    ---- Extended example: streaming updates -------------------
    from typing import TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        topic: str
        joke: str

    def refine_topic(state: State):
        return {"topic": state["topic"] + " and cats"}

    def generate_joke(state: State):
        return {"joke": f"This is a joke about {state['topic']}"}

    graph = (
        StateGraph(State)
        .add_node(refine_topic)
        .add_node(generate_joke)
        .add_edge(START, "refine_topic")
        .add_edge("refine_topic", "generate_joke")
        .add_edge("generate_joke", END)
        .compile()
    )

    for chunk in graph.stream( 
        {"topic": "ice cream"},
        stream_mode="updates", 
    ):
        print(chunk)

   ==== Stream from a workflow --> Stream multiple modes =======================================
   You can pass a list as the stream_mode parameter to stream multiple modes at once.

   ---- Sync -------------------
   for mode, chunk in graph.stream(inputs, stream_mode=["updates", "custom"]):
      print(chunk)

   ---- Async -------------------
   async for mode, chunk in graph.astream(inputs, stream_mode=["updates", "custom"]):
      print(chunk)


   ==== Stream from a workflow --> Stream graph state =======================================
    Use the stream modes updates and values to stream the state of the graph as it executes.

    updates streams the updates to the state after each step of the graph.
    values streams the full value of the state after each step of the graph.
    API Reference: StateGraph | START | END

    from typing import TypedDict
    from langgraph.graph import StateGraph, START, END


    class State(TypedDict):
    topic: str
    joke: str


    def refine_topic(state: State):
        return {"topic": state["topic"] + " and cats"}


    def generate_joke(state: State):
        return {"joke": f"This is a joke about {state['topic']}"}

    graph = (
    StateGraph(State)
    .add_node(refine_topic)
    .add_node(generate_joke)
    .add_edge(START, "refine_topic")
    .add_edge("refine_topic", "generate_joke")
    .add_edge("generate_joke", END)
    .compile()
    )

    ---- updates -------------------
    Use this to stream only the state updates returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.

    for chunk in graph.stream(
        {"topic": "ice cream"},
        stream_mode="updates",
    ):
        print(chunk)

    ---- values -------------------
    Use this to stream the full state of the graph after each step.

    for chunk in graph.stream(
        {"topic": "ice cream"},
        stream_mode="values",
    ):
        print(chunk)

   ==== Stream from a workflow --> Stream subgraph outputs =======================================

"""

