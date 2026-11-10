import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "intents.json"


def normalize(text):
    return " ".join(text.lower().split()).strip(" ?!.,")


MOVES = {
    "document_clearance": [
        "process ng clearance request",
    ],
    "document_walk_in": [
        "paano kung walang email ang walk in",
    ],
    "payment_info": [
        "Magkano ang clearance?",
        "May bayad ba ang barangay clearance?",
        "how much is the barangay clearance",
        "magkano po ang clearance",
        "mgkano clearance",
        "brgy clearance magkano",
        "may fee ba ang clearance",
        "Magkano ang bayad sa indigency certificate?",
        "Libre ba ang indigency certificate?",
        "is the indigency certificate free",
        "libre po ba ang indigency",
        "indigency magkano",
        "Magkano ang residency certificate?",
    ],
}

# These questions do not have one clear, supported answer
# under their current labels.
REMOVE = [
    "kailan ang census",
    "kailangan ba pumunta pa sa barangay hall",
]

ADDITIONS = {
    "document_status": [
        "Naaprubahan na ba ang certificate of indigency request ko?",
        "Paano tingnan ang progress ng clearance application ko?",
        "Pending pa rin ang residency certificate request ko",
        "Saan makikita kung rejected ang clearance request?",
        "May update na ba sa application ko para sa indigency?",
        "How can I track my barangay clearance application?",
        "Is my certificate of indigency request already approved?",
        "Where can I check the status of my residency request?",
    ],

    "document_pickup": [
        "Saan ko kukunin ang clearance na ready for release na?",
        "May pickup instructions na ang indigency ko paano magclaim?",
        "Handa na ang residency certificate saan ito irerelease?",
        "Naemail na ready for pickup ang clearance saan pupunta?",
        "Where do I collect my approved and prepared clearance?",
        "How do I claim my certificate of indigency at the office?",
        "My residency certificate is ready for release where do I go?",
        "Where are the collection instructions for my document?",
    ],

    "payment_info": [
        "Magkano ang singil para sa barangay documents?",
        "Saan ko babayaran ang certificate of indigency?",
        "Puwede bang GCash ang bayad sa residency certificate?",
        "May online checkout ba para sa clearance fee?",
        "Kailangan bang magbayad sa portal para sa dokumento?",
        "How much is the fee for a residency certificate?",
        "Can I pay the barangay clearance fee through the website?",
        "Where should I pay for my requested certificate?",
    ],

    "account_identity_verification": [
        "Hindi bumubukas ang camera sa resident registration form",
        "Paano payagan ang camera access para sa ID capture?",
        "Ayaw gumana ng camera habang kumukuha ng selfie",
        "How do I enable the camera for identity verification?",
        "Where do I photograph the front of my identification card?",
        "The ID capture camera is blocked by my browser",
    ],

    "account_access": [
        "Saan ang form para gumawa ng bagong resident account?",
        "Gusto kong magsign up bilang resident user",
        "Paano simulan ang online account registration?",
        "How can a new resident create a login account?",
        "Where is the sign up page for SMART MASIPIT?",
        "I want to register a new portal account",
    ],

    "document_list": [
        "Bukod sa clearance ano pa ang dokumentong available?",
        "May ibang certificates pa maliban sa indigency?",
        "Pakilista lahat ng document types sa request form",
        "What other certificates can I request besides clearance?",
        "List all available barangay document types",
        "Are clearance and indigency the only available documents?",
    ],

    "health_patient_record": [
        "Saan ipapawasto ang pangalan sa patient profile?",
        "May mali sa patient details ko sino ang lalapitan?",
        "Paano humingi ng sariling patient record sa health staff?",
        "Who handles corrections to patient registration details?",
        "Where can I request a copy of my own patient record?",
        "My patient profile contains an incorrect contact number",
    ],

    "health_privacy_access": [
        "Makikita ba ng ibang residente ang BP record ko?",
        "May access ba ang secretary sa maternal records?",
        "Sino lang ang puwedeng bumasa ng consultation details?",
        "Can other users read my confidential health information?",
        "Are patient records restricted to authorized health staff?",
        "Can a regular barangay employee view clinical records?",
    ],

    "data_privacy": [
        "Paano pinoprotektahan ang login password?",
        "Nakikita ba ng staff ang mismong password ko?",
        "Ligtas bang ibigay ang password sa chatbot?",
        "Is my account password confidential?",
        "Should I share my login credentials in this chat?",
        "How is personal account information protected?",
    ],

    "out_of_scope": [
        "Paano magapply ng business clearance para sa tindahan?",
        "Barangay business clearance requirements para sa negosyo",
        "Kailangan ko ng permit para magbukas ng sari sari store",
        "How do I obtain a business clearance for my shop?",
        "Can I apply for a business operating permit here?",
        "Where do I pay my electricity bill?",
        "Pwede bang magbayad ng water bill dito?",
        "Paano bayaran ang internet bill sa website na ito?",
        "Does this portal accept payments for utility bills?",
        "Magkano ang bayad sa passport application?",
    ],
}


def main():
    original = SOURCE.read_bytes()
    data = json.loads(original.decode("utf-8-sig"))

    by_tag = {}

    for intent in data["intents"]:
        tag = intent["tag"]

        if tag in by_tag:
            raise ValueError(f"Duplicate intent tag: {tag}")

        by_tag[tag] = intent

    required_tags = set(MOVES) | set(ADDITIONS)

    for tag in required_tags:
        if tag not in by_tag:
            raise ValueError(f"Missing intent: {tag}")

    remove_keys = {normalize(text) for text in REMOVE}

    for intent in by_tag.values():
        intent["patterns"] = [
            text
            for text in intent["patterns"]
            if normalize(text) not in remove_keys
        ]

    for target, questions in MOVES.items():
        for question in questions:
            question_key = normalize(question)

            for intent in by_tag.values():
                intent["patterns"] = [
                    text
                    for text in intent["patterns"]
                    if normalize(text) != question_key
                ]

            by_tag[target]["patterns"].append(question)

    for target, questions in ADDITIONS.items():
        by_tag[target]["patterns"].extend(questions)

    # The payment intent now handles both fees and payment methods.
    by_tag["payment_info"]["responses"] = [
        "Walang online payment feature sa kasalukuyang SMART MASIPIT. "
        "Hindi rin ako makapagkukumpirma ng eksaktong fee o exemption "
        "para sa bawat certificate. Makipag-ugnayan sa barangay office "
        "para sa applicable fees at paraan ng pagbabayad."
    ]

    owners = {}

    for tag, intent in by_tag.items():
        unique = {}

        for question in intent["patterns"]:
            question_key = normalize(question)

            if (
                question_key in owners
                and owners[question_key] != tag
            ):
                raise ValueError(
                    f"Conflicting labels for: {question}"
                )

            owners[question_key] = tag
            unique.setdefault(question_key, question)

        intent["patterns"] = list(unique.values())

    backup = BASE / "intents.before-refinement.json"

    if not backup.exists():
        backup.write_bytes(original)

    SOURCE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Dataset refinement completed.")
    print(
        "Patterns:",
        sum(len(item["patterns"]) for item in by_tag.values()),
    )
    print("Intents:", len(by_tag))
    print("Backup:", backup.name)
    print("Next: run train.py")


if __name__ == "__main__":
    main()