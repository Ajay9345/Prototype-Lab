import json
import os
from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional

TOPIC_KEYWORDS = {
    "Emergency":            ["emergency", "urgent", "severe", "chest pain", "can't breathe"],
    "Symptoms & Diagnosis": ["symptom", "pain", "ache", "fever", "cough", "sick", "ill", "unwell"],
    "Diet & Nutrition":     ["diet", "food", "eat", "nutrition", "meal"],
    "Exercise & Fitness":   ["exercise", "workout", "fitness", "gym", "run"],
    "Sleep & Rest":         ["sleep", "rest", "insomnia", "tired"],
    "Mental Health":        ["stress", "anxiety", "mental", "mood"],
    "Medications":          ["medicine", "medication", "drug", "prescription"],
}

DEFAULT_SETTINGS   = {"theme": "light", "notifications": True, "data_sharing": False}
DEFAULT_CHALLENGES = {"active": {}, "completed_history": [], "badges": [], "points": 0}
MAX_CHAT_HISTORY   = 100


class UserProfile:
    def __init__(
        self,
        age=None, conditions=None, allergies=None, medications=None, goals=None,
        chat_history=None, prescriptions=None, lab_reports=None,
        settings=None, challenges=None, preferred_language="en", gender="male",
    ):
        self.age                = age
        self.conditions         = conditions or []
        self.allergies          = allergies or []
        self.medications        = medications or []
        self.goals              = goals or []
        self.chat_history       = chat_history or []
        self.prescriptions      = prescriptions or []
        self.lab_reports        = lab_reports or []
        self.preferred_language = preferred_language
        self.gender             = gender

        if settings and "challenges" in settings:
            self.challenges = settings.pop("challenges")
        else:
            self.challenges = challenges or dict(DEFAULT_CHALLENGES)
        self.settings = settings or dict(DEFAULT_SETTINGS)

    def add_chat_interaction(self, message: str, response: str, topic: Optional[str] = None) -> None:
        self.chat_history.append({
            "timestamp": datetime.now().isoformat(),
            "message":   message,
            "response":  response,
            "topic":     topic or self._detect_topic(message),
        })
        if len(self.chat_history) > MAX_CHAT_HISTORY:
            self.chat_history = self.chat_history[-MAX_CHAT_HISTORY:]

    def clear_chat_history(self) -> None:
        self.chat_history = []

    def _detect_topic(self, message: str) -> str:
        msg = message.lower()
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(kw in msg for kw in keywords):
                return topic
        return "General Health"

    def add_prescription(self, prescription: Dict) -> None:
        self.prescriptions.append(prescription)

    def get_prescriptions(self) -> List[Dict]:
        return self.prescriptions

    def delete_prescription(self, prescription_id: str) -> bool:
        for i, rx in enumerate(self.prescriptions):
            if rx.get("id") == prescription_id:
                self.prescriptions.pop(i)
                return True
        return False

    def add_lab_report(self, lab_report: Dict) -> None:
        self.lab_reports.append(lab_report)

    def get_lab_reports(self) -> List[Dict]:
        return self.lab_reports

    def delete_lab_report(self, report_id: str) -> bool:
        for i, report in enumerate(self.lab_reports):
            if report.get("id") == report_id:
                self.lab_reports.pop(i)
                return True
        return False

    def get_statistics(self) -> Dict:
        topics = Counter(chat.get("topic", "General Health") for chat in self.chat_history)
        key_fields = [self.age, self.conditions, self.allergies, self.medications, self.goals]
        return {
            "total_conversations": len(self.chat_history),
            "topics":              dict(topics.most_common()),
            "recent_interactions": self.chat_history[-5:],
            "profile_completion":  int(sum(1 for f in key_fields if f) / len(key_fields) * 100),
            "health_profile": {
                "age":               self.age,
                "conditions_count":  len(self.conditions),
                "allergies_count":   len(self.allergies),
                "medications_count": len(self.medications),
                "goals_count":       len(self.goals),
            },
        }

    def to_dict(self) -> Dict:
        return {
            "age": self.age, "conditions": self.conditions, "allergies": self.allergies,
            "medications": self.medications, "goals": self.goals, "chat_history": self.chat_history,
            "prescriptions": self.prescriptions, "lab_reports": self.lab_reports,
            "settings": self.settings, "challenges": self.challenges,
            "preferred_language": self.preferred_language, "gender": self.gender,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "UserProfile":
        return cls(
            age=data.get("age"), conditions=data.get("conditions", []),
            allergies=data.get("allergies", []), medications=data.get("medications", []),
            goals=data.get("goals", []), chat_history=data.get("chat_history", []),
            prescriptions=data.get("prescriptions"), lab_reports=data.get("lab_reports"),
            preferred_language=data.get("preferred_language", "en"),
            gender=data.get("gender", "male"),
            settings=data.get("settings"), challenges=data.get("challenges"),
        )

    def to_context_string(self) -> str:
        if not any([self.age, self.conditions, self.allergies, self.medications, self.goals, self.prescriptions]):
            return ""

        lines = ["User Health Profile:"]
        if self.age:        lines.append(f"- Age: {self.age} years old")
        if self.conditions: lines.append(f"- Medical Conditions: {', '.join(self.conditions)}")
        if self.allergies:  lines.append(f"- Allergies: {', '.join(self.allergies)}")
        if self.medications:lines.append(f"- Current Medications: {', '.join(self.medications)}")
        if self.goals:      lines.append(f"- Health Goals: {', '.join(self.goals)}")

        if self.prescriptions:
            lines.append("\nPrescriptions on File:")
            for i, rx in enumerate(self.prescriptions, 1):
                lines.append(f"\nPrescription {i}:")
                if rx.get("doctor_name"): lines.append(f"  - Doctor: {rx['doctor_name']}")
                if rx.get("date"):        lines.append(f"  - Date: {rx['date']}")
                if rx.get("medications"): lines.append(f"  - Medications: {', '.join(rx['medications'][:5])}")

        return "\n".join(lines)


class ProfileManager:
    def __init__(self, storage_path: str = "user_profiles.json"):
        self.storage_path = storage_path
        self.profiles: Dict[str, UserProfile] = {}
        self._load_profiles()

    def _load_profiles(self) -> None:
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path) as f:
                self.profiles = {uid: UserProfile.from_dict(d) for uid, d in json.load(f).items()}
        except Exception as e:
            print(f"Error loading profiles: {e}")
            self.profiles = {}

    def save_profiles(self) -> None:
        try:
            with open(self.storage_path, "w") as f:
                json.dump({uid: p.to_dict() for uid, p in self.profiles.items()}, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def get_profile(self, user_id: str = "default") -> UserProfile:
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile()
        return self.profiles[user_id]

    def update_profile(self, profile_data: Dict, user_id: str = "default") -> UserProfile:
        self.profiles[user_id] = UserProfile.from_dict(profile_data)
        self.save_profiles()
        return self.profiles[user_id]
