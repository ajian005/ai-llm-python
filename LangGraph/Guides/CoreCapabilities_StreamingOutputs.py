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
    To include outputs from subgraphs in the streamed outputs, you can set subgraphs=True in the .stream() method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.

    The outputs will be streamed as tuples (namespace, data), where namespace is a tuple with the path to the node where a subgraph is invoked, e.g. ("parent_node:<task_id>", "child_node:<task_id>").

    for chunk in graph.stream(
        {"foo": "foo"},
        subgraphs=True, 
        stream_mode="updates",
    ):
        print(chunk)

    ---- Extended example: streaming from subgraphs -------------------
    from langgraph.graph import START, StateGraph
    from typing import TypedDict

    # Define subgraph
    class SubgraphState(TypedDict):
        foo: str  # note that this key is shared with the parent graph state
        bar: str

    def subgraph_node_1(state: SubgraphState):
        return {"bar": "bar"}

    def subgraph_node_2(state: SubgraphState):
        return {"foo": state["foo"] + state["bar"]}

    subgraph_builder = StateGraph(SubgraphState)
    subgraph_builder.add_node(subgraph_node_1)
    subgraph_builder.add_node(subgraph_node_2)
    subgraph_builder.add_edge(START, "subgraph_node_1")
    subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
    subgraph = subgraph_builder.compile()

    # Define parent graph
    class ParentState(TypedDict):
        foo: str

    def node_1(state: ParentState):
        return {"foo": "hi! " + state["foo"]}

    builder = StateGraph(ParentState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", subgraph)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    graph = builder.compile()

    for chunk in graph.stream(
        {"foo": "foo"},
        stream_mode="updates",
        subgraphs=True, 
    ):
        print(chunk)

    ((), {'node_1': {'foo': 'hi! foo'}})
    (('node_2:dfddc4ba-c3c5-6887-5012-a243b5b377c2',), {'subgraph_node_1': {'bar': 'bar'}})
    (('node_2:dfddc4ba-c3c5-6887-5012-a243b5b377c2',), {'subgraph_node_2': {'foo': 'hi! foobar'}})
    ((), {'node_2': {'foo': 'hi! foobar'}})
    Note that we are receiving not just the node updates, but we also the namespaces which tell us what graph (or subgraph) we are streaming from.

   ==== Stream from a workflow --> Debugging =======================================
   Use the debug streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.

    for chunk in graph.stream(
        {"topic": "ice cream"},
        stream_mode="debug",
    ):
        print(chunk)

    
   ==== Stream from a workflow --> LLM tokens =======================================
Use the messages streaming mode to stream Large Language Model (LLM) outputs token by token from any part of your graph, including nodes, tools, subgraphs, or tasks.

The streamed output from messages mode is a tuple (message_chunk, metadata) where:

message_chunk: the token or message segment from the LLM.
metadata: a dictionary containing details about the graph node and LLM invocation.
If your LLM is not available as a LangChain integration, you can stream its outputs using custom mode instead. See use with any LLM for details.

    from dataclasses import dataclass

    from langchain.chat_models import init_chat_model
    from langgraph.graph import StateGraph, START


    @dataclass
    class MyState:
        topic: str
        joke: str = ""


    llm = init_chat_model(model="openai:gpt-4o-mini")

    def call_model(state: MyState):
        ''' Call the LLM to generate a joke about a topic''' 
        llm_response = llm.invoke( 
            [
                {"role": "user", "content": f"Generate a joke about {state.topic}"}
            ]
        )
        return {"joke": llm_response.content}

    graph = (
        StateGraph(MyState)
        .add_node(call_model)
        .add_edge(START, "call_model")
        .compile()
    )

    for message_chunk, metadata in graph.stream( 
        {"topic": "ice cream"},
        stream_mode="messages",
    ):
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)

    ------Filter by LLM invocation------------------------------
    from typing import TypedDict

    from langchain.chat_models import init_chat_model
    from langgraph.graph import START, StateGraph

    joke_model = init_chat_model(model="openai:gpt-4o-mini", tags=["joke"]) 
    poem_model = init_chat_model(model="openai:gpt-4o-mini", tags=["poem"]) 


    class State(TypedDict):
        topic: str
        joke: str
        poem: str


    async def call_model(state, config):
        topic = state["topic"]
        print("Writing joke...")
        # Note: Passing the config through explicitly is required for python < 3.11
        # Since context var support wasn't added before then: https://docs.python.org/3/library/asyncio-task.html#creating-tasks
        joke_response = await joke_model.ainvoke(
                [{"role": "user", "content": f"Write a joke about {topic}"}],
                config, 
        )
        print("\n\nWriting poem...")
        poem_response = await poem_model.ainvoke(
                [{"role": "user", "content": f"Write a short poem about {topic}"}],
                config, 
        )
        return {"joke": joke_response.content, "poem": poem_response.content}


    graph = (
        StateGraph(State)
        .add_node(call_model)
        .add_edge(START, "call_model")
        .compile()
    )

    async for msg, metadata in graph.astream(
        {"topic": "cats"},
        stream_mode="messages", 
    ):
        if metadata["tags"] == ["joke"]: 
            print(msg.content, end="|", flush=True)

    ------Filter by node------------------------------
    from typing import TypedDict
    from langgraph.graph import START, StateGraph
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(model="gpt-4o-mini")


    class State(TypedDict):
        topic: str
        joke: str
        poem: str


    def write_joke(state: State):
        topic = state["topic"]
        joke_response = model.invoke(
                [{"role": "user", "content": f"Write a joke about {topic}"}]
        )
        return {"joke": joke_response.content}


    def write_poem(state: State):
        topic = state["topic"]
        poem_response = model.invoke(
                [{"role": "user", "content": f"Write a short poem about {topic}"}]
        )
        return {"poem": poem_response.content}


    graph = (
        StateGraph(State)
        .add_node(write_joke)
        .add_node(write_poem)
        # write both the joke and the poem concurrently
        .add_edge(START, "write_joke")
        .add_edge(START, "write_poem")
        .compile()
    )

    for msg, metadata in graph.stream( 
        {"topic": "cats"},
        stream_mode="messages",
    ):
        if msg.content and metadata["langgraph_node"] == "write_poem": 
            print(msg.content, end="|", flush=True)

"""

