import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "intents.json"

ADDITIONS = {
    "account_identity_verification": [
        "Paano buksan ang camera para magpasa ng verification pictures?",
        "Anong button ang gagamitin para kumuha ng ID photo?",
        "Paano paganahin ang camera habang gumagawa ng resident account?",
        "Ayaw magstart ng camera sa identity submission page",
        "Na-block ko ang camera permission paano ko ito papayagan?",
        "Kailangan bang payagan ang browser camera para sa selfie?",
        "Paano kumuha ulit kapag malabo ang verification picture?",
        "Pwede bang i-retake ang litrato ng harap ng ID?",
        "Hindi mabasa ang likod ng ID sa picture paano uulitin?",
        "Anong mga larawan ang kasama sa identity evidence?",
        "Kailangan ba parehong harap at likod ng identification card?",
        "Para saan ang selfie sa resident registration?",
        "Saan dapat isumite ang litrato ng valid identification?",
        "Paano kumpletuhin ang ID at selfie submission?",
        "How do I activate the camera on the identity submission form?",
        "Which control takes a photo of my identification card?",
        "My browser blocked the camera for resident verification",
        "How can I allow camera access for the registration page?",
        "Can I take another photo if my ID image is blurry?",
        "How do I retake the back photo of my identification card?",
        "Which identity photographs must I submit?",
        "Do I need both sides of the ID and a selfie?",
        "Where should I submit my resident verification pictures?",
        "What is the selfie capture step used for?",
    ],

    "health_blood_pressure": [
        "Saang input ilalagay ang blood pressure sa consultation form?",
        "Paano itatala ng health staff ang dalawang BP values?",
        "May hiwalay bang systolic at diastolic input?",
        "Ano ang field para sa unang numero ng blood pressure?",
        "Ano ang field para sa pangalawang numero ng blood pressure?",
        "Saan isusulat ang nasukat na pressure sa consultation entry?",
        "Paano idagdag ang BP measurement sa bagong consultation?",
        "Health staff ba ang mag-eencode ng blood pressure values?",
        "Maaaring bang isama ang BP sa consultation notes at record?",
        "Kung hindi nakuhanan ng BP kailangan bang maglagay ng numero?",
        "Pwede bang blanko ang blood pressure fields kapag walang measurement?",
        "Kailangan bang parehong systolic at diastolic ang ilagay?",
        "Where are the blood pressure inputs in the consultation form?",
        "How can a health worker save a patient's measured BP?",
        "Does the form have separate systolic and diastolic inputs?",
        "Which field stores the first blood pressure number?",
        "Which field stores the second blood pressure number?",
        "Can a consultation entry include measured blood pressure?",
        "Who enters blood pressure measurements in the health module?",
        "Should unmeasured BP values be left empty?",
        "Do staff need to enter both blood pressure numbers together?",
        "How do I add systolic and diastolic values to a consultation?",
        "Is there a place to encode blood pressure during a checkup?",
        "Can the health worker leave both BP inputs blank?",
    ],

    "health_no_advice": [
        "Pakisabi kung delikado ang BP result ko",
        "Mababa ba ang systolic reading ko?",
        "Ano ang ibig sabihin ng mataas na diastolic pressure?",
        "Anong gamot ang dapat inumin para bumaba ang BP?",
        "Can you tell me whether my systolic result is dangerous?",
        "What does my diastolic blood pressure result mean?",
        "Should I change my medicine because of this BP reading?",
        "Please interpret these blood pressure numbers for me",
    ],

    "account_pending": [
        "Naisumite ko na ang verification pictures naghihintay na lang ba?",
        "Kumpleto na ang selfie at ID pero hindi pa activated ang account",
        "Sino ang magrereview pagkatapos maipasa ang identity evidence?",
        "I submitted all identity photos but my account is still pending",
        "Who approves the account after the verification pictures are submitted?",
        "Does submitting the selfie automatically approve my account?",
    ],
}

UPDATED_RESPONSES = {
    "account_identity_verification": [
        "Sa identity verification form, kunan ang harap at likod "
        "ng valid ID at ang inyong selfie. Payagan ang camera "
        "permission ng browser. Kung na-block, tingnan ang site "
        "permissions at payagan ang camera, pagkatapos buksan muli "
        "ang capture step. Kung malabo ang larawan, gamitin ang "
        "Retake o pagkuha muli bago isumite. "
        "Secretary o Captain ang magre-review ng submission. "
        "Sa verification form lamang isumite ang mga larawan, "
        "hindi sa chatbot."
    ],

    "health_blood_pressure": [
        "Authorized health staff ang nag-eencode ng blood pressure "
        "sa consultation form gamit ang magkahiwalay na systolic "
        "at diastolic fields, sa mmHg. Kung magtatala ng BP, "
        "ilagay ang parehong values. Kung hindi nasukat, "
        "iwanang blanko ang parehong fields; huwag mag-imbento "
        "ng reading. Para sa interpretasyon ng resulta, "
        "makipag-ugnayan sa health professional. "
        "Hindi nagbibigay ng clinical interpretation ang chatbot."
    ],
}


def normalize(text):
    return " ".join(text.lower().split()).strip(" ?!.,")


def main():
    original = SOURCE.read_bytes()
    data = json.loads(original.decode("utf-8-sig"))

    by_tag = {}

    for intent in data["intents"]:
        tag = intent["tag"]

        if tag in by_tag:
            raise ValueError(f"Duplicate intent tag: {tag}")

        by_tag[tag] = intent

    required_tags = set(ADDITIONS) | set(UPDATED_RESPONSES)

    for tag in required_tags:
        if tag not in by_tag:
            raise ValueError(f"Missing intent: {tag}")

    before = sum(
        len(intent["patterns"])
        for intent in by_tag.values()
    )

    for tag, questions in ADDITIONS.items():
        by_tag[tag]["patterns"].extend(questions)

    for tag, responses in UPDATED_RESPONSES.items():
        by_tag[tag]["responses"] = responses

    owners = {}

    for tag, intent in by_tag.items():
        unique = {}

        for question in intent["patterns"]:
            if not isinstance(question, str) or not question.strip():
                raise ValueError(f"Invalid pattern in {tag}")

            key = normalize(question)

            if key in owners and owners[key] != tag:
                raise ValueError(
                    f"Conflicting labels: {owners[key]} / {tag}\n"
                    f"Question: {question}\n"
                    "No files were changed."
                )

            owners[key] = tag
            unique.setdefault(key, question.strip())

        intent["patterns"] = list(unique.values())

    updated = (
        json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    if updated == original:
        print("These changes are already applied.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = BASE / f"intents.before-verification-bp-{timestamp}.json"
    backup.write_bytes(original)

    SOURCE.write_bytes(updated)

    after = sum(
        len(intent["patterns"])
        for intent in by_tag.values()
    )

    print(f"Previous patterns: {before}")
    print(f"Updated patterns: {after}")
    print(f"Net added: {after - before}")
    print(f"Backup: {backup.name}")
    print("Updated responses: identity verification and BP recording.")
    print("Next: run train.py")


if __name__ == "__main__":
    main()