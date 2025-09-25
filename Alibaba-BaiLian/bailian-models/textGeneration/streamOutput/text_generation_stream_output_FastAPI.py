import os
from openai import OpenAI, APIError
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import json


class ChatRequest(BaseModel):
    messages: list[dict]
    model: str = "qwen-plus"
    api_key: str | None = None
    base_url: str | None = None


app = FastAPI()


@app.post("/chat/completions/stream")
async def create_chat_completion_stream(request: ChatRequest):
    api_key = request.api_key or os.getenv("DASHSCOPE_API_KEY")
    base_url = request.base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"

    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY not provided and not found in environment variables.")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    async def generate_stream():
        try:
            completion = client.chat.completions.create(
                model=request.model,
                messages=request.messages,
                stream=True,
                stream_options={"include_usage": True}
            )

            for chunk in completion:
                if chunk.choices:
                    content = chunk.choices[0].delta.content or ""
                    yield f"data: {json.dumps({"content": content})}\n\n"


                elif chunk.usage:
                    usage_info = {
                        "prompt_tokens": chunk.usage.prompt_tokens,
                        "completion_tokens": chunk.usage.completion_tokens,
                        "total_tokens": chunk.usage.total_tokens
                    }
                    yield f"data: {json.dumps({"usage": usage_info})}\n\n"


        except APIError as e:
            yield f"data: {json.dumps({"error": str(e)})}\n\n"


        except Exception as e:
            yield f"data: {json.dumps({"error": str(e)})}\n\n"

    return StreamingResponse(generate_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)