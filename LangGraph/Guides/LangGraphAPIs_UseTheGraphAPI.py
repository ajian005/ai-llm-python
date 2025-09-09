"""
    Graph API How to use the graph API : https://langchain-ai.github.io/langgraph/how-tos/graph-api/

    This guide demonstrates the basics of LangGraph's Graph API. It walks through state, as well as composing common graph structures such as sequences, branches, and loops. 
    It also covers LangGraph's control features, including the Send API for map-reduce workflows and the Command API for combining state updates with "hops" across nodes.
"""

"""
    === Setup ====================
    Install langgraph
        pip install langgraph

    Set up LangSmith for better debugging
    Sign up for LangSmith to quickly spot issues and improve the performance of your LangGraph projects. 
    LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph 
    — read more about how to get started in the docs.
"""

"""
    === Define and update state ====================
    Here we show how to define and update state in LangGraph. We will demonstrate:

       1 How to use state to define a graph's schema
       2 How to use reducers to control how state updates are processed.

    === Define and update state --> Define state ====================
    State in LangGraph can be a TypedDict, Pydantic model, or dataclass. Below we will use TypedDict. See this section for detail on using Pydantic.
    By default, graphs will have the same input and output schema, and the state determines that schema. See this section for how to define distinct input and output schemas.
    Let's consider a simple example using messages. This represents a versatile formulation of state for many LLM applications. See our concepts page for more detail.
    API Reference: AnyMessage

    from langchain_core.messages import AnyMessage
    from typing_extensions import TypedDict

    class State(TypedDict):
        messages: list[AnyMessage]
        extra_field: int

    This state tracks a list of message objects, as well as an extra integer field.

    === Define and update state --> Update state ====================
    Let's build an example graph with a single node. Our node is just a Python function that reads our graph's state and makes updates to it. The first argument to this function will always be the state:

    API Reference: AIMessage : 

    from langchain_core.messages import AIMessage

    def node(state: State):
        messages = state["messages"]
        new_message = AIMessage("Hello!")
        return {"messages": messages + [new_message], "extra_field": 10}
    
    This node simply appends a message to our message list, and populates an extra field.

    Important: Nodes should return updates to the state directly, instead of mutating the state.

    Let's next define a simple graph containing this node. We use StateGraph to define a graph that operates on this state. We then use add_node populate our graph.

    API Reference: StateGraph

    from langgraph.graph import StateGraph

    builder = StateGraph(State)
    builder.add_node(node)
    builder.set_entry_point("node")
    graph = builder.compile()

    LangGraph provides built-in utilities for visualizing your graph. Let's inspect our graph. See this section for detail on visualization.

    from IPython.display import Image, display
    display(Image(graph.get_graph().draw_mermaid_png()))

    In this case, our graph just executes a single node. Let's proceed with a simple invocation:
    API Reference: HumanMessage

    from langchain_core.messages import HumanMessage
    result = graph.invoke({"messages": [HumanMessage("Hi")]})
    result

    Note that:
       - We kicked off invocation by updating a single key of the state.
       - We receive the entire state in the invocation result.

    For convenience, we frequently inspect the content of message objects via pretty-print:
    
    for message in result["messages"]:
    message.pretty_print()

    === Define and update state --> Process state updates with reducers ====================
    Each key in the state can have its own independent reducer function, which controls how updates from nodes are applied. If no reducer function is explicitly specified then it is assumed that all updates to the key should override it.
    For TypedDict state schemas, we can define reducers by annotating the corresponding field of the state with a reducer function.
    In the earlier example, our node updated the "messages" key in the state by appending a message to it. Below, we add a reducer to this key, such that updates are automatically appended:

    from typing_extensions import Annotated

    def add(left, right):
        '''Can also import `add` from the `operator` built-in.'''
        return left + right

    class State(TypedDict):
        messages: Annotated[list[AnyMessage], add]
        extra_field: int

    Now our node can be simplified:
    def node(state: State):
        new_message = AIMessage("Hello!")
        return {"messages": [new_message], "extra_field": 10}

    API Reference: START

    from langgraph.graph import START

    graph = StateGraph(State).add_node(node).add_edge(START, "node").compile()

    result = graph.invoke({"messages": [HumanMessage("Hi")]})

    for message in result["messages"]:
        message.pretty_print()

    === Define and update state --> Process state updates with reducers --> MessagesState ====================
    In practice, there are additional considerations for updating lists of messages:
        We may wish to update an existing message in the state.
        We may want to accept short-hands for message formats, such as OpenAI format.

    LangGraph includes a built-in reducer add_messages that handles these considerations:

    API Reference: add_messages

    from langgraph.graph.message import add_messages

    class State(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]
        extra_field: int

    def node(state: State):
        new_message = AIMessage("Hello!")
        return {"messages": [new_message], "extra_field": 10}

    graph = StateGraph(State).add_node(node).set_entry_point("node").compile()
    input_message = {"role": "user", "content": "Hi"}
    result = graph.invoke({"messages": [input_message]})

    for message in result["messages"]:
        message.pretty_print()

    input_message = {"role": "user", "content": "Hi"}

    result = graph.invoke({"messages": [input_message]})

    for message in result["messages"]:
        message.pretty_print()

    This is a versatile representation of state for applications involving chat models. LangGraph includes a pre-built MessagesState for convenience, so that we can have:


    from langgraph.graph import MessagesState

    class State(MessagesState):
        extra_field: int

    === Define and update state --> Define input and output schemas ====================
    By default, StateGraph operates with a single schema, and all nodes are expected to communicate using that schema. However, it's also possible to define distinct input and output schemas for a graph.

    When distinct schemas are specified, an internal schema will still be used for communication between nodes. The input schema ensures that the provided input matches the expected structure, while the output schema filters the internal data to return only the relevant information according to the defined output schema.

    Below, we'll see how to define distinct input and output schema.

    API Reference: StateGraph | START | END

        from langgraph.graph import StateGraph, START, END
        from typing_extensions import TypedDict

        # Define the schema for the input
        class InputState(TypedDict):
            question: str

        # Define the schema for the output
        class OutputState(TypedDict):
            answer: str

        # Define the overall schema, combining both input and output
        class OverallState(InputState, OutputState):
            pass

        # Define the node that processes the input and generates an answer
        def answer_node(state: InputState):
            # Example answer and an extra key
            return {"answer": "bye", "question": state["question"]}

        # Build the graph with input and output schemas specified
        builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
        builder.add_node(answer_node)  # Add the answer node
        builder.add_edge(START, "answer_node")  # Define the starting edge
        builder.add_edge("answer_node", END)  # Define the ending edge
        graph = builder.compile()  # Compile the graph

        # Invoke the graph with an input and print the result
        print(graph.invoke({"question": "hi"}))

     Notice that the output of invoke only includes the output schema.

    === Define and update state --> Pass private state between nodes ====================
    In some cases, you may want nodes to exchange information that is crucial for intermediate logic but doesn't need to be part of the main schema of the graph. This private data is not relevant to the overall input/output of the graph and should only be shared between certain nodes.
    Below, we'll create an example sequential graph consisting of three nodes (node_1, node_2 and node_3), where private data is passed between the first two steps (node_1 and node_2), while the third step (node_3) only has access to the public overall state.

    API Reference: StateGraph | START | END

    from langgraph.graph import StateGraph, START, END
    from typing_extensions import TypedDict

    # The overall state of the graph (this is the public state shared across nodes)
    class OverallState(TypedDict):
        a: str

    # Output from node_1 contains private data that is not part of the overall state
    class Node1Output(TypedDict):
        private_data: str

    # The private data is only shared between node_1 and node_2
    def node_1(state: OverallState) -> Node1Output:
        output = {"private_data": "set by node_1"}
        print(f"Entered node `node_1`:\n\tInput: {state}.\n\tReturned: {output}")
        return output

    # Node 2 input only requests the private data available after node_1
    class Node2Input(TypedDict):
        private_data: str

    def node_2(state: Node2Input) -> OverallState:
        output = {"a": "set by node_2"}
        print(f"Entered node `node_2`:\n\tInput: {state}.\n\tReturned: {output}")
        return output

    # Node 3 only has access to the overall state (no access to private data from node_1)
    def node_3(state: OverallState) -> OverallState:
        output = {"a": "set by node_3"}
        print(f"Entered node `node_3`:\n\tInput: {state}.\n\tReturned: {output}")
        return output

    # Connect nodes in a sequence
    # node_2 accepts private data from node_1, whereas
    # node_3 does not see the private data.
    builder = StateGraph(OverallState).add_sequence([node_1, node_2, node_3])
    builder.add_edge(START, "node_1")
    graph = builder.compile()

    # Invoke the graph with the initial state
    response = graph.invoke(
        {
            "a": "set at start",
        }
    )

    print()
    print(f"Output of graph invocation: {response}")

    === Define and update state --> Use Pydantic models for graph state ====================
    A StateGraph accepts a state_schema argument on initialization that specifies the "shape" of the state that the nodes in the graph can access and update.

    In our examples, we typically use a python-native TypedDict or dataclass for state_schema, but state_schema can be any type.

    Here, we'll see how a Pydantic BaseModel can be used for state_schema to add run-time validation on inputs.

    from langgraph.graph import StateGraph, START, END
    from typing_extensions import TypedDict
    from pydantic import BaseModel

    # The overall state of the graph (this is the public state shared across nodes)
    class OverallState(BaseModel):
        a: str

    def node(state: OverallState):
        return {"a": "goodbye"}

    # Build the state graph
    builder = StateGraph(OverallState)
    builder.add_node(node)  # node_1 is the first node
    builder.add_edge(START, "node")  # Start the graph with node_1
    builder.add_edge("node", END)  # End the graph after node_1
    graph = builder.compile()

    # Test the graph with a valid input
    graph.invoke({"a": "hello"})

    try:
        graph.invoke({"a": 123})  # Should be a string
    except Exception as e:
        print("An exception was raised because `a` is an integer rather than a string.")
        print(e)


"""



"""
    === Add runtime configuration ====================
    Sometimes you want to be able to configure your graph when calling it. For example, you might want to be able to specify what LLM or system prompt to use at runtime, without polluting the graph state with these parameters.

    To add runtime configuration:

    Specify a schema for your configuration
    Add the configuration to the function signature for nodes or conditional edges
    Pass the configuration into the graph.
    See below for a simple example:

    API Reference: END | StateGraph | START

        from langgraph.graph import END, StateGraph, START
        from langgraph.runtime import Runtime
        from typing_extensions import TypedDict

        # 1. Specify config schema
        class ContextSchema(TypedDict):
            my_runtime_value: str

        # 2. Define a graph that accesses the config in a node
        class State(TypedDict):
            my_state_value: str

        def node(state: State, runtime: Runtime[ContextSchema]):
            if runtime.context["my_runtime_value"] == "a":
                return {"my_state_value": 1}
            elif runtime.context["my_runtime_value"] == "b":
                return {"my_state_value": 2}
            else:
                raise ValueError("Unknown values.")

        builder = StateGraph(State, context_schema=ContextSchema)
        builder.add_node(node)
        builder.add_edge(START, "node")
        builder.add_edge("node", END)

        graph = builder.compile()

        # 3. Pass in configuration at runtime:
        print(graph.invoke({}, context={"my_runtime_value": "a"}))
        print(graph.invoke({}, context={"my_runtime_value": "b"}))


   Extended example: specifying LLM at runtime

    Below we demonstrate a practical example in which we configure what LLM to use at runtime. We will use both OpenAI and Anthropic models.

    from dataclasses import dataclass

    from langchain.chat_models import init_chat_model
    from langgraph.graph import MessagesState, END, StateGraph, START
    from langgraph.runtime import Runtime
    from typing_extensions import TypedDict

    @dataclass
    class ContextSchema:
        model_provider: str = "anthropic"

    MODELS = {
        "anthropic": init_chat_model("anthropic:claude-3-5-haiku-latest"),
        "openai": init_chat_model("openai:gpt-4.1-mini"),
    }

    def call_model(state: MessagesState, runtime: Runtime[ContextSchema]):
        model = MODELS[runtime.context.model_provider]
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(MessagesState, context_schema=ContextSchema)
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")
    builder.add_edge("model", END)

    graph = builder.compile()

    # Usage
    input_message = {"role": "user", "content": "hi"}
    # With no configuration, uses default (Anthropic)
    response_1 = graph.invoke({"messages": [input_message]})["messages"][-1]
    # Or, can set OpenAI
    response_2 = graph.invoke({"messages": [input_message]}, context={"model_provider": "openai"})["messages"][-1]

    print(response_1.response_metadata["model_name"])
    print(response_2.response_metadata["model_name"])

Extended example: specifying model and system message at runtime
    Below we demonstrate a practical example in which we configure two parameters: the LLM and system message to use at runtime.
    
    from dataclasses import dataclass
    from typing import Optional
    from langchain.chat_models import init_chat_model
    from langchain_core.messages import SystemMessage
    from langgraph.graph import END, MessagesState, StateGraph, START
    from langgraph.runtime import Runtime
    from typing_extensions import TypedDict

    @dataclass
    class ContextSchema:
        model_provider: str = "anthropic"
        system_message: str | None = None

    MODELS = {
        "anthropic": init_chat_model("anthropic:claude-3-5-haiku-latest"),
        "openai": init_chat_model("openai:gpt-4.1-mini"),
    }

    def call_model(state: MessagesState, runtime: Runtime[ContextSchema]):
        model = MODELS[runtime.context.model_provider]
        messages = state["messages"]
        if (system_message := runtime.context.system_message):
            messages = [SystemMessage(system_message)] + messages
        response = model.invoke(messages)
        return {"messages": [response]}

    builder = StateGraph(MessagesState, context_schema=ContextSchema)
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")
    builder.add_edge("model", END)

    graph = builder.compile()

    # Usage
    input_message = {"role": "user", "content": "hi"}
    response = graph.invoke({"messages": [input_message]}, context={"model_provider": "openai", "system_message": "Respond in Italian."})
    for message in response["messages"]:
        message.pretty_print()
"""

"""
    === Add retry policies ====================
    There are many use cases where you may wish for your node to have a custom retry policy, for example if you are calling an API, querying a database, or calling an LLM, etc. LangGraph lets you add retry policies to nodes.

    To configure a retry policy, pass the retry_policy parameter to the add_node. The retry_policy parameter takes in a RetryPolicy named tuple object. Below we instantiate a RetryPolicy object with the default parameters and associate it with a node:

    from langgraph.pregel import RetryPolicy

    builder.add_node(
        "node_name",
        node_function,
        retry_policy=RetryPolicy(),)

        By default, the retry_on parameter uses the default_retry_on function, which retries on any exception except for the following:

        ValueError
        TypeError
        ArithmeticError
        ImportError
        LookupError
        NameError
        SyntaxError
        RuntimeError
        ReferenceError
        StopIteration
        StopAsyncIteration
        OSError
        In addition, for exceptions from popular http request libraries such as requests and httpx it only retries on 5xx status codes.

    # Extended example: customizing retry policies
    Consider an example in which we are reading from a SQL database. Below we pass two different retry policies to nodes:

    import sqlite3
    from typing_extensions import TypedDict
    from langchain.chat_models import init_chat_model
    from langgraph.graph import END, MessagesState, StateGraph, START
    from langgraph.pregel import RetryPolicy
    from langchain_community.utilities import SQLDatabase
    from langchain_core.messages import AIMessage

    db = SQLDatabase.from_uri("sqlite:///:memory:")
    model = init_chat_model("anthropic:claude-3-5-haiku-latest")

    def query_database(state: MessagesState):
        query_result = db.run("SELECT * FROM Artist LIMIT 10;")
        return {"messages": [AIMessage(content=query_result)]}

    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    # Define a new graph
    builder = StateGraph(MessagesState)
    builder.add_node(
        "query_database",
        query_database,
        retry_policy=RetryPolicy(retry_on=sqlite3.OperationalError),
    )
    builder.add_node("model", call_model, retry_policy=RetryPolicy(max_attempts=5))
    builder.add_edge(START, "model")
    builder.add_edge("model", "query_database")
    builder.add_edge("query_database", END)
    graph = builder.compile()
"""

"""
    === Add retry policies ====================

    from langgraph.types import CachePolicy

    builder.add_node(
        "node_name",
        node_function,
        cache_policy=CachePolicy(ttl=120),
    )

    Then, to enable node-level caching for a graph, set the cache argument when compiling the graph. 
    The example below uses InMemoryCache to set up a graph with in-memory cache, but SqliteCache is also available.

    from langgraph.cache.memory import InMemoryCache
    graph = builder.compile(cache=InMemoryCache())
"""

"""
    === Create a sequence of steps ====================
    Here we demonstrate how to construct a simple sequence of steps. We will show:

        How to build a sequential graph
        Built-in short-hand for constructing similar graphs.

    To add a sequence of nodes, we use the .add_node and .add_edge methods of our graph:

    API Reference: START | StateGraph

    from langgraph.graph import START, StateGraph

    builder = StateGraph(State)

    # Add nodes
    builder.add_node(step_1)
    builder.add_node(step_2)
    builder.add_node(step_3)

    # Add edges
    builder.add_edge(START, "step_1")
    builder.add_edge("step_1", "step_2")
    builder.add_edge("step_2", "step_3")

    We can also use the built-in shorthand .add_sequence:
 
    builder = StateGraph(State).add_sequence([step_1, step_2, step_3])
    builder.add_edge(START, "step_1")

    
    Why split application steps into a sequence with LangGraph ?

    Let's demonstrate an end-to-end example. We will create a sequence of three steps:
        Populate a value in a key of the state
        Update the same value
        Populate a different value

    Let's first define our state. This governs the schema of the graph, and can also specify how to apply updates. See this section for more detail.

    In our case, we will just keep track of two values:
       
        from typing_extensions import TypedDict

        class State(TypedDict):
            value_1: str
            value_2: int

    Our nodes are just Python functions that read our graph's state and make updates to it. The first argument to this function will always be the state:
    
    def step_1(state: State):
        return {"value_1": "a"}

    def step_2(state: State):
        current_value_1 = state["value_1"]
        return {"value_1": f"{current_value_1} b"}

    def step_3(state: State):
        return {"value_2": 10}

    Finally, we define the graph. We use StateGraph to define a graph that operates on this state.
    We will then use add_node and add_edge to populate our graph and define its control flow.
    API Reference: START | StateGraph

    from langgraph.graph import START, StateGraph

    builder = StateGraph(State)

    # Add nodes
    builder.add_node(step_1)
    builder.add_node(step_2)
    builder.add_node(step_3)

    # Add edges
    builder.add_edge(START, "step_1")
    builder.add_edge("step_1", "step_2")
    builder.add_edge("step_2", "step_3")

"""

"""
    === Create branches ====================

    Parallel execution of nodes is essential to speed up overall graph operation. LangGraph offers native support for parallel execution of nodes, which can significantly enhance the performance of graph-based workflows. This parallelization is achieved through fan-out and fan-in mechanisms, utilizing both standard edges and conditional_edges. Below are some examples showing how to add create branching dataflows that work for you.

    === Create branches --> Run graph nodes in parallel ====================
    In this example, we fan out from Node A to B and C and then fan in to D. With our state, we specify the reducer add operation. This will combine or accumulate values for the specific key in the State, rather than simply overwriting the existing value. For lists, this means concatenating the new list with the existing list. See the above section on state reducers for more detail on updating state with reducers.
    API Reference: StateGraph | START | END

    import operator
    from typing import Annotated, Any
    from typing_extensions import TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        # The operator.add reducer fn makes this append-only
        aggregate: Annotated[list, operator.add]

    def a(state: State):
        print(f'Adding "A" to {state["aggregate"]}')
        return {"aggregate": ["A"]}

    def b(state: State):
        print(f'Adding "B" to {state["aggregate"]}')
        return {"aggregate": ["B"]}

    def c(state: State):
        print(f'Adding "C" to {state["aggregate"]}')
        return {"aggregate": ["C"]}

    def d(state: State):
        print(f'Adding "D" to {state["aggregate"]}')
        return {"aggregate": ["D"]}

    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(c)
    builder.add_node(d)
    builder.add_edge(START, "a")
    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_edge("b", "d")
    builder.add_edge("c", "d")
    builder.add_edge("d", END)
    graph = builder.compile()

    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))

    === Create branches --> Defer node execution ====================
    Deferring node execution is useful when you want to delay the execution of a node until all other pending tasks are completed. This is particularly relevant when branches have different lengths, which is common in workflows like map-reduce flows.

    The above example showed how to fan-out and fan-in when each path was only one step. But what if one branch had more than one step? Let's add a node "b_2" in the "b" branch:

    API Reference: StateGraph | START | END

    import operator
    from typing import Annotated, Any
    from typing_extensions import TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        # The operator.add reducer fn makes this append-only
        aggregate: Annotated[list, operator.add]

    def a(state: State):
        print(f'Adding "A" to {state["aggregate"]}')
        return {"aggregate": ["A"]}

    def b(state: State):
        print(f'Adding "B" to {state["aggregate"]}')
        return {"aggregate": ["B"]}

    def b_2(state: State):
        print(f'Adding "B_2" to {state["aggregate"]}')
        return {"aggregate": ["B_2"]}

    def c(state: State):
        print(f'Adding "C" to {state["aggregate"]}')
        return {"aggregate": ["C"]}

    def d(state: State):
        print(f'Adding "D" to {state["aggregate"]}')
        return {"aggregate": ["D"]}

    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(b_2)
    builder.add_node(c)
    builder.add_node(d, defer=True)
    builder.add_edge(START, "a")
    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_edge("b", "b_2")
    builder.add_edge("b_2", "d")
    builder.add_edge("c", "d")
    builder.add_edge("d", END)
    graph = builder.compile()

    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))


    === Create branches --> Conditional branching ====================
    If your fan-out should vary at runtime based on the state, you can use add_conditional_edges to select one or more paths using the graph state. See example below, where node a generates a state update that determines the following node.

    API Reference: StateGraph | START | END

    import operator
    from typing import Annotated, Literal, Sequence
    from typing_extensions import TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        aggregate: Annotated[list, operator.add]
        # Add a key to the state. We will set this key to determine
        # how we branch.
        which: str

    def a(state: State):
        print(f'Adding "A" to {state["aggregate"]}')
        return {"aggregate": ["A"], "which": "c"}

    def b(state: State):
        print(f'Adding "B" to {state["aggregate"]}')
        return {"aggregate": ["B"]}

    def c(state: State):
        print(f'Adding "C" to {state["aggregate"]}')
        return {"aggregate": ["C"]}

    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(c)
    builder.add_edge(START, "a")
    builder.add_edge("b", END)
    builder.add_edge("c", END)

    def conditional_edge(state: State) -> Literal["b", "c"]:
        # Fill in arbitrary logic here that uses the state
        # to determine the next node
        return state["which"]

    builder.add_conditional_edges("a", conditional_edge)

    graph = builder.compile()

    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))

    result = graph.invoke({"aggregate": []})
    print(result)
"""

"""
    === Map-Reduce and the Send API ====================
    LangGraph supports map-reduce and other advanced branching patterns using the Send API. Here is an example of how to use it:

    API Reference: StateGraph | START | END | Send

    from langgraph.graph import StateGraph, START, END
    from langgraph.types import Send
    from typing_extensions import TypedDict, Annotated
    import operator

    class OverallState(TypedDict):
        topic: str
        subjects: list[str]
        jokes: Annotated[list[str], operator.add]
        best_selected_joke: str

    def generate_topics(state: OverallState):
        return {"subjects": ["lions", "elephants", "penguins"]}

    def generate_joke(state: OverallState):
        joke_map = {
            "lions": "Why don't lions like fast food? Because they can't catch it!",
            "elephants": "Why don't elephants use computers? They're afraid of the mouse!",
            "penguins": "Why don't penguins like talking to strangers at parties? Because they find it hard to break the ice."
        }
        return {"jokes": [joke_map[state["subject"]]]}

    def continue_to_jokes(state: OverallState):
        return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

    def best_joke(state: OverallState):
        return {"best_selected_joke": "penguins"}

    builder = StateGraph(OverallState)
    builder.add_node("generate_topics", generate_topics)
    builder.add_node("generate_joke", generate_joke)
    builder.add_node("best_joke", best_joke)
    builder.add_edge(START, "generate_topics")
    builder.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
    builder.add_edge("generate_joke", "best_joke")
    builder.add_edge("best_joke", END)
    builder.add_edge("generate_topics", END)
    graph = builder.compile()

    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))

    # Call the graph: here we call it to generate a list of jokes
    for step in graph.stream({"topic": "animals"}):
        print(step)

"""

"""
    === Create and control loops ====================
    When creating a graph with a loop, we require a mechanism for terminating execution. This is most commonly done by adding a conditional edge that routes to the END node once we reach some termination condition.
    You can also set the graph recursion limit when invoking or streaming the graph. The recursion limit sets the number of supersteps that the graph is allowed to execute before it raises an error. Read more about the concept of recursion limits here.

    Let's consider a simple graph with a loop to better understand how these mechanisms work.

    When creating a loop, you can include a conditional edge that specifies a termination condition:

    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)

    def route(state: State) -> Literal["b", END]:
        if termination_condition(state):
            return END
        else:
            return "b"

    builder.add_edge(START, "a")
    builder.add_conditional_edges("a", route)
    builder.add_edge("b", "a")
    graph = builder.compile()

    To control the recursion limit, specify "recursionLimit" in the config. This will raise a GraphRecursionError, which you can catch and handle:
    
    from langgraph.errors import GraphRecursionError

    try:
        graph.invoke(inputs, {"recursion_limit": 3})
    except GraphRecursionError:
        print("Recursion Error")

    Let's define a graph with a simple loop. Note that we use a conditional edge to implement a termination condition.

    API Reference: StateGraph | START | END

    import operator
    from typing import Annotated, Literal
    from typing_extensions import TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        # The operator.add reducer fn makes this append-only
        aggregate: Annotated[list, operator.add]

    def a(state: State):
        print(f'Node A sees {state["aggregate"]}')
        return {"aggregate": ["A"]}

    def b(state: State):
        print(f'Node B sees {state["aggregate"]}')
        return {"aggregate": ["B"]}

    # Define nodes
    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)

    # Define edges
    def route(state: State) -> Literal["b", END]:
        if len(state["aggregate"]) < 7:
            return "b"
        else:
            return END

    builder.add_edge(START, "a")
    builder.add_conditional_edges("a", route)
    builder.add_edge("b", "a")
    graph = builder.compile()

    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))

    This architecture is similar to a React agent in which node "a" is a tool-calling model, and node "b" represents the tools.

    In our route conditional edge, we specify that we should end after the "aggregate" list in the state passes a threshold length.

    Invoking the graph, we see that we alternate between nodes "a" and "b" before terminating once we reach the termination condition.

    === Create and control loops --> Impose a recursion limit ====================
    
    In some applications, we may not have a guarantee that we will reach a given termination condition. In these cases, we can set the graph's recursion limit. This will raise a GraphRecursionError after a given number of supersteps. We can then catch and handle this exception:
    
    from langgraph.errors import GraphRecursionError
    try:
        graph.invoke({"aggregate": []}, {"recursion_limit": 4})
    except GraphRecursionError:
        print("Recursion Error")


    Extended example: loops with branches

    import operator
    from typing import Annotated, Literal
    from typing_extensions import TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        aggregate: Annotated[list, operator.add]

    def a(state: State):
        print(f'Node A sees {state["aggregate"]}')
        return {"aggregate": ["A"]}

    def b(state: State):
        print(f'Node B sees {state["aggregate"]}')
        return {"aggregate": ["B"]}

    def c(state: State):
        print(f'Node C sees {state["aggregate"]}')
        return {"aggregate": ["C"]}

    def d(state: State):
        print(f'Node D sees {state["aggregate"]}')
        return {"aggregate": ["D"]}

    # Define nodes
    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(c)
    builder.add_node(d)

    # Define edges
    def route(state: State) -> Literal["b", END]:
        if len(state["aggregate"]) < 7:
            return "b"
        else:
            return END

    builder.add_edge(START, "a")
    builder.add_conditional_edges("a", route)
    builder.add_edge("b", "c")
    builder.add_edge("b", "d")
    builder.add_edge(["c", "d"], "a")
    graph = builder.compile()

    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))

"""

"""
    === Async ====================
    Using the async programming paradigm can produce significant performance improvements when running IO-bound code concurrently (e.g., making concurrent API requests to a chat model provider).

    To convert a sync implementation of the graph to an async implementation, you will need to:

    Update nodes use async def instead of def.
    Update the code inside to use await appropriately.
    Invoke the graph with .ainvoke or .astream as desired.
    Because many LangChain objects implement the Runnable Protocol which has async variants of all the sync methods it's typically fairly quick to upgrade a sync graph to an async graph.

    See example below. To demonstrate async invocations of underlying LLMs, we will include a chat model:

    pip install -U "langchain[openai]"

    import os
    from langchain.chat_models import init_chat_model

    os.environ["OPENAI_API_KEY"] = "sk-..."

    llm = init_chat_model("openai:gpt-4.1")

    from langchain.chat_models import init_chat_model
    from langgraph.graph import MessagesState, StateGraph

    async def node(state: MessagesState): 
        new_message = await llm.ainvoke(state["messages"]) 
        return {"messages": [new_message]}

    builder = StateGraph(MessagesState).add_node(node).set_entry_point("node")
    graph = builder.compile()

    input_message = {"role": "user", "content": "Hello"}
    result = await graph.ainvoke({"messages": [input_message]})

"""

"""
    === ACombine control flow and state updates with Command ====================
    
    It can be useful to combine control flow (edges) and state updates (nodes). For example, you might want to BOTH perform state updates AND decide which node to go to next in the SAME node. LangGraph provides a way to do so by returning a Command object from node functions:
 
    def my_node(state: State) -> Command[Literal["my_other_node"]]:
        return Command(
            # state update
            update={"foo": "bar"},
            # control flow
            goto="my_other_node"
        )

    We show an end-to-end example below. Let's create a simple graph with 3 nodes: A, B and C. 
    We will first execute node A, and then decide whether to go to Node B or Node C next based on the output of node A.
    API Reference: StateGraph | START | Command

    import random
    from typing_extensions import TypedDict, Literal
    from langgraph.graph import StateGraph, START
    from langgraph.types import Command

    # Define graph state
    class State(TypedDict):
        foo: str

    # Define the nodes

    def node_a(state: State) -> Command[Literal["node_b", "node_c"]]:
        print("Called A")
        value = random.choice(["b", "c"])
        # this is a replacement for a conditional edge function
        if value == "b":
            goto = "node_b"
        else:
            goto = "node_c"

        # note how Command allows you to BOTH update the graph state AND route to the next node
        return Command(
            # this is the state update
            update={"foo": value},
            # this is a replacement for an edge
            goto=goto,
        )

    def node_b(state: State):
        print("Called B")
        return {"foo": state["foo"] + "b"}

    def node_c(state: State):
        print("Called C")
        return {"foo": state["foo"] + "c"}

        builder = StateGraph(State)

    builder.add_edge(START, "node_a")
    builder.add_node(node_a)
    builder.add_node(node_b)
    builder.add_node(node_c)
    # NOTE: there are no edges between nodes A, B and C!

    graph = builder.compile()

    from IPython.display import display, Image

    display(Image(graph.get_graph().draw_mermaid_png()))


    === ACombine control flow and state updates with Command -->  Navigate to a node in a parent graph ====================
    If you are using subgraphs, you might want to navigate from a node within a subgraph to a different subgraph (i.e. a different node in the parent graph). To do so, you can specify graph=Command.PARENT in Command:

    def my_node(state: State) -> Command[Literal["my_other_node"]]:
    return Command(
        update={"foo": "bar"},
        goto="other_subgraph",  # where `other_subgraph` is a node in the parent graph
        graph=Command.PARENT
    )

    Let's demonstrate this using the above example. We'll do so by changing nodeA in the above example into a single-node graph that we'll add as a subgraph to our parent graph.

    import operator
    from typing_extensions import Annotated

    class State(TypedDict):
        # NOTE: we define a reducer here
        foo: Annotated[str, operator.add]

    def node_a(state: State):
        print("Called A")
        value = random.choice(["a", "b"])
        # this is a replacement for a conditional edge function
        if value == "a":
            goto = "node_b"
        else:
            goto = "node_c"

        # note how Command allows you to BOTH update the graph state AND route to the next node
        return Command(
            update={"foo": value},
            goto=goto,
            # this tells LangGraph to navigate to node_b or node_c in the parent graph
            # NOTE: this will navigate to the closest parent graph relative to the subgraph
            graph=Command.PARENT,
        )

    subgraph = StateGraph(State).add_node(node_a).add_edge(START, "node_a").compile()

    def node_b(state: State):
        print("Called B")
        # NOTE: since we've defined a reducer, we don't need to manually append
        # new characters to existing 'foo' value. instead, reducer will append these
        # automatically (via operator.add)
        return {"foo": "b"}

    def node_c(state: State):
        print("Called C")
        return {"foo": "c"}

    builder = StateGraph(State)
    builder.add_edge(START, "subgraph")
    builder.add_node("subgraph", subgraph)
    builder.add_node(node_b)
    builder.add_node(node_c)

    graph = builder.compile()

    
    === ACombine control flow and state updates with Command -->  Use inside tools ====================
    A common use case is updating graph state from inside a tool. For example, in a customer support application you might want to look up customer information based on their account number or ID in the beginning of the conversation. To update the graph state from the tool, you can return Command(update={"my_custom_key": "foo", "messages": [...]}) from the tool:

    @tool
    def lookup_user_info(tool_call_id: Annotated[str, InjectedToolCallId], config: RunnableConfig):
        ''' Use this to look up user information to better assist them with their questions.'''
        user_info = get_user_info(config.get("configurable", {}).get("user_id"))
        return Command(
            update={
                # update the state keys
                "user_info": user_info,
                # update the message history
                "messages": [ToolMessage("Successfully looked up user information", tool_call_id=tool_call_id)]
            }
        )

    If you are using tools that update state via Command, we recommend using prebuilt ToolNode which automatically handles tools returning Command objects and propagates them to the graph state. If you're writing a custom node that calls tools, you would need to manually propagate Command objects returned by the tools as the update from the node.

"""

"""
    === Visualize your graph ====================
    Here we demonstrate how to visualize the graphs you create.

    You can visualize any arbitrary Graph, including StateGraph.

    Let's have some fun by drawing fractals :).

    API Reference: StateGraph | START | END | add_messages

    import random
    from typing import Annotated, Literal
    from typing_extensions import TypedDict
    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.message import add_messages

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    class MyNode:
        def __init__(self, name: str):
            self.name = name
        def __call__(self, state: State):
            return {"messages": [("assistant", f"Called node {self.name}")]}

    def route(state) -> Literal["entry_node", "__end__"]:
        if len(state["messages"]) > 10:
            return "__end__"
        return "entry_node"

    def add_fractal_nodes(builder, current_node, level, max_level):
        if level > max_level:
            return
        # Number of nodes to create at this level
        num_nodes = random.randint(1, 3)  # Adjust randomness as needed
        for i in range(num_nodes):
            nm = ["A", "B", "C"][i]
            node_name = f"node_{current_node}_{nm}"
            builder.add_node(node_name, MyNode(node_name))
            builder.add_edge(current_node, node_name)
            # Recursively add more nodes
            r = random.random()
            if r > 0.2 and level + 1 < max_level:
                add_fractal_nodes(builder, node_name, level + 1, max_level)
            elif r > 0.05:
                builder.add_conditional_edges(node_name, route, node_name)
            else:
                # End
                builder.add_edge(node_name, "__end__")

    def build_fractal_graph(max_level: int):
        builder = StateGraph(State)
        entry_point = "entry_node"
        builder.add_node(entry_point, MyNode(entry_point))
        builder.add_edge(START, entry_point)
        add_fractal_nodes(builder, entry_point, 1, max_level)
        # Optional: set a finish point if required
        builder.add_edge(entry_point, END)  # or any specific node
        return builder.compile()

    app = build_fractal_graph(3)

    === Visualize your graph --> Mermaid ====================
    We can also convert a graph class into Mermaid syntax.

    print(app.get_graph().draw_mermaid())

    === Visualize your graph --> PNG ====================
    If preferred, we could render the Graph into a .png. Here we could use three options:

    Using Mermaid.ink API (does not require additional packages)
    Using Mermaid + Pyppeteer (requires pip install pyppeteer)
    Using graphviz (which requires pip install graphviz)

    === Visualize your graph --> PNG --> Using Mermaid.Ink ====================
    By default, draw_mermaid_png() uses Mermaid.Ink's API to generate the diagram.

    API Reference: CurveStyle | MermaidDrawMethod | NodeStyles


    from IPython.display import Image, display
    from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

    display(Image(app.get_graph().draw_mermaid_png()))

    === Visualize your graph --> PNG --> Using Mermaid + Pyppeteer ====================
    import nest_asyncio

    nest_asyncio.apply()  # Required for Jupyter Notebook to run async functions

    display(
        Image(
            app.get_graph().draw_mermaid_png(
                curve_style=CurveStyle.LINEAR,
                node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"),
                wrap_label_n_words=9,
                output_file_path=None,
                draw_method=MermaidDrawMethod.PYPPETEER,
                background_color="white",
                padding=10,
            )
        )
    )

    === Visualize your graph --> PNG --> Using Graphviz ====================
    try:
        display(Image(app.get_graph().draw_png()))
    except ImportError:
        print(
            "You likely need to install dependencies for pygraphviz, see more here https://github.com/pygraphviz/pygraphviz/blob/main/INSTALL.txt"
        )
"""
