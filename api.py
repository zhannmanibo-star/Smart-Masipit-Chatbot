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
REVIEWED_ANSWERS = {
    "greeting": [
        "Magandang araw! Ako ang SMART MASIPIT Virtual Assistant. "
        "Makakatulong ako sa paggamit ng account, document requests, "
        "at impormasyon tungkol sa resident at health modules. "
        "Hindi ko nakikita ang personal records o actual request status ninyo."
    ],
    "document_list": [
        "Available sa SMART MASIPIT ang Barangay Clearance, "
        "Certificate of Indigency, at Certificate of Residency. "
        "Maaari ring mag-encode ang authorized staff ng walk-in request."
    ],
    "document_clearance": [
        "Mag-sign in gamit ang verified resident account, piliin ang "
        "Request a document, at piliin ang Barangay Clearance. "
        "Ilagay ang purpose at isumite para sa review. "
        "Kumpirmahin ang requirements at fees sa barangay office."
    ],
    "document_indigency": [
        "Sa Request a document, piliin ang Certificate of Indigency "
        "at ilagay ang purpose. Dadaan ito sa barangay review. "
        "Kumpirmahin ang eligibility, requirements, at anumang fee "
        "sa barangay office."
    ],
    "document_status": [
        "Buksan ang View my requests para makita ang actual status. "
        "Ang Approved ay para pa lamang sa preparation. "
        "Hintayin ang Ready for release at basahin ang pickup instructions. "
        "Sa barangay office ipi-print at ire-release ang dokumento. "
        "Hindi kayang tingnan ng chatbot ang personal request status."
    ],
    "payment_info": [
        "Walang online payment feature sa kasalukuyang SMART MASIPIT. "
        "Kumpirmahin sa barangay office ang anumang bayad at paraan "
        "ng pagbabayad."
    ],
    "health_patient_record": [
        "Authorized health staff ang nagtatala ng patient profile, "
        "consultations, health history, at immunizations. "
        "Makipag-ugnayan sa health staff para sa registration "
        "o pagwawasto ng record. Huwag maglagay ng medical details sa chat."
    ],
    "health_immunization_record": [
        "Authorized health staff ang nagtatala ng immunization records. "
        "Para sa sariling record o record ng inyong anak, "
        "makipag-ugnayan sa Barangay Health Center."
    ],
    "health_center_schedule": [
        "Makipag-ugnayan sa Barangay Health Center para sa confirmed "
        "consultation at immunization schedules at anumang fee."
    ],
    "census_registration": [
        "Piliin ang Create an account sa login page para mag-register. "
        "Secretary o Captain ang magve-verify ng resident application. "
        "Authorized staff ang nagma-maintain ng resident registry."
    ],
    "census_household_update": [
        "Authorized barangay staff ang nag-u-update ng household membership "
        "at head assignment. Ipa-review sa staff ang kinakailangang "
        "pagbabago; walang self-service household editing ang resident account."
    ],
    "census_summary": [
        "Authorized staff ang nakakakita ng demographic summaries batay "
        "sa saved resident records. Makipag-ugnayan sa barangay office "
        "para sa report inquiries."
    ],
    "data_privacy": [
        "May account permissions ang SMART MASIPIT para sa iba't ibang "
        "modules. Hindi nakakabasa ang chatbot ng resident o health records. "
        "Huwag magpadala ng password, reset link, o medical details sa chat."
    ],
    "account_access": [
        "Piliin ang Create an account para mag-register. "
        "Kailangan muna ng resident verification ng Secretary o Captain. "
        "Kung nakalimutan ang password, piliin ang Forgot your password? "
        "sa login page at sundin ang reset email."
    ],
    "barangay_operating_hours": [
        "Makipag-ugnayan sa barangay office para sa kasalukuyang "
        "office hours at holiday schedule."
    ],
    "out_of_scope": [FALLBACK],
}


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

    responses.update(REVIEWED_ANSWERS)

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