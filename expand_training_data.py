import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "intents.json"

ADDITIONS = {
    "document_request_process": [
        "Ano ang unang hakbang sa pagsusumite ng document request?",
        "Paano magsimula ng bagong application para sa dokumento?",
        "Ano ang dapat gawin pagkatapos piliin ang document type?",
        "Paano isumite ang purpose ng document request?",
        "Ano ang sunod matapos maipasa ang document application?",
        "Paano dumadaan sa review ang bagong document request?",
        "Ano ang buong proseso mula submission hanggang release?",
        "Kailangan bang hintayin ang review bago maihanda ang dokumento?",
        "Sino ang susuri sa dokumentong nirequest sa portal?",
        "Ano ang ginagawa ng staff pagkatapos makatanggap ng request?",
        "Paano gamitin ang form para humiling ng barangay document?",
        "Saan magsisimula sa online document application?",
        "What steps should I follow to submit a document application?",
        "What happens after I send my document request?",
        "How does a submitted application reach document preparation?",
        "Explain the workflow from document submission to release",
        "Does staff review my application before preparing the document?",
        "What should I enter before submitting the document request form?",
        "How do I start a new document application in the portal?",
        "What is the review process for a submitted document application?",
    ],

    "document_list": [
        "Ano lahat ang pagpipilian sa document type dropdown?",
        "May listahan ba ng supported barangay documents?",
        "Anong certificates at permits ang kasama sa system?",
        "Ilan ang klase ng dokumentong puwedeng piliin?",
        "Pakisabi ang mga pangalan ng available certificates",
        "Ano ang sakop ng document services ninyo?",
        "Which document categories are supported by SMART MASIPIT?",
        "Show me the available certificate and permit types",
        "What choices appear in the document type menu?",
        "Can you name the documents offered in the request module?",
    ],

    "document_status": [
        "Naisubmit ko na ang application saan titingnan ang progress?",
        "Paano ko malalaman kung under review pa ang request?",
        "Ano ang ibig sabihin ng submitted sa request list?",
        "Paano makita kung nireject ng staff ang document application?",
        "Nagbago ba ang status ng certificate request ko?",
        "Saan nakalagay ang current stage ng nirequest kong dokumento?",
        "I already submitted a request where can I follow its progress?",
        "Where does the portal show whether my request was rejected?",
        "How do I know if my document application is under review?",
        "Can you check the current stage of my document request?",
    ],

    "census_requirements": [
        "Anong personal details ang kailangan sa resident registry?",
        "Required ba ang birth date sa resident information?",
        "Anong address details ang itinatala sa resident record?",
        "Anong fields ang pinupunan kapag nagrerehistro ng residente?",
        "Kasama ba ang first name at last name sa resident profile?",
        "Anong contact information ang puwedeng ilagay sa registry?",
        "Bakit hinihingi ang sitio sa resident registration?",
        "Ano ang nilalaman ng basic resident information form?",
        "Anong demographic details ang ginagamit sa resident registry?",
        "Ano ang kailangang impormasyon bago maencode ang residente?",
        "Which fields are collected when registering a resident?",
        "Does the resident form ask for a date of birth?",
        "What address information belongs in the resident profile?",
        "What basic details should I prepare for resident registration?",
        "Is contact information included in the resident registry?",
        "What information is stored in a basic resident record?",
    ],

    "census_registration": [
        "Hindi pa ako nakalista bilang residente saan magpaparehistro?",
        "Bagong lipat sa barangay paano magkaroon ng resident record?",
        "Paano maidagdag ang pangalan ko sa barangay registry?",
        "Wala pa akong entry sa resident masterlist",
        "Sino ang puwedeng magencode ng bagong resident record?",
        "Pwede bang resident record lang at walang online login?",
        "Kailangan kong magpalista bilang residente ng Masipit",
        "Paano magparehistro sa barangay nang hindi gumagawa ng account?",
        "How do I get listed in the barangay resident registry?",
        "I recently moved to Masipit how can I register as a resident?",
        "Who can create a resident registry entry for me?",
        "Can staff register a resident without creating an online account?",
    ],

    "census_household_update": [
        "Lilipat ang isang miyembro sa ibang household paano ito itatala?",
        "Paano ipapalipat sa ibang household ang resident record?",
        "May bagong household head sino ang maguupdate?",
        "Kailangan naming baguhin ang listahan ng kasama sa bahay",
        "Paano ipapaayos ang maling household assignment?",
        "Nasa ibang household ang pangalan ko paano ililipat?",
        "Paano magrequest ng correction sa address ng existing resident?",
        "May bagong miyembro ang bahay namin paano idagdag?",
        "Hindi na dito nakatira ang dating household member",
        "Sino ang magtatala ng pagbabago sa household membership?",
        "How do I request a transfer to another household?",
        "Who updates the household head in the registry?",
        "My resident record is linked to the wrong household",
        "A family member moved out how should the household be updated?",
        "Can staff correct the address on an existing resident record?",
        "How do I report a change in household membership?",
    ],

    "census_summary": [
        "May report ba ng bilang ng residente kada sitio?",
        "Saan makikita ng staff ang population summary?",
        "Paano tingnan ang breakdown ng edad sa barangay?",
        "May summary ba ng bilang ng babae at lalaki?",
        "Paano makikita ang kabuuang bilang ng households?",
        "Sino ang may permission sa demographic reports?",
        "May aggregated report ba ng registered residents?",
        "Makikita ba ang age distribution ng resident registry?",
        "Can authorized staff view resident counts by sitio?",
        "Where are the demographic summaries in the system?",
        "Does the census report show age group totals?",
        "Who is allowed to access population summary reports?",
    ],

    "account_access": [
        "First time kong gagamit ng portal paano gumawa ng login?",
        "Anong button ang pipindutin para magsign up?",
        "Saan ang Create resident account sa website?",
        "Gusto kong gumawa ng account para sa online services",
        "Paano pumasok sa portal gamit ang registered email?",
        "May login page ba para sa resident users?",
        "Paano maglogout pagkatapos gamitin ang account?",
        "Kailangan ko ng sariling account para sa resident portal",
        "Where do I create my first SMART MASIPIT account?",
        "Which button opens the resident sign-up form?",
        "How do I sign in with my registered email address?",
        "Where can residents log in to use online services?",
        "How can I sign out of the resident portal?",
        "I am a new portal user how do I create an account?",
    ],

    "account_pending": [
        "Nagsubmit na ako ng registration kailan ito irereview?",
        "Bakit pending pa rin kahit nakapagsubmit na ng ID?",
        "Account verification pending ang nakalagay sa screen",
        "Sino ang magdedesisyon sa resident account application?",
        "Kailangan ba ng approval bago magamit ang resident services?",
        "Hindi pa activated ang account pagkatapos magregister",
        "Paano magfollow up sa barangay tungkol sa pending account?",
        "Secretary o Captain ba ang reviewer ng registration?",
        "My registration was submitted but my account is not active",
        "Why does my account still say verification pending?",
        "Who decides whether my resident application is approved?",
        "Can I use resident services while account approval is pending?",
    ],

    "health_patient_record": [
        "Paano magbukas ng bagong patient profile sa health module?",
        "Hindi pa ako registered patient paano magsisimula?",
        "Sino ang gagawa ng patient record kapag unang punta?",
        "May existing resident record na ako paano maging registered patient?",
        "Walang online account ang pasyente pwede bang mairegister?",
        "Saan ipapaayos ang maling pangalan sa patient registration?",
        "May duplicate bang patient profile kapag registered na?",
        "Paano hahanapin ng health staff ang existing patient record?",
        "Paano magparegister ng patient na wala pang resident record?",
        "Kailangan bang may portal login bago gumawa ng patient profile?",
        "How can health staff register a first-time patient?",
        "Can a patient be registered without an online account?",
        "How is an existing resident linked to a patient profile?",
        "Where should I report incorrect patient registration details?",
        "How do staff find a patient's existing registration?",
        "Who creates patient profiles in the health module?",
    ],

    "health_privacy_access": [
        "Pwede bang makita ng kapitbahay ang consultation notes ko?",
        "Makakabasa ba ang resident account ng clinical records?",
        "May permission ba ang barangay staff sa patient consultations?",
        "Sino ang authorized bumasa ng maternal health information?",
        "Nakikita ba ng chatbot ang private patient details?",
        "Pwede bang makita ng ibang account ang bakuna record ng anak ko?",
        "Restricted ba ang medical history sa health personnel?",
        "Makikita ba ng ordinaryong user ang patient profile ng iba?",
        "Can the chatbot access confidential patient information?",
        "Can ordinary residents read another patient's consultation notes?",
        "Are clinical records limited to authorized health personnel?",
        "Who has permission to view maternal health information?",
        "Can non-health staff access consultation records?",
        "Are vaccination records visible to other resident accounts?",
    ],

    "health_center_schedule": [
        "Kailan available ang health staff para sa konsultasyon?",
        "Sino ang dapat tanungin tungkol sa schedule ng health center?",
        "Anong araw puwedeng pumunta para sa prenatal consultation?",
        "May schedule ba ngayong linggo para sa pagpapabakuna?",
        "Paano malalaman ang oras ng serbisyo sa health center?",
        "Kanino iko-confirm ang appointment schedule ng health center?",
        "May consultation service ba sa susunod na araw?",
        "Saan kukumpirmahin ang maternal clinic schedule?",
        "Who can confirm the health center's consultation schedule?",
        "What day is the next immunization session?",
        "How can I confirm prenatal clinic availability?",
        "Where should I ask about health center service hours?",
        "Is the health center offering consultations this week?",
        "Who should I contact for the vaccination schedule?",
    ],

    "health_immunization_record": [
        "Saan ipaparecord ang bakunang naibigay na sa bata?",
        "May mali sa date ng vaccination entry paano ipapawasto?",
        "Sino ang nagtatala ng vaccine history sa system?",
        "Paano mareview ng health staff ang recorded immunizations?",
        "May entry na ba ang huling bakuna sa patient record?",
        "Paano humingi ng sariling vaccination history sa health center?",
        "Where are previously administered vaccinations recorded?",
        "Who maintains the patient's immunization history?",
        "How do I report an incorrect vaccination record entry?",
        "Can health staff review the vaccines already recorded?",
    ],

    "health_no_advice": [
        "Pwede mo bang sabihin kung may sakit ako base sa nararamdaman ko?",
        "Anong gamot ang dapat kong bilhin para sa sintomas?",
        "Pakibasa kung normal ang blood pressure reading ko",
        "Ilang beses sa isang araw ko iinumin ang gamot?",
        "Ano ang diagnosis kapag ganito ang sintomas?",
        "Ligtas bang inumin ang gamot na ito habang buntis?",
        "Anong treatment ang kailangan sa nararamdaman ko?",
        "Pakisuri ang resulta ng laboratory test ko",
        "Can you recommend a medicine for my symptoms?",
        "Can you tell whether my blood pressure result is normal?",
        "What dose of medication should I take?",
        "Please diagnose me from these symptoms",
        "Can you interpret my laboratory results?",
        "Which treatment should I use during pregnancy?",
    ],

    "out_of_scope": [
        "Dito ba nagbabayad ng tuition fee?",
        "Paano magbayad ng internet subscription?",
        "Pwede ba akong magrenew ng passport sa portal?",
        "Saan kukuha ng driving license renewal?",
        "Magkano ang business permit para sa bagong tindahan?",
        "Paano magapply ng mayor's permit para sa negosyo?",
        "Paano magbook ng dental extraction sa chatbot?",
        "May available bang laboratory package sa clinic?",
        "Paano magreserve ng basketball court?",
        "Pwede magorder ng gamot sa website?",
        "Can I pay school tuition through this portal?",
        "How do I renew my passport here?",
        "Can you process my driver's license application?",
        "How do I apply for a mayor's business permit?",
        "Can this chatbot book a dental procedure?",
        "Can I order prescription medicine from this website?",
    ],
}


def normalize(text):
    return " ".join(text.lower().split()).strip(" ?!.,")


def main():
    if not SOURCE.is_file():
        raise SystemExit(
            "Hindi makita ang intents.json. "
            "Ilagay ang script sa chatbot folder."
        )

    original = SOURCE.read_bytes()
    data = json.loads(original.decode("utf-8-sig"))

    if not isinstance(data.get("intents"), list):
        raise ValueError("Invalid intents.json structure.")

    by_tag = {}

    for intent in data["intents"]:
        tag = intent["tag"]

        if tag in by_tag:
            raise ValueError(f"Duplicate intent tag: {tag}")

        by_tag[tag] = intent

    before = sum(
        len(intent["patterns"])
        for intent in by_tag.values()
    )

    for tag, questions in ADDITIONS.items():
        if tag not in by_tag:
            raise ValueError(f"Missing intent: {tag}")

        by_tag[tag]["patterns"].extend(questions)

    owners = {}

    for tag, intent in by_tag.items():
        unique = {}

        for question in intent["patterns"]:
            if not isinstance(question, str) or not question.strip():
                raise ValueError(f"Invalid question in {tag}")

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

    after = sum(
        len(intent["patterns"])
        for intent in by_tag.values()
    )

    if after == before:
        print("No new patterns added. These examples may already exist.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = BASE / f"intents.before-expansion-{timestamp}.json"
    backup.write_bytes(original)

    SOURCE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Previous patterns: {before}")
    print(f"Updated patterns: {after}")
    print(f"Net added: {after - before}")
    print(f"Intents: {len(by_tag)}")
    print(f"Backup: {backup.name}")
    print("Existing responses were preserved.")
    print("Next: run train.py")


if __name__ == "__main__":
    main()