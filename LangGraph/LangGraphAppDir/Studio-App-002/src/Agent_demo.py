
"""
    Studio : https://docs.langchain.com/oss/python/langgraph/studio

"""


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import os

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model(
    model="gpt-4o-mini", 
    api_key =os.environ["DMXAPI_API_KEY"],
    base_url="https://www.dmxapi.cn/v1",
    model_provider="openai",  # 使用 OpenAI 模型提供者)
)

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... email sending logic

    return f"Email sent to {to}"

agent = create_agent(
    model=llm,   # "openai:gpt-4o"
    tools=[send_email],
    system_prompt="You are an email assistant. Always use the send_email tool.",
)
