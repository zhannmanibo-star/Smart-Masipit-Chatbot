"""
Checks the conversation features of the assistant:

  * "english please" / "tagalog po" repeats the last answer in that
    language, and later answers keep that language;
  * random letters or unrelated words ("secret", "gadgsgd") get a
    "please ask again" reply without topic suggestions;
  * real but unclear questions still get suggestions.

Run:  python test_conversation.py
"""

import os

from chatbot_engine import ChatbotEngine, language_request

FAILURES = []


def check(name, condition):
    print(("ok   " if condition else "FAIL ") + name)
    if not condition:
        FAILURES.append(name)


def main():
    engine = ChatbotEngine()

    # Language requests: only when the whole message asks for a language.
    for text in ["english please", "English po", "pa-english naman", "in english pls",
                 "can you say that in english", "translate to english",
                 "i dont understand tagalog", "english"]:
        check(f"'{text}' asks for English", language_request(text) == "en")
    for text in ["tagalog po", "pakitagalog", "sa filipino please", "tagalog nga",
                 "di ko maintindihan ang english", "filipino"]:
        check(f"'{text}' asks for Tagalog", language_request(text) == "fil")
    for text in ["may english version ba ang certificate", "paano kumuha ng clearance",
                 "english teacher ako pwede ba mag register", "how do i get a clearance"]:
        check(f"'{text}' is a normal question", language_request(text) is None)

    # Tagalog question, then "english please": same answer in English.
    first = engine.get_response("paano kunin ang barangay clearance")
    check("first answer is in Tagalog", first.lang == "fil" and first.intent == "document_clearance")
    again = engine.get_response("english please", previous=first.key)
    check("english please repeats the same topic", again.intent == "document_clearance")
    check("...in English", again.lang == "en" and again.reply == engine.render(first.key, "en"))
    check("...and remembers the choice", again.chosen_lang == "en")

    # After choosing English, a Tagalog question is answered in English.
    next_one = engine.get_response("paano pumili ng oras ng pagkuha", lang="en")
    check("chosen English stays for the next answer", next_one.lang == "en" and next_one.reply.startswith("When the request"))

    # And back to Tagalog.
    back = engine.get_response("tagalog po", lang="en", previous=next_one.key)
    check("tagalog po switches back", back.lang == "fil" and back.reply == engine.render(next_one.key, "fil"))

    # Rule answers can be repeated too.
    rule = engine.get_response("mataas ba ang bp ko na 150 over 90")
    check("rule answer has a key", rule.key == "rule:bp_interpretation")
    check("rule answer in English", engine.get_response("english please", previous=rule.key).reply.startswith("The chatbot does not interpret"))

    # Suggestions are kept when the answer is repeated.
    unsure = engine.get_response("musta na kaya yung pinasa kong request")
    if unsure.suggestions:
        repeated = engine.get_response("english please", previous=unsure.key)
        check("suggestions kept in the other language", repeated.suggestions == unsure.suggestions and repeated.lang == "en")

    # No earlier answer: a short confirmation.
    alone = engine.get_response("english please")
    check("english please with nothing before", alone.intent == "language_switch" and alone.chosen_lang == "en")

    # A broken or made-up previous key is ignored, not an error.
    check("bad previous key is ignored", engine.get_response("english please", previous="intent:not_a_topic").intent == "language_switch")

    # Nonsense: no suggestions, a clear "ask again" reply.
    for text in ["secret", "gadgsgd", "ano yan", "hoho", "qwrtyp zxcv"]:
        result = engine.get_response(text)
        check(f"'{text}' gets no suggestions", result.suggestions == () and result.source in {"model:not_understood", "rule:smalltalk"} or result.intent not in {"unknown", "out_of_scope"} and not result.suggestions)
    check("nonsense reply asks to try again", engine.get_response("secret").reply.startswith("Pasensya na, hindi ko naintindihan"))
    check("nonsense reply in English when chosen", engine.get_response("gadgsgd", lang="en").reply.startswith("Sorry, I did not understand"))

    # Unclear but real questions still get suggestions.
    check("real unclear question still gets suggestions", len(engine.get_response("musta na kaya yung pinasa kong request").suggestions) > 0)

    # Picking a suggestion in the chosen language.
    picked = engine.answer_intent("document_pickup_time", "Paano pumili ng oras ng pagkuha?", lang="en")
    check("picked suggestion answers in the chosen language", picked.lang == "en" and picked.key == "intent:document_pickup_time")

    # Short follow-ups use the previous question; other messages do not.
    followup = engine.get_response("magkano naman", context="paano kumuha ng barangay clearance")
    check("'magkano naman' after clearance", followup.intent == "payment_info")
    time = engine.get_response("pano kung puno na lahat", context="paano pumili ng pickup time")
    check("'pano kung puno na lahat' after pickup time", time.intent == "document_pickup_time")
    noise = engine.get_response("qwrtyp zxcv", context="paano kumuha ng barangay clearance")
    check("nonsense is not answered from context", noise.source == "model:not_understood")
    same = engine.get_response("paano kumuha ng barangay clearance", context="kailan ang bakuna")
    check("a full question ignores the context", same.intent == engine.get_response("paano kumuha ng barangay clearance").intent)

    # Staff get answers about their own pages, only for parts they work in.
    resident_qr = engine.get_response("paano gamitin ang qr code")
    staff_qr = engine.get_response("paano gamitin ang qr code", staff_areas=["documents"])
    health_qr = engine.get_response("paano gamitin ang qr code", staff_areas=["events"])
    check("staff QR answer is about Scan QR", resident_qr.intent == "document_qr_code" and "Scan QR" in staff_qr.reply and "Scan QR" not in resident_qr.reply)
    check("staff without that part get the usual answer", health_qr.reply == resident_qr.reply)
    english_staff = engine.get_response("english please", previous=staff_qr.key, staff_areas=["documents"])
    check("staff answer in English", "Start camera" in english_staff.reply)
    check("unknown staff areas are ignored", engine.get_response("paano gamitin ang qr code", staff_areas=["admin"]).reply == resident_qr.reply)
    picked = engine.answer_intent("account_pending", "pending", staff_areas=["verification"])
    check("picked topic gives the staff answer", "Account Approval" in picked.reply)

    # The API passes everything through.
    os.environ.setdefault("CHATBOT_API_KEY", "t" * 40)
    os.environ["CHATBOT_LOG_UNANSWERED"] = "0"
    try:
        from fastapi.testclient import TestClient
    except Exception:
        TestClient = None

    if TestClient is not None:
        import api
        headers = {"x-api-key": os.environ["CHATBOT_API_KEY"]}
        with TestClient(api.app) as client:
            one = client.post("/chat", json={"message": "paano kunin ang barangay clearance"}, headers=headers).json()
            two = client.post("/chat", json={"message": "english please", "previous": one["answer_key"]}, headers=headers).json()
            check("API: english please", two["lang"] == "en" and two["chosen_lang"] == "en" and two["intent"] == "document_clearance")
            three = client.post("/chat", json={"message": "kailan ang bakuna", "lang": "en"}, headers=headers).json()
            check("API: chosen language used", three["lang"] == "en")
            bad = client.post("/chat", json={"message": "hi", "previous": "<script>"}, headers=headers)
            check("API: invalid previous refused", bad.status_code == 422)
            bad = client.post("/chat", json={"message": "hi", "lang": "es"}, headers=headers)
            check("API: invalid language refused", bad.status_code == 422)
            old = client.post("/chat", json={"message": "paano kunin ang barangay clearance"}, headers=headers)
            check("API: old clients still work", old.status_code == 200)
            ctx = client.post("/chat", json={"message": "pano kung puno na lahat", "context": "paano pumili ng pickup time"}, headers=headers).json()
            check("API: context is used", ctx["intent"] == "document_pickup_time")
            staff = client.post("/chat", json={"message": "paano gamitin ang qr code", "staff_areas": ["documents"]}, headers=headers).json()
            check("API: staff answer", "Scan QR" in staff["reply"])
            bad = client.post("/chat", json={"message": "hi", "staff_areas": ["admin"]}, headers=headers)
            check("API: unknown staff area refused", bad.status_code == 422)
            check("API: context is passed on", ctx["context"] == "paano pumili ng pickup time pano kung puno na lahat")
            thanks = client.post("/chat", json={"message": "salamat", "context": "paano pumili ng pickup time"}, headers=headers).json()
            check("API: thanks keeps the topic", thanks["context"] == "paano pumili ng pickup time")
            long = client.post("/chat", json={"message": "hi", "context": "x" * 501}, headers=headers)
            check("API: too long context refused", long.status_code == 422)

    print()
    print("All checks passed." if not FAILURES else f"{len(FAILURES)} check(s) failed.")
    raise SystemExit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
