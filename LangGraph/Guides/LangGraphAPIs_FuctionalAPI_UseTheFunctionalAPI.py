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
