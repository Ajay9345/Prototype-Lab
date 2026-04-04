"""
AI Insurance Concierge Module
Analyzes health insurance policy texts to verify coverage for 
specific treatments or diagnostics.
"""

import os
from typing import Dict, List, Optional
from groq import Groq

class InsuranceConcierge:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None

    def analyze_coverage(self, policy_text: str, diagnostic_or_treatment: str) -> Dict:
        """
        Check if a specific diagnostic/treatment is covered by the user's policy.
        """
        if not policy_text or not diagnostic_or_treatment:
            return {"status": "error", "message": "Policy text or treatment name missing."}

        if not self.groq_client:
            return {
                "status": "fallback",
                "coverage": "Unknown",
                "message": "AI Policy Auditor offline. Please check your policy document for 'Exclusions' and 'Benefits'."
            }

        prompt = f"""You are an insurance claim specialist. Audit the following policy text to see if '{diagnostic_or_treatment}' is covered.

Policy Context:
{policy_text[:4000]}

Please provide:
1. "is_covered": "Yes", "No", or "Partially".
2. "estimated_co_pay": A percentage or fixed amount mentioned in the policy (if any).
3. "limitations": List any specific conditions or waiting periods mentioned for this item.
4. "required_docs": List of documents needed for a claim (e.g., doctor's note, original bill).
5. "summary_logic": Brief explanation of where you found this in the policy.

Return valid JSON only.
"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a professional insurance policy document auditor. Be precise about coverage details, exclusions, and claim requirements. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            result["status"] = "success"
            return result
        except Exception as e:
            return {"status": "error", "message": f"Policy audit failed: {str(e)}"}

_concierge_instance = None

def get_insurance_concierge() -> InsuranceConcierge:
    global _concierge_instance
    if _concierge_instance is None:
        _concierge_instance = InsuranceConcierge()
    return _concierge_instance
