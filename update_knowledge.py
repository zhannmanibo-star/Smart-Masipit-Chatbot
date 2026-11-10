import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / "intents.json"
BACKUP = BASE_DIR / "intents.before-system-update.json"

# Updated answers for existing intents.
UPDATED_ANSWERS = {
    "greeting": (
        "Magandang araw! Ako ang SMART MASIPIT Virtual Assistant. "
        "Makakatulong ako sa account registration, verification, "
        "document requests, walk-in services, resident registry, "
        "health records, at lokasyon ng barangay hall. "
        "Gabay sa paggamit ng system ang maibibigay ko; "
        "hindi ko nakikita ang personal records o actual request status."
    ),

    "goodbye": (
        "Salamat po! Kung may iba pa kayong tanong tungkol sa "
        "SMART MASIPIT, maaari kayong magtanong muli."
    ),

    "document_list": (
        "Ang mga document type na naidagdag sa SMART MASIPIT ay "
        "Barangay Clearance, Certificate of Indigency, "
        "Certificate of Residency, Oath of Undertaking, "
        "First-Time Jobseeker Barangay Certification, "
        "Certificate of Closure, Certificate of Good Moral, "
        "at Barangay Occupancy Permit. "
        "Piliin ang naaangkop na dokumento sa request form. "
        "Ang bawat request ay sasailalim sa verification at barangay review."
    ),

    "document_clearance": (
        "Para sa Barangay Clearance, mag-sign in gamit ang approved "
        "resident account, buksan ang document requests, "
        "piliin ang Barangay Clearance, at kumpletuhin ang required fields. "
        "Maaari ring magpa-encode ng walk-in request sa barangay hall. "
        "Kumpirmahin sa barangay ang requirements at anumang bayad."
    ),

    "document_indigency": (
        "Piliin ang Certificate of Indigency sa document request form "
        "at ilagay ang layunin ng request. "
        "Susuriin ng authorized barangay personnel ang eligibility "
        "at supporting information bago aprubahan. "
        "Para sa confirmed requirements at anumang bayad, "
        "makipag-ugnayan sa barangay office."
    ),

    "document_request_process": (
        "Maaaring magsumite online gamit ang approved resident account "
        "o magpa-encode ng walk-in request sa barangay hall. "
        "Dadaan ang request sa review at approval o rejection. "
        "Kapag approved, ihahanda muna ng staff ang dokumento. "
        "Hintayin ang Ready for release at basahin ang pickup instructions "
        "bago pumunta. Sa barangay office ginagawa ang printing at release."
    ),

    "document_status": (
        "Buksan ang My Document Requests para makita ang actual status "
        "ng inyong request. Maaaring Submitted, Under review, Approved, "
        "Rejected, Ready for release, Released, o Closed — Not released. "
        "Ang Approved ay para sa document preparation pa lamang. "
        "Hindi kayang tingnan ng chatbot ang personal request status."
    ),

    "payment_info": (
        "Walang online payment feature sa kasalukuyang SMART MASIPIT. "
        "Kumpirmahin sa barangay office ang anumang bayad at "
        "paraan ng pagbabayad para sa inyong dokumento."
    ),

    "health_patient_record": (
        "Maaaring mag-register ng patient ang authorized health staff "
        "kahit walang online resident account ang pasyente. "
        "Hahanapin muna ang existing resident record. "
        "Kung wala, maaaring magdagdag ng resident at patient record "
        "sa health registration flow matapos ma-verify ang impormasyon. "
        "Hindi ito awtomatikong gumagawa ng online account."
    ),

    "health_consultation_history": (
        "Authorized health staff ang nagtatala ng consultations "
        "at nagre-review ng consultation history. "
        "Ang corrections o clarifications ay itinatala bilang addendum "
        "upang mapanatili ang original entry. "
        "Para sa sariling record, makipag-ugnayan sa health staff. "
        "Hindi ito mababasa ng chatbot."
    ),

    "health_immunization_record": (
        "Authorized health staff ang nagtatala at nagre-review ng "
        "immunization records at correction history. "
        "Makipag-ugnayan sa Barangay Health Center para sa sariling "
        "record o record ng inyong anak. "
        "Kumpirmahin sa health staff ang schedule at mga kailangang dalhin."
    ),

    "health_center_schedule": (
        "Wala akong verified real-time schedule ng Barangay Health Center. "
        "Makipag-ugnayan sa health staff para sa consultation, "
        "immunization, at maternal service schedules."
    ),

    "health_privacy_access": (
        "Ang clinical records ay para lamang sa authorized health personnel. "
        "Ang resident account at ordinaryong barangay account "
        "ay hindi nagbibigay ng access sa clinical records. "
        "Hindi rin nakakabasa ang chatbot ng patient records."
    ),

    "health_no_advice": (
        "Ang chatbot na ito ay gabay sa paggamit ng SMART MASIPIT. "
        "Hindi ito nagbibigay ng diagnosis, interpretasyon ng clinical "
        "readings, reseta, o dosage ng gamot. "
        "Makipag-ugnayan sa qualified health professional "
        "para sa inyong health concern."
    ),

    "census_registration": (
        "Magkaiba ang resident registry record at online account. "
        "Maaaring magdagdag ang authorized staff ng resident record "
        "kahit walang online account ang tao. "
        "Para magkaroon ng online access, gumawa ng resident account "
        "at kumpletuhin ang barangay verification."
    ),

    "census_requirements": (
        "Nagtatala ang resident registry ng pangalan, birth date, sex, "
        "sitio, address, at contact number kung mayroon. "
        "Authorized staff ang nagve-verify ng impormasyon. "
        "Para sa eksaktong supporting documents na kailangan, "
        "makipag-ugnayan sa barangay office."
    ),

    "census_household_update": (
        "Authorized barangay staff ang namamahala sa household records, "
        "membership, at head assignment. "
        "Makipag-ugnayan sa staff para sa paglipat o pagwawasto. "
        "Walang self-service household editing ang resident account."
    ),

    "census_duplicate_check": (
        "May duplicate checking sa resident registration. "
        "Kapag may posibleng kaparehong pangalan at birth date, "
        "kailangang i-review ng staff ang existing record. "
        "Huwag gumawa ng panibagong record para lamang malampasan "
        "ang duplicate warning."
    ),

    "census_summary": (
        "Authorized barangay personnel ang nakakakita ng demographic "
        "summaries mula sa saved resident records. "
        "Para sa report inquiries, makipag-ugnayan sa barangay office. "
        "Hindi nakakakuha ng live census figures ang chatbot."
    ),

    "census_not_official": (
        "Ang census module ng SMART MASIPIT ay batay sa local resident "
        "registry ng Barangay Masipit. Hindi ito kapalit ng "
        "opisyal na pambansang census."
    ),

    "data_privacy": (
        "May permissions ang SMART MASIPIT ayon sa tungkulin ng account. "
        "Hindi nakakabasa ang chatbot ng resident, identity-verification, "
        "o health records. Huwag magpadala ng password, reset link, "
        "ID photo, PhilHealth number, o medical details sa chat."
    ),

    "account_access": (
        "Piliin ang Create resident account sa landing page "
        "o Create an account sa login page. "
        "Ilagay ang required information at kumpletuhin ang "
        "identity verification submission. Pending muna ang account "
        "hanggang ma-review ng Barangay Secretary o Captain. "
        "Kung nakalimutan ang password, gamitin ang Forgot your password."
    ),

    "barangay_operating_hours": (
        "Makipag-ugnayan sa barangay office para sa confirmed office hours, "
        "holiday schedule, at service availability. "
        "Hindi ako nakakakita ng real-time opening hours."
    ),

    "out_of_scope": (
        "Hindi ko matiyak ang sagot sa tanong na iyan. "
        "Makakatulong ako sa paggamit ng SMART MASIPIT: "
        "accounts, document requests, walk-in services, resident registry, "
        "health modules, at barangay location. "
        "Maaari bang linawin ang inyong tanong?"
    ),
}

# Each new intent has its own examples and answer.
NEW_INTENTS = [
    {
        "tag": "account_identity_verification",
        "patterns": [
            "Paano mag submit ng valid ID",
            "Kailangan ba ng selfie sa registration",
            "Bakit may front at back ng ID",
            "Ano ang identity verification",
            "Paano gamitin ang camera para sa account",
            "Need ba ng realtime photo",
            "What photos are required for registration",
            "Saan magpapasa ng ID at selfie",
        ],
        "responses": [
            "Para sa resident account verification, kailangan ang "
            "larawan ng harap at likod ng valid ID at selfie gamit ang "
            "camera capture sa verification form. Payagan ang camera "
            "permission at tiyaking malinaw ang mga larawan. "
            "Secretary o Captain ang magre-review. "
            "Sa verification form lamang isumite ang mga larawan, "
            "hindi sa chatbot."
        ],
    },
    {
        "tag": "account_pending",
        "patterns": [
            "Pending pa ang account ko",
            "Bakit hindi pa approved ang registration",
            "Sino ang nag aapprove ng account",
            "Paano malalaman kung verified na ako",
            "Matagal nang pending ang account",
            "Can the chatbot approve my account",
            "Pwede mo bang i approve ang account ko",
            "Account verification status",
        ],
        "responses": [
            "Secretary o Captain ang nagre-review ng resident account. "
            "Mag-sign in para makita ang Account Status at kumpletuhin "
            "ang hinihinging verification evidence kung kulang. "
            "Para sa follow-up, makipag-ugnayan sa barangay office. "
            "Hindi kayang mag-approve o tingnan ng chatbot ang inyong application."
        ],
    },
    {
        "tag": "account_password_reset",
        "patterns": [
            "Nakalimutan ko password ko",
            "Paano mag reset ng password",
            "Forgot password",
            "Hindi gumagana ang reset link",
            "Pwede bang gamitin ulit ang reset link",
            "Saan makikita password reset email",
            "How do I change a forgotten password",
            "Expired ang link sa email",
        ],
        "responses": [
            "Sa login page, piliin ang Forgot your password at "
            "ilagay ang registered email. Buksan ang reset email "
            "at sundin ang instructions. Tingnan din ang Spam folder. "
            "Kung nagamit na o hindi na valid ang link, humingi ng bago. "
            "Huwag ibahagi ang reset link o password sa chatbot."
        ],
    },
    {
        "tag": "document_walk_in",
        "patterns": [
            "Pwede mag request kahit walang account",
            "Paano mag walk in request",
            "Wala akong online account kailangan ko clearance",
            "Pwede staff ang mag encode ng request",
            "May account ako pwede pa rin ba walk in",
            "Walk in document request",
            "Can I request a document without registering online",
            "Wala pa akong resident record sa barangay",
        ],
        "responses": [
            "Puwedeng mag-walk-in document request kahit may online account "
            "o wala. Authorized staff ang magve-verify ng identity at "
            "maghahanap ng resident record. Kung wala pang record, "
            "kailangang mairehistro muna ang resident bago i-encode "
            "ang document request. Dadaan pa rin ito sa review at approval."
        ],
    },
    {
        "tag": "document_pickup",
        "patterns": [
            "Ready for pickup na document ko",
            "Kailan kukunin ang certificate",
            "Approved na pwede na kunin",
            "Wala akong natanggap na pickup email",
            "Saan kukunin ang barangay clearance",
            "Ready for release meaning",
            "How do I collect my document",
            "Paano kung walang email ang walk in",
        ],
        "responses": [
            "Ang Approved ay hindi pa nangangahulugang handa nang kunin "
            "ang dokumento. Tingnan kung Ready for release na at basahin "
            "ang pickup instructions. Maaaring makatanggap ng notification "
            "ang eligible linked resident account. Kung walang online account "
            "o walang dumating na email, mag-follow up sa barangay office. "
            "Hindi kayang kumpirmahin ng chatbot ang actual readiness."
        ],
    },
    {
        "tag": "document_additional_types",
        "patterns": [
            "Paano humingi ng certificate of residency",
            "Paano kumuha ng good moral",
            "May certificate of closure ba",
            "Barangay occupancy permit request",
            "Paano mag request ng oath of undertaking",
            "First time jobseeker certification",
            "Ano ang signed oath reference",
            "Kailangan ba ng oath sa first time jobseeker",
            "Requirements para sa jobseeker certificate",
        ],
        "responses": [
            "Piliin ang kaukulang certificate o permit sa document request "
            "form at kumpletuhin ang additional fields na ipinapakita. "
            "Para sa First-Time Jobseeker Certification, sinusuri rin "
            "ng staff ang signed oath at reference nito. "
            "Ang draft na hindi pa napipirmahan ay hindi signed oath. "
            "Kumpirmahin sa barangay ang eligibility at supporting requirements."
        ],
    },
    {
        "tag": "health_maternal",
        "patterns": [
            "May maternal records ba",
            "Paano mag register ng pregnancy record",
            "Saan makikita prenatal record",
            "Ano ang antepartum visits",
            "Pwede iprint maternal health record",
            "Paano magdagdag ng prenatal visit",
            "Maternal health record",
            "Pregnancy record registration",
        ],
        "responses": [
            "May maternal records module para sa authorized health staff. "
            "Mula sa patient profile, maaaring gumawa ng hiwalay na record "
            "bawat pregnancy, magtala ng antepartum visits, at magdagdag "
            "ng correction notes. Draft pa ang printable maternal form "
            "habang hinihintay ang official template confirmation. "
            "Makipag-ugnayan sa health staff para sa registration; "
            "hindi nakikita ng chatbot ang clinical details."
        ],
    },
    {
        "tag": "health_blood_pressure",
        "patterns": [
            "May blood pressure field ba sa system",
            "Saan ini encode ang BP",
            "Paano mag record ng blood pressure",
            "Systolic at diastolic fields",
            "Pwede ba mag save ng BP sa consultation",
            "Blood pressure recording feature",
            "Sino ang maglalagay ng BP reading",
            "May BP ba sa consultation records",
        ],
        "responses": [
            "Maaaring itala ng authorized health staff ang systolic at "
            "diastolic blood pressure sa consultation record. "
            "Ang chatbot ay nagpapaliwanag lamang ng system feature; "
            "hindi nito sinusuri kung normal o abnormal ang inyong reading. "
            "Para sa interpretasyon, makipag-ugnayan sa health professional."
        ],
    },
    {
        "tag": "barangay_location",
        "patterns": [
            "Saan ang barangay hall",
            "Paano pumunta sa Masipit barangay hall",
            "May Google Maps ba",
            "Saan makikita ang lokasyon",
            "Directions papunta barangay",
            "Address ng barangay hall",
            "Where is Masipit Barangay Hall",
            "Paano gamitin ang Get Directions",
        ],
        "responses": [
            "Sa landing page ng SMART MASIPIT, piliin ang Lokasyon. "
            "Nandoon ang Google Maps ng Masipit Barangay Hall "
            "sa Barangay Masipit, Calapan City, Oriental Mindoro. "
            "Pindutin ang Get Directions para buksan ang Google Maps "
            "at ilagay ang inyong pinanggagalingan."
        ],
    },
]


def main():
    if not SOURCE.is_file():
        raise SystemExit(
            "Hindi makita ang intents.json. "
            "Ilagay ang script sa chatbot project folder."
        )

    original = SOURCE.read_bytes()
    data = json.loads(original.decode("utf-8-sig"))

    if not isinstance(data, dict) or not isinstance(data.get("intents"), list):
        raise SystemExit("Invalid intents.json structure.")

    by_tag = {}

    for intent in data["intents"]:
        tag = intent["tag"]

        if tag in by_tag:
            raise SystemExit(f"Duplicate intent tag: {tag}")

        by_tag[tag] = intent

    missing = set(UPDATED_ANSWERS) - set(by_tag)

    if missing:
        raise SystemExit(
            "Missing existing tags; no files changed: "
            + ", ".join(sorted(missing))
        )

    for tag, answer in UPDATED_ANSWERS.items():
        by_tag[tag]["responses"] = [answer]

    for new_intent in NEW_INTENTS:
        tag = new_intent["tag"]

        if tag in by_tag:
            existing = by_tag[tag]
            existing["patterns"] = list(dict.fromkeys(
                existing["patterns"] + new_intent["patterns"]
            ))
            existing["responses"] = new_intent["responses"]
        else:
            data["intents"].append(new_intent)
            by_tag[tag] = new_intent

    # Keep the original source once, even if the script is run again.
    if not BACKUP.exists():
        BACKUP.write_bytes(original)

    SOURCE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {SOURCE.name}")
    print(f"Backup: {BACKUP.name}")
    print(f"Intent count: {len(data['intents'])}")
    print("Next: run train.py to regenerate the model and responses.json.")


if __name__ == "__main__":
    main()