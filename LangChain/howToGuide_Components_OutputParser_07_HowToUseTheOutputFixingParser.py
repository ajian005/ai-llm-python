"""
   How to use the output-fixing parser  https://python.langchain.com/docs/how_to/output_parser_fixing/
"""

from typing import List

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class Actor(BaseModel):
    name: str = Field(description="name of an actor")
    film_names: List[str] = Field(description="list of names of films they starred in")


actor_query = "Generate the filmography for a random actor."

parser = PydanticOutputParser(pydantic_object=Actor)

misformatted = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

try:
    parser.parse(misformatted)
except OutputParserException as e:
    print(e)

 # Now we can construct and use a OutputFixingParser. This output parser takes as an argument another output parser but also an LLM with which to try to correct any formatting mistakes.
from langchain.output_parsers import OutputFixingParser

new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())

new_parser.parse(misformatted)


