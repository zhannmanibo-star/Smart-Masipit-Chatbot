"""
Brings the chatbot in line with what SMART MASIPIT does now (November 2026):

New topics
  document_pickup_time     choosing, changing or removing a pickup time
  account_two_factor       two-factor sign-in for staff, recovery codes,
                           "Remember this device for 30 days"
  app_install              installing SMART MASIPIT on a phone or computer
  barangay_events          events page, landing page section, Calendar
  barangay_announcements   announcements page and categories
  aid_programs             ayuda: recorded by barangay staff only

Updated answers
  account_password_reset   now a 6-digit code sent by email (not a link)
  document_pickup          bring a valid ID and the QR or reference number,
                           pickup time, the bilingual "ready" notice
  barangay_operating_hours pickup times follow the barangay's office days
  greeting, out_of_scope, system_overview, chatbot_capabilities mention the
  new features

Clearer topics (fewer mix-ups found by the evaluation)
  "Paano palitan ang password?" moves from account_access to
  account_profile_settings, and weak topics get more examples.

A backup of intents.json is written first, like the other scripts.
Run, then retrain and test:
    python align_with_system.py
    python train.py
    python evaluate_assistant.py
    python test_real_questions.py
"""

import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
INTENTS = BASE / "intents.json"


NEW_INTENTS = {
    "document_pickup_time": {
        "responses": [
            "Kapag Ready for release na ang request, buksan ito sa My Document "
            "Requests. Sa bahaging Pickup time, pumili ng petsa at oras mula sa "
            "mga bakanteng slot at pindutin ang Save pickup time. Maaari itong "
            "palitan gamit ang Change pickup time o alisin gamit ang Remove my "
            "pickup time. Sumusunod ang mga slot sa office days at oras na "
            "itinakda ng barangay; may limitadong bilang ng tao bawat slot, at "
            "walang slot sa mga araw na sarado ang tanggapan. Kung walang "
            "angkop na oras, makipag-ugnayan sa barangay office."
        ],
        "patterns": [
            "paano mag set ng pickup time",
            "saan pipili ng oras ng pagkuha",
            "paano mag book ng oras para kunin ang dokumento",
            "pwede ba akong pumili kung anong oras ako pupunta para kunin",
            "paano baguhin ang pickup time ko",
            "gusto kong ilipat ang oras ng pagkuha ko",
            "paano tanggalin ang pickup time",
            "bakit walang lumalabas na oras sa pickup",
            "full na lahat ng slot ng pickup",
            "bakit walang slot sa araw na gusto ko",
            "may pickup slot ba tuwing sabado",
            "ilang tao bawat pickup slot",
            "kailangan ko bang pumili ng pickup time",
            "save pickup time saan makikita",
            "ano ang pickup time sa request ko",
            "pwede ba akong pumunta kahit hindi ako pumili ng oras",
            "hindi ako makakapunta sa napili kong oras",
            "how do i book a pickup time",
            "where do i choose when to pick up my document",
            "how do i change my pickup time",
            "how do i remove my pickup slot",
            "why are there no pickup times available",
            "all pickup slots are full what now",
            "is there a limit of people per pickup slot",
            "do i need to pick a time before claiming",
            "pickup slot schedule",
            "schedule ng pagclaim ng certificate",
        ],
        "english": (
            "When the request is Ready for release, open it in My Document "
            "Requests. Under Pickup time, choose a date and time from the open "
            "slots and press Save pickup time. You can change it with Change "
            "pickup time or remove it with Remove my pickup time. Slots follow "
            "the office days and hours set by the barangay; each slot takes a "
            "limited number of people, and there are no slots on days the "
            "office is closed. If no time fits, contact the barangay office."
        ),
        "labels": ("Paano pumili ng oras ng pagkuha?", "How do I choose a pickup time?"),
    },
    "account_two_factor": {
        "responses": [
            "Ang two-factor sign-in ay required sa staff accounts ng SMART "
            "MASIPIT; password lang ang gamit ng resident accounts. I-set up ito "
            "sa My profile, sa Two-factor sign-in: i-scan ang QR gamit ang "
            "authenticator app (halimbawa Google o Microsoft Authenticator), "
            "ilagay ang code, at itabi ang recovery codes. Sa pag-sign in, "
            "ilagay ang 6-digit code mula sa app. Maaaring i-check ang Remember "
            "this device for 30 days sa sariling device lang; magagamit ang "
            "Forget all devices sa My profile. Kapag nawala ang phone, gumamit "
            "ng recovery code; kung wala, makipag-ugnayan sa administrator. "
            "Huwag ibigay ang code o recovery codes sa chatbot."
        ],
        "patterns": [
            "ano ang two factor authentication",
            "paano i-set up ang 2fa",
            "bakit humihingi ng 6 digit code pagka login",
            "anong app ang gagamitin para sa two factor",
            "kailangan ko bang mag 2fa",
            "required ba ang two factor sa staff",
            "may 2fa ba ang resident account",
            "nawala ang cellphone ko na may authenticator",
            "paano gamitin ang recovery code",
            "saan makikita ang recovery codes ko",
            "ano ang remember this device",
            "paano tanggalin ang naka remember na device",
            "forget all devices ano yun",
            "ayaw tanggapin ang authenticator code",
            "bago akong staff kailangan daw i-on ang two factor",
            "pwede bang patayin ang two factor ng staff account",
            "google authenticator para sa smart masipit",
            "what is two-factor sign in",
            "how do i turn on 2fa",
            "which authenticator app should i use",
            "i lost my phone with my authenticator",
            "where are my recovery codes",
            "what does remember this device for 30 days do",
            "my two factor code is not accepted",
            "do residents need two factor authentication",
            "can i disable two factor on a staff account",
        ],
        "english": (
            "Two-factor sign-in is required for SMART MASIPIT staff accounts; "
            "resident accounts sign in with a password only. Set it up in My "
            "profile under Two-factor sign-in: scan the QR code with an "
            "authenticator app (for example Google or Microsoft Authenticator), "
            "enter the code, and keep the recovery codes safe. When signing "
            "in, enter the 6-digit code from the app. Tick Remember this "
            "device for 30 days only on your own device; Forget all devices "
            "in My profile undoes it. If you lose your phone, use a recovery "
            "code; if you have none, contact the administrator. Never share "
            "codes or recovery codes with the chatbot."
        ),
        "labels": ("Ano ang two-factor sign-in?", "What is two-factor sign-in?"),
    },
    "app_install": {
        "responses": [
            "Maaaring i-install ang SMART MASIPIT sa phone o computer na parang "
            "app; wala itong hiwalay na app sa Play Store o App Store. Sa "
            "Chrome o Edge, pindutin ang Install app (o I-install ang app sa "
            "landing page) kapag lumabas ito, o buksan ang menu ng browser at "
            "piliin ang Install app o Add to Home screen. Sa iPhone, buksan ito "
            "sa Safari, pindutin ang Share, at piliin ang Add to Home Screen. "
            "Pareho pa rin ang account at mga feature."
        ],
        "patterns": [
            "may app ba ang smart masipit",
            "paano i-install sa cellphone",
            "paano ilagay sa home screen ang smart masipit",
            "ano ang install app button",
            "saan ang i-install ang app",
            "wala sa playstore ang smart masipit",
            "may app store ba kayo",
            "paano i-install sa iphone",
            "walang install button sa safari",
            "pwede bang i-download ang system",
            "gusto ko sanang may icon sa phone ko",
            "pwede ba sa laptop i-install",
            "pareho ba ang account sa app at website",
            "android app ng barangay masipit",
            "is there a mobile app",
            "how do i install smart masipit",
            "can i download the app from the play store",
            "add to home screen on iphone",
            "the install app button is missing",
            "can i install it on my computer",
            "is the app different from the website",
            "how to put the website on my phone like an app",
        ],
        "english": (
            "You can install SMART MASIPIT on your phone or computer like an "
            "app; there is no separate app in the Play Store or App Store. In "
            "Chrome or Edge, press Install app (or I-install ang app on the "
            "landing page) when it appears, or open the browser menu and "
            "choose Install app or Add to Home screen. On iPhone, open it in "
            "Safari, press Share, and choose Add to Home Screen. Your account "
            "and features stay the same."
        ),
        "labels": ("Paano i-install ang app?", "How do I install the app?"),
    },
    "barangay_events": {
        "responses": [
            "Makikita ang mga darating na public event ng Barangay Masipit sa "
            "landing page (Mga darating na event) at sa Events page. Kapag "
            "naka-sign in, buksan ang Calendar para makita ang mga event bawat "
            "buwan. Ang mga barangay official ang naglalagay ng events; may "
            "ilang event na para sa staff lamang. Hindi nakikita ng chatbot "
            "ang mismong listahan, kaya tingnan ang Events page o makipag-ugnayan "
            "sa barangay office."
        ],
        "patterns": [
            "may event ba sa barangay",
            "ano ang mga darating na event",
            "saan makikita ang events",
            "saan ang calendar",
            "paano makita ang schedule ng mga aktibidad ng barangay",
            "may liga ba ngayong buwan",
            "kailan ang feeding program",
            "may medical mission ba",
            "may barangay assembly ba",
            "kailan ang fiesta ng masipit",
            "saan ko makikita ang mga aktibidad",
            "events page ng smart masipit",
            "bakit hindi ko makita ang ibang event sa calendar",
            "sino ang naglalagay ng events",
            "pwede ba akong maglagay ng event",
            "upcoming events in barangay masipit",
            "where is the events calendar",
            "what activities are scheduled this month",
            "is there a community event this weekend",
            "where can i see barangay activities",
            "who posts the events",
            "calendar of activities",
        ],
        "english": (
            "Upcoming public events of Barangay Masipit are on the landing page "
            "(Mga darating na event) and on the Events page. When signed in, "
            "open Calendar to see events month by month. Barangay officials "
            "post the events; some events are for staff only. The chatbot "
            "cannot see the list itself, so check the Events page or contact "
            "the barangay office."
        ),
        "labels": ("Saan makikita ang mga event?", "Where can I see the events?"),
    },
    "barangay_announcements": {
        "responses": [
            "Makikita ang mga abiso ng barangay sa landing page (Mga abiso ng "
            "barangay) at sa Announcements page. Nakaayos ang mga ito ayon sa "
            "kategorya: General, Health, Event, Advisory, at Emergency; nauuna "
            "ang mga naka-pin. Ang Barangay Secretary, Captain, o administrator "
            "ang nagpo-post ng announcements. Hindi binabasa ng chatbot ang "
            "mismong mga abiso, kaya tingnan ang Announcements page."
        ],
        "patterns": [
            "saan ang announcements",
            "may abiso ba ang barangay",
            "saan makikita ang balita ng barangay",
            "may bagong paalala ba",
            "saan nakapost ang mga advisory",
            "may emergency announcement ba",
            "paano malaman ang mga anunsyo",
            "sino ang nagpo-post ng announcement",
            "pwede ba akong mag post ng announcement",
            "ano ang pinned announcement",
            "may health advisory ba",
            "saan ko makikita ang mga paalala",
            "announcements page",
            "where are the barangay announcements",
            "is there any news from the barangay",
            "where can i read the latest advisory",
            "who posts announcements",
            "are there emergency announcements",
            "how will i know about barangay news",
            "barangay bulletin",
        ],
        "english": (
            "Barangay notices are on the landing page (Mga abiso ng barangay) "
            "and on the Announcements page. They are grouped by category: "
            "General, Health, Event, Advisory and Emergency; pinned ones come "
            "first. The Barangay Secretary, Captain or administrator posts "
            "them. The chatbot does not read the notices themselves, so check "
            "the Announcements page."
        ),
        "labels": ("Saan makikita ang mga anunsyo?", "Where are the announcements?"),
    },
    "aid_programs": {
        "responses": [
            "Ang ayuda o relief distribution ay itinatala ng authorized "
            "barangay staff bawat household, batay sa resident registry. "
            "Walang online na pag-apply o listahan ng ayuda para sa resident "
            "account, at hindi kayang kumpirmahin ng chatbot kung kasama kayo "
            "o kung may ayuda ngayon. Para sa schedule at eligibility, "
            "makipag-ugnayan sa barangay office o abangan ang Announcements. "
            "Huwag ipadala sa chat ang personal o household details."
        ],
        "patterns": [
            "kailan ang bigay ng ayuda",
            "paano mag apply ng ayuda",
            "kasama ba kami sa ayuda",
            "saan makikita kung nakatanggap na kami ng ayuda",
            "may relief goods ba",
            "may cash assistance ba ang barangay",
            "bakit hindi kami nabigyan ng ayuda",
            "paano malalaman kung qualified ako sa ayuda",
            "ayuda para sa 4ps",
            "ayuda para sa senior at pwd",
            "may listahan ba ng ayuda online",
            "sino ang nagbibigay ng ayuda",
            "ayuda tracker",
            "how do i apply for aid",
            "is there any relief distribution",
            "am i qualified for financial assistance",
            "how do i check if we received aid",
            "when is the next ayuda",
            "is there cash assistance from the barangay",
        ],
        "english": (
            "Aid or relief distributions are recorded by authorized barangay "
            "staff for each household, based on the resident registry. There "
            "is no online application or aid list for resident accounts, and "
            "the chatbot cannot confirm whether you are included or whether "
            "aid is being given now. For schedules and eligibility, contact "
            "the barangay office or watch the Announcements. Do not send "
            "personal or household details in the chat."
        ),
        "labels": ("May ayuda ba?", "Is there any aid?"),
    },
}


# Answers updated to match the system (Filipino; English below).
UPDATED_RESPONSES = {
    "account_password_reset": (
        "Sa login page, piliin ang Forgot your password at ilagay ang "
        "registered email. Magpapadala ang system ng 6-digit code sa email; "
        "tingnan din ang Spam folder. Ilagay ang code at ang bagong password "
        "(hindi bababa sa 12 characters, may letra at numero). Valid ang code "
        "nang 15 minuto; maaaring humingi ng bago pagkalipas ng isang minuto, "
        "hanggang 5 code bawat araw. Huwag ibigay ang code o password sa "
        "chatbot.",
        "On the login page, choose Forgot your password and enter your "
        "registered email. The system sends a 6-digit code to that email; "
        "check the Spam folder too. Enter the code and your new password (at "
        "least 12 characters, with letters and numbers). The code works for "
        "15 minutes; you can ask for a new one after a minute, up to 5 codes "
        "a day. Never give the code or your password to the chatbot.",
    ),
    "document_pickup": (
        "Ang Approved ay hindi pa nangangahulugang handa nang kunin ang "
        "dokumento; hintayin ang Ready for release. Kapag handa na, may "
        "pickup notice sa inyong request at sa email ng eligible na account. "
        "Maaari ring pumili ng pickup time sa request page. Pagpunta sa "
        "barangay office, magdala ng isang valid ID at ipakita ang QR code o "
        "reference number ng request (Show QR sa My Document Requests). "
        "Hindi kayang kumpirmahin ng chatbot ang aktuwal na status.",
        "Approved does not yet mean the document can be picked up; wait for "
        "Ready for release. When it is ready, a pickup notice appears on your "
        "request and is emailed to the eligible account. You can also choose "
        "a pickup time on the request page. At the barangay office, bring one "
        "valid ID and show the request's QR code or reference number (Show QR "
        "in My Document Requests). The chatbot cannot confirm the actual "
        "status.",
    ),
    "barangay_operating_hours": (
        "Makipag-ugnayan sa barangay office para sa confirmed office hours at "
        "holiday schedule. Ang mga pickup time na makikita sa inyong request "
        "ay sumusunod sa office days at oras na itinakda ng barangay. Hindi "
        "ako nakakakita ng real-time na impormasyon.",
        "Contact the barangay office for confirmed office hours and the "
        "holiday schedule. The pickup times shown on your request follow the "
        "office days and hours set by the barangay. I cannot see real-time "
        "information.",
    ),
    "greeting": (
        "Magandang araw! Ako ang SMART MASIPIT Virtual Assistant. Makakatulong "
        "ako sa account registration at verification, document requests at "
        "pickup time, walk-in services, resident registry, health records, "
        "events, announcements, at lokasyon ng barangay hall. Gabay sa "
        "paggamit ng system ang maibibigay ko; hindi ko nakikita ang personal "
        "records o actual request status.",
        "Good day! I am the SMART MASIPIT Virtual Assistant. I can help with "
        "account registration and verification, document requests and pickup "
        "times, walk-in services, the resident registry, health records, "
        "events, announcements, and the barangay hall location. I give "
        "guidance on using the system; I cannot see personal records or "
        "actual request status.",
    ),
    "out_of_scope": (
        "Hindi ko matiyak ang sagot sa tanong na iyan. Makakatulong ako sa "
        "paggamit ng SMART MASIPIT: accounts, document requests at pickup, "
        "walk-in services, resident registry, health modules, events, "
        "announcements, at lokasyon ng barangay. Maaari bang linawin ang "
        "inyong tanong?",
        "I am not sure how to answer that. I can help with using SMART "
        "MASIPIT: accounts, document requests and pickup, walk-in services, "
        "the resident registry, health modules, events, announcements, and "
        "the barangay location. Could you clarify your question?",
    ),
    "system_overview": (
        "Ang SMART MASIPIT ay isang web-based information system para sa "
        "Barangay Masipit. Sakop nito ang resident registry at household "
        "records, resident account registration at verification, document "
        "requests na may pickup time at QR code, health record management, "
        "announcements, at events calendar. Kasama sa health module ang "
        "consultations, blood pressure records, immunization, health history, "
        "at maternal records. Magkakaiba ang access ng residents at "
        "authorized staff ayon sa kanilang role.",
        "SMART MASIPIT is a web-based information system for Barangay "
        "Masipit. It covers the resident registry and household records, "
        "resident account registration and verification, document requests "
        "with pickup times and QR codes, health record management, "
        "announcements, and an events calendar. The health module includes "
        "consultations, blood pressure records, immunization, health history, "
        "and maternal records. Residents and authorized staff have different "
        "access according to their role.",
    ),
    "chatbot_capabilities": (
        "Gabay sa paggamit ng SMART MASIPIT ang maibibigay ko: accounts at "
        "verification, document requests at pickup time, walk-in services, "
        "resident registry, health modules, events, at announcements. Hindi "
        "ko nakikita ang personal records o aktuwal na request status, at "
        "hindi ako nagsusumite, nag-eedit, o nag-aapprove ng records at "
        "requests. Gamitin ang kaukulang page o makipag-ugnayan sa authorized "
        "staff. Huwag ipadala dito ang password, code, valid ID, selfie, o "
        "clinical records.",
        "I can guide you in using SMART MASIPIT: accounts and verification, "
        "document requests and pickup times, walk-in services, the resident "
        "registry, health modules, events, and announcements. I cannot see "
        "personal records or actual request status, and I do not submit, "
        "edit or approve records and requests. Use the matching page or "
        "contact authorized staff. Do not send passwords, codes, valid IDs, "
        "selfies or clinical records here.",
    ),
}


# Examples that belong to another topic.
MOVED_PATTERNS = [
    ("Paano palitan ang password?", "account_access", "account_profile_settings"),
    # The system now has an aid tracker, so these are no longer out of scope.
    ("may ayuda ba ngayon", "out_of_scope", "aid_programs"),
    ("relief goods paano makakuha", "out_of_scope", "aid_programs"),
]


# More examples for topics that are weak or mixed up in the evaluation.
EXTRA_PATTERNS = {
    "account_two_factor": [
        "bakit may hinihinging code pagkatapos ng password",
        "staff ako at may code na hinihingi tuwing mag sign in",
        "saan kukunin ang code na hinihingi sa login ng staff",
        "why does the staff login ask for a code",
        "where do i get the sign in code for my staff account",
    ],
    "account_password_reset": [
        "hindi ko natanggap ang 6 digit code",
        "expired na ang reset code",
        "ilang beses pwede humingi ng reset code",
        "mali daw ang code sa forgot password",
        "saan ilalagay ang code galing sa email",
        "the reset code did not arrive",
        "my reset code expired",
        "how many reset codes can i request",
    ],
    "account_profile_settings": [
        "gusto kong palitan ang password habang naka login",
        "saan ang change password",
        "paano mag change password sa profile",
        "saan ang my profile page",
        "paano mag-logout sa smart masipit",
        "paano palitan ang larawan sa account",
        "where is the change password option",
        "how do i update my profile photo",
    ],
    "account_access": [
        "paano mag register ng bagong account",
        "saan ang create resident account",
        "ayaw akong papasukin sa login",
        "mali daw ang email o password ko",
        "may account na ba ako o wala pa",
        "how do i make a resident account",
        "i cannot sign in to my account",
    ],
    "account_minimum_age": [
        "ilang taon dapat para makapag-account",
        "pwede ba ang menor de edad gumawa ng account",
        "anong edad pwede mag sign up",
        "13 years old pwede na ba",
        "is there an age limit for signing up",
        "how old do i need to be to register",
    ],
    "chatbot_capabilities": [
        "ano ang alam mo",
        "anong mga tanong ang kaya mong sagutin",
        "tao ba ang kausap ko",
        "robot ka ba",
        "pwede mo bang gawin ang request para sa akin",
        "kaya mo bang makita ang status ng application ko",
        "are you a real person",
        "what topics do you know",
        "can you do the request on my behalf",
    ],
    "system_overview": [
        "ano ang laman ng smart masipit",
        "anu-ano ang pwedeng gawin sa website",
        "ano ang mga parte ng system",
        "para kanino ang smart masipit",
        "who is smart masipit for",
        "what can residents do on this website",
    ],
    "census_requirements": [
        "anong impormasyon ang hinihingi sa resident registry",
        "ano ang kailangan para maitala bilang residente",
        "anong dokumento ang dadalhin para sa resident registration",
        "what details are needed for the resident registry",
    ],
    "census_registration": [
        "paano maitala sa resident registry",
        "hindi pa ako nakarehistro bilang residente",
        "kailangan ko bang maging residente bago gumawa ng account",
        "how do i get listed as a resident",
    ],
    "health_center_schedule": [
        "anong araw ang bakunahan sa health center",
        "kailan may check up sa barangay health center",
        "oras ng health center",
        "when is the vaccination schedule",
        "health center schedule today",
    ],
    "health_immunization_record": [
        "saan nakatala ang bakuna ng anak ko",
        "may kopya ba ng immunization record",
        "nakarecord ba ang mga bakuna ko",
        "where is my child's vaccination record kept",
    ],
}


def main():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = BASE / f"intents.before-system-align-{stamp}.json"
    backup.write_bytes(INTENTS.read_bytes())

    data = json.loads(INTENTS.read_text(encoding="utf-8-sig"))
    by_tag = {intent["tag"]: intent for intent in data["intents"]}

    for tag, item in NEW_INTENTS.items():
        if tag in by_tag:
            raise SystemExit(f"{tag} already exists; this script was already run.")
        entry = {"tag": tag, "patterns": item["patterns"], "responses": item["responses"]}
        data["intents"].append(entry)
        by_tag[tag] = entry

    for tag, (filipino, _english) in UPDATED_RESPONSES.items():
        by_tag[tag]["responses"] = [filipino]

    for text, source, target in MOVED_PATTERNS:
        by_tag[source]["patterns"].remove(text)
        by_tag[target]["patterns"].append(text)

    for tag, extra in EXTRA_PATTERNS.items():
        existing = {" ".join(p.lower().split()) for p in by_tag[tag]["patterns"]}
        by_tag[tag]["patterns"].extend(p for p in extra if " ".join(p.lower().split()) not in existing)

    text = json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\r\n") + "\r\n"
    INTENTS.write_bytes(text.encode("utf-8"))

    print(f"Backup: {backup.name}")
    print(f"Added {len(NEW_INTENTS)} topics, updated {len(UPDATED_RESPONSES)} answers, "
          f"added examples to {len(EXTRA_PATTERNS)} topics.")
    print("English answers and suggestion labels are in english_responses.py and suggestion_labels.py.")
    print("Next: python train.py, then python evaluate_assistant.py and python test_real_questions.py")


if __name__ == "__main__":
    main()
