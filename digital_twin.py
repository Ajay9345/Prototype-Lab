"""
AI Health Digital Twin Module
Simulates predictive health outcomes based on lifestyle changes
and user-specific health profiles.
"""

import os
from typing import Dict, List, Optional
from groq import Groq

class HealthDigitalTwin:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None

    def simulate_outcome(self, user_profile: Dict, choice: str) -> Dict:
        """
        Simulate health outcomes for a hypothetical choice.
        """
        if not choice:
            return {"status": "error", "message": "No scenario provided for simulation."}

        if not self.groq_client:
             return {
                "status": "fallback",
                "simulation": "Prediction requires AI model. General advice: Quitting smoking improves heart health within weeks."
            }

        prompt = f"""You are a predictive health scientist. Generate a 'Digital Twin Simulation' for this user:

Scenario: {choice}

Current User Profile:
- Age: {user_profile.get('age', 'Unknown')}
- Conditions: {', '.join(user_profile.get('conditions', [])) or 'None'}
- Current Medications: {', '.join(user_profile.get('medications', [])) or 'None'}

Please provide a simulation prediction including:
1. "expected_physical_changes": List of metabolic/physiological changes (e.g. 'Reduced Heart Rate', 'Lowered LDL').
2. "timeline": A breakdown of changes at 1 week, 1 month, 6 months, and 1 year.
3. "risk_reduction": Specific percentages of lower risk for their conditions (if applicable).
4. "visual_preview_desc": A descriptive sentence of how their body would change.

Return valid JSON only.
"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a health simulation engine. Provide evidence-based predictions. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return {"status": "error", "message": f"Simulation failed: {str(e)}"}

_twin_instance = None

def get_digital_twin() -> HealthDigitalTwin:
    global _twin_instance
    if _twin_instance is None:
        _twin_instance = HealthDigitalTwin()
    return _twin_instance
