"""
FSSAI Food Safety Scanner Module
Audits food ingredient lists against FSSAI guidelines and user-specific 
health conditions/allergies.
"""

import os
from typing import Dict, List, Optional
from groq import Groq

class FoodSafetyScanner:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None
            
        self.fssai_context = self._load_fssai_context()

    def _load_fssai_context(self) -> str:
        """Load FSSAI guidelines for grounding the audit."""
        try:
            with open('data/fssai_guidelines.txt', 'r') as f:
                return f.read()[:5000] # Limit context for efficiency
        except:
            return "FSSAI guidelines not found."

    def _encode_image(self, image_path: str) -> str:
        """Encode local image to base64 string."""
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def audit_food_image(self, image_path: str, user_profile: Dict) -> Dict:
        """
        Analyze food ingredient labels from a photo and provide a personalized safety audit.
        """
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image file not found."}

        if not self.groq_client:
             return {
                "status": "warning",
                "grade": "Unknown",
                "message": "AI Audit Engine unavailable. Please check labels manually for allergens."
            }

        try:
            base64_image = self._encode_image(image_path)
            
            prompt = f"""You are an FSSAI-trained food safety auditor. Analyze the provided photo of an ingredient list for this specific user:

User Profile:
- Allergies: {', '.join(user_profile.get('allergies', [])) or 'None'}
- Conditions: {', '.join(user_profile.get('conditions', [])) or 'None'}

FSSAI Reference Context:
{self.fssai_context[:1000]}

Please provide a detailed assessment in the following JSON format:
{{
    "grade": "Green" (Safe), "Yellow" (Caution/Occasional), "Red" (Avoid),
    "risks": ["Specific ingredient risk 1", "Specific ingredient risk 2"],
    "fssai_violations": ["Violation 1 (e.g. high trans fats)", "Violation 2"],
    "alternatives": ["Healthier FSSAI-approved alternative 1", "Alternative 2"],
    "summary": "Short 2-sentence summary of the assessment."
}}

Return valid JSON only.
"""

            response = self.groq_client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            result["status"] = "success"
            return result
        except Exception as e:
            return {"status": "error", "message": f"Audit failed: {str(e)}"}

_scanner_instance = None

def get_food_safety_scanner() -> FoodSafetyScanner:
    global _scanner_instance
    if _scanner_instance is None:
        _scanner_instance = FoodSafetyScanner()
    return _scanner_instance
