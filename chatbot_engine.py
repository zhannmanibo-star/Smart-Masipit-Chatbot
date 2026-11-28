import json
import re
from dataclasses import dataclass, replace
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent
THRESHOLD = 0.40
MAX_MESSAGE_LENGTH = 500

FALLBACK = (
    "Hindi ko pa matiyak ang sagot. Maaari bang linawin ang tanong? "
    "Makakatulong ako sa paggamit ng SMART MASIPIT. "
    "Para sa fees, requirements, at schedules, "
    "makipag-ugnayan sa barangay office."
)

SYSTEM_OVERVIEW = " ".join("""
Ang SMART MASIPIT ay isang web-based information system para sa Barangay
Masipit. Sakop nito ang resident registry at household records, resident account
registration at verification, document requests na may pickup time at QR code,
health record management, announcements, at events calendar. Kasama sa health
module ang consultations, blood pressure records, immunization, health history,
at maternal records. Magkakaiba ang access ng residents at authorized staff ayon
sa kanilang role.
""".split())

BP_FEATURE_SCOPE = (
    "Ang maipapaliwanag ko ay ang gamit ng Blood Pressure section "
    "sa SMART MASIPIT: dito nagtatala ang authorized health staff "
    "ng systolic at diastolic readings sa consultation record. "
    "Para sa pangkalahatang paliwanag tungkol sa blood pressure "
    "o kahulugan ng inyong reading, magtanong sa health professional."
)

MEDICAL_FALLBACK = (
    "Hindi nagbibigay ang chatbot ng interpretasyon ng blood pressure, "
    "diagnosis, o payo sa gamot. Para sa kahulugan ng inyong reading, "
    "makipag-ugnayan sa isang health professional. "
    "Ang BP feature ng SMART MASIPIT ay para sa pagtatala ng readings "
    "ng authorized health staff."
)

UNSUPPORTED_PAYMENT = (
    "Ang chatbot ay nagbibigay ng impormasyon tungkol sa "
    "SMART MASIPIT barangay services. Hindi nito pinoproseso o "
    "kinukumpirma ang pagbabayad ng tuition, utility bills, "
    "o community tax certificate / cedula. "
    "Makipag-ugnayan sa kaukulang paaralan, service provider, "
    "o tanggapang nangangasiwa sa bayarin."
)

DENTAL_FALLBACK = (
    "Wala akong kumpirmadong impormasyon tungkol sa availability "
    "o schedule ng dental services. Makipag-ugnayan sa Barangay "
    "Health Center o City Health Office para makumpirma."
)

GARBAGE_FALLBACK = (
    "Hindi kasama sa kasalukuyang impormasyon ng chatbot ang "
    "schedule ng koleksiyon ng basura. Makipag-ugnayan sa "
    "barangay office para sa tamang schedule sa inyong lugar."
)

RESIDENCY_FALLBACK = (
    "Wala pa akong kumpirmadong patakaran ng Barangay Masipit "
    "tungkol sa minimum na tagal ng paninirahan para sa resident "
    "verification o bawat serbisyo. Makipag-ugnayan sa Barangay "
    "Secretary o Captain at sabihin kung resident registration "
    "o anong certificate ang kailangan ninyo. Hindi ako "
    "makapagkukumpirma ng bilang ng buwan hangga't hindi ito "
    "verified ng barangay."
)


NOT_UNDERSTOOD = (
    "Pasensya na, hindi ko naintindihan ang mensahe. Subukang itanong "
    "nang buo, halimbawa: \"Paano kumuha ng barangay clearance?\" o "
    "\"Paano pumili ng pickup time?\""
)

# Common Taglish shortcuts and spellings, written out before the model reads
# a message (the same is done to the training questions in train.py).
SHORTCUTS = {
    "pano": "paano", "panu": "paano", "pnu": "paano", "pno": "paano", "paanu": "paano",
    "ung": "yung", "yng": "yung",
    "pde": "pwede", "pede": "pwede", "pwde": "pwede", "pwed": "pwede",
    "cert": "certificate", "certi": "certificate", "certs": "certificates",
    "brgy": "barangay", "bgy": "barangay", "brgay": "barangay",
    "acc": "account", "acct": "account", "accnt": "account",
    "docu": "document", "doc": "document", "docs": "documents",
    "pw": "password", "pword": "password", "passw": "password",
    "bkt": "bakit", "bat": "bakit",
    "san": "saan",
    "kelan": "kailan", "kylan": "kailan",
    "mgkano": "magkano", "mgkno": "magkano", "mkano": "magkano",
    "d2": "dito", "jan": "diyan", "dyan": "diyan",
    "ndi": "hindi", "hnd": "hindi", "di": "hindi",
    "kc": "kasi", "kse": "kasi",
    "lng": "lang", "nmn": "naman", "nman": "naman",
    "tlga": "talaga", "tlg": "talaga",
    "kpg": "kapag", "pag": "kapag",
    "pls": "please", "plz": "please",
    "u": "you", "ur": "your", "wat": "what", "hw": "how", "wer": "where", "wen": "when",
    "sched": "schedule", "bday": "birthday",
    "gud": "good", "eve": "evening", "morn": "morning",
    "thx": "thanks", "tnx": "thanks",
}


def normalize_text(message: str) -> str:
    """
    Lowercase, shorten stretched letters ("helloooo" -> "hello") and write
    out common shortcuts ("pano" -> "paano", "brgy" -> "barangay").
    """
    text = " ".join(str(message).casefold().split())
    text = re.sub(r"([a-z])\1{2,}", r"\1", text)
    return re.sub(r"[a-z0-9]+", lambda m: SHORTCUTS.get(m.group(0), m.group(0)), text)


# Words too common to show what a message is about.
COMMON_WORDS = {
    "ano", "anong", "ang", "ng", "sa", "po", "ba", "na", "ko", "mo", "ka",
    "ako", "you", "the", "is", "are", "to", "of", "in", "it", "my", "me",
    "what", "how", "yan", "yung", "ito", "pa", "lang", "naman", "din",
    "rin", "may", "mga", "and", "or", "for", "do", "can", "pano", "paano",
    "saan", "kailan", "bakit", "sino", "yes", "no", "ok", "oo", "hindi",
}


def build_vocabulary(texts) -> set[str]:
    """Words (3+ letters) used in in-scope training questions."""
    words = set()
    for text in texts:
        words.update(w for w in re.findall(r"[a-z0-9]+", normalize_text(text)) if len(w) >= 3)
    return words - COMMON_WORDS


def is_meaningful(message: str, vocabulary: set[str] | None) -> bool:
    """
    True when the message has at least one word the chatbot knows from its
    topics. Random letters ("gadgsgd") or unrelated words ("secret") get a
    "please ask again" reply instead of topic suggestions.
    """
    if not vocabulary:
        return True
    return any(word in vocabulary for word in re.findall(r"[a-z0-9]+", normalize_text(message)))


# Words that usually point back to the previous question.
FOLLOWUP_WORDS = {
    "naman", "yun", "yon", "yan", "ito", "iyon", "iyan", "dun", "doon",
    "diyan", "kung", "eh", "e", "edi", "tapos", "din", "rin",
    "then", "about", "also", "it", "that", "this", "there",
}


# A weaker combined topic is accepted only when the follow-up alone agrees.
CONTEXT_AGREE_MIN = 0.25
CONTEXT_ALONE_MIN = 0.15


def looks_like_followup(message: str) -> bool:
    """Short messages (up to 4 words), or up to 7 words with a word like "naman"/"kung"."""
    words = re.findall(r"[a-z0-9]+", normalize_text(message))

    if len(words) <= 4:
        return True

    return len(words) <= 7 and any(word in FOLLOWUP_WORDS for word in words)


# When the model is unsure, offer up to this many topics as buttons,
# but only topics with at least this probability.
MAX_SUGGESTIONS = 2
MIN_SUGGESTION_PROBABILITY = 0.10

# Short greetings and thanks are too short for the model to classify
# reliably, so a whole-message rule handles them. Measured on the
# training set: 34 matches, 0 wrong.
GREETING_RULE = re.compile(
    r"^(?:hi+|hello|helo|hey|good\s+(?:morning|afternoon|evening|day)|"
    r"magandang\s+(?:umaga|hapon|gabi|araw)|kumusta|kamusta|musta)"
    r"(?:\s+po)?(?:\s+(?:sa\s+inyo|smart\s+masipit|bot|assistant))?$"
)
GOODBYE_RULE = re.compile(
    r"^(?:bye|goodbye|paalam|salamat|maraming\s+salamat|thank\s+you|"
    r"thanks|ty|sige(?:\s+po)?|ok(?:ay)?(?:\s+po)?(?:\s+salamat)?|see\s+you)"
    r"(?:\s+po)?(?:\s+sa\s+tulong)?$"
)


@dataclass(frozen=True)
class ChatResult:
    reply: str
    intent: str
    confidence: float | None
    source: str
    # Intent tags to offer as "Ito ba ang ibig mong sabihin?" buttons.
    suggestions: tuple[str, ...] = ()
    # Language of the reply ("fil" or "en").
    lang: str = "fil"
    # Which answer this is (e.g. "intent:document_pickup" or
    # "rule:bp_interpretation", plus "|tag,tag" for suggestions), so the
    # same answer can be shown again in the other language.
    key: str = ""
    # Set only when the user asked for a language ("english please").
    chosen_lang: str | None = None


def smalltalk_response(message: str) -> ChatResult | None:
    text = message.casefold()
    text = re.sub(r"smart[\s-]+masipit", "smart masipit", text)
    text = " ".join(re.sub(r"[^\w\s]", " ", text).split())

    for pattern, intent in (
        (GREETING_RULE, "greeting"),
        (GOODBYE_RULE, "goodbye"),
    ):
        if pattern.match(text):
            return ChatResult(
                reply="",
                intent=intent,
                confidence=None,
                source="rule:smalltalk",
            )

    return None


def contains(pattern: str, text: str) -> bool:
    return re.search(pattern, text) is not None


def informational_response(message: str) -> ChatResult | None:
    text = " ".join(message.casefold().split())
    text = text.strip(" \t\r\n?!.,")
    text = re.sub(r"smart[\s-]+masipit", "smart masipit", text)

    overview_question = contains(
        r"\b(?:"
        r"what\s+is|what\s+does|tell\s+me\s+about|"
        r"ano\s+(?:po\s+)?(?:ang|yung)|"
        r"para\s+saan|tungkol\s+saan|"
        r"anong\s+(?:klaseng\s+)?(?:system|sistema)"
        r")\b",
        text,
    )

    specific_topic = contains(
        r"\b(?:"
        r"payment|bayad|fee|fees|"
        r"status|pending|rejected|"
        r"password|camera|selfie|"
        r"schedule|oras|"
        r"blood|bp|maternal|"
        r"requirements|requirement|"
        r"clearance|indigency|"
        r"registration|verification|"
        r"privacy|security"
        r")\b",
        text,
    )

    other_services_question = (
        contains(
            r"\b(?:"
            r"bukod|maliban|besides|apart\s+from|"
            r"other|else|iba|ibang"
            r")\b",
            text,
        )
        and contains(
            r"\b(?:"
            r"services?|serbisyo|"
            r"features?|modules?|"
            r"gawin|magagawa|pwedeng|puwedeng"
            r")\b",
            text,
        )
        and contains(
            r"\b(?:"
            r"smart masipit|documents?|request|system|sistema"
            r")\b",
            text,
        )
    )

    if (
        "smart masipit" in text
        and overview_question
        and not specific_topic
    ) or other_services_question:
        return ChatResult(
            reply=SYSTEM_OVERVIEW,
            intent="system_overview",
            confidence=None,
            source="rule:system_overview",
        )

    # Standalone definition questions only.
    # Personal reading questions continue to the medical rule.
    general_bp_question = re.fullmatch(
        r"(?:"
        r"what\s+is\s+(?:the\s+)?(?:meaning|definition)\s+of\s+"
        r"(?:blood\s+pressure|bp)"
        r"|what\s+is\s+(?:blood\s+pressure|bp)"
        r"|what\s+does\s+(?:bp|blood\s+pressure)\s+mean"
        r"|ano\s+(?:po\s+)?ang\s+"
        r"(?:(?:ibig\s+sabihin|kahulugan)\s+ng\s+)?"
        r"(?:blood\s+pressure|bp)"
        r")(?:\s+po)?",
        text,
    )

    if general_bp_question:
        return ChatResult(
            reply=BP_FEATURE_SCOPE,
            intent="health_blood_pressure",
            confidence=None,
            source="rule:bp_feature_scope",
        )

    residency_topic = contains(
        r"\b(?:"
        r"resident|residente|residency|paninirahan|naninirahan"
        r")\b",
        text,
    )

    duration_question = contains(
        r"\b(?:"
        r"ilang|gaano\s+katagal|"
        r"how\s+long|how\s+many|"
        r"months?|buwan|years?|taon|"
        r"minimum\s+(?:stay|duration|residency)"
        r")\b",
        text,
    )

    if residency_topic and duration_question:
        return ChatResult(
            reply=RESIDENCY_FALLBACK,
            intent="residency_policy_referral",
            confidence=None,
            source="rule:unconfirmed_residency_duration",
        )

    return None


def targeted_response(message: str) -> ChatResult | None:
    information = informational_response(message)

    if information is not None:
        return information

    text = " ".join(message.casefold().split())

    bp_topic = contains(
        r"\b(?:bp|blood\s+pressure|systolic|diastolic|presyon)\b",
        text,
    )

    clinical_question = contains(
        r"\b(?:"
        r"ibig\s+sabihin|kahulugan|interpret(?:ation)?|"
        r"mean(?:s|ing)?|normal|abnormal|"
        r"mataas|mababa|high|low|"
        r"delikado|dangerous|"
        r"gamot|gamutin|medicine|medication|"
        r"pababain|pataasin|"
        r"should\s+i\s+worry"
        r")\b",
        text,
    )

    if bp_topic and clinical_question:
        return ChatResult(
            reply=MEDICAL_FALLBACK,
            intent="health_no_advice",
            confidence=None,
            source="rule:bp_interpretation",
        )

    payment_question = contains(
        r"\b(?:"
        r"\w*bayad\w*|payment|pay|paying|"
        r"fee|fees|bill|bills|magkano|"
        r"cost|price|singil"
        r")\b",
        text,
    )

    unsupported_payment_topic = contains(
        r"\b(?:"
        r"tuition|kuryente|electricity|electric|"
        r"water|tubig|internet|"
        r"cedula|community\s+tax\s+certificate"
        r")\b",
        text,
    )

    if payment_question and unsupported_payment_topic:
        return ChatResult(
            reply=UNSUPPORTED_PAYMENT,
            intent="out_of_scope",
            confidence=None,
            source="rule:unsupported_payment",
        )

    if contains(
        r"\b(?:dentista|dentist|dental|dentistry)\b",
        text,
    ):
        return ChatResult(
            reply=DENTAL_FALLBACK,
            intent="out_of_scope",
            confidence=None,
            source="rule:unconfirmed_dental_service",
        )

    garbage_topic = contains(
        r"\b(?:basura|basurero|garbage|trash|waste)\b",
        text,
    )

    collection_question = contains(
        r"\b(?:"
        r"schedule|iskedyul|kailan|when|"
        r"collection|collect|pickup|pick\s*up|"
        r"hakot|hahakot|kinokolekta|koleksiyon|koleksyon"
        r")\b",
        text,
    )

    if garbage_topic and collection_question:
        return ChatResult(
            reply=GARBAGE_FALLBACK,
            intent="out_of_scope",
            confidence=None,
            source="rule:garbage_schedule",
        )

    return None


class BaseChatbotEngine:
    def __init__(self, base_dir: Path = BASE_DIR):
        self.model = joblib.load(
            base_dir / "intent_model.joblib"
        )

        with (base_dir / "responses.json").open(
            encoding="utf-8-sig"
        ) as file:
            self.responses = json.load(file)

        if not isinstance(self.responses, dict):
            raise RuntimeError(
                "responses.json must contain an object."
            )

        for label in self.model.classes_:
            answers = self.responses.get(str(label))

            if (
                not isinstance(answers, list)
                or not answers
                or any(
                    not isinstance(answer, str)
                    or not answer.strip()
                    for answer in answers
                )
            ):
                raise RuntimeError(
                    f"Missing or invalid responses for intent: {label}"
                )

        try:
            with (base_dir / "intents.json").open(encoding="utf-8-sig") as file:
                intents = json.load(file).get("intents", [])
            self.vocabulary = build_vocabulary(
                pattern
                for intent in intents
                if intent.get("tag") != "out_of_scope"
                for pattern in intent.get("patterns", [])
            )
        except (OSError, ValueError, AttributeError):
            self.vocabulary = None  # no check: suggestions as before

    def suggest(self, probabilities) -> tuple[str, ...]:
        """The closest in-scope topics, offered when the model is unsure."""
        order = probabilities.argsort()[::-1]
        picks = []

        for index in order:
            label = str(self.model.classes_[index])

            if label == "out_of_scope":
                continue

            if probabilities[index] < MIN_SUGGESTION_PROBABILITY:
                break

            picks.append(label)

            if len(picks) == MAX_SUGGESTIONS:
                break

        return tuple(picks)

    def answer_intent(self, intent: str, message: str = "") -> ChatResult:
        """Answers a topic the user picked from the suggestion buttons."""
        if (
            intent == "out_of_scope"
            or intent not in self.responses
            or intent not in set(map(str, self.model.classes_))
        ):
            raise ValueError("Unknown topic.")

        return ChatResult(
            reply=self.responses[intent][0],
            intent=intent,
            confidence=None,
            source="suggestion",
        )

    def get_response(self, message: str, context: str | None = None) -> ChatResult:
        """
        context: the user's previous question. A short follow-up such as
        "magkano naman" is read together with it when the follow-up alone
        is unclear.
        """
        if not isinstance(message, str):
            raise ValueError("Enter a text message.")

        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError(
                f"Use at most {MAX_MESSAGE_LENGTH} characters."
            )

        message = message.strip()

        if not message:
            raise ValueError("Enter a message.")

        smalltalk = smalltalk_response(message)

        if smalltalk is not None:
            return replace(
                smalltalk,
                reply=self.responses[smalltalk.intent][0],
            )

        rule_result = targeted_response(message)

        if rule_result is not None:
            return rule_result

        probabilities = self.model.predict_proba(
            [normalize_text(message)]
        )[0]

        best = int(probabilities.argmax())
        intent = str(self.model.classes_[best])
        confidence = float(probabilities[best])

        if confidence < THRESHOLD or intent == "out_of_scope":
            followup = self.context_answer(message, context)

            if followup is not None:
                return followup

        if (confidence < THRESHOLD or intent == "out_of_scope") and not is_meaningful(
            message, self.vocabulary
        ):
            return ChatResult(
                reply=NOT_UNDERSTOOD,
                intent="unknown",
                confidence=confidence,
                source="model:not_understood",
            )

        if confidence < THRESHOLD:
            return ChatResult(
                reply=FALLBACK,
                intent="unknown",
                confidence=confidence,
                source="model:fallback",
                suggestions=self.suggest(probabilities),
            )

        if intent == "out_of_scope":
            return ChatResult(
                reply=FALLBACK,
                intent=intent,
                confidence=confidence,
                source="model:out_of_scope",
                suggestions=self.suggest(probabilities),
            )

        return ChatResult(
            reply=self.responses[intent][0],
            intent=intent,
            confidence=confidence,
            source="model:answer",
        )

    def context_answer(self, message: str, context: str | None) -> ChatResult | None:
        """
        Read an unclear short follow-up together with the previous question.
        Used only when the follow-up has a word the chatbot knows and the
        combined text gives one confident topic.
        """
        if not isinstance(context, str) or not context.strip():
            return None

        if not looks_like_followup(message) or not is_meaningful(message, self.vocabulary):
            return None

        combined = normalize_text(context.strip()[:MAX_MESSAGE_LENGTH] + " " + message)
        probabilities = self.model.predict_proba([combined])[0]
        best = int(probabilities.argmax())
        intent = str(self.model.classes_[best])
        confidence = float(probabilities[best])

        if confidence < THRESHOLD or intent == "out_of_scope":
            # Still accept a weaker topic when the follow-up alone already
            # leaned the same way ("magkano naman" -> payments).
            topics = [str(tag) for tag in self.model.classes_]
            alone = self.model.predict_proba([normalize_text(message)])[0].copy()
            together = probabilities.copy()

            if "out_of_scope" in topics:
                alone[topics.index("out_of_scope")] = 0
                together[topics.index("out_of_scope")] = 0

            best = int(together.argmax())

            if not (
                int(alone.argmax()) == best
                and together[best] >= CONTEXT_AGREE_MIN
                and alone[best] >= CONTEXT_ALONE_MIN
            ):
                return None

            intent = topics[best]
            confidence = float(together[best])

        return ChatResult(
            reply=self.responses[intent][0],
            intent=intent,
            confidence=confidence,
            source="model:context",
        )

from english_responses import ENGLISH_RESPONSES, ENGLISH_SPECIAL


FILIPINO_MARKERS = {
    "ako", "akin", "aking", "ang", "ano", "anong",
    "ba", "bakit", "bago", "bukod", "din", "dito",
    "doon", "gaano", "gawin", "gusto", "hindi",
    "ilang", "inyong", "ito", "iyan", "iyon",
    "kailan", "kailangan", "kami", "kapag", "kayo",
    "ko", "kung", "lang", "mga", "mo", "na",
    "naman", "namin", "natin", "ng", "ninyo",
    "nyo", "nung", "opo", "pa", "paano", "pano",
    "pakisabi", "po", "puwede", "pwede", "rin",
    "sa", "saan", "sakin", "salamat", "sila",
    "sino", "tayo", "wala", "walang", "yung",
    "magkano", "kumuha", "makakuha", "magrequest",
    "magregister", "magbayad", "magpa", "mag",
    "pag", "pagkuha", "pagrequest", "pagregister",
    "pagbayad", "ni", "si",
}

ENGLISH_MARKERS = {
    "a", "an", "the", "what", "when", "where", "why",
    "how", "who", "which", "can", "could", "would",
    "should", "do", "does", "did", "is", "are",
    "am", "was", "were", "i", "my", "me", "you",
    "your", "we", "our", "they", "their", "it",
    "its", "this", "that", "these", "those",
    "please", "tell", "explain", "about", "for",
    "with", "without", "have", "has", "need",
    "want", "get", "find", "check", "show",
    "hello", "hi", "hey", "thanks", "thank",
    "goodbye", "bye", "help",
}


def detect_reply_language(message: str) -> str:
    """
    A lightweight heuristic, not a trained language detector.

    Filipino markers take priority for Taglish.
    Ambiguous short messages default to Filipino.
    """
    tokens = set(
        re.findall(r"[a-z]+", message.casefold())
    )

    if tokens & FILIPINO_MARKERS:
        return "fil"

    if tokens & ENGLISH_MARKERS:
        return "en"

    return "fil"


# Filipino text of each rule reply, by source (English is in english_responses.py).
RULE_REPLIES = {
    "rule:system_overview": SYSTEM_OVERVIEW,
    "rule:bp_feature_scope": BP_FEATURE_SCOPE,
    "rule:bp_interpretation": MEDICAL_FALLBACK,
    "rule:unsupported_payment": UNSUPPORTED_PAYMENT,
    "rule:unconfirmed_dental_service": DENTAL_FALLBACK,
    "rule:garbage_schedule": GARBAGE_FALLBACK,
    "rule:unconfirmed_residency_duration": RESIDENCY_FALLBACK,
}

SWITCH_REPLY = {
    "en": "Sure, I will answer in English. What would you like to ask?",
    "fil": "Sige po, sasagot ako sa Tagalog. Ano po ang inyong tanong?",
}

# "english please", "pa-english po", "can you say that in english",
# "tagalog po", "pakitagalog", "translate to filipino": the whole message
# must be such a request, so questions like "may english version ba ang
# certificate?" are still answered normally.
LANGUAGE_WORDS = {
    "en": {"english", "eng", "ingles", "inglis"},
    "fil": {"tagalog", "filipino", "pilipino", "tagalug"},
}
REQUEST_FILLER = {
    "please", "pls", "plz", "po", "nga", "naman", "lang", "can", "could",
    "you", "pa", "paki", "pwede", "puwede", "mo", "ba", "in", "to", "into",
    "sa", "ng", "say", "that", "it", "this", "again", "ulit", "translate",
    "isalin", "itranslate", "i", "version", "speak", "explain", "sagot",
    "sagutin", "use", "the", "gamitin", "ang", "na", "yan", "iyan", "ito",
    "ko", "me", "reply", "answer", "mode", "language", "wika", "salita",
    "only", "now", "na", "ngayon", "talk", "write", "lagay",
}
PREVIOUS_KEY = re.compile(
    r"^(?:intent:[a-z_]{1,60}|rule:[a-z_]{1,60}|fallback|not_understood)"
    r"(?:\|[a-z_]{1,60}(?:,[a-z_]{1,60}){0,2})?$"
)


def language_request(message: str) -> str | None:
    """'en' or 'fil' when the whole message asks for that language."""
    text = message.casefold().replace("-", " ")
    if re.search(r"\b(?:don\'?t|dont|do\s+not|cannot|can\'?t|cant)\s+understand\s+(?:tagalog|filipino)\b", text):
        return "en"
    if re.search(r"\b(?:don\'?t|dont|do\s+not|cannot|can\'?t|cant)\s+understand\s+english\b", text) or re.search(
        r"\b(?:hindi|di)\s+ko\s+(?:maintindihan|naiintindihan|gets)\s+(?:ang\s+)?english\b", text
    ):
        return "fil"

    names = set().union(*LANGUAGE_WORDS.values())
    words = []
    for word in re.findall(r"[a-z]+", text):
        # "pakitagalog", "paenglish", "itagalog" -> "tagalog", "english"
        for prefix in ("paki", "pa", "i"):
            if word.startswith(prefix) and word[len(prefix):] in names:
                word = word[len(prefix):]
                break
        words.append(word)

    if not words or len(words) > 8:
        return None

    for lang, names in LANGUAGE_WORDS.items():
        if any(word in names for word in words) and all(
            word in names or word in REQUEST_FILLER for word in words
        ):
            return lang

    return None


class ChatbotEngine(BaseChatbotEngine):
    def __init__(self, base_dir: Path = BASE_DIR):
        super().__init__(base_dir)

        missing = [
            str(label)
            for label in self.model.classes_
            if (
                not isinstance(
                    ENGLISH_RESPONSES.get(str(label)),
                    str,
                )
                or not ENGLISH_RESPONSES[str(label)].strip()
            )
        ]

        if missing:
            raise RuntimeError(
                "Missing English responses for intents: "
                + ", ".join(missing)
                + ". Add their translations to english_responses.py."
            )

        required_special = {"fallback", "not_understood", *RULE_REPLIES}

        for key in required_special:
            value = ENGLISH_SPECIAL.get(key)

            if not isinstance(value, str) or not value.strip():
                raise RuntimeError(
                    f"Missing English special response: {key}"
                )

    @staticmethod
    def answer_key(result: ChatResult) -> str:
        if result.source in {"model:fallback", "model:out_of_scope"}:
            key = "fallback"
        elif result.source == "model:not_understood":
            key = "not_understood"
        elif result.source.startswith("rule:") and result.source != "rule:smalltalk":
            key = result.source
        else:
            key = "intent:" + result.intent

        if result.suggestions:
            key += "|" + ",".join(result.suggestions)

        return key

    def render(self, key: str, lang: str) -> str:
        """The reply for an answer key, in Filipino ("fil") or English ("en")."""
        main = key.split("|", 1)[0]

        if main.startswith("intent:"):
            intent = main[len("intent:"):]
            if intent not in self.responses:
                raise ValueError("Unknown topic.")
            return ENGLISH_RESPONSES[intent] if lang == "en" else self.responses[intent][0]

        if main in RULE_REPLIES:
            return ENGLISH_SPECIAL[main] if lang == "en" else RULE_REPLIES[main]

        if main == "fallback":
            return ENGLISH_SPECIAL["fallback"] if lang == "en" else FALLBACK

        if main == "not_understood":
            return ENGLISH_SPECIAL["not_understood"] if lang == "en" else NOT_UNDERSTOOD

        raise ValueError("Unknown answer.")

    def get_response(
        self,
        message: str,
        lang: str | None = None,
        previous: str | None = None,
        context: str | None = None,
    ) -> ChatResult:
        """
        lang: the language the user chose earlier ("fil" or "en"); when not
        given, the reply follows the language of the message.
        previous: the answer key of the last reply, so "english please"
        can show that same answer in English.
        context: the user's previous question, for short follow-ups.
        """
        if isinstance(message, str) and message.strip():
            wanted = language_request(message.strip()[:MAX_MESSAGE_LENGTH])

            if wanted is not None:
                if previous and PREVIOUS_KEY.match(previous):
                    main, _, tags = previous.partition("|")
                    suggestions = tuple(t for t in tags.split(",") if t in self.responses) if tags else ()
                    try:
                        reply = self.render(main, wanted)
                    except ValueError:
                        reply = None

                    if reply is not None:
                        return ChatResult(
                            reply=reply,
                            intent=main[len("intent:"):] if main.startswith("intent:") else main,
                            confidence=None,
                            source="rule:language_switch",
                            suggestions=suggestions,
                            lang=wanted,
                            key=previous,
                            chosen_lang=wanted,
                        )

                return ChatResult(
                    reply=SWITCH_REPLY[wanted],
                    intent="language_switch",
                    confidence=None,
                    source="rule:language_switch",
                    lang=wanted,
                    chosen_lang=wanted,
                )

        # Run existing validation, rules, and model selection first.
        result = super().get_response(message, context=context)
        language = lang if lang in {"fil", "en"} else detect_reply_language(message)
        key = self.answer_key(result)

        return replace(result, reply=self.render(key, language), lang=language, key=key)

    def answer_intent(self, intent: str, message: str = "", lang: str | None = None) -> ChatResult:
        result = super().answer_intent(intent, message)
        language = lang if lang in {"fil", "en"} else detect_reply_language(message)
        key = "intent:" + intent

        return replace(result, reply=self.render(key, language), lang=language, key=key)
