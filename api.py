import csv
import os
import re
import secrets
import threading
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from chatbot_engine import (
    ChatbotEngine,
    MAX_MESSAGE_LENGTH,
    detect_reply_language,
)
from suggestion_labels import SUGGESTION_LABELS


# ---- Log of questions the chatbot could not answer ----------------------
# Each row is a question that got "Hindi ko pa matiyak" (with or without
# suggestion buttons), or a suggestion the user picked. Use it to find
# real questions worth adding to intents.json, then retrain.
# No user name or account is recorded; emails and long numbers are masked.
# Turn off with CHATBOT_LOG_UNANSWERED=0.
LOG_FILE = Path(__file__).resolve().parent / "unanswered_questions.csv"
LOG_COLUMNS = [
    "time", "action", "question", "model_guess",
    "confidence", "suggestions_offered", "picked_topic",
]
_log_lock = threading.Lock()

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
LONG_NUMBER = re.compile(r"\d[\d\s-]{5,}\d")


def mask(text: str) -> str:
    text = EMAIL.sub("[email]", text)
    return LONG_NUMBER.sub("[number]", text)


def log_unanswered(**row) -> None:
    if os.environ.get("CHATBOT_LOG_UNANSWERED", "1") == "0":
        return

    row["time"] = datetime.now().isoformat(timespec="seconds")
    row["question"] = mask(row.get("question") or "")

    try:
        with _log_lock:
            new_file = not LOG_FILE.exists()
            # utf-8-sig so Excel shows Filipino text correctly.
            with LOG_FILE.open("a", newline="", encoding="utf-8-sig" if new_file else "utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=LOG_COLUMNS)
                if new_file:
                    writer.writeheader()
                writer.writerow({key: row.get(key, "") for key in LOG_COLUMNS})
    except OSError:
        # Logging must never break the chat.
        pass


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
    # Set when the user taps a suggestion button: answer that topic directly.
    intent: str | None = Field(
        default=None,
        pattern=r"^[a-z_]{1,60}$",
    )
    # The question that led to the suggestion (for the unanswered log).
    asked: str | None = Field(
        default=None,
        max_length=MAX_MESSAGE_LENGTH,
    )


class Suggestion(BaseModel):
    intent: str
    label: str


class ChatOutput(BaseModel):
    reply: str
    intent: str
    suggestions: list[Suggestion] = []


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

    engine = app.state.engine

    try:
        if body.intent:
            result = engine.answer_intent(body.intent, body.message)
        else:
            result = engine.get_response(body.message)
    except ValueError as exception:
        raise HTTPException(
            status_code=422,
            detail=str(exception),
        ) from exception

    if body.intent:
        log_unanswered(
            action="picked_suggestion",
            question=body.asked or "",
            picked_topic=body.intent,
        )
    elif result.source in {"model:fallback", "model:out_of_scope"}:
        log_unanswered(
            action="suggested" if result.suggestions else "no_answer",
            question=body.message,
            model_guess=result.intent,
            confidence=(
                f"{result.confidence:.2f}"
                if result.confidence is not None else ""
            ),
            suggestions_offered=" | ".join(result.suggestions),
        )

    language = 1 if detect_reply_language(body.message) == "en" else 0

    return ChatOutput(
        reply=result.reply,
        intent=result.intent,
        suggestions=[
            Suggestion(intent=tag, label=SUGGESTION_LABELS[tag][language])
            for tag in result.suggestions
            if tag in SUGGESTION_LABELS
        ],
    )