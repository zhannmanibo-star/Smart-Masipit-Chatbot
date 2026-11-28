"""
Answers for barangay staff (Secretary, Captain, barangay and health staff).

SMART MASIPIT sends audience="staff" when a staff account asks. For the
topics below, staff get these answers about their own pages; for every
other topic they get the usual answer. Only the answer changes, so the
model does not need retraining.

Each topic has a Filipino ("fil") and an English ("en") answer.
"""

STAFF_RESPONSES = {
    "document_qr_code": {
        "fil": (
            "Para mag-scan, buksan ang Scan QR sa menu at pindutin ang Start camera, tapos itapat sa QR "
            "sa phone o printout ng residente. Kung hindi mabasa, gamitin ang Type it instead para i-type "
            "ang code, o Scan from a photo para sa larawan ng QR. Ang QR ng request ay magbubukas ng mismong "
            "request; ang personal QR ay magpapakita ng resident record. Tingnan pa rin ang valid ID bago mag-release."
        ),
        "en": (
            "To scan, open Scan QR in the menu, press Start camera, and point it at the QR on the resident's "
            "phone or printout. If it cannot be read, use Type it instead to enter the code, or Scan from a "
            "photo for a picture of the QR. A request QR opens that request; a personal QR shows the resident "
            "record. Still check a valid ID before releasing."
        ),
    },
    "document_status": {
        "fil": (
            "Buksan ang Document Processing sa menu para makita ang lahat ng request ayon sa status: "
            "Submitted, Under review, Approved, Ready for release, Released, Rejected o Closed. "
            "Ang pulang bilang sa menu ay ang mga request na naghihintay ng review. "
            "Makikita sa ibaba ang bilang sa bawat status ngayon, kung mayroon."
        ),
        "en": (
            "Open Document Processing in the menu to see every request by status: Submitted, Under review, "
            "Approved, Ready for release, Released, Rejected or Closed. The red number in the menu shows "
            "requests waiting for review. The current count for each status is shown below, if there are any."
        ),
    },
    "document_request_process": {
        "fil": (
            "Sa Document Processing, buksan ang request at sundan ang mga hakbang: Start review, saka "
            "Approval decision (approve o reject na may dahilan), Prepare certificate, Mark ready for release, "
            "at Record actual release kapag nakuha na. Naitatala ang bawat hakbang sa Request history. "
            "Para sa residenteng pumunta sa barangay hall, gamitin ang walk-in request."
        ),
        "en": (
            "In Document Processing, open the request and follow the steps: Start review, then the Approval "
            "decision (approve, or reject with a reason), Prepare certificate, Mark ready for release, and "
            "Record actual release once it is picked up. Every step is saved in the Request history. "
            "For residents who come to the barangay hall, use a walk-in request."
        ),
    },
    "document_walk_in": {
        "fil": (
            "Sa Document Processing, piliin ang walk-in request. Hanapin ang resident record, tingnan ang "
            "valid ID ng residente, piliin ang dokumento at ilagay ang layunin. Pareho na itong dadaan sa "
            "review, approval at release gaya ng online request."
        ),
        "en": (
            "In Document Processing, choose walk-in request. Find the resident record, check the resident's "
            "valid ID, choose the document and enter the purpose. It then goes through review, approval and "
            "release like an online request."
        ),
    },
    "document_pickup": {
        "fil": (
            "Buksan ang Pickup schedule sa menu para makita kung sino ang kukuha at kailan. Pagdating ng "
            "residente, i-scan ang QR ng request o hanapin ito sa Document Processing, tingnan ang valid ID, "
            "saka pindutin ang Record actual release at ilagay kung sino ang tumanggap."
        ),
        "en": (
            "Open Pickup schedule in the menu to see who is coming and when. When the resident arrives, scan "
            "the request QR or find it in Document Processing, check a valid ID, then press Record actual "
            "release and enter who received it."
        ),
    },
    "document_pickup_time": {
        "fil": (
            "Sa Pickup schedule, buksan ang Pickup settings para itakda ang office days at hours, ang haba "
            "ng bawat slot, at ilan ang puwede bawat slot. Sa Closed dates, ilagay ang mga araw na sarado "
            "ang opisina (may dahilan). Sa What residents see, makikita ang mensaheng lalabas sa residente."
        ),
        "en": (
            "In Pickup schedule, open Pickup settings to set the office days and hours, the length of each "
            "slot, and how many people fit in a slot. Under Closed dates, add the days the office is closed "
            "(with a reason). What residents see shows the message residents will get."
        ),
    },
    "account_pending": {
        "fil": (
            "Buksan ang Account Approval sa menu. Sa bawat application, tingnan ang Identity evidence "
            "(harap at likod ng ID at selfie), hanapin o ikumpara sa Resident record, at i-approve kapag "
            "tugma. Kung hindi, i-reject na may malinaw na dahilan para alam ng residente ang aayusin. "
            "Secretary o Captain lamang ang puwedeng mag-approve."
        ),
        "en": (
            "Open Account Approval in the menu. For each application, check the Identity evidence (front and "
            "back of the ID and the selfie), find or compare the Resident record, and approve when they match. "
            "Otherwise reject it with a clear reason so the resident knows what to fix. "
            "Only the Secretary or Captain can approve."
        ),
    },
    "account_identity_verification": {
        "fil": (
            "Sa Account Approval, buksan ang application at tingnan ang Identity evidence: dapat malinaw ang "
            "harap at likod ng valid ID at tugma ang selfie sa larawan sa ID. Lagyan ng check ang identity "
            "confirmation bago mag-approve. Kung malabo, i-reject at sabihin sa dahilan kung ano ang ipapadala muli."
        ),
        "en": (
            "In Account Approval, open the application and check the Identity evidence: the front and back of "
            "the valid ID must be clear and the selfie must match the ID photo. Tick the identity confirmation "
            "before approving. If it is unclear, reject it and say in the reason what to send again."
        ),
    },
    "barangay_announcements": {
        "fil": (
            "Buksan ang Announcements sa menu para gumawa ng bagong abiso. Ilagay ang title, mensahe at "
            "category (hal. Health, Advisory, Emergency). Puwedeng i-pin para manatili sa itaas at maglagay "
            "ng expiry date para kusang mawala. Lalabas ito sa landing page at sa 🔔 ng mga residente."
        ),
        "en": (
            "Open Announcements in the menu to post a new notice. Enter the title, message and category "
            "(for example Health, Advisory, Emergency). You can pin it to keep it on top and set an expiry "
            "date so it disappears on its own. It shows on the landing page and in residents' 🔔."
        ),
    },
    "barangay_events": {
        "fil": (
            "Buksan ang Calendar sa menu at gumawa ng event: title, category, petsa at oras, at lugar. "
            "Piliin kung Public (makikita ng lahat) o para sa staff lamang. Lalabas ang public events sa "
            "landing page at sa kalendaryo ng mga residente."
        ),
        "en": (
            "Open Calendar in the menu and add an event: title, category, date and time, and place. "
            "Choose Public (everyone sees it) or staff only. Public events show on the landing page and "
            "in residents' calendar."
        ),
    },
    "census_household_update": {
        "fil": (
            "Buksan ang Households sa menu. Para gumawa ng bago, piliin ang head mula sa resident records, "
            "ang sitio at address. Sa household page, gamitin ang Manage members para magdagdag, maglipat o "
            "magtanggal ng member at ilagay ang relationship sa head. Naitatala ang bawat pagbabago sa History."
        ),
        "en": (
            "Open Households in the menu. To add one, choose the head from the resident records, the sitio and "
            "address. On the household page, use Manage members to add, move or remove members and set their "
            "relationship to the head. Every change is saved in History."
        ),
    },
    "census_registration": {
        "fil": (
            "Buksan ang Residents sa menu at piliin ang pagdagdag ng resident record. Ilagay ang pangalan, "
            "birth date, sex, sitio at address. Babalaan ka ng system kapag may posibleng kaparehong record "
            "(parehong pangalan at birth date) para hindi magdoble. Makikita ang buod sa Resident Census."
        ),
        "en": (
            "Open Residents in the menu and add a resident record. Enter the name, birth date, sex, sitio and "
            "address. The system warns you about a possible existing record (same name and birth date) so it "
            "is not entered twice. The summary is in Resident Census."
        ),
    },
    "aid_programs": {
        "fil": (
            "Buksan ang Ayuda tracker sa menu. Gumawa ng programa (pangalan, ayudang ibibigay at petsa), "
            "tapos itala ang bawat household na nakatanggap at kung sino ang tumanggap. Isang beses lang "
            "puwedeng mabigyan ang bawat household sa isang programa. Puwedeng i-undo na may dahilan, "
            "i-close ang programa kapag tapos na, at i-download ang listahan."
        ),
        "en": (
            "Open Ayuda tracker in the menu. Create a program (name, what is given and the date), then record "
            "each household that received it and who received it. A household can be recorded once per "
            "program. You can undo an entry with a reason, close the program when done, and download the list."
        ),
    },
}

# Which part of the system each staff answer is about. The staff answer is
# used only when SMART MASIPIT says the user can work in that part; others
# (for example health staff asking about document processing) get the
# usual answer.
STAFF_AREAS = {
    "document_qr_code": "documents",
    "document_status": "documents",
    "document_request_process": "documents",
    "document_walk_in": "documents",
    "document_pickup": "documents",
    "document_pickup_time": "pickup_settings",
    "account_pending": "verification",
    "account_identity_verification": "verification",
    "barangay_announcements": "announcements",
    "barangay_events": "events",
    "census_household_update": "households",
    "census_registration": "residents",
    "aid_programs": "households",
}

KNOWN_AREAS = frozenset(STAFF_AREAS.values())
