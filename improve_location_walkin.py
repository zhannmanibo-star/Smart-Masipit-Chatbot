import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "intents.json"

ADDITIONS = {
    "barangay_location": [
        "Paano makarating sa barangay office?",
        "Hindi ako pamilyar sa lugar saan ang barangay hall?",
        "Anong ruta ang papunta sa opisina ng barangay?",
        "Paturo naman ng daan papuntang Masipit hall",
        "Naliligaw ako saan banda ang barangay office?",
        "Saan banda nakatayo ang barangay hall ng Masipit?",
        "May mapang puwedeng sundan papunta sa opisina?",
        "Paano hanapin ang barangay hall sa Google Maps?",
        "Pupunta ako sa barangay office paano makita ang directions?",
        "Hindi ko mahanap ang lokasyon ng barangay hall",
        "Can you help me find the way to the barangay office?",
        "I am unfamiliar with Masipit where is the barangay hall?",
        "How can I get directions to the barangay office?",
        "I need a map showing where the barangay hall is",
        "Where should I go to visit the Masipit barangay office?",
        "Which website button opens the route to the barangay hall?",
    ],

    "document_walk_in": [
        "Walang email address ang aplikante pwede bang humingi ng clearance?",
        "Hindi gumagamit ng internet ang tatay ko paano siya magrequest?",
        "Kailangan ng nanay ko ng indigency pero wala siyang login",
        "May certificate bang makukuha kahit hindi registered online?",
        "Walang smartphone ang aplikante paano magsubmit ng document request?",
        "Pwede bang staff na ang magencode dahil walang account ang residente?",
        "Senior citizen na walang email paano magrequest ng dokumento?",
        "Kailangan ba munang gumawa ng email bago magwalkin request?",
        "Pupunta na lang kami sa barangay dahil walang online account",
        "Hindi marunong magregister online paano makakahingi ng certificate?",
        "Can someone without an email address request a certificate?",
        "My father has no portal account can he request clearance in person?",
        "How can an applicant without internet submit a document request?",
        "Can barangay staff encode a request for a resident without a login?",
        "Does an elderly applicant need an email for a walk-in certificate request?",
        "Can my mother request indigency at the office without signing up?",
    ],
}


def normalize(text):
    return " ".join(text.lower().split()).strip(" ?!.,")


def main():
    original = SOURCE.read_bytes()
    data = json.loads(original.decode("utf-8-sig"))

    by_tag = {}

    for item in data["intents"]:
        tag = item["tag"]

        if tag in by_tag:
            raise ValueError(f"Duplicate intent tag: {tag}")

        by_tag[tag] = item

    for tag, questions in ADDITIONS.items():
        if tag not in by_tag:
            raise ValueError(f"Missing intent: {tag}")

        by_tag[tag]["patterns"].extend(questions)

    owners = {}

    for tag, item in by_tag.items():
        unique = {}

        for question in item["patterns"]:
            key = normalize(question)

            if key in owners and owners[key] != tag:
                raise ValueError(
                    f"Question belongs to conflicting intents: {question}"
                )

            owners[key] = tag
            unique.setdefault(key, question)

        item["patterns"] = list(unique.values())

    backup = BASE / "intents.before-location-walkin.json"

    if not backup.exists():
        backup.write_bytes(original)

    SOURCE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Updated location and walk-in examples.")
    print(
        "Total patterns:",
        sum(len(item["patterns"]) for item in by_tag.values()),
    )
    print("Responses unchanged.")
    print("Backup:", backup.name)


if __name__ == "__main__":
    main()