import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "intents.json"

MOVES = {
    "account_password_reset": [
        "Nakalimutan ko ang password ko",
        "i forgot my password",
        "paano mag-reset ng password",
    ],

    "account_pending": [
        "paano ma-activate ang account",
    ],

    "document_walk_in": [
        "Pwede ba mag-walk-in na lang?",
        "kailangan ba ng account para mag-request",
        "pwede ba i-encode ng staff ang request ko",
        "walk-in request paano",
        "online request o walk-in",
        "pwede ba ako humiling kahit walang internet",
    ],

    "document_pickup": [
        "paano makuha ang dokumento pagkatapos maaprubahan",
        "kailan ko makukuha ang dokumento ko",
    ],

    "document_status": [
        "paano malalaman kung aprubado na",
    ],

    "document_additional_types": [
        "Paano kumuha ng Certificate of Residency?",
        "Magkano ang residency certificate?",
    ],

    "health_center_schedule": [
        "Anong araw ang prenatal checkup?",
    ],

    "health_privacy_access": [
        "sino ang nakakakita ng consultation record ko",
    ],

    "census_registration": [
        "Wala pa akong resident record sa barangay",
    ],

    "account_access": [
        "paano mag-register sa SMART MASIPIT",
    ],

    "greeting": [
        "How are you?",
    ],
}

ADDITIONS = {
    "account_identity_verification": [
        "Bakit kailangan ang dalawang side ng valid ID?",
        "Anong gagawin kapag denied ang camera permission?",
        "Malabo ang kuha ng ID ko paano uulitin?",
        "Kailangan bang mukha ko mismo ang nasa selfie?",
        "Saan ko makikita ang submit identity evidence?",
        "Can I retake my verification photo?",
        "The registration camera will not open",
        "Do I send my identification pictures in this chat?",
        "Required ba ang selfie bago mareview ang application?",
        "Paano palitan ang blurry na ID back photo?",
    ],

    "account_pending": [
        "Nakapagregister na ako pero awaiting verification pa",
        "Bakit account status lang ang lumalabas pagkatapos maglogin?",
        "Kumpleto na ID ko pero pending pa rin",
        "May paraan bang mapabilis ang review ng account?",
        "Captain lang ba ang puwedeng magverify ng resident account?",
        "Can the secretary activate my resident account?",
        "Who reviews a resident registration application?",
        "My application is still waiting for approval",
        "Paano magfollow up ng resident application?",
        "Automatic bang activated kapag nakapagselfie na?",
    ],

    "account_password_reset": [
        "Walang dumating na email matapos mag forgot password",
        "Saan ako hihingi ng bagong reset link?",
        "Nagamit ko na ang password link pwede pa ba ulitin?",
        "Ayaw tanggapin ang token para magreset",
        "How do I request another password recovery email?",
        "My password reset token has expired",
        "I cannot remember my login password",
        "Can I send you my password reset link?",
        "Nakalimutan ang password ng resident login",
        "Nasa spam ba ang password recovery message?",
    ],

    "document_walk_in": [
        "Walang email ang nanay ko makakahingi ba ng dokumento?",
        "Pwede sa opisina na lang magfile ng certificate?",
        "Ayokong online saan puwedeng magpasa ng request?",
        "May resident record pero walang login pwede clearance?",
        "Can staff submit a document application on my behalf?",
        "Do walk-in applicants need an online resident account?",
        "Can registered online users also request at the barangay counter?",
        "How do I request papers in person?",
        "Secretary ba ang magtatype ng request kapag walkin?",
        "Wala akong cellphone paano magrequest ng dokumento?",
    ],

    "document_pickup": [
        "May ready for release email saan ako pupunta?",
        "Pwede ko na bang kunin pag approved for preparation?",
        "Ano ang ibig sabihin ng pickup instructions?",
        "Saan makikita ang instructions sa pagclaim?",
        "Will I get an email when my document can be collected?",
        "Where do I collect the printed certificate?",
        "Does approval mean my document is ready for collection?",
        "I did not receive a ready for pickup notification",
        "Sa barangay ba irerelease ang printed document?",
        "Ano ang kaibahan ng approved at ready for release?",
    ],

    "health_maternal": [
        "Hiwalay ba ang record sa bawat pagbubuntis?",
        "Paano idagdag ang follow up ng buntis?",
        "May pregnancy history ba sa patient profile?",
        "Sino ang magtatala ng maternal visits?",
        "Draft pa ba ang maternal form na ipiprint?",
        "Where can health staff record antenatal visits?",
        "Can the maternal health form be printed?",
        "Does each pregnancy have a separate record?",
        "Paano ilalagay ang correction sa maternal record?",
        "Saan ieencode ang LMP sa maternal module?",
    ],

    "health_blood_pressure": [
        "Dalawang input ba ang blood pressure sa consultation?",
        "Pwede bang walang BP kapag hindi nasukat?",
        "Saan ilalagay ang systolic reading sa form?",
        "May diastolic field ba ang consultation?",
        "Does the consultation form store blood pressure values?",
        "Where do health workers enter systolic and diastolic values?",
        "Can staff record BP with the consultation notes?",
        "Is blood pressure part of the patient consultation record?",
        "May field para sa taas at baba na numero ng BP?",
        "Paano isave ang nasukat na BP sa patient consultation?",
    ],

    "barangay_location": [
        "Paano gamitin ang mapa sa landing page?",
        "Anong pipindutin para makita ang ruta sa barangay hall?",
        "May directions button ba sa home page?",
        "Hindi ko alam saan ang Masipit hall",
        "How can I find the barangay office on the map?",
        "Where is the location section on the website?",
        "Can Google Maps show the route to Masipit Hall?",
        "How do I enter my starting point for directions?",
        "Pwede bang buksan ang barangay map sa cellphone?",
        "Saan makikita ang pin ng Masipit Barangay Hall?",
    ],

    "health_no_advice": [
        "Normal ba ang blood pressure ko?",
        "Please interpret my BP reading",
        "Mataas ba ang 160 over 100?",
        "Anong gamot sa mataas na blood pressure?",
        "Masakit ang tiyan ko habang buntis ano ito?",
        "What medicine can I take during pregnancy?",
        "Ano ang ibig sabihin ng prenatal result ko?",
        "Can you diagnose my pregnancy symptoms?",
    ],

    "document_additional_types": [
        "Certificate of residency application",
        "Proof of residency certificate paano humingi?",
        "Paano magrequest ng certificate of good moral?",
        "Good moral certificate application",
        "Kailangan ko ng certificate of closure ng negosyo",
        "How to request a certificate of closure?",
        "Saan magapply ng barangay occupancy permit?",
        "Occupancy permit sa document form",
        "Oath of undertaking request process",
        "How to request first time jobseeker certification?",
    ],
}


def key(text):
    return " ".join(text.lower().split()).strip(" ?!.,")


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))

    items = {}

    for item in data["intents"]:
        tag = item["tag"]

        if tag in items:
            raise ValueError(f"Duplicate intent tag: {tag}")

        items[tag] = item

    for tag in set(MOVES) | set(ADDITIONS):
        if tag not in items:
            raise ValueError(f"Missing intent: {tag}")

    # Remove a moved question from every old label.
    # Then assign it to exactly one intended label.
    for target, phrases in MOVES.items():
        for phrase in phrases:
            for item in items.values():
                item["patterns"] = [
                    pattern
                    for pattern in item["patterns"]
                    if key(pattern) != key(phrase)
                ]

            items[target]["patterns"].append(phrase)

    for target, phrases in ADDITIONS.items():
        items[target]["patterns"].extend(phrases)

    # Remove duplicates and reject conflicting labels.
    owners = {}

    for tag, item in items.items():
        unique = {}

        for phrase in item["patterns"]:
            normalized = key(phrase)

            if normalized in owners and owners[normalized] != tag:
                raise ValueError(
                    f"Conflicting labels for question: {phrase}"
                )

            owners[normalized] = tag
            unique.setdefault(normalized, phrase)

        item["patterns"] = list(unique.values())

    backup = BASE / "intents.before-label-repair.json"

    if not backup.exists():
        backup.write_bytes(raw)

    SOURCE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    count = sum(len(item["patterns"]) for item in items.values())

    print(f"Updated patterns: {count}")
    print(f"Intents: {len(items)}")
    print(f"Backup: {backup.name}")
    print("Responses unchanged. Retrain next.")


if __name__ == "__main__":
    main()