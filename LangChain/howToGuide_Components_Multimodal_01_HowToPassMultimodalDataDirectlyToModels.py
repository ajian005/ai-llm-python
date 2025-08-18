"""
  How to pass multimodal data to models: https://python.langchain.com/docs/how_to/multimodal_inputs/
"""

""" Images Images from base64 data  """
import base64
import httpx
import os
from langchain.chat_models import init_chat_model

# Fetch image data
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

# Pass to LLM
# llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",)    # 使用OpenAI模型提供者

message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe the weather in this image:",
        },
        {
            "type": "image",
            "source_type": "base64",
            "data": image_data,
            "mime_type": "image/jpeg",
        },
    ],
}
response = llm.invoke([message])
print(response.text())


""" Images from a URL """
message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe the weather in this image:",
        },
        {
            "type": "image",
            "source_type": "url",
            "url": image_url,
        },
    ],
}
response = llm.invoke([message])
print(response.text())

# We can also pass in multiple images:
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Are these two images the same?"},
        {"type": "image", "source_type": "url", "url": image_url},
        {"type": "image", "source_type": "url", "url": image_url},
    ],
}
response = llm.invoke([message])
print(response.text())

"""  Documents (PDF) """
import base64

import httpx
from langchain.chat_models import init_chat_model

# Fetch PDF data
pdf_url = "https://pdfobject.com/pdf/sample.pdf"
pdf_data = base64.b64encode(httpx.get(pdf_url).content).decode("utf-8")


# Pass to LLM
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe the document:",
        },
        {
            "type": "file",
            "source_type": "base64",
            "data": pdf_data,
            "mime_type": "application/pdf",
        },
    ],
}
response = llm.invoke([message])
print(response.text())

""" Documents from a URL """
message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe the document:",
        },
        {
            "type": "file",
            "source_type": "url",
            "url": pdf_url,
        },
    ],
}
response = llm.invoke([message])
print(response.text())


""" Audio from base64 data """
import base64

import httpx
from langchain.chat_models import init_chat_model

# Fetch audio data
audio_url = "https://upload.wikimedia.org/wikipedia/commons/3/3d/Alcal%C3%A1_de_Henares_%28RPS_13-04-2024%29_canto_de_ruise%C3%B1or_%28Luscinia_megarhynchos%29_en_el_Soto_del_Henares.wav"
audio_data = base64.b64encode(httpx.get(audio_url).content).decode("utf-8")


# Pass to LLM
llm = init_chat_model("google_genai:gemini-2.5-flash")

message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe this audio:",
        },
        {
            "type": "audio",
            "source_type": "base64",
            "data": audio_data,
            "mime_type": "audio/wav",
        },
    ],
}
response = llm.invoke([message])
print(response.text())



""" Tool calls  """
from typing import Literal
from langchain_core.tools import tool

@tool
def weather_tool(weather: Literal["sunny", "cloudy", "rainy"]) -> None:
    """Describe the weather"""
    pass

llm_with_tools = llm.bind_tools([weather_tool])
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the weather in this image:"},
        {"type": "image", "source_type": "url", "url": image_url},
    ],
}
response = llm_with_tools.invoke([message])
response.tool_calls

