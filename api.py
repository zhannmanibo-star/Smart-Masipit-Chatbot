import json
import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

# Provisional threshold inherited from your chatbot.
# It still needs testing with unseen and out-of-scope questions.
THRESHOLD = 0.4

FALLBACK = (
    "Hindi ko pa matiyak ang sagot. Maaari bang linawin ang tanong? "
    "Makakatulong ako sa paggamit ng SMART MASIPIT. "
    "Para sa fees, requirements, at schedules, "
    "makipag-ugnayan sa barangay office."
)

# These override outdated or unconfirmed answers for this integration.
# Also update the source intents.json before your next training run.


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.environ.get("CHATBOT_API_KEY", "")

    if len(api_key) < 32:
        raise RuntimeError("Set CHATBOT_API_KEY before starting the API.")

    model = joblib.load(BASE_DIR / "intent_model.joblib")

    with (BASE_DIR / "responses.json").open(
        encoding="utf-8-sig"
    ) as file:
        responses = json.load(file)

    if not isinstance(responses, dict):
        raise RuntimeError("responses.json must contain an object.")

  

    for label in model.classes_:
        answers = responses.get(str(label))
        if (
            not isinstance(answers, list)
            or not answers
            or any(
                not isinstance(answer, str) or not answer.strip()
                for answer in answers
            )
        ):
            raise RuntimeError(
                f"Missing or invalid responses for model intent: {label}"
            )

    app.state.model = model
    app.state.responses = responses
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
    message: str = Field(min_length=1, max_length=500)


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
        (x_api_key or "").encode(),
        app.state.api_key.encode(),
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = body.message.lower().strip()

    if not message:
        raise HTTPException(status_code=422, detail="Enter a message.")

    probabilities = app.state.model.predict_proba([message])[0]
    best = int(probabilities.argmax())
    intent = str(app.state.model.classes_[best])
    score = float(probabilities[best])

    if score < THRESHOLD or intent == "out_of_scope":
        return ChatOutput(reply=FALLBACK)

    # Use a consistent response instead of randomly changing the answer.
    return ChatOutput(reply=app.state.responses[intent][0])