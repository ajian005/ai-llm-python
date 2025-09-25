"""
    Models   https://langchain-ai.github.io/langgraph/agents/models/

    Models¶
    LangGraph provides built-in support for LLMs (language models) via the LangChain library. This makes it easy to integrate various LLMs into your agents and workflows.

"""

"""
==== Initialize a model ========================================================================================
    Use init_chat_model to initialize models:

---- OpenAI -----------------------------------------
    pip install -U "langchain[openai]"

    import os
    from langchain.chat_models import init_chat_model

    os.environ["OPENAI_API_KEY"] = "sk-..."

    llm = init_chat_model("openai:gpt-4.1")
    👉 Read the OpenAI integration docs for more information.

---- Anthropic -----------------------------------------
    pip install -U "langchain[anthropic]"

    import os
    from langchain.chat_models import init_chat_model

    os.environ["ANTHROPIC_API_KEY"] = "sk-..."

    llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

---- Azure -----------------------------------------
    pip install -U "langchain[openai]"

    import os
    from langchain.chat_models import init_chat_model

    os.environ["AZURE_OPENAI_API_KEY"] = "..."
    os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
    os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

    llm = init_chat_model(
        "azure_openai:gpt-4.1",
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    )
    Read the Azure integration docs

---- Google Gemini -----------------------------------------
    pip install -U "langchain[google-genai]"

    import os
    from langchain.chat_models import init_chat_model

    os.environ["GOOGLE_API_KEY"] = "..."

    llm = init_chat_model("google_genai:gemini-2.0-flash")
    👉 Read the Google GenAI integration docs

---- AWS Bedrock -----------------------------------------
    pip install -U "langchain[aws]"

    from langchain.chat_models import init_chat_model

    # Follow the steps here to configure your credentials:
    # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

    llm = init_chat_model(
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_provider="bedrock_converse",
    )
    👉 Read the AWS Bedrock integration docs

==== Initialize a model ----> Instantiate a model directly ========================================================================================
    If a model provider is not available via init_chat_model, you can instantiate the provider's model class directly. The model must implement the BaseChatModel interface and support tool calling:

    API Reference: ChatAnthropic

    # Anthropic is already supported by `init_chat_model`,
    # but you can also instantiate it directly.
    from langchain_anthropic import ChatAnthropic

    model = ChatAnthropic(
    model="claude-3-7-sonnet-latest",
    temperature=0,
    max_tokens=2048
    )

    Tool calling support

    If you are building an agent or workflow that requires the model to call external tools, ensure that the underlying language model supports tool calling. Compatible models can be found in the LangChain integrations directory.

"""


"""
==== Use in an agent========================================================================================

When using create_react_agent you can specify the model by its name string, which is a shorthand for initializing the model using init_chat_model. This allows you to use the model without needing to import or instantiate it directly.

---- model name -----------------------------------------
    from langgraph.prebuilt import create_react_agent

    create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    # other parameters
    )

---- model instance -----------------------------------------
    from langchain_anthropic import ChatAnthropic
    from langgraph.prebuilt import create_react_agent

    model = ChatAnthropic(
        model="claude-3-7-sonnet-latest",
        temperature=0,
        max_tokens=2048
    )
    # Alternatively
    # model = init_chat_model("anthropic:claude-3-7-sonnet-latest")

    agent = create_react_agent(
    model=model,
    # other parameters
    )

==== Use in an agent ----> Dynamic model selection ========================================================================================
    Pass a callable function to create_react_agent to dynamically select the model at runtime. This is useful for scenarios where you want to choose a model based on user input, configuration settings, or other runtime conditions.

    The selector function must return a chat model. If you're using tools, you must bind the tools to the model within the selector function.

    API Reference: init_chat_model | BaseChatModel | tool | create_react_agent | AgentState


    from dataclasses import dataclass
    from typing import Literal
    from langchain.chat_models import init_chat_model
    from langchain_core.language_models import BaseChatModel
    from langchain_core.tools import tool
    from langgraph.prebuilt import create_react_agent
    from langgraph.prebuilt.chat_agent_executor import AgentState
    from langgraph.runtime import Runtime

    @tool
    def weather() -> str:
        '''Returns the current weather conditions.'''
        return "It's nice and sunny."


    # Define the runtime context
    @dataclass
    class CustomContext:
        provider: Literal["anthropic", "openai"]

    # Initialize models
    openai_model = init_chat_model("openai:gpt-4o")
    anthropic_model = init_chat_model("anthropic:claude-sonnet-4-20250514")


    # Selector function for model choice
    def select_model(state: AgentState, runtime: Runtime[CustomContext]) -> BaseChatModel:
        if runtime.context.provider == "anthropic":
            model = anthropic_model
        elif runtime.context.provider == "openai":
            model = openai_model
        else:
            raise ValueError(f"Unsupported provider: {runtime.context.provider}")

        # With dynamic model selection, you must bind tools explicitly
        return model.bind_tools([weather])


    # Create agent with dynamic model selection
    agent = create_react_agent(select_model, tools=[weather])

    # Invoke with context to select model
    output = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Which model is handling this?",
                }
            ]
        },
        context=CustomContext(provider="openai"),
    )

    print(output["messages"][-1].text())

"""

"""
==== Advanced model configuration ========================================================================================

==== Advanced model configuration ----> Disable streaming ========================================================================================


==== Advanced model configuration ----> Add model fallbacks ========================================================================================


==== Advanced model configuration ----> Use the built-in rate limiter ========================================================================================


"""



