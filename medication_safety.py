"""
Medication Safety Module
Handles drug-drug, drug-allergy, and drug-condition interaction checks.
"""

import os
from typing import List, Dict, Optional
from groq import Groq

class MedicationSafetyChecker:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None

    def check_interactions(self, new_meds: List[str], current_profile: Dict) -> Dict:
        """
        Check for potential interactions between new medications and the user's profile.
        
        Args:
            new_meds: List of newly prescribed or mentioned medications
            current_profile: User's health profile (allergies, conditions, current meds)
            
        Returns:
            Dict containing interaction warnings and status
        """
        if not new_meds:
            return {"status": "safe", "warnings": [], "details": "No new medications to check."}

        if not self.groq_client:
            return {
                "status": "warning", 
                "warnings": ["AI Interaction Check Unavailable"],
                "details": "Could not connect to medical safety engine. Please consult a pharmacist."
            }

        # Prepare context for LLM
        current_meds = current_profile.get('medications', [])
        allergies = current_profile.get('allergies', [])
        conditions = current_profile.get('conditions', [])

        prompt = f"""You are a medical safety assistant. Analyze the following new medications for potential risks:

New Medications: {', '.join(new_meds)}

User Profile:
- Current Medications: {', '.join(current_meds) if current_meds else 'None'}
- Allergies: {', '.join(allergies) if allergies else 'None'}
- Medical Conditions: {', '.join(conditions) if conditions else 'None'}

Please check for:
1. Drug-Drug interactions with current medications.
2. Drug-Allergy interactions.
3. Drug-Condition contraindications (reasons the user should NOT take these meds based on their health).

Return a JSON-formatted response with:
- "status": "safe", "caution", or "danger"
- "warnings": A list of short warning strings
- "details": A slightly more detailed explanation
"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a clinical safety system. Provide accurate interaction checks. Always prioritize safety. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            return {
                "status": "error",
                "warnings": [f"Safety check error: {str(e)}"],
                "details": "Technical error during safety analysis."
            }

_safety_checker_instance = None

def get_medication_safety_checker() -> MedicationSafetyChecker:
    global _safety_checker_instance
    if _safety_checker_instance is None:
        _safety_checker_instance = MedicationSafetyChecker()
    return _safety_checker_instance
