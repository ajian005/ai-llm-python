"""
  Response metadata : https://python.langchain.com/docs/how_to/response_metadata/
"""

# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")
msg = llm.invoke("What's the oldest known example of cuneiform")
msg.response_metadata

# Anthropic
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-7-sonnet-20250219")
msg = llm.invoke("What's the oldest known example of cuneiform")
msg.response_metadata

# Google Generative AI
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
msg = llm.invoke("What's the oldest known example of cuneiform")
msg.response_metadata

# Bedrock (Anthropic)
from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(model="anthropic.claude-3-7-sonnet-20250219-v1:0")
msg = llm.invoke("What's the oldest known example of cuneiform")
msg.response_metadata

# MistralAI
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(model="mistral-small-latest")
msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
msg.response_metadata

# Groq
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.1-8b-instant")
msg = llm.invoke("What's the oldest known example of cuneiform")
msg.response_metadata

# FireworksAI
from langchain_fireworks import ChatFireworks
llm = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")
msg = llm.invoke("What's the oldest known example of cuneiform")
msg.response_metadata
