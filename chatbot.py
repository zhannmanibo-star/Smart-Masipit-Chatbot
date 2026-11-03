import json
import random
import joblib

model = joblib.load("intent_model.joblib")
with open("responses.json", encoding="utf-8") as f:
    RESPONSES = json.load(f)

THRESHOLD = 0.4   # 27 intents kaya natural na mababa ang probability; i-tune ito

FALLBACK = (
    "Pasensya na po, hindi ko po masyadong naintindihan. "
    "Pwede po bang linawin ang tanong, o makipag-ugnayan sa Barangay Hall "
    "(Lunes-Biyernes, 8AM-5PM)."
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