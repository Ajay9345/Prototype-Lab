"""
Virtual Clinical Triage Engine
Simulates a primary care provider's initial assessment to determine 
urgency and recommend appropriate care pathways.
"""

import os
from typing import Dict, List, Optional
from groq import Groq

class VirtualTriageEngine:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None

    def conduct_triage(self, symptom_analysis: Dict, user_profile: Dict) -> Dict:
        """
        Conduct a deep clinical triage based on initial symptom analysis.
        """
        if not symptom_analysis.get('has_symptoms'):
            return {"status": "no_symptoms", "message": "No specific symptoms to triage."}

        if not self.groq_client:
            return {
                "status": "fallback",
                "urgency": symptom_analysis.get('risk_level', 'low'),
                "message": "AI Triage engine offline. Follow standard symptom guidance."
            }

        symptoms = symptom_analysis.get('symptoms', [])
        history = user_profile.get('chat_history', [])[-3:] # Recent context

        prompt = f"""You are a senior clinical triage officer. A patient presents with: {', '.join(symptoms)}.

User Profile:
- Age: {user_profile.get('age', 'Unknown')}
- Conditions: {', '.join(user_profile.get('conditions', [])) or 'None'}

Initial Assessment: {symptom_analysis.get('risk_level', 'low')} risk.

Your Task:
1. "follow_up_questions": Provide 3-4 deep clinical questions a doctor would ask (e.g. about radiation of pain, duration, specific triggers).
2. "urgency_level": Red (Emergency), Orange (Priority - same day), Yellow (Routine - within 3 days), Green (Self-care).
3. "recommended_specialist": The most relevant type of doctor (e.g. Cardiologist, Dermatologist).
4. "rationale": Brief clinical reasoning for your decision.

Return valid JSON only.
"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a clinical decision support system. Be precise and safety-first. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return {"status": "error", "message": f"Triage failed: {str(e)}"}

_triage_instance = None

def get_triage_engine() -> VirtualTriageEngine:
    global _triage_instance
    if _triage_instance is None:
        _triage_instance = VirtualTriageEngine()
    return _triage_instance
