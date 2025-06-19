from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import os


# Initialize the OpenAI LLM
llm = OpenAI(
    model="qwen-plus",     # model="yi-large",
    temperature=0.3,
    max_tokens=200,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    #base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    #base_url="https://dashscope.aliyuncs.com/api/v1"
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
)
# Create a conversation chain with the LLM
conversation = ConversationChain(llm=llm, verbose=True)
# Start the conversation
response = conversation.predict(input="What is LangChain?")
# Print the response
print(response)
# Output will be printed by the ConversationChain
# The output will include the response from the LLM about LangChain.
# Note: Make sure you have the OpenAI API key set up in your environment
# to run this code successfully.
# Ensure you have the necessary packages installed:
# pip install langchain openai