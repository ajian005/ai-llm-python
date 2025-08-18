"""
  How to use multimodal prompts: https://python.langchain.com/docs/how_to/multimodal_prompts/
"""

from langchain_core.prompts import ChatPromptTemplate

# Define prompt
prompt = ChatPromptTemplate(
    [
        {
            "role": "system",
            "content": "Describe the image provided.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source_type": "url",
                    "url": "{image_url}",
                },
            ],
        },
    ])


from langchain.chat_models import init_chat_model
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
chain = prompt | llm
response = chain.invoke({"image_url": url})
print(response.text())

prompt = ChatPromptTemplate(
    [
        {
            "role": "system",
            "content": "Describe the image provided.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source_type": "base64",
                    "mime_type": "{image_mime_type}",
                    "data": "{image_data}",
                    "cache_control": {"type": "{cache_type}"},
                },
            ],
        },
    ]
)


import base64

import httpx

image_data = base64.b64encode(httpx.get(url).content).decode("utf-8")

chain = prompt | llm
response = chain.invoke(
    {
        "image_data": image_data,
        "image_mime_type": "image/jpeg",
        "cache_type": "ephemeral",
    }
)
print(response.text())