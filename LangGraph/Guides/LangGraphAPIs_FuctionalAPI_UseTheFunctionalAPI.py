"""
    Use the functional API : https://langchain-ai.github.io/langgraph/how-tos/use-functional-api/

    The Functional API allows you to add LangGraph's key features — persistence, memory, human-in-the-loop, and streaming — to your applications with minimal changes to your existing code.

"""
"""
    === Creating a simple workflow ====================
    When defining an entrypoint, input is restricted to the first argument of the function. To pass multiple inputs, you can use a dictionary.

    @entrypoint(checkpointer=checkpointer)
    def my_workflow(inputs: dict) -> int:
        value = inputs["value"]
        another_value = inputs["another_value"]
        ...

    my_workflow.invoke({"value": 1, "another_value": 2})

    Extended example: simple workflow

    import uuid
    from langgraph.func import entrypoint, task
    from langgraph.checkpoint.memory import InMemorySaver

    # Task that checks if a number is even
    @task
    def is_even(number: int) -> bool:
        return number % 2 == 0

    # Task that formats a message
    @task
    def format_message(is_even: bool) -> str:
        return "The number is even." if is_even else "The number is odd."

    # Create a checkpointer for persistence
    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def workflow(inputs: dict) -> str:
        ''' Simple workflow to classify a number. ''' 
        even = is_even(inputs["number"]).result()
        return format_message(even).result()

    # Run the workflow with a unique thread ID
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = workflow.invoke({"number": 7}, config=config)
    print(result)


    Extended example: Compose an essay with an LLM
    import uuid
    from langchain.chat_models import init_chat_model
    from langgraph.func import entrypoint, task
    from langgraph.checkpoint.memory import InMemorySaver

    llm = init_chat_model('openai:gpt-3.5-turbo')

    # Task: generate essay using an LLM
    @task
    def compose_essay(topic: str) -> str:
        '''Generate an essay about the given topic. '''
        return llm.invoke([
            {"role": "system", "content": "You are a helpful assistant that writes essays."},
            {"role": "user", "content": f"Write an essay about {topic}."}
        ]).content

    # Create a checkpointer for persistence
    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def workflow(topic: str) -> str:
        '''Simple workflow that generates an essay with an LLM.'''
        return compose_essay(topic).result()

    # Execute the workflow
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = workflow.invoke("the history of flight", config=config)
    print(result)

"""


"""
    === Parallel execution ====================

    Tasks can be executed in parallel by invoking them concurrently and waiting for the results. This is useful for improving performance in IO bound tasks (e.g., calling APIs for LLMs).

    @task
    def add_one(number: int) -> int:
        return number + 1

    @entrypoint(checkpointer=checkpointer)
    def graph(numbers: list[int]) -> list[str]:
        futures = [add_one(i) for i in numbers]
        return [f.result() for f in futures]

    Extended example: parallel LLM calls

    This example demonstrates how to run multiple LLM calls in parallel using @task. Each call generates a paragraph on a different topic, and results are joined into a single text output.

    import uuid
    from langchain.chat_models import init_chat_model
    from langgraph.func import entrypoint, task
    from langgraph.checkpoint.memory import InMemorySaver

    # Initialize the LLM model
    llm = init_chat_model("openai:gpt-3.5-turbo")

    # Task that generates a paragraph about a given topic
    @task
    def generate_paragraph(topic: str) -> str:
        response = llm.invoke([
            {"role": "system", "content": "You are a helpful assistant that writes educational paragraphs."},
            {"role": "user", "content": f"Write a paragraph about {topic}."}
        ])
        return response.content

    # Create a checkpointer for persistence
    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def workflow(topics: list[str]) -> str:
        '''Generates multiple paragraphs in parallel and combines them.'''
        futures = [generate_paragraph(topic) for topic in topics]
        paragraphs = [f.result() for f in futures]
        return "\n\n".join(paragraphs)

    # Run the workflow
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = workflow.invoke(["quantum computing", "climate change", "history of aviation"], config=config)
    print(result)

"""

"""
    === Parallel execution ====================
    Tasks can be executed in parallel by invoking them concurrently and waiting for the results. This is useful for improving performance in IO bound tasks (e.g., calling APIs for LLMs).

    @task
    def add_one(number: int) -> int:
        return number + 1

    @entrypoint(checkpointer=checkpointer)
    def graph(numbers: list[int]) -> list[int]:
        futures = [add_one(i) for i in numbers]
        return [f.result() for f in futures]

    ----- Extended example: parallel LLM calls --------------------
    This example demonstrates how to run multiple LLM calls in parallel using @task. Each call generates a paragraph on a different topic, and results are joined into a single text output.

    import uuid
    from langchain.chat_models import init_chat_model
    from langgraph.func import entrypoint, task
    from langgraph.checkpoint.memory import InMemorySaver

    # Initialize the LLM model
    llm = init_chat_model("openai:gpt-3.5-turbo")

    # Task that generates a paragraph about a given topic
    @task
    def generate_paragraph(topic: str) -> str:
        response = llm.invoke([
            {"role": "system", "content": "You are a helpful assistant that writes educational paragraphs."},
            {"role": "user", "content": f"Write a paragraph about {topic}."}
        ])
        return response.content

    # Create a checkpointer for persistence
    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def workflow(topics: list[str]) -> str:
        ''' Generates multiple paragraphs in parallel and combines them. '''
        futures = [generate_paragraph(topic) for topic in topics]
        paragraphs = [f.result() for f in futures]
        return "\n\n".join(paragraphs)

    # Run the workflow
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = workflow.invoke(["quantum computing", "climate change", "history of aviation"], config=config)
    print(result)

    This example uses LangGraph's concurrency model to improve execution time, especially when tasks involve I/O like LLM completions.
"""

"""
    === Calling graphs ====================
    The Functional API and the Graph API can be used together in the same application as they share the same underlying runtime.

    API Reference: entrypoint | StateGraph

    from langgraph.func  import entrypoint
    from langgraph.graph import StateGraph

    builder = StateGraph()
    ...
    some_graph = builder.compile()

    @entrypoint()
    def some_workflow(some_input: dict) -> int:
        # Call a graph defined using the graph API
        result_1 = some_graph.invoke(...)
        # Call another graph defined using the graph API
        result_2 = another_graph.invoke(...)
        return {
            "result_1": result_1,
            "result_2": result_2
        }

    ----- Extended example: calling a simple graph from the functional API --------------------
    import uuid
    from typing import TypedDict
    from langgraph.func import entrypoint
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.graph import StateGraph

    # Define the shared state type
    class State(TypedDict):
        foo: int

    # Define a simple transformation node
    def double(state: State) -> State:
        return {"foo": state["foo"] * 2}

    # Build the graph using the Graph API
    builder = StateGraph(State)
    builder.add_node("double", double)
    builder.set_entry_point("double")
    graph = builder.compile()

    # Define the functional API workflow
    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def workflow(x: int) -> dict:
        result = graph.invoke({"foo": x})
        return {"bar": result["foo"]}

    # Execute the workflow
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    print(workflow.invoke(5, config=config))  # Output: {'bar': 10}

"""

"""
    === Call other entrypoints ====================
    You can call other entrypoints from within an entrypoint or a task.

    @entrypoint() # Will automatically use the checkpointer from the parent entrypoint
    def some_other_workflow(inputs: dict) -> int:
        return inputs["value"]

    @entrypoint(checkpointer=checkpointer)
    def my_workflow(inputs: dict) -> int:
        value = some_other_workflow.invoke({"value": 1})
        return value

    ----- Extended example: calling another entrypoint --------------------
    import uuid
    from langgraph.func import entrypoint
    from langgraph.checkpoint.memory import InMemorySaver

    # Initialize a checkpointer
    checkpointer = InMemorySaver()

    # A reusable sub-workflow that multiplies a number
    @entrypoint()
    def multiply(inputs: dict) -> int:
        return inputs["a"] * inputs["b"]

    # Main workflow that invokes the sub-workflow
    @entrypoint(checkpointer=checkpointer)
    def main(inputs: dict) -> dict:
        result = multiply.invoke({"a": inputs["x"], "b": inputs["y"]})
        return {"product": result}

    # Execute the main workflow
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    print(main.invoke({"x": 6, "y": 7}, config=config))  # Output: {'product': 42}

"""

"""
    === Streaming ====================
    The Functional API uses the same streaming mechanism as the Graph API. Please read the streaming guide section for more details.

    Example of using the streaming API to stream both updates and custom data.

    API Reference: entrypoint | InMemorySaver | get_stream_writer

    from langgraph.func import entrypoint
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.config import get_stream_writer 

    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def main(inputs: dict) -> int:
        writer = get_stream_writer() 
        writer("Started processing") 
        result = inputs["x"] * 2
        writer(f"Result is {result}") 
        return result

    config = {"configurable": {"thread_id": "abc"}}

    for mode, chunk in main.stream( 
        {"x": 5},
        stream_mode=["custom", "updates"], 
        config=config
    ):
        print(f"{mode}: {chunk}")

"""


"""
    === Retry policy ====================

    API Reference: InMemorySaver | entrypoint | task | RetryPolicy
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.func import entrypoint, task
    from langgraph.types import RetryPolicy

    # This variable is just used for demonstration purposes to simulate a network failure.
    # It's not something you will have in your actual code.
    attempts = 0

    # Let's configure the RetryPolicy to retry on ValueError.
    # The default RetryPolicy is optimized for retrying specific network errors.
    retry_policy = RetryPolicy(retry_on=ValueError)

    @task(retry_policy=retry_policy)
    def get_info():
        global attempts
        attempts += 1

        if attempts < 2:
            raise ValueError('Failure')
        return "OK"

    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def main(inputs, writer):
        return get_info().result()

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    main.invoke({'any_input': 'foobar'}, config=config)
"""

"""
    === Caching Tasks ====================
    API Reference: entrypoint | task

    import time
    from langgraph.cache.memory import InMemoryCache
    from langgraph.func import entrypoint, task
    from langgraph.types import CachePolicy


    @task(cache_policy=CachePolicy(ttl=120))  
    def slow_add(x: int) -> int:
        time.sleep(1)
        return x * 2


    @entrypoint(cache=InMemoryCache())
    def main(inputs: dict) -> dict[str, int]:
        result1 = slow_add(inputs["x"]).result()
        result2 = slow_add(inputs["x"]).result()
        return {"result1": result1, "result2": result2}


    for chunk in main.stream({"x": 5}, stream_mode="updates"):
        print(chunk)

    #> {'slow_add': 10}
    #> {'slow_add': 10, '__metadata__': {'cached': True}}
    #> {'main': {'result1': 10, 'result2': 10}}

"""

"""
    === Resuming after an error ====================
    import time
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.func import entrypoint, task
    from langgraph.types import StreamWriter

    # This variable is just used for demonstration purposes to simulate a network failure.
    # It's not something you will have in your actual code.
    attempts = 0

    @task()
    def get_info():
        '''
        Simulates a task that fails once before succeeding.
        Raises an exception on the first attempt, then returns "OK" on subsequent tries.
        '''
        global attempts
        attempts += 1

        if attempts < 2:
            raise ValueError("Failure")  # Simulate a failure on the first attempt
        return "OK"

    # Initialize an in-memory checkpointer for persistence
    checkpointer = InMemorySaver()

    @task
    def slow_task():
        '''
        Simulates a slow-running task by introducing a 1-second delay.
        '''
        time.sleep(1)
        return "Ran slow task."

    @entrypoint(checkpointer=checkpointer)
    def main(inputs, writer: StreamWriter):
        '''
        Main workflow function that runs the slow_task and get_info tasks sequentially.

        Parameters:
        - inputs: Dictionary containing workflow input values.
        - writer: StreamWriter for streaming custom data.

        The workflow first executes `slow_task` and then attempts to execute `get_info`,
        which will fail on the first invocation.
        '''
        slow_task_result = slow_task().result()  # Blocking call to slow_task
        get_info().result()  # Exception will be raised here on the first attempt
        return slow_task_result

    # Workflow execution configuration with a unique thread identifier
    config = {
        "configurable": {
            "thread_id": "1"  # Unique identifier to track workflow execution
        }
    }

    # This invocation will take ~1 second due to the slow_task execution
    try:
        # First invocation will raise an exception due to the `get_info` task failing
        main.invoke({'any_input': 'foobar'}, config=config)
    except ValueError:
        pass  # Handle the failure gracefully

"""

"""
    === Human-in-the-loop ====================
    
    The functional API supports human-in-the-loop workflows using the interrupt function and the Command primitive.

    ----- Basic human-in-the-loop workflow --------------------------------

    We will create three tasks:

    Append "bar".
    Pause for human input. When resuming, append human input.
    Append "qux".
    API Reference: entrypoint | task | Command | interrupt

    from langgraph.func import entrypoint, task
    from langgraph.types import Command, interrupt


    @task
    def step_1(input_query):
        ''' Append bar. '''
        return f"{input_query} bar"


    @task
    def human_feedback(input_query):
        ''' Append user input. ''' 
        feedback = interrupt(f"Please provide feedback: {input_query}")
        return f"{input_query} {feedback}"


    @task
    def step_3(input_query):
        '''  Append qux. ''' 
        return f"{input_query} qux"

    We can now compose these tasks in an entrypoint:

    API Reference: InMemorySaver

    from langgraph.checkpoint.memory import InMemorySaver

    checkpointer = InMemorySaver()


    @entrypoint(checkpointer=checkpointer)
    def graph(input_query):
        result_1 = step_1(input_query).result()
        result_2 = human_feedback(result_1).result()
        result_3 = step_3(result_2).result()

        return result_3

    interrupt() is called inside a task, enabling a human to review and edit the output of the previous task. The results of prior tasks-- in this case step_1-- are persisted, so that they are not run again following the interrupt.

    Let's send in a query string:

    config = {"configurable": {"thread_id": "1"}}

    for event in graph.stream("foo", config):
        print(event)
        print("\n")


    Note that we've paused with an interrupt after step_1. The interrupt provides instructions to resume the run. To resume, we issue a Command containing the data expected by the human_feedback task.
        # Continue execution
        for event in graph.stream(Command(resume="baz"), config):
            print(event)
            print("\n")

    ----- Review tool calls --------------------------------
    To review tool calls before execution, we add a review_tool_call function that calls interrupt. When this function is called, execution will be paused until we issue a command to resume it.

    Given a tool call, our function will interrupt for human review. At that point we can either:

    Accept the tool call
    Revise the tool call and continue
    Generate a custom tool message (e.g., instructing the model to re-format its tool call)

    from typing import Union

    def review_tool_call(tool_call: ToolCall) -> Union[ToolCall, ToolMessage]:
        ''' Review a tool call, returning a validated version. ''' 
        human_review = interrupt(
            {
                "question": "Is this correct?",
                "tool_call": tool_call,
            }
        )
        review_action = human_review["action"]
        review_data = human_review.get("data")
        if review_action == "continue":
            return tool_call
        elif review_action == "update":
            updated_tool_call = {**tool_call, **{"args": review_data}}
            return updated_tool_call
        elif review_action == "feedback":
            return ToolMessage(
                content=review_data, name=tool_call["name"], tool_call_id=tool_call["id"]
            )

    We can now update our entrypoint to review the generated tool calls. If a tool call is accepted or revised, we execute in the same way as before. 
    Otherwise, we just append the ToolMessage supplied by the human. The results of prior tasks — in this case the initial model call — are persisted, 
    so that they are not run again following the interrupt.

    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.graph.message import add_messages
    from langgraph.types import Command, interrupt

    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def agent(messages, previous):
        if previous is not None:
            messages = add_messages(previous, messages)

        llm_response = call_model(messages).result()
        while True:
            if not llm_response.tool_calls:
                break

            # Review tool calls
            tool_results = []
            tool_calls = []
            for i, tool_call in enumerate(llm_response.tool_calls):
                review = review_tool_call(tool_call)
                if isinstance(review, ToolMessage):
                    tool_results.append(review)
                else:  # is a validated tool call
                    tool_calls.append(review)
                    if review != tool_call:
                        llm_response.tool_calls[i] = review  # update message

            # Execute remaining tool calls
            tool_result_futures = [call_tool(tool_call) for tool_call in tool_calls]
            remaining_tool_results = [fut.result() for fut in tool_result_futures]

            # Append to message list
            messages = add_messages(
                messages,
                [llm_response, *tool_results, *remaining_tool_results],
            )

            # Call model again
            llm_response = call_model(messages).result()

        # Generate final response
        messages = add_messages(messages, llm_response)
        return entrypoint.final(value=llm_response, save=messages)

"""


"""
    === Short-term memory ====================
    Short-term memory allows storing information across different invocations of the same thread id. See short-term memory for more details.

    
    ----- Short-term memory --> Manage checkpoints --------------------------------
    You can view and delete the information stored by the checkpointer.

    View thread state (checkpoint)
        config = {
            "configurable": {
                "thread_id": "1",
                # optionally provide an ID for a specific checkpoint,
                # otherwise the latest checkpoint is shown
                # "checkpoint_id": "1f029ca3-1f5b-6704-8004-820c16b69a5a"

            }
        }
    graph.get_state(config)

    View the history of the thread (checkpoints)¶
        config = {
        "configurable": {
            "thread_id": "1"
            }
    }
    list(graph.get_state_history(config))

    ----- Short-term memory --> Decouple return value from saved value --------------------------------

    Use entrypoint.final to decouple what is returned to the caller from what is persisted in the checkpoint. This is useful when:

    You want to return a computed result (e.g., a summary or status), but save a different internal value for use on the next invocation.
    You need to control what gets passed to the previous parameter on the next run.

    from typing import Optional
    from langgraph.func import entrypoint
    from langgraph.checkpoint.memory import InMemorySaver

    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def accumulate(n: int, *, previous: Optional[int]) -> entrypoint.final[int, int]:
        previous = previous or 0
        total = previous + n
        # Return the *previous* value to the caller but save the *new* total to the checkpoint.
        return entrypoint.final(value=previous, save=total)

    config = {"configurable": {"thread_id": "my-thread"}}

    print(accumulate.invoke(1, config=config))  # 0
    print(accumulate.invoke(2, config=config))  # 1
    print(accumulate.invoke(3, config=config))  # 3

    ----- Short-term memory --> Chatbot example¶ --------------------------------

    An example of a simple chatbot using the functional API and the InMemorySaver checkpointer. The bot is able to remember the previous conversation and continue from where it left off.

    API Reference: BaseMessage | add_messages | entrypoint | task | InMemorySaver | ChatAnthropic


    from langchain_core.messages import BaseMessage
    from langgraph.graph import add_messages
    from langgraph.func import entrypoint, task
    from langgraph.checkpoint.memory import InMemorySaver
    from langchain_anthropic import ChatAnthropic

    model = ChatAnthropic(model="claude-3-5-sonnet-latest")

    @task
    def call_model(messages: list[BaseMessage]):
        response = model.invoke(messages)
        return response

    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage]):
        if previous:
            inputs = add_messages(previous, inputs)

        response = call_model(inputs).result()
        return entrypoint.final(value=response, save=add_messages(inputs, response))

    config = {"configurable": {"thread_id": "1"}}
    input_message = {"role": "user", "content": "hi! I'm bob"}
    for chunk in workflow.stream([input_message], config, stream_mode="values"):
        chunk.pretty_print()

    input_message = {"role": "user", "content": "what's my name?"}
    for chunk in workflow.stream([input_message], config, stream_mode="values"):
        chunk.pretty_print()
"""


"""
    === Short-term memory ====================
Long-term memory
    long-term memory allows storing information across different thread ids. This could be useful for learning information about a given user in one conversation and using it in another.

"""

"""
    === Workflows ====================

    Workflows and agent guide for more examples of how to build workflows using the Functional API.
    
"""

"""
    === Agents ====================
    How to create an agent from scratch (Functional API): Shows how to create a simple agent from scratch using the functional API.
    How to build a multi-agent network: Shows how to build a multi-agent network using the functional API.
    How to add multi-turn conversation in a multi-agent application (functional API): allow an end-user to engage in a multi-turn conversation with one or more agents.

"""

"""
    === Integrate with other libraries ====================
    Add LangGraph's features to other frameworks using the functional API: Add LangGraph features like persistence, 
    memory and streaming to other agent frameworks that do not provide them out of the box.
"""
