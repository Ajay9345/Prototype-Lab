import json
import os
import base64
from typing import Dict, Optional
from groq import Groq

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


class GroceryAuditor:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    def analyze_receipt_image(self, image_path: str, user_profile: Dict) -> Dict:
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image file not found."}

        if not self.groq_client:
            return {"status": "warning", "health_score": 60, "message": "AI Auditor unavailable. Buy more fresh fruits and vegetables."}

        conditions = ", ".join(user_profile.get("conditions", [])) or "None"
        goals = ", ".join(user_profile.get("goals", [])) or "None"

        prompt = (
            "You are a professional nutrition auditor. Analyse the provided grocery receipt photo.\n\n"
            f"User Profile:\n- Conditions: {conditions}\n- Goals: {goals}\n\n"
            'Return JSON with: "health_score" (0–100), '
            '"categorization" ({"Produce":[],"Processed":[],"Dairy":[],"Snacks":[],"Other":[]}), '
            '"red_flags" (list), "personalized_advice" (string), "swaps" (list of healthier alternatives).'
        )

        try:
            b64 = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
            response = self.groq_client.chat.completions.create(
                model=VISION_MODEL,
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ]}],
                response_format={"type": "json_object"},
            )
            result = json.loads(response.choices[0].message.content)
            result["status"] = "success"
            return result
        except Exception as e:
            return {"status": "error", "message": f"Audit failed: {e}"}


_instance: Optional[GroceryAuditor] = None


def get_grocery_auditor() -> GroceryAuditor:
    global _instance
    if _instance is None:
        _instance = GroceryAuditor()
    return _instance
