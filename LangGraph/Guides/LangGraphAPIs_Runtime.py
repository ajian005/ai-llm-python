"""
    LangGraph runtime : https://langchain-ai.github.io/langgraph/concepts/pregel/

    Pregel implements LangGraph's runtime, managing the execution of LangGraph applications.

    Compiling a StateGraph or creating an entrypoint produces a Pregel instance that can be invoked with input.

    This guide explains the runtime at a high level and provides instructions for directly implementing applications with Pregel.

    Note: The Pregel runtime is named after Google's Pregel algorithm, which describes an efficient method for large-scale parallel computation using graphs.

"""

"""
    === Overview ====================

    In LangGraph, Pregel combines actors and channels into a single application. Actors read data from channels and write data to channels. Pregel organizes the execution of the application into multiple steps, following the Pregel Algorithm/Bulk Synchronous Parallel model.

    Each step consists of three phases:

    Plan: Determine which actors to execute in this step. For example, in the first step, select the actors that subscribe to the special input channels; in subsequent steps, select the actors that subscribe to channels updated in the previous step.
    Execution: Execute all selected actors in parallel, until all complete, or one fails, or a timeout is reached. During this phase, channel updates are invisible to actors until the next step.
    Update: Update the channels with the values written by the actors in this step.
    Repeat until no actors are selected for execution, or a maximum number of steps is reached.
"""

"""
    === Actors ====================
    An actor is a PregelNode. It subscribes to channels, reads data from them, and writes data to them. 
    It can be thought of as an actor in the Pregel algorithm. 
    PregelNodes implement LangChain's Runnable interface.
"""

"""
    === Channels ====================
    Channels are used to communicate between actors (PregelNodes). Each channel has a value type, an update type, and an update function – which takes a sequence of updates and modifies the stored value. Channels can be used to send data from one chain to another, or to send data from a chain to itself in a future step. LangGraph provides a number of built-in channels:

    LastValue: The default channel, stores the last value sent to the channel, useful for input and output values, or for sending data from one step to the next.
    Topic: A configurable PubSub Topic, useful for sending multiple values between actors, or for accumulating output. Can be configured to deduplicate values or to accumulate values over the course of multiple steps.
    BinaryOperatorAggregate: stores a persistent value, updated by applying a binary operator to the current value and each update sent to the channel, useful for computing aggregates over multiple steps; e.g.,total = BinaryOperatorAggregate(int, operator.add)
"""

"""
    === Channels ====================
    While most users will interact with Pregel through the StateGraph API or the entrypoint decorator, it is possible to interact with Pregel directly.
    Below are a few different examples to give you a sense of the Pregel API.

    ------Single node----------------------------
    from langgraph.channels import EphemeralValue
    from langgraph.pregel import Pregel, NodeBuilder

    node1 = (
        NodeBuilder().subscribe_only("a")
        .do(lambda x: x + x)
        .write_to("b")
    )

    app = Pregel(
        nodes={"node1": node1},
        channels={
            "a": EphemeralValue(str),
            "b": EphemeralValue(str),
        },
        input_channels=["a"],
        output_channels=["b"],
    )

    app.invoke({"a": "foo"})


    ------Multiple nodes----------------------------
    from langgraph.channels import LastValue, EphemeralValue
    from langgraph.pregel import Pregel, NodeBuilder

    node1 = (
        NodeBuilder().subscribe_only("a")
        .do(lambda x: x + x)
        .write_to("b")
    )

    node2 = (
        NodeBuilder().subscribe_only("b")
        .do(lambda x: x + x)
        .write_to("c")
    )


    app = Pregel(
        nodes={"node1": node1, "node2": node2},
        channels={
            "a": EphemeralValue(str),
            "b": LastValue(str),
            "c": EphemeralValue(str),
        },
        input_channels=["a"],
        output_channels=["b", "c"],
    )

    app.invoke({"a": "foo"})

"""

"""
    === High-level API ====================
    High-level API
     
    LangGraph provides two high-level APIs for creating a Pregel application: the StateGraph (Graph API) and the Functional API.

    ----------------------------Functional API----------------------------
    In the Functional API, you can use an entrypoint to create a Pregel application. The entrypoint decorator allows you to define a function that takes input and returns output.

    from typing import TypedDict, Optional

    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.func import entrypoint

    class Essay(TypedDict):
        topic: str
        content: Optional[str]
        score: Optional[float]


    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def write_essay(essay: Essay):
        return {
            "content": f"Essay about {essay['topic']}",
        }

    print("Nodes: ")
    print(write_essay.nodes)
    print("Channels: ")
    print(write_essay.channels)


    ---------------------------- StateGraph (Graph API) ----------------------------
    The StateGraph (Graph API) is a higher-level abstraction that simplifies the creation of Pregel applications. 
    It allows you to define a graph of nodes and edges. 
    When you compile the graph, the StateGraph API automatically creates the Pregel application for you.

    from typing import TypedDict, Optional

    from langgraph.constants import START
    from langgraph.graph import StateGraph

    class Essay(TypedDict):
        topic: str
        content: Optional[str]
        score: Optional[float]

    def write_essay(essay: Essay):
        return {
            "content": f"Essay about {essay['topic']}",
        }

    def score_essay(essay: Essay):
        return {
            "score": 10
        }

    builder = StateGraph(Essay)
    builder.add_node(write_essay)
    builder.add_node(score_essay)
    builder.add_edge(START, "write_essay")

    # Compile the graph.
    # This will return a Pregel instance.
    graph = builder.compile()

    The compiled Pregel instance will be associated with a list of nodes and channels. You can inspect the nodes and channels by printing them.

    print(graph.nodes)

    You will see something like this:

    {'__start__': <langgraph.pregel.read.PregelNode at 0x7d05e3ba1810>,
    'write_essay': <langgraph.pregel.read.PregelNode at 0x7d05e3ba14d0>,
    'score_essay': <langgraph.pregel.read.PregelNode at 0x7d05e3ba1710>}

    print(graph.channels)

    You should see something like this

    {'topic': <langgraph.channels.last_value.LastValue at 0x7d05e3294d80>,
    'content': <langgraph.channels.last_value.LastValue at 0x7d05e3295040>,
    'score': <langgraph.channels.last_value.LastValue at 0x7d05e3295980>,
    '__start__': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e3297e00>,
    'write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e32960c0>,
    'score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8ab80>,
    'branch:__start__:__self__:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e32941c0>,
    'branch:__start__:__self__:score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d88800>,
    'branch:write_essay:__self__:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e3295ec0>,
    'branch:write_essay:__self__:score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8ac00>,
    'branch:score_essay:__self__:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d89700>,
    'branch:score_essay:__self__:score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8b400>,
    'start:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8b280>}



"""
