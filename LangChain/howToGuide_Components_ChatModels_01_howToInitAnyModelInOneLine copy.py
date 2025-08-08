"""
  How to init any model in one line : https://python.langchain.com/docs/how_to/chat_models_universal_init/
"""

""" 
  Basic usage
"""
from langchain.chat_models import init_chat_model
import os


llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
    )

print("GPT-4o: " + llm.invoke("what's your name").content + "\n")


# Don't forget to set your environment variables for the API keys of the respective providers!
# For example, you can set them in your terminal or in a .env file:
# export OPENAI_API_KEY="your_openai_api_key"
# Returns a langchain_openai.ChatOpenAI instance.
gpt_4o = init_chat_model("gpt-4o", model_provider="openai", temperature=0)
# Returns a langchain_anthropic.ChatAnthropic instance.
claude_opus = init_chat_model("claude-3-opus-20240229", model_provider="anthropic", temperature=0)
# Returns a langchain_google_vertexai.ChatVertexAI instance.
gemini_15 = init_chat_model("gemini-2.5-pro", model_provider="google_genai", temperature=0)



# Since all model integrations implement the ChatModel interface, you can use them in the same way.
print("GPT-4o: " + gpt_4o.invoke("what's your name").content + "\n")
print("Claude Opus: " + claude_opus.invoke("what's your name").content + "\n")
print("Gemini 2.5: " + gemini_15.invoke("what's your name").content + "\n")


# Creating a configurable model
configurable_model = init_chat_model(temperature=0)

configurable_model.invoke(
    "what's your name", config={"configurable": {"model": "gpt-4o"}}
)

# Configurable model with default values
first_llm = init_chat_model(
    model="gpt-4o",
    temperature=0,
    configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
    config_prefix="first",  # useful when you have a chain with multiple models
)

first_llm.invoke("what's your name")