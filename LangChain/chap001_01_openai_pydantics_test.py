"""
    How to return structured data from a model    https://python.langchain.com/docs/how_to/structured_output/#choosing-between-multiple-schemas
"""

import getpass
import os
from langchain.chat_models import init_chat_model

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# 初始化 OpenAI 模型
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

from typing import Optional
from pydantic import BaseModel, Field

flag = 7
# Pydantic
if flag == 1:
    class Joke(BaseModel):
        """Joke to tell user."""
        setup: str = Field(description="The setup of the joke")
        punchline: str = Field(description="The punchline to the joke")
        rating: Optional[int] = Field(
            default=None, description="How funny the joke is, from 1 to 10"
        )
    structured_llm = llm.with_structured_output(Joke)
    result = structured_llm.invoke("Tell me a joke about cats")
    print("result=", result)

# TypedDict or JSON Schema
if flag == 2:
   from typing import Optional
   from typing_extensions import Annotated, TypedDict
    # TypedDict
   class Joke(TypedDict):
        """Joke to tell user."""
        setup: Annotated[str, ..., "The setup of the joke"]
        # Alternatively, we could have specified setup as:
        # setup: str                    # no default, no description
        # setup: Annotated[str, ...]    # no default, no description
        # setup: Annotated[str, "foo"]  # default, no description
        punchline: Annotated[str, ..., "The punchline of the joke"]
        rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]
   structured_llm = llm.with_structured_output(Joke)
   result = structured_llm.invoke("Tell me a joke about cats")
   print("result=", result)


# Choosing between multiple schemas  Using Pydantic
if flag == 3:
    from typing import Union
    class Joke(BaseModel):
        """Joke to tell user."""

        setup: str = Field(description="The setup of the joke")
        punchline: str = Field(description="The punchline to the joke")
        rating: Optional[int] = Field(
            default=None, description="How funny the joke is, from 1 to 10"
        )
    class ConversationalResponse(BaseModel):
        """Respond in a conversational manner. Be kind and helpful."""
        response: str = Field(description="A conversational response to the user's query")
    class FinalResponse(BaseModel):
        final_output: Union[Joke, ConversationalResponse]

    structured_llm = llm.with_structured_output(FinalResponse)
    result = structured_llm.invoke("Tell me a joke about cats")
    print("result=", result)

#  Choosing between multiple schemas  Using TypedDict
if flag == 4:
    from typing import Optional, Union
    from typing_extensions import Annotated, TypedDict

    class Joke(TypedDict):
        """Joke to tell user."""
        setup: Annotated[str, ..., "The setup of the joke"]
        punchline: Annotated[str, ..., "The punchline of the joke"]
        rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

    class ConversationalResponse(TypedDict):
        """Respond in a conversational manner. Be kind and helpful."""
        response: Annotated[str, ..., "A conversational response to the user's query"]

    class FinalResponse(TypedDict):
        final_output: Union[Joke, ConversationalResponse]

    structured_llm = llm.with_structured_output(FinalResponse)
    result = structured_llm.invoke("Tell me a joke about cats")
    print("result=", result)

# Streaming
if flag == 5:
    from typing_extensions import Annotated, TypedDict

    # TypedDict
    class Joke(TypedDict):
        """Joke to tell user."""
        setup: Annotated[str, ..., "The setup of the joke"]
        punchline: Annotated[str, ..., "The punchline of the joke"]
        rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

    structured_llm = llm.with_structured_output(Joke)
    for chunk in structured_llm.stream("Tell me a joke about cats"):
        print(chunk)

# Few-shot prompting
if flag == 6:
    from typing_extensions import Annotated, TypedDict

    # TypedDict
    class Joke(TypedDict):
        """Joke to tell user."""
        setup: Annotated[str, ..., "The setup of the joke"]
        punchline: Annotated[str, ..., "The punchline of the joke"]
        rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

    structured_llm = llm.with_structured_output(Joke)
    from langchain_core.prompts import ChatPromptTemplate
    system = """You are a hilarious comedian. Your specialty is knock-knock jokes. \
    Return a joke which has the setup (the response to "Who's there?") and the final punchline (the response to "<setup> who?").

    Here are some examples of jokes:

    example_user: Tell me a joke about planes
    example_assistant: {{"setup": "Why don't planes ever get tired?", "punchline": "Because they have rest wings!", "rating": 2}}

    example_user: Tell me another joke about planes
    example_assistant: {{"setup": "Cargo", "punchline": "Cargo 'vroom vroom', but planes go 'zoom zoom'!", "rating": 10}}

    example_user: Now about caterpillars
    example_assistant: {{"setup": "Caterpillar", "punchline": "Caterpillar really slow, but watch me turn into a butterfly and steal the show!", "rating": 5}}"""

    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])

    few_shot_structured_llm = prompt | structured_llm
    result = few_shot_structured_llm.invoke("what's something funny about woodpeckers")
    print("result=", result)

if flag == 7:
    # Prompting and parsing model outputs directly   Using PydanticOutputParser
    from typing import List
    from langchain_core.output_parsers import PydanticOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel, Field

    class Person(BaseModel):
        """Information about a person."""
        name: str = Field(..., description="The name of the person")
        height_in_meters: float = Field(
            ..., description="The height of the person expressed in meters."
        )
    class People(BaseModel):
        """Identifying information about all people in a text."""
        people: List[Person]
    # Set up a parser
    parser = PydanticOutputParser(pydantic_object=People)
    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",
            ),
            ("human", "{query}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    query = "Anna is 23 years old and she is 6 feet tall"
    print(prompt.invoke({"query": query}).to_string())

    # Chain the prompt, LLM, and parser together
    chain = prompt | llm | parser
    print(chain.invoke({"query": query}))

if flag == 8:
    # Custom Parsing
    import json
    import re
    from typing import List
    from langchain_core.messages import AIMessage
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel, Field

    class Person(BaseModel):
        """Information about a person."""
        name: str = Field(..., description="The name of the person")
        height_in_meters: float = Field(
            ..., description="The height of the person expressed in meters."
        )

    class People(BaseModel):
        """Identifying information about all people in a text."""
        people: List[Person]


    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user query. Output your answer as JSON that  "
                "matches the given schema: \`\`\`json\n{schema}\n\`\`\`. "
                "Make sure to wrap the answer in \`\`\`json and \`\`\` tags",
            ),
            ("human", "{query}"),
        ]
    ).partial(schema=People.schema())


    # Custom parser
    def extract_json(message: AIMessage) -> List[dict]:
        """Extracts JSON content from a string where JSON is embedded between \`\`\`json and \`\`\` tags.

        Parameters:
            text (str): The text containing the JSON content.

        Returns:
            list: A list of extracted JSON strings.
        """
        text = message.content
        # Define the regular expression pattern to match JSON blocks
        pattern = r"\`\`\`json(.*?)\`\`\`"

        # Find all non-overlapping matches of the pattern in the string
        matches = re.findall(pattern, text, re.DOTALL)

        # Return the list of matched JSON strings, stripping any leading or trailing whitespace
        try:
            return [json.loads(match.strip()) for match in matches]
        except Exception:
            raise ValueError(f"Failed to parse: {message}")
        # Here is the prompt sent to the model:
        query = "Anna is 23 years old and she is 6 feet tall"
        print(prompt.format_prompt(query=query).to_string())

        # And here's what it looks like when we invoke it:
        chain = prompt | llm | extract_json
        print(chain.invoke({"query": query}))