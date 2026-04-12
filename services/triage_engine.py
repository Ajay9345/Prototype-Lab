import json
import os
from typing import Dict, Optional
from groq import Groq

TRIAGE_MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = "You are a clinical decision support system. Be precise and safety-first. Return valid JSON only."


class VirtualTriageEngine:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    def conduct_triage(self, symptom_analysis: Dict, user_profile: Dict) -> Dict:
        if not symptom_analysis.get("has_symptoms"):
            return {"status": "no_symptoms", "message": "No specific symptoms to triage."}
        if not self.groq_client:
            return {"status": "fallback", "urgency": symptom_analysis.get("risk_level", "low"), "message": "AI Triage engine offline. Follow standard symptom guidance."}

        symptoms   = ", ".join(symptom_analysis.get("symptoms", []))
        age        = user_profile.get("age", "Unknown")
        conditions = ", ".join(user_profile.get("conditions", [])) or "None"
        risk       = symptom_analysis.get("risk_level", "low")

        prompt = (
            f"You are a senior clinical triage officer. A patient presents with: {symptoms}.\n\n"
            f"User Profile:\n- Age: {age}\n- Conditions: {conditions}\nInitial Assessment: {risk} risk.\n\n"
            "Provide:\n"
            '1. "follow_up_questions": 3–4 deep clinical questions.\n'
            '2. "urgency_level": Red (Emergency) / Orange (Same day) / Yellow (Within 3 days) / Green (Self-care).\n'
            '3. "recommended_specialist": Most relevant doctor type.\n'
            '4. "rationale": Brief clinical reasoning.\n\nReturn valid JSON only.'
        )

        try:
            response = self.groq_client.chat.completions.create(
                model=TRIAGE_MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"status": "error", "message": f"Triage failed: {e}"}


_instance: Optional[VirtualTriageEngine] = None


def get_triage_engine() -> VirtualTriageEngine:
    global _instance
    if _instance is None:
        _instance = VirtualTriageEngine()
    return _instance
