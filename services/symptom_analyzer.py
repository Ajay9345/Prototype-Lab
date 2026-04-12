from datetime import datetime
from typing import Dict, List, Optional, Tuple

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "can't breathe", "cannot breathe",
    "difficulty breathing", "severe bleeding", "uncontrolled bleeding",
    "unconscious", "seizure", "severe burn", "poisoning", "overdose",
    "severe head injury", "broken bone", "severe allergic reaction",
    "anaphylaxis", "choking", "severe abdominal pain", "coughing blood",
    "vomiting blood", "suicidal", "severe chest pressure",
]

HIGH_RISK_KEYWORDS = [
    "severe pain", "intense pain", "unbearable pain", "sharp pain",
    "sudden pain", "high fever", "persistent vomiting", "blood in stool",
    "blood in urine", "severe headache", "vision loss", "slurred speech",
    "numbness", "paralysis", "confusion", "disorientation", "fainting",
    "dizziness", "rapid heartbeat", "irregular heartbeat", "shortness of breath",
]

MEDIUM_RISK_KEYWORDS = [
    "fever", "cough", "sore throat", "body ache", "fatigue", "weakness",
    "nausea", "vomiting", "diarrhea", "abdominal pain", "headache",
    "muscle pain", "joint pain", "rash", "swelling", "persistent pain",
    "loss of appetite", "weight loss", "night sweats", "chills",
]

LOW_RISK_KEYWORDS = [
    "mild headache", "slight fever", "runny nose", "sneezing", "tired",
    "sleepy", "mild cough", "dry throat", "minor ache", "slight pain",
    "feeling unwell", "low energy", "mild discomfort",
]

SYMPTOM_INDICATORS = [
    "pain", "ache", "hurt", "feel", "symptom", "sick", "ill", "unwell",
    "fever", "cough", "bleeding", "swelling", "rash", "dizzy", "nausea",
    "vomit", "headache", "tired", "fatigue", "weak", "sore",
]

SYMPTOM_CATEGORIES: Dict[str, List[str]] = {
    "respiratory":      ["cough", "breathing", "breath", "chest", "lung", "throat", "wheeze"],
    "cardiovascular":   ["heart", "chest pain", "palpitation", "heartbeat", "blood pressure"],
    "gastrointestinal": ["stomach", "abdominal", "nausea", "vomit", "diarrhea", "constipation"],
    "neurological":     ["headache", "dizzy", "numbness", "seizure", "confusion", "memory"],
    "musculoskeletal":  ["joint", "muscle", "bone", "back pain", "neck pain", "arthritis"],
    "dermatological":   ["rash", "skin", "itch", "burn", "wound", "bruise"],
    "general":          ["fever", "fatigue", "weakness", "tired", "pain", "ache"],
}

FOLLOW_UP_QUESTIONS: Dict[str, List[str]] = {
    "high": [
        "How long have you been experiencing these symptoms?",
        "Are the symptoms getting worse?",
        "Have you taken any medication for this?",
    ],
    "medium": [
        "When did these symptoms start?",
        "Have you experienced this before?",
        "Are there any other symptoms you're experiencing?",
    ],
    "low": [
        "How long have you had these symptoms?",
        "Have you tried any home remedies?",
        "Is there anything that makes it better or worse?",
    ],
}

CATEGORY_QUESTIONS: Dict[str, str] = {
    "respiratory":      "Do you have any difficulty breathing or chest tightness?",
    "cardiovascular":   "Do you have any history of heart problems?",
    "gastrointestinal": "Have you noticed any changes in your diet recently?",
}

RECOMMENDATIONS: Dict[str, List[str]] = {
    "emergency": [
        "🚨 This appears to be a medical emergency. Call 108 immediately.",
        "Do not delay seeking emergency medical care.",
        "If possible, have someone stay with you until help arrives.",
    ],
    "high": [
        "⚠️ These symptoms require medical attention. Please consult a doctor soon.",
        "Consider visiting a nearby hospital or clinic within 24 hours.",
        "Monitor your symptoms closely and seek immediate care if they worsen.",
    ],
    "medium": [
        "📋 Schedule an appointment with your doctor if symptoms persist.",
        "Keep track of your symptoms and any changes.",
        "Rest and stay hydrated while monitoring your condition.",
    ],
    "low": [
        "💡 These symptoms are typically mild and may resolve on their own.",
        "Try rest, hydration, and over-the-counter remedies if appropriate.",
        "Consult a doctor if symptoms persist for more than a few days.",
    ],
}


class SymptomAnalyzer:
    def analyze_message(self, message: str, user_profile: Optional[Dict] = None) -> Dict:
        msg = message.lower()

        if not self._has_symptoms(msg):
            return {"has_symptoms": False, "risk_level": "none", "symptoms": [], "is_emergency": False}

        symptoms = self._extract_symptoms(msg)
        risk, is_emrg = self._assess_risk(msg, user_profile)
        category = self._categorize(msg)

        return {
            "has_symptoms":        True,
            "symptoms":            symptoms,
            "risk_level":          risk,
            "is_emergency":        is_emrg,
            "category":            category,
            "follow_up_questions": self._follow_up_questions(risk, category),
            "recommendations":     self._recommendations(risk, is_emrg),
            "timestamp":           datetime.now().isoformat(),
        }

    def check_emergency(self, message: str) -> bool:
        msg = message.lower()
        return any(kw in msg for kw in EMERGENCY_KEYWORDS)

    def _has_symptoms(self, message: str) -> bool:
        return any(ind in message for ind in SYMPTOM_INDICATORS)

    def _extract_symptoms(self, message: str) -> List[str]:
        all_keywords = EMERGENCY_KEYWORDS + HIGH_RISK_KEYWORDS + MEDIUM_RISK_KEYWORDS + LOW_RISK_KEYWORDS
        return list({kw for kw in all_keywords if kw in message})

    def _assess_risk(self, message: str, user_profile: Optional[Dict]) -> Tuple[str, bool]:
        if any(kw in message for kw in EMERGENCY_KEYWORDS):
            return ("high", True)

        if any(kw in message for kw in HIGH_RISK_KEYWORDS):
            if user_profile:
                age = user_profile.get("age") or 0
                conditions = user_profile.get("conditions", [])
                if age > 65 or conditions:
                    return ("high", True)
            return ("high", False)

        if any(kw in message for kw in MEDIUM_RISK_KEYWORDS):
            severity_mods = ["severe", "intense", "persistent", "chronic"]
            if any(mod in message for mod in severity_mods):
                return ("high", False)
            return ("medium", False)

        if any(kw in message for kw in LOW_RISK_KEYWORDS):
            return ("low", False)

        return ("low", False)

    def _categorize(self, message: str) -> str:
        for category, keywords in SYMPTOM_CATEGORIES.items():
            if any(kw in message for kw in keywords):
                return category
        return "general"

    def _follow_up_questions(self, risk_level: str, category: str) -> List[str]:
        questions = list(FOLLOW_UP_QUESTIONS.get(risk_level, FOLLOW_UP_QUESTIONS["low"]))
        if category in CATEGORY_QUESTIONS:
            questions.append(CATEGORY_QUESTIONS[category])
        return questions[:3]

    def _recommendations(self, risk_level: str, is_emergency: bool) -> List[str]:
        key = "emergency" if is_emergency else risk_level
        return RECOMMENDATIONS.get(key, RECOMMENDATIONS["low"])


_instance: Optional[SymptomAnalyzer] = None


def get_symptom_analyzer() -> SymptomAnalyzer:
    global _instance
    if _instance is None:
        _instance = SymptomAnalyzer()
    return _instance
