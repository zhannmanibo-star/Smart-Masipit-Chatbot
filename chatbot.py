import json
import random
import joblib

model = joblib.load("intent_model.joblib")
with open("responses.json", encoding="utf-8") as f:
    RESPONSES = json.load(f)

THRESHOLD = 0.4   # 27 intents kaya natural na mababa ang probability; i-tune ito

FALLBACK = (
    "Hindi ko pa matiyak ang sagot. Maaari bang linawin ang tanong? "
    "Makakatulong ako sa paggamit ng SMART MASIPIT. "
    "Para sa fees, requirements, at schedules, "
    "makipag-ugnayan sa barangay office."
)

def get_response(message):
    probs = model.predict_proba([message.lower().strip()])[0]
    best = probs.argmax()
    intent, conf = model.classes_[best], probs[best]
    if conf < THRESHOLD:
        return FALLBACK, "unknown", conf
    return random.choice(RESPONSES[intent]), intent, conf

print("SMART MASIPIT Virtual Assistant. Type 'exit' para tumigil.\n")
while True:
    msg = input("Ikaw: ").strip()
    if not msg:
        continue
    if msg.lower() == "exit":
        break
    reply, intent, conf = get_response(msg)
    print(f"Bot: {reply}")
    print(f"     [debug: {intent}, {conf:.2f}]\n")