import json
import os
from typing import Dict, Optional
from groq import Groq

CONCIERGE_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "You are a professional insurance policy document auditor. "
    "Be precise about coverage details, exclusions, and claim requirements. "
    "Return valid JSON only."
)


class InsuranceConcierge:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    def analyze_coverage(self, policy_text: str, treatment: str) -> Dict:
        if not policy_text or not treatment:
            return {"status": "error", "message": "Policy text and treatment name are required."}

        if not self.groq_client:
            return {
                "status":   "fallback",
                "coverage": "Unknown",
                "message":  "AI Policy Auditor offline. Check your policy document for 'Exclusions' and 'Benefits'.",
            }

        prompt = (
            f"You are an insurance claim specialist. Audit the following policy to see if '{treatment}' is covered.\n\n"
            f"Policy Context:\n{policy_text[:4000]}\n\n"
            "Provide:\n"
            '1. "is_covered": "Yes" / "No" / "Partially".\n'
            '2. "estimated_co_pay": Percentage or fixed amount (if mentioned).\n'
            '3. "limitations": Specific conditions or waiting periods.\n'
            '4. "required_docs": Documents needed for a claim.\n'
            '5. "summary_logic": Where you found this in the policy.\n\n'
            "Return valid JSON only."
        )

        try:
            response = self.groq_client.chat.completions.create(
                model=CONCIERGE_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            result = json.loads(response.choices[0].message.content)
            for field in ("limitations", "required_docs"):
                if field in result and not isinstance(result[field], list):
                    result[field] = [result[field]] if result[field] else []
            result["status"] = "success"
            return result
        except Exception as e:
            return {"status": "error", "message": f"Policy audit failed: {e}"}


_instance: Optional[InsuranceConcierge] = None


def get_insurance_concierge() -> InsuranceConcierge:
    global _instance
    if _instance is None:
        _instance = InsuranceConcierge()
    return _instance
