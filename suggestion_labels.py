"""
Short button labels shown when the chatbot is unsure.

Instead of only saying "Hindi ko pa matiyak", the chatbot offers the two
topics the model thinks are closest. Tapping one answers that topic directly.
Each intent has a Filipino and an English label.
"""

SUGGESTION_LABELS = {
    "greeting": ("Kumusta", "Hello"),
    "goodbye": ("Salamat", "Thank you"),
    "document_list": ("Anong dokumento ang pwedeng i-request?", "Which documents can I request?"),
    "document_clearance": ("Paano kumuha ng barangay clearance?", "How do I get a barangay clearance?"),
    "document_indigency": ("Paano kumuha ng certificate of indigency?", "How do I get a certificate of indigency?"),
    "document_request_process": ("Paano mag-request ng dokumento online?", "How do I request a document online?"),
    "document_status": ("Paano i-check ang status ng request ko?", "How do I check my request status?"),
    "payment_info": ("Paano magbayad ng dokumento?", "How do I pay for a document?"),
    "health_patient_record": ("Paano magkaroon ng health record?", "How do I get a health record?"),
    "health_consultation_history": ("Makikita ba ang consultation history ko?", "Can I see my consultation history?"),
    "health_immunization_record": ("Saan makikita ang immunization record?", "Where is the immunization record?"),
    "health_center_schedule": ("Anong oras bukas ang health center?", "When is the health center open?"),
    "health_privacy_access": ("Sino ang nakakakita ng health record ko?", "Who can see my health record?"),
    "health_no_advice": ("Nagbibigay ba ng medical advice ang chatbot?", "Does the chatbot give medical advice?"),
    "census_registration": ("Paano magparehistro sa resident census?", "How do I register in the resident census?"),
    "census_requirements": ("Anong impormasyon ang kailangan sa census?", "What information does the census need?"),
    "census_household_update": ("Paano magdagdag ng miyembro ng pamilya?", "How do I add a household member?"),
    "census_duplicate_check": ("May duplicate akong record", "I have a duplicate record"),
    "census_summary": ("Ilan ang residente sa Masipit?", "How many residents are in Masipit?"),
    "census_not_official": ("Ito ba ang opisyal na census (PSA)?", "Is this the official PSA census?"),
    "data_privacy": ("Ligtas ba ang personal data ko?", "Is my personal data safe?"),
    "account_access": ("Paano gumawa o mag-login sa account?", "How do I create or sign in to an account?"),
    "barangay_operating_hours": ("Anong oras bukas ang barangay hall?", "When is the barangay hall open?"),
    "account_identity_verification": ("Paano mag-submit ng valid ID at selfie?", "How do I submit my ID and selfie?"),
    "account_pending": ("Bakit pending pa ang account ko?", "Why is my account still pending?"),
    "account_password_reset": ("Nakalimutan ko ang password ko", "I forgot my password"),
    "document_walk_in": ("Pwede bang mag-request nang walk-in?", "Can I request as a walk-in?"),
    "document_pickup": ("Kailan at paano kukunin ang dokumento?", "When and how do I pick up my document?"),
    "document_additional_types": ("May iba pa bang certificate (residency, atbp.)?", "Are there other certificates (residency, etc.)?"),
    "health_maternal": ("May maternal o pregnancy records ba?", "Are there maternal or pregnancy records?"),
    "health_blood_pressure": ("Para saan ang Blood Pressure section?", "What is the Blood Pressure section for?"),
    "barangay_location": ("Saan ang barangay hall?", "Where is the barangay hall?"),
    "system_overview": ("Ano ang SMART MASIPIT?", "What is SMART MASIPIT?"),
    "chatbot_capabilities": ("Ano ang kaya mong gawin?", "What can you do?"),
    "document_qr_code": ("Saan makikita ang QR ng request ko?", "Where is my request QR code?"),
    "document_for_dependent": ("Paano mag-request para sa anak ko?", "How do I request for my child?"),
    "account_minimum_age": ("Ilang taon pwede gumawa ng account?", "What is the minimum age to register?"),
    "account_profile_settings": ("Paano palitan ang profile photo o password?", "How do I change my photo or password?"),
    "census_sitio": ("Anong sitio ang pipiliin ko?", "Which sitio should I choose?"),
}
