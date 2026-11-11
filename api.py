import os
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from chatbot_engine import ChatbotEngine, MAX_MESSAGE_LENGTH


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.environ.get("CHATBOT_API_KEY", "")

    if len(api_key) < 32:
        raise RuntimeError(
            "Set CHATBOT_API_KEY to at least 32 characters "
            "before starting the API."
        )

    app.state.engine = ChatbotEngine()
    app.state.api_key = api_key

    yield


app = FastAPI(
    title="SMART MASIPIT Chatbot",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


class ChatInput(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=MAX_MESSAGE_LENGTH,
    )


class ChatOutput(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatOutput)
def chat(
    body: ChatInput,
    x_api_key: str | None = Header(default=None),
):
    if not secrets.compare_digest(
        (x_api_key or "").encode("utf-8"),
        app.state.api_key.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    try:
        result = app.state.engine.get_response(body.message)
    except ValueError as exception:
        raise HTTPException(
            status_code=422,
            detail=str(exception),
        ) from exception

    return ChatOutput(reply=result.reply)