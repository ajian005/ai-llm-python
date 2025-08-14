"""
   How to parse XML output  https://python.langchain.com/docs/how_to/output_parser_xml/
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import PromptTemplate

model = ChatAnthropic(model="claude-2.1", max_tokens_to_sample=512, temperature=0.1)

actor_query = "Generate the shortened filmography for Tom Hanks."

output = model.invoke(
    f"""{actor_query}
Please enclose the movies in <movie></movie> tags"""
)

print(output.content)

parser = XMLOutputParser()

# We will add these instructions to the prompt below
parser.get_format_instructions()

prompt = PromptTemplate(
    template="""{query}\n{format_instructions}""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

output = chain.invoke({"query": actor_query})
print(output)

parser = XMLOutputParser(tags=["movies", "actor", "film", "name", "genre"])

# We will add these instructions to the prompt below
parser.get_format_instructions()

prompt = PromptTemplate(
    template="""{query}\n{format_instructions}""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


chain = prompt | model | parser

output = chain.invoke({"query": actor_query})

print(output)

for s in chain.stream({"query": actor_query}):
    print(s)

