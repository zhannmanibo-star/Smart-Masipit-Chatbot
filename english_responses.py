# This file is independent of train.py.
# Keep these translations updated when system behavior changes.

ENGLISH_RESPONSES = {
    "greeting": (
        "Good day! I am the SMART MASIPIT Virtual Assistant. I can help with "
        "account registration and verification, document requests and pickup "
        "times, walk-in services, the resident registry, health records, "
        "events, announcements, and the barangay hall location. I give guidance "
        "on using the system; I cannot see personal records or actual request "
        "status."
    ),

    "goodbye": (
        "Thank you! You can ask again if you have other questions "
        "about SMART MASIPIT."
    ),

    "document_list": (
        "SMART MASIPIT supports Barangay Clearance, Certificate of "
        "Indigency, Certificate of Residency, Oath of Undertaking, "
        "First-Time Jobseeker Barangay Certification, Certificate of "
        "Closure, Certificate of Good Moral, and Barangay Occupancy "
        "Permit. Select the appropriate document in the request form. "
        "Each request is subject to verification and barangay review."
    ),

    "document_clearance": (
        "To request a Barangay Clearance, sign in using an approved "
        "resident account, open document requests, select Barangay "
        "Clearance, and complete the required fields. You may also "
        "ask authorized staff to encode a walk-in request at the "
        "barangay hall. Confirm the requirements and any applicable "
        "fees with the barangay office."
    ),

    "document_indigency": (
        "Select Certificate of Indigency in the document request form "
        "and provide your purpose. Authorized barangay personnel will "
        "review eligibility and supporting information before approval. "
        "Contact the barangay office to confirm the requirements "
        "and any applicable fees."
    ),

    "document_request_process": (
        "You may submit a request online using an approved resident "
        "account or ask staff to encode a walk-in request at the "
        "barangay hall. The request will be reviewed and approved "
        "or rejected. After approval, staff must prepare the document. "
        "Wait until its status is Ready for release and read the "
        "pickup instructions before visiting. Printing and release "
        "are handled at the barangay office."
    ),

    "document_status": (
        "Open My Document Requests to view your actual request status. "
        "Statuses include Submitted, Under review, Approved, Rejected, "
        "Ready for release, Released, and Closed — Not released. "
        "Approved means the request is approved for document "
        "preparation; it does not yet mean the document is ready "
        "for pickup. I cannot check your personal request status."
    ),

    "payment_info": (
        "SMART MASIPIT currently has no online payment feature. "
        "I cannot confirm the exact fee or exemption for each "
        "certificate. Contact the barangay office for applicable "
        "fees and payment instructions."
    ),

    "health_patient_record": (
        "Authorized health staff can register a patient even without "
        "an online resident account. Staff first look for an existing "
        "resident record. If none exists, they can add a resident "
        "and patient record through the health registration workflow "
        "after verifying the information. This does not automatically "
        "create an online account."
    ),

    "health_consultation_history": (
        "Authorized health staff record consultations and review "
        "consultation history. Corrections or clarifications are "
        "recorded as addendums to preserve the original entry. "
        "Contact health staff about your own records. "
        "The chatbot cannot read consultation records."
    ),

    "health_immunization_record": (
        "Authorized health staff record and review immunization "
        "records and their correction history. Contact the Barangay "
        "Health Center about your own or your child's records. "
        "Confirm schedules and what to bring with health staff."
    ),

    "health_center_schedule": (
        "I do not have a verified, real-time Barangay Health Center "
        "schedule. Contact health staff to confirm consultation, "
        "immunization, and maternal service schedules."
    ),

    "health_privacy_access": (
        "Clinical records are accessible only to authorized health "
        "personnel. A resident account or ordinary barangay account "
        "does not provide access to clinical records. "
        "The chatbot cannot read patient records either."
    ),

    "health_no_advice": (
        "This chatbot provides guidance on using SMART MASIPIT. "
        "It does not provide diagnoses, interpretations of clinical "
        "readings, prescriptions, or medication dosages. "
        "Contact a qualified health professional about your "
        "health concern."
    ),

    "census_registration": (
        "A resident registry record and an online account are "
        "different. Authorized staff can add a resident record "
        "even if the person has no online account. To access "
        "online resident services, create a resident account "
        "and complete barangay verification."
    ),

    "census_requirements": (
        "The resident registry records a person's name, birth date, "
        "sex, sitio, address, and contact number if available. "
        "Authorized staff verify the information. Contact the "
        "barangay office for the exact supporting documents required."
    ),

    "census_household_update": (
        "Authorized barangay staff manage household records, "
        "membership, and household head assignments. Contact staff "
        "to request a transfer or correction. Resident accounts "
        "do not have self-service household editing."
    ),

    "census_duplicate_check": (
        "Resident registration includes duplicate checking. "
        "When a possible match in name and birth date is found, "
        "staff must review the existing record. Do not create "
        "another record just to bypass a duplicate warning."
    ),

    "census_summary": (
        "Authorized barangay personnel can view demographic "
        "summaries based on saved resident records. Contact the "
        "barangay office for report inquiries. The chatbot cannot "
        "retrieve live census figures."
    ),

    "census_not_official": (
        "The SMART MASIPIT census module is based on Barangay "
        "Masipit's local resident registry. It does not replace "
        "the official national census."
    ),

    "data_privacy": (
        "SMART MASIPIT uses permissions based on account roles. "
        "The chatbot cannot read resident, identity-verification, "
        "or health records. Do not send passwords, reset links, "
        "ID photos, PhilHealth numbers, or medical details in chat."
    ),

    "account_access": (
        "Select Create resident account on the landing page or "
        "Create an account on the login page. Enter the required "
        "information and complete the identity verification "
        "submission. Your account remains pending until reviewed "
        "by the Barangay Secretary or Captain. If you forgot your "
        "password, use Forgot your password."
    ),

    "barangay_operating_hours": (
        "Contact the barangay office for confirmed office hours and the holiday "
        "schedule. The pickup times shown on your request follow the office "
        "days and hours set by the barangay. I cannot see real-time "
        "information."
    ),

    "out_of_scope": (
        "I am not sure how to answer that. I can help with using SMART MASIPIT: "
        "accounts, document requests and pickup, walk-in services, the resident "
        "registry, health modules, events, announcements, and the barangay "
        "location. Could you clarify your question?"
    ),

    "account_identity_verification": (
        "Use the identity verification form to capture the front "
        "and back of your valid ID and your selfie. Allow camera "
        "access in your browser. If access is blocked, check the "
        "site permissions, allow the camera, and reopen the "
        "capture step. If a photo is blurry, use Retake before "
        "submitting. The Secretary or Captain will review your "
        "submission. Submit photos through the verification form, "
        "not through this chatbot. "
        "In the selfie, hold your valid ID and follow the random "
        "instruction on screen, such as how many fingers to raise. "
        "It proves the person in the photo is you, not an old picture."
    ),

    "account_pending": (
        "The Secretary or Captain reviews resident accounts. "
        "Sign in to view Account Status and provide any missing "
        "verification evidence requested. Contact the barangay "
        "office for a follow-up. The chatbot cannot approve "
        "or view your application."
    ),

    "account_password_reset": (
        "On the login page, choose Forgot your password and enter your "
        "registered email. The system sends a 6-digit code to that email; check "
        "the Spam folder too. Enter the code and your new password (at least 12 "
        "characters, with letters and numbers). The code works for 15 minutes; "
        "you can ask for a new one after a minute, up to 5 codes a day. Never "
        "give the code or your password to the chatbot."
    ),

    "document_walk_in": (
        "You can make a walk-in document request with or without "
        "an online account. Authorized staff will verify your "
        "identity and look for your resident record. If you "
        "do not have one, you must first be registered as a "
        "resident before staff encode the document request. "
        "The request still requires review and approval."
    ),

    "document_pickup": (
        "Approved does not yet mean the document can be picked up; wait for "
        "Ready for release. When it is ready, a pickup notice appears on your "
        "request and is emailed to the eligible account. You can also choose a "
        "pickup time on the request page. At the barangay office, bring one "
        "valid ID and show the request's QR code or reference number (Show QR "
        "in My Document Requests). The chatbot cannot confirm the actual "
        "status."
    ),

    "document_additional_types": (
        "Select the appropriate certificate or permit in the "
        "document request form and complete the additional "
        "fields shown. For First-Time Jobseeker Certification, "
        "staff also review the signed oath and its reference. "
        "An unsigned draft is not a signed oath. Confirm "
        "eligibility and supporting requirements with the barangay."
    ),

    "health_maternal": (
        "The maternal records module is for authorized health "
        "staff. From a patient profile, staff can create a "
        "separate record for each pregnancy, record antepartum "
        "visits, and add correction notes. The printable maternal "
        "form is still a draft pending confirmation of the "
        "official template. Contact health staff for registration. "
        "The chatbot cannot view clinical details."
    ),

    "health_blood_pressure": (
        "Authorized health staff record blood pressure in the "
        "consultation form using separate systolic and diastolic "
        "fields in mmHg. When recording BP, enter both values. "
        "If it was not measured, leave both fields blank; "
        "do not invent a reading. Contact a health professional "
        "for interpretation of the result. The chatbot does "
        "not provide clinical interpretations."
    ),

    "barangay_location": (
        "On the SMART MASIPIT landing page, select Lokasyon. "
        "You will find a Google Maps view of Masipit Barangay "
        "Hall in Barangay Masipit, Calapan City, Oriental Mindoro. "
        "Select Get Directions to open Google Maps and enter "
        "your starting location."
    ),

    "system_overview": (
        "SMART MASIPIT is a web-based information system for Barangay Masipit. "
        "It covers the resident registry and household records, resident "
        "account registration and verification, document requests with pickup "
        "times and QR codes, health record management, announcements, and an "
        "events calendar. The health module includes consultations, blood "
        "pressure records, immunization, health history, and maternal records. "
        "Residents and authorized staff have different access according to "
        "their role."
    ),

    "chatbot_capabilities": (
        "I can guide you in using SMART MASIPIT: accounts and verification, "
        "document requests and pickup times, walk-in services, the resident "
        "registry, health modules, events, and announcements. I cannot see "
        "personal records or actual request status, and I do not submit, edit "
        "or approve records and requests. Use the matching page or contact "
        "authorized staff. Do not send passwords, codes, valid IDs, selfies or "
        "clinical records here."
    ),

    "document_qr_code": (
        "Every open document request has its own QR code. Open My "
        "Document Requests and select Show QR; you can also keep "
        "it with Save image. Show the QR at the barangay office "
        "and the staff will scan it to open your request right "
        "away. There is also a personal barangay QR on My "
        "profile. Still bring a valid ID when you pick up the "
        "document, and do not post your QR online."
    ),

    "document_for_dependent": (
        "A linked parent or guardian can request documents for a "
        "child under 18 who has no account of their own. Barangay "
        "staff link the parent or guardian to the child's record. "
        "Once linked, choose the child's name in Request a "
        "document. The request appears in your My Document "
        "Requests marked as being for the child. When the child "
        "turns 13, they may create their own account."
    ),

    "account_minimum_age": (
        "You must be at least 13 years old to create your own "
        "SMART MASIPIT account. For a younger child, a linked "
        "parent or guardian can request documents for them. If "
        "the child is already on the barangay records and "
        "registers at 13, the Secretary or Captain connects the "
        "new account to the existing record during verification."
    ),

    "account_profile_settings": (
        "Open My profile by selecting your avatar at the top "
        "right. It shows your resident information, household, "
        "and account details. You can upload a profile photo "
        "(JPG, PNG, or WebP, up to 4 MB) and change your password "
        "with Change password; the new password must be at least "
        "12 characters. Other resident details are updated by "
        "barangay staff. To sign out, open the same avatar menu "
        "and choose Sign out."
    ),

    "census_sitio": (
        "Barangay Masipit has seven sitios: Balaasan, Mataas na "
        "Kahoy (Road I), Centro, Irrigation Site, Masitao, "
        "Pulapog, and Road II. Choose the sitio where you "
        "currently live. If you moved to another sitio, contact "
        "barangay staff to update your record."
    ),
    "document_pickup_time": (
        "When the request is Ready for release, open it in My Document "
        "Requests. Under Pickup time, choose a date and time from the open "
        "slots and press Save pickup time. You can change it with Change pickup "
        "time or remove it with Remove my pickup time. Slots follow the office "
        "days and hours set by the barangay; each slot takes a limited number "
        "of people, and there are no slots on days the office is closed. If no "
        "time fits, contact the barangay office."
    ),
    "account_two_factor": (
        "Two-factor sign-in is required for SMART MASIPIT staff accounts; "
        "resident accounts sign in with a password only. Set it up in My "
        "profile under Two-factor sign-in: scan the QR code with an "
        "authenticator app (for example Google or Microsoft Authenticator), "
        "enter the code, and keep the recovery codes safe. When signing in, "
        "enter the 6-digit code from the app. Tick Remember this device for 30 "
        "days only on your own device; Forget all devices in My profile undoes "
        "it. If you lose your phone, use a recovery code; if you have none, "
        "contact the administrator. Never share codes or recovery codes with "
        "the chatbot."
    ),
    "app_install": (
        "You can install SMART MASIPIT on your phone or computer like an app; "
        "there is no separate app in the Play Store or App Store. In Chrome or "
        "Edge, press Install app (or I-install ang app on the landing page) "
        "when it appears, or open the browser menu and choose Install app or "
        "Add to Home screen. On iPhone, open it in Safari, press Share, and "
        "choose Add to Home Screen. Your account and features stay the same."
    ),
    "barangay_events": (
        "Upcoming public events of Barangay Masipit are on the landing page "
        "(Mga darating na event) and on the Events page. When signed in, open "
        "Calendar to see events month by month. Barangay officials post the "
        "events; some events are for staff only. The chatbot cannot see the "
        "list itself, so check the Events page or contact the barangay office."
    ),
    "barangay_announcements": (
        "Barangay notices are on the landing page (Mga abiso ng barangay) and "
        "on the Announcements page. They are grouped by category: General, "
        "Health, Event, Advisory and Emergency; pinned ones come first. The "
        "Barangay Secretary, Captain or administrator posts them. The chatbot "
        "does not read the notices themselves, so check the Announcements page."
    ),
    "aid_programs": (
        "Aid or relief distributions are recorded by authorized barangay staff "
        "for each household, based on the resident registry. There is no online "
        "application or aid list for resident accounts, and the chatbot cannot "
        "confirm whether you are included or whether aid is being given now. "
        "For schedules and eligibility, contact the barangay office or watch "
        "the Announcements. Do not send personal or household details in the "
        "chat."
    ),
}


ENGLISH_SPECIAL = {
    "not_understood": (
        "Sorry, I did not understand the message. Try asking a full "
        "question, for example: \"How do I get a barangay clearance?\" or "
        "\"How do I choose a pickup time?\""
    ),

    "fallback": (
        "I am not sure how to answer that. Could you clarify "
        "your question? I can help with using SMART MASIPIT. "
        "For fees, requirements, and schedules, contact the "
        "barangay office."
    ),

    "rule:system_overview": ENGLISH_RESPONSES["system_overview"],

    "rule:bp_feature_scope": (
        "I can explain how the Blood Pressure section works "
        "in SMART MASIPIT: authorized health staff use it to "
        "record systolic and diastolic readings in consultation "
        "records. For a general explanation of blood pressure "
        "or the meaning of your reading, ask a health professional."
    ),

    "rule:bp_interpretation": (
        "The chatbot does not interpret blood pressure readings "
        "or provide diagnoses or medication advice. Contact a "
        "health professional about the meaning of your reading. "
        "The SMART MASIPIT BP feature allows authorized health "
        "staff to record readings."
    ),

    "rule:unsupported_payment": (
        "This chatbot provides information about SMART MASIPIT "
        "barangay services. It does not process or confirm "
        "payments for tuition, utility bills, or a community "
        "tax certificate / cedula. Contact the relevant school, "
        "service provider, or office responsible for the payment."
    ),

    "rule:unconfirmed_dental_service": (
        "I do not have confirmed information about dental "
        "service availability or schedules. Contact the "
        "Barangay Health Center or City Health Office "
        "to confirm."
    ),

    "rule:garbage_schedule": (
        "Garbage collection schedules are not included in "
        "the chatbot's current information. Contact the "
        "barangay office for the correct schedule in your area."
    ),

    "rule:unconfirmed_residency_duration": (
        "I do not yet have a confirmed Barangay Masipit policy "
        "on the minimum length of residence required for "
        "resident verification or individual services. "
        "Contact the Barangay Secretary or Captain and specify "
        "whether you need resident registration or a particular "
        "certificate. I cannot confirm a number of months "
        "without a verified barangay policy."
    ),
}