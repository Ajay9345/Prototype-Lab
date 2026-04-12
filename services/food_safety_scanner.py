import json
import os
import base64
from typing import Dict, Optional
from groq import Groq

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


class FoodSafetyScanner:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None
        self.fssai_context = self._load_fssai_guidelines()

    def audit_food_image(self, image_path: str, user_profile: Dict) -> Dict:
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image file not found."}
        if not self.groq_client:
            return {"status": "warning", "grade": "Unknown", "message": "AI Audit Engine unavailable. Check labels manually for allergens."}

        allergies  = ", ".join(user_profile.get("allergies", [])) or "None"
        conditions = ", ".join(user_profile.get("conditions", [])) or "None"

        prompt = (
            "You are an FSSAI-trained food safety auditor. Analyse the provided photo of an ingredient list.\n\n"
            f"User Profile:\n- Allergies: {allergies}\n- Conditions: {conditions}\n\n"
            f"FSSAI Reference:\n{self.fssai_context[:1000]}\n\n"
            'Return JSON with: "grade" (Green/Yellow/Red), "risks" (list), "fssai_violations" (list), "alternatives" (list), "summary" (2 sentences).'
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

    def _load_fssai_guidelines(self) -> str:
        try:
            with open("data/fssai_guidelines.txt") as f:
                return f.read()[:5000]
        except Exception:
            return "FSSAI guidelines not found."


_instance: Optional[FoodSafetyScanner] = None


def get_food_safety_scanner() -> FoodSafetyScanner:
    global _instance
    if _instance is None:
        _instance = FoodSafetyScanner()
    return _instance
