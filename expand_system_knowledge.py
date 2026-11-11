import json
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "intents.json"


def normalize(text):
    text = unicodedata.normalize("NFKC", text)
    return " ".join(text.casefold().split()).strip(" ?!.,;:")


ADDITIONS = [
    {
        "tag": "system_overview",
        "patterns": [
            "Ano ang SMART MASIPIT?",
            "What is SMART MASIPIT?",
            "Para saan ang system na ito?",
            "Tell me about SMART MASIPIT.",
            "Ano ang purpose ng SMART MASIPIT?",
            "Anong klaseng sistema ang SMART MASIPIT?",
            "Paliwanag naman kung para saan ang portal.",
            "What services are available in SMART MASIPIT?",
            "Ano ang mga serbisyo sa portal?",
            "May ibang services ba bukod sa document requests?",
            "What else can the system do besides certificates?",
            "Hindi lang ba pang clearance ang website na ito?",
            "Ano ang mga module ng system?",
            "What are the main features of the portal?",
            "May health records din ba ang SMART MASIPIT?",
            "Kasama ba ang resident registry sa system?",
            "Ano ang pinagkaiba ng mga module dito?",
            "Sino ang gumagamit ng SMART MASIPIT?",
            "Para lang ba sa residents ang website?",
            "May bahagi rin ba dito para sa barangay staff?",
            "Can you give me an overview of the system?",
            "Baguhan ako dito ano ang gamit ng website?",
            "What barangay is this portal for?",
            "Para sa Barangay Masipit ba itong system?",
        ],
        "responses": [
            "Ang SMART MASIPIT ay isang web-based information system "
            "para sa Barangay Masipit. Sakop nito ang resident registry "
            "at household records, resident account registration at "
            "verification, document requests, at health record management. "
            "Kasama sa health module ang consultations, blood pressure "
            "records, immunization, health history, at maternal records. "
            "Maaaring mag-request ng dokumento online gamit ang approved "
            "resident account o magpa-encode ng walk-in request sa "
            "barangay hall. Magkakaiba ang access ng residents at "
            "authorized staff ayon sa kanilang role; hindi lahat ng "
            "module ay direktang magagamit ng resident account."
        ],
    },
    {
        "tag": "chatbot_capabilities",
        "patterns": [
            "Ano ang kaya mong gawin?",
            "What can this chatbot do?",
            "Ano ang limitations ng chatbot?",
            "Can you access my personal records?",
            "Nakikita mo ba ang account ko?",
            "Kaya mo bang tingnan ang personal information ko?",
            "May access ka ba sa database ng barangay?",
            "Can you check my actual request status?",
            "Ikaw na ba ang magsusubmit ng request ko?",
            "Can you submit a document request for me?",
            "Pwede mo bang iapprove ang request ko?",
            "Can this chatbot approve my application?",
            "Pwede mo bang baguhin ang address ko sa system?",
            "Can you update my resident profile?",
            "Pwede kitang padalhan ng picture ng valid ID?",
            "Can I send my verification selfie here?",
            "Pwede bang dito ko ilagay ang password ko?",
            "Can you retrieve my medical records?",
            "Nakikita mo ba ang consultation results ko?",
            "Pwede bang dito na lang ako magrequest ng certificate?",
            "Ikaw ba ang nagveverify ng resident accounts?",
            "Can this chat create an account for me?",
            "Do you process transactions or only provide guidance?",
            "Gabay lang ba ito o kaya nitong magprocess ng request?",
        ],
        "responses": [
            "Gabay sa paggamit ng SMART MASIPIT ang maibibigay ko. "
            "Maaari kong ipaliwanag ang account verification, document "
            "requests, walk-in services, resident registry, at health "
            "modules. Hindi ako nakakakita ng personal records o "
            "aktuwal na request status, at hindi ako nagsusumite, "
            "nag-eedit, o nag-aapprove ng records at requests. "
            "Gamitin ang kaukulang portal form o makipag-ugnayan sa "
            "authorized staff para sa mga transaksiyon. Huwag ipadala "
            "dito ang password, valid ID, selfie, o clinical records; "
            "gamitin ang nakalaang verification o health workflow."
        ],
    },
]


def validate_dataset(data):
    if not isinstance(data, dict):
        raise ValueError("Ang intents.json ay dapat JSON object.")

    intents = data.get("intents")

    if not isinstance(intents, list):
        raise ValueError("Missing o invalid ang intents list.")

    tags = set()
    owners = {}

    for item in intents:
        if not isinstance(item, dict):
            raise ValueError("Bawat intent ay dapat object.")

        tag = item.get("tag")

        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("May intent na walang valid tag.")

        if tag in tags:
            raise ValueError(f"Duplicate intent tag: {tag}")

        tags.add(tag)

        for field in ("patterns", "responses"):
            values = item.get(field)

            if (
                not isinstance(values, list)
                or not values
                or any(
                    not isinstance(value, str) or not value.strip()
                    for value in values
                )
            ):
                raise ValueError(
                    f"Invalid {field} sa intent: {tag}"
                )

        for pattern in item["patterns"]:
            key = normalize(pattern)

            if not key:
                raise ValueError(
                    f"Empty normalized pattern sa {tag}."
                )

            previous = owners.get(key)

            if previous is not None and previous != tag:
                raise ValueError(
                    "Conflicting existing labels:\n"
                    f"  Question: {pattern}\n"
                    f"  Intents: {previous} / {tag}"
                )

            owners[key] = tag

    return owners


def main():
    with DATASET_PATH.open(encoding="utf-8-sig") as file:
        data = json.load(file)

    owners = validate_dataset(data)

    existing = {
        item["tag"]: item
        for item in data["intents"]
    }

    # Check conflicts before changing or saving anything.
    conflicts = []

    for addition in ADDITIONS:
        for pattern in addition["patterns"]:
            owner = owners.get(normalize(pattern))

            if owner is not None and owner != addition["tag"]:
                conflicts.append(
                    f"{pattern!r}\n"
                    f"  Existing: {owner}\n"
                    f"  Proposed: {addition['tag']}"
                )

    if conflicts:
        print("Walang binagong file.")
        print(
            "May questions na nasa ibang intent na. "
            "Kailangang i-review muna ang labels:\n"
        )

        for conflict in conflicts:
            print(conflict)
            print()

        raise SystemExit(1)

    added_patterns = 0
    added_intents = 0

    for addition in ADDITIONS:
        tag = addition["tag"]

        if tag not in existing:
            item = {
                "tag": tag,
                "patterns": [],
                "responses": addition["responses"].copy(),
            }

            data["intents"].append(item)
            existing[tag] = item
            added_intents += 1
        else:
            item = existing[tag]
            # Keep the existing responses unchanged.

        known = {
            normalize(pattern)
            for pattern in item["patterns"]
        }

        for pattern in addition["patterns"]:
            key = normalize(pattern)

            if key in known:
                continue

            item["patterns"].append(pattern)
            known.add(key)
            added_patterns += 1

    validate_dataset(data)

    if added_patterns == 0 and added_intents == 0:
        print("Nasa dataset na ang lahat ng examples.")
        print("Walang binagong file.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = BASE_DIR / (
        f"intents.before-system-knowledge-{timestamp}.json"
    )

    shutil.copy2(DATASET_PATH, backup_path)

    # Write separately before replacing the original file.
    temporary_path = BASE_DIR / (
        f"intents.system-knowledge-{timestamp}.tmp"
    )

    try:
        with temporary_path.open("x", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )
            file.write("\n")

        temporary_path.replace(DATASET_PATH)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    print(f"Backup: {backup_path.name}")
    print(f"Added intents: {added_intents}")
    print(f"Added patterns: {added_patterns}")
    print(f"Total intents: {len(data['intents'])}")
    print("Saved: intents.json")
    print("\nNext: py train.py")


if __name__ == "__main__":
    main()