import base64
import json
import os
from typing import Dict, Optional
from groq import Groq

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


class SymptomCamAnalyzer:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    def analyze_symptom_image(self, image_path: str, symptoms_history: str = "") -> Dict:
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image file not found."}

        if not self.groq_client:
            return {
                "status":  "warning",
                "message": "Vision Analysis Engine offline. Please describe your symptoms in text.",
            }

        prompt = (
            "You are a specialised medical AI assistant. Analyse the provided symptom image "
            "(skin rash, eye redness, swelling, etc.) alongside the user's context.\n\n"
            f"USER CONTEXT: {symptoms_history}\n\n"
            "Return JSON with:\n"
            '- "analysis": Detailed visual description (colour, texture, shape, distribution).\n'
            '- "possible_indications": List of possible conditions.\n'
            '- "urgency": "Routine" / "Urgent" / "Emergency".\n'
            '- "recommendation": Specific actionable advice.\n\n'
            "DISCLAIMER: This is an AI assessment, not a professional medical diagnosis."
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
            data = json.loads(response.choices[0].message.content)
            return {
                "status":               "success",
                "analysis":             data.get("analysis", "No visual analysis available."),
                "possible_indications": data.get("possible_indications", []),
                "urgency":              data.get("urgency", "Routine"),
                "recommendation":       data.get("recommendation", "Please consult a doctor."),
            }
        except Exception as e:
            print(f"Vision analysis error: {e}")
            return {
                "status":         "error",
                "message":        f"Failed to analyse image: {e}",
                "recommendation": "Please describe your symptoms to the chatbot instead.",
            }


_instance: Optional[SymptomCamAnalyzer] = None


def get_symptom_cam_analyzer() -> SymptomCamAnalyzer:
    global _instance
    if _instance is None:
        _instance = SymptomCamAnalyzer()
    return _instance
