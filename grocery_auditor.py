"""
Grocery Receipt Auditor Module
Analyzes supermarket receipts, provides a Basket Health Score, 
and suggests healthier FSSAI-approved alternatives.
"""

import os
from typing import Dict, List, Optional
from groq import Groq

class GroceryAuditor:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None

    def _encode_image(self, image_path: str) -> str:
        """Encode local image to base64 string."""
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_receipt_image(self, image_path: str, user_profile: Dict) -> Dict:
        """
        Analyze grocery receipt items from a photo and calculate a health score.
        """
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image file not found."}

        if not self.groq_client:
            return {
                "status": "warning",
                "health_score": 60,
                "message": "AI Auditor unavailable. Suggestion: Buy more fresh fruits and vegetables."
            }

        try:
            base64_image = self._encode_image(image_path)
            
            prompt = f"""You are a professional nutrition auditor. Analyze the provided photo of a grocery receipt:

User Health Profile:
- Conditions: {', '.join(user_profile.get('conditions', [])) or 'None'}
- Goals: {', '.join(user_profile.get('goals', [])) or 'None'}

Please provide a detailed assessment in the following JSON format:
{{
    "health_score": A number from 0-100 indicating the overall healthiness of the basket,
    "categorization": {{ "Produce": [], "Processed": [], "Dairy": [], "Snacks": [], "Other": [] }},
    "red_flags": ["List of unhealthy items"],
    "personalized_advice": "How this basket aligns with the user's specific goals/conditions.",
    "swaps": ["Suggested healthier FSSAI-approved alternatives for red-flag items"]
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

_auditor_instance = None

def get_grocery_auditor() -> GroceryAuditor:
    global _auditor_instance
    if _auditor_instance is None:
        _auditor_instance = GroceryAuditor()
    return _auditor_instance
