import json
import os
from typing import Dict, List, Optional
from groq import Groq

SAFETY_MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = "You are a clinical safety system. Provide accurate interaction checks. Always prioritise safety. Return valid JSON only."


class MedicationSafetyChecker:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    def check_interactions(self, new_meds: List[str], current_profile: Dict) -> Dict:
        if not new_meds:
            return {"status": "safe", "warnings": [], "details": "No new medications to check."}
        if not self.groq_client:
            return {"status": "warning", "warnings": ["AI Interaction Check Unavailable"], "details": "Could not connect to medical safety engine. Please consult a pharmacist."}

        current_meds = current_profile.get("medications", [])
        allergies    = current_profile.get("allergies", [])
        conditions   = current_profile.get("conditions", [])

        prompt = (
            f"You are a medical safety assistant. Analyse the following new medications for potential risks:\n\n"
            f"New Medications: {', '.join(new_meds)}\n\nUser Profile:\n"
            f"- Current Medications: {', '.join(current_meds) or 'None'}\n"
            f"- Allergies: {', '.join(allergies) or 'None'}\n"
            f"- Medical Conditions: {', '.join(conditions) or 'None'}\n\n"
            "Check for:\n1. Drug-Drug interactions.\n2. Drug-Allergy interactions.\n3. Drug-Condition contraindications.\n\n"
            'Return JSON with: "status" ("safe"/"caution"/"danger"), "warnings" (list), "details" (explanation).'
        )

        try:
            response = self.groq_client.chat.completions.create(
                model=SAFETY_MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"status": "error", "warnings": [f"Safety check error: {e}"], "details": "Technical error during safety analysis."}


_instance: Optional[MedicationSafetyChecker] = None


def get_medication_safety_checker() -> MedicationSafetyChecker:
    global _instance
    if _instance is None:
        _instance = MedicationSafetyChecker()
    return _instance
