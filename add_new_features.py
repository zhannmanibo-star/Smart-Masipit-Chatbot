"""
Teaches the chatbot the SMART MASIPIT features added in November 2026:
claim QR codes, requests for a child or ward, the minimum account age,
the My profile page, sitios, and the selfie-with-ID challenge.

It also adds examples to intents that the evaluation shows are weak
(document_status, data_privacy, chatbot_capabilities).

A backup of intents.json is written first, like the other expand scripts.
Run, then retrain:
    python add_new_features.py
    python train.py
"""

import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
INTENTS = BASE / "intents.json"


NEW_INTENTS = {
    "document_qr_code": {
        "responses": [
            "Bawat bukas na document request ay may sariling QR code. "
            "Buksan ang My Document Requests at pindutin ang Show QR; "
            "maaari rin itong i-save bilang larawan gamit ang Save image. "
            "Ipakita ang QR sa barangay office at i-scan ito ng staff para "
            "mabuksan agad ang inyong request. May personal na barangay QR "
            "din sa My profile. Dalhin pa rin ang valid ID sa pagkuha ng "
            "dokumento, at huwag i-post online ang inyong QR."
        ],
        "patterns": [
            "saan ko makikita ang QR ko",
            "saan makikita yung qr code ng request ko",
            "para saan ang QR code",
            "ano ang gamit ng QR sa request",
            "paano ipakita ang QR sa barangay",
            "may QR code ba ang document request",
            "kailangan ko ba ng QR pagkuha ng dokumento",
            "paano i-save ang QR ko",
            "nawala ang QR ko paano ulit makuha",
            "pwede ko bang i-screenshot ang QR",
            "i-scan ba ng secretary ang QR ko",
            "ano ang show qr button",
            "ano yung barangay QR sa profile ko",
            "personal QR code sa profile",
            "pwede bang ipakita ang qr sa cellphone",
            "kailangan pa ba ng id kung may qr na",
            "ok lang ba i-post ang qr code ko",
            "qr code para sa pickup ng clearance",
            "where is my qr code",
            "what is the qr code for",
            "how do i show my qr at the barangay",
            "can i save my qr code",
            "do i still need an id if i have the qr",
            "how does the qr scanning work",
            "where can i find the claim qr",
        ],
        "english": (
            "Every open document request has its own QR code. Open My "
            "Document Requests and select Show QR; you can also keep it with "
            "Save image. Show the QR at the barangay office and the staff will "
            "scan it to open your request right away. There is also a personal "
            "barangay QR on My profile. Still bring a valid ID when you pick up "
            "the document, and do not post your QR online."
        ),
        "labels": ("Saan makikita ang QR ng request ko?", "Where is my request QR code?"),
    },

    "document_for_dependent": {
        "responses": [
            "Ang naka-link na magulang o guardian ay maaaring mag-request ng "
            "dokumento para sa batang wala pang 18 taong gulang na walang "
            "sariling account. Ang barangay staff ang nag-uugnay ng magulang o "
            "guardian sa record ng bata. Kapag naka-link na, piliin ang "
            "pangalan ng bata sa Request a document. Lalabas ito sa inyong My "
            "Document Requests na may tatak na para sa bata. Kapag 13 taong "
            "gulang na ang bata, maaari na siyang gumawa ng sariling account."
        ],
        "patterns": [
            "pwede ko bang i-request ang clearance ng anak ko",
            "paano mag request ng dokumento para sa anak ko",
            "pwede bang ako ang mag request para sa anak kong bata pa",
            "mag request para sa menor de edad",
            "ako ang guardian ng pamangkin ko pwede ba ako mag request para sa kanya",
            "paano ma-link ang anak ko sa account ko",
            "bakit hindi ko makita ang pangalan ng anak ko sa request form",
            "sino ang nag-li-link ng magulang sa record ng bata",
            "pwede bang mag request ang lola para sa apo",
            "may account ba ang batang 5 taong gulang",
            "request ng indigency para sa anak ko",
            "paano kung wala pang account ang anak ko",
            "lalabas ba sa requests ko yung para sa anak ko",
            "ang anak ko ay 10 years old paano siya makakakuha ng certificate",
            "can i request a document for my child",
            "how do i request a certificate for my kid",
            "can a parent request for a minor",
            "i am the guardian of a child how do i request for them",
            "how do i link my child to my account",
            "why is my child's name not in the request form",
            "request on behalf of my son",
            "request on behalf of my daughter",
            "can the guardian file the request for a minor",
            "who links a parent to a child's record",
        ],
        "english": (
            "A linked parent or guardian can request documents for a child "
            "under 18 who has no account of their own. Barangay staff link the "
            "parent or guardian to the child's record. Once linked, choose the "
            "child's name in Request a document. The request appears in your "
            "My Document Requests marked as being for the child. When the child "
            "turns 13, they may create their own account."
        ),
        "labels": ("Paano mag-request para sa anak ko?", "How do I request for my child?"),
    },

    "account_minimum_age": {
        "responses": [
            "Kailangang 13 taong gulang pataas para gumawa ng sariling SMART "
            "MASIPIT account. Kung mas bata, ang naka-link na magulang o "
            "guardian ang maaaring mag-request ng dokumento para sa kanya. "
            "Kung naka-record na ang bata sa barangay at nag-register siya "
            "pagdating ng 13, iuugnay ng Secretary o Captain ang bagong account "
            "sa existing record habang nagve-verify."
        ],
        "patterns": [
            "ilang taon pwede gumawa ng account",
            "ilang taon bago makapag register",
            "pwede bang mag register ang 12 years old",
            "pwede ba gumawa ng account ang 15 years old",
            "may age limit ba ang registration",
            "minimum age sa smart masipit",
            "bata pa ako pwede ba ako mag register",
            "estudyante ako 14 years old pwede ba ako gumawa ng account",
            "bakit ayaw tanggapin ang birthday ko sa registration",
            "naka-register na ako sa barangay noong bata pa ako paano gumawa ng account ngayon",
            "dati record lang ako ngayon gusto ko ng sariling account",
            "kailangan bang 18 para mag register",
            "what is the minimum age to register",
            "can a 13 year old create an account",
            "how old do i need to be to sign up",
            "is there an age requirement for registration",
            "my child is 12 can they register",
            "i was registered as a kid how do i get my own account now",
            "why does registration reject my birth date",
            "do i need to be 18 to create an account",
        ],
        "english": (
            "You must be at least 13 years old to create your own SMART MASIPIT "
            "account. For a younger child, a linked parent or guardian can "
            "request documents for them. If the child is already on the "
            "barangay records and registers at 13, the Secretary or Captain "
            "connects the new account to the existing record during "
            "verification."
        ),
        "labels": ("Ilang taon pwede gumawa ng account?", "What is the minimum age to register?"),
    },

    "account_profile_settings": {
        "responses": [
            "Buksan ang My profile sa pamamagitan ng pag-click sa inyong avatar "
            "sa kanang itaas. Makikita rito ang inyong resident information, "
            "household, at account details. Maaaring mag-upload ng profile "
            "photo (JPG, PNG, o WebP, hanggang 4 MB) at magpalit ng password "
            "gamit ang Change password; hindi bababa sa 12 characters ang "
            "bagong password. Ang ibang resident details ay ina-update ng "
            "barangay staff."
        ],
        "patterns": [
            "paano magpalit ng profile picture",
            "paano mag upload ng profile photo",
            "saan ang my profile",
            "paano makita ang profile ko",
            "paano palitan ang password ko",
            "gusto kong baguhin ang password ko alam ko pa ang luma",
            "ilang characters ang password",
            "bakit ayaw tanggapin ang bagong password ko",
            "paano tanggalin ang profile picture",
            "anong file ang pwede sa profile photo",
            "masyadong malaki daw ang larawan ko",
            "paano i-edit ang pangalan ko sa account",
            "paano mag sign out",
            "saan ang logout",
            "how do i change my profile picture",
            "how do i upload a profile photo",
            "where is my profile page",
            "how do i change my password while signed in",
            "how long should my password be",
            "how do i remove my profile photo",
            "what file types are allowed for the photo",
            "how do i log out",
            "where is the sign out button",
            "can i edit my own details",
        ],
        "english": (
            "Open My profile by selecting your avatar at the top right. It shows "
            "your resident information, household, and account details. You can "
            "upload a profile photo (JPG, PNG, or WebP, up to 4 MB) and change "
            "your password with Change password; the new password must be at "
            "least 12 characters. Other resident details are updated by barangay "
            "staff. To sign out, open the same avatar menu and choose Sign out."
        ),
        "labels": ("Paano palitan ang profile photo o password?", "How do I change my photo or password?"),
    },

    "census_sitio": {
        "responses": [
            "May pitong sitio ang Barangay Masipit: Balaasan, Mataas na Kahoy "
            "(Road I), Centro, Irrigation Site, Masitao, Pulapog, at Road II. "
            "Piliin ang sitio kung saan kayo kasalukuyang nakatira. Kung lumipat "
            "kayo sa ibang sitio, makipag-ugnayan sa barangay staff para "
            "ma-update ang inyong record."
        ],
        "patterns": [
            "anong sitio ang pipiliin ko",
            "ano ang mga sitio sa masipit",
            "ilang sitio ang meron sa barangay masipit",
            "wala sa listahan ang sitio namin",
            "saang sitio ang centro",
            "nasaan ang sitio pulapog",
            "sitio balaasan ba ako o masitao",
            "lumipat kami ng sitio paano i-update",
            "ano ang road i at road ii",
            "mataas na kahoy ba ay road i",
            "irrigation site ba ay sitio",
            "paano kung mali ang sitio sa record ko",
            "listahan ng sitio",
            "which sitio should i choose",
            "what are the sitios in masipit",
            "how many sitios are there",
            "my sitio is not in the list",
            "we moved to another sitio how do i update it",
            "list of sitios in barangay masipit",
            "i picked the wrong sitio",
        ],
        "english": (
            "Barangay Masipit has seven sitios: Balaasan, Mataas na Kahoy "
            "(Road I), Centro, Irrigation Site, Masitao, Pulapog, and Road II. "
            "Choose the sitio where you currently live. If you moved to another "
            "sitio, contact barangay staff to update your record."
        ),
        "labels": ("Anong sitio ang pipiliin ko?", "Which sitio should I choose?"),
    },
}


# More examples for existing intents (new features or weak spots).
EXTRA_PATTERNS = {
    "account_identity_verification": [
        "bakit kailangan magtaas ng daliri sa selfie",
        "ano ang instruction sa selfie hawak ang id",
        "kailangan bang hawak ko ang id sa selfie",
        "bakit iba-iba ang bilang ng daliri sa selfie",
        "paano kung mali ang bilang ng daliri ko sa selfie",
        "selfie na hawak ang valid id",
        "why do i need to raise fingers in the selfie",
        "do i need to hold my id in the selfie",
        "what is the random selfie instruction",
    ],
    "document_status": [
        "ano na ang status ng clearance ko",
        "approved na ba ang certificate ko",
        "may update na ba sa request ko",
        "bakit under review pa rin ang request ko",
        "gaano katagal ang review ng request",
        "ano ibig sabihin ng closed not released",
        "rejected ang request ko ano gagawin ko",
        "naproseso na ba ang indigency ko",
        "has my request been approved",
        "what does under review mean",
        "why was my request rejected",
    ],
    "data_privacy": [
        "sino ang nakakakita ng personal information ko",
        "ligtas ba ang id na inupload ko",
        "ano ang ginagawa ninyo sa id at selfie ko",
        "ibinibigay ba ninyo ang data ko sa iba",
        "nakikita ba ng ibang resident ang info ko",
        "data privacy act ba ang sinusunod",
        "who can see my uploaded id",
        "do you share my personal data",
        "is my id photo kept private",
    ],
    "chatbot_capabilities": [
        "ano ang pwede kong itanong sa iyo",
        "anong tulong ang maibibigay mo",
        "kaya mo bang tingnan ang request ko",
        "pwede ka bang mag file ng request para sa akin",
        "what questions can i ask you",
        "can you check my request for me",
        "can you file a request for me",
    ],
}


# Answers that now mention the new features (Filipino; English is in english_responses.py).
RESPONSE_UPDATES = {
    "document_pickup": (
        " Pagpunta sa barangay, ipakita ang QR ng request (Show QR sa My "
        "Document Requests) para mabilis itong mahanap ng staff, at dalhin "
        "ang valid ID."
    ),
    "account_identity_verification": (
        " Sa selfie, hawakan ang valid ID at sundin ang random na instruction "
        "sa screen, halimbawa ilang daliri ang itataas. Patunay ito na kayo "
        "mismo ang nasa larawan at hindi lumang litrato."
    ),
}


def main():
    with INTENTS.open(encoding="utf-8-sig") as file:
        data = json.load(file)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BASE / f"intents.before-new-features-{stamp}.json"
    backup.write_bytes(INTENTS.read_bytes())

    by_tag = {intent["tag"]: intent for intent in data["intents"]}

    for tag, spec in NEW_INTENTS.items():
        if tag in by_tag:
            raise SystemExit(f"{tag} already exists; this script was already applied.")

        data["intents"].append({
            "tag": tag,
            "patterns": spec["patterns"],
            "responses": spec["responses"],
        })

    for tag, patterns in EXTRA_PATTERNS.items():
        existing = {p.casefold().strip() for p in by_tag[tag]["patterns"]}
        by_tag[tag]["patterns"].extend(p for p in patterns if p.casefold().strip() not in existing)

    for tag, addition in RESPONSE_UPDATES.items():
        responses = by_tag[tag]["responses"]
        if addition.strip() not in responses[0]:
            responses[0] = responses[0].rstrip() + addition

    # Same format as the original file: 2-space indent, UTF-8, CRLF line endings.
    text = json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\r\n") + "\r\n"
    INTENTS.write_bytes(text.encode("utf-8"))

    print(f"Backup: {backup.name}")
    print(f"Added intents: {', '.join(NEW_INTENTS)}")
    print(f"Added examples to: {', '.join(EXTRA_PATTERNS)}")
    print("Next: update english_responses.py, then run python train.py")


if __name__ == "__main__":
    main()
