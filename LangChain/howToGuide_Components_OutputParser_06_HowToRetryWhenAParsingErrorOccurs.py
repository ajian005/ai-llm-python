"""
   How to retry when a parsing error occurs  https://python.langchain.com/docs/how_to/output_parser_retry/
"""

from langchain.output_parsers import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from pydantic import BaseModel, Field

template = """Based on the user question, provide an Action and Action Input for what step should be taken.
{format_instructions}
Question: {query}
Response:"""


class Action(BaseModel):
    action: str = Field(description="action to take")
    action_input: str = Field(description="input to the action")


parser = PydanticOutputParser(pydantic_object=Action)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

prompt_value = prompt.format_prompt(query="who is leo di caprios gf?")

bad_response = '{"action": "search"}'

try:
    parser.parse(bad_response)
except OutputParserException as e:
    print(e)

fix_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())

fix_parser.parse(bad_response)

from langchain.output_parsers import RetryOutputParser

retry_parser = RetryOutputParser.from_llm(parser=parser, llm=OpenAI(temperature=0))

retry_parser.parse_with_prompt(bad_response, prompt_value)

from langchain_core.runnables import RunnableLambda, RunnableParallel

completion_chain = prompt | OpenAI(temperature=0)

main_chain = RunnableParallel(
    completion=completion_chain, prompt_value=prompt
) | RunnableLambda(lambda x: retry_parser.parse_with_prompt(**x))


main_chain.invoke({"query": "who is leo di caprios gf?"})