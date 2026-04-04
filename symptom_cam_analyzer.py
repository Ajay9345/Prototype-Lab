"""
Symptom Cam Analyzer Module
Uses Vision-LLM to analyze photos of symptoms (skin, eyes, throat)
and provides visual health context.
"""

import os
import base64
from typing import Dict, Optional
from groq import Groq

class SymptomCamAnalyzer:
    def __init__(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None

    def _encode_image(self, image_path: str) -> str:
        """Encode local image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_symptom_image(self, image_path: str, symptoms_history: str = "") -> Dict:
        """
        Analyze a symptom image using Groq Vision capabilities.
        Uses meta-llama/llama-4-scout-17b-16e-instruct for multimodal analysis.
        """
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image file not found."}

        if not self.groq_client:
            return {
                "status": "warning",
                "message": "Vision Analysis Engine offline (missing API key). Please describe the symptoms in text."
            }

        try:
            base64_image = self._encode_image(image_path)
            
            prompt = f"""
            You are a specialized medical AI assistant. Analyze the provided image of a symptom (could be a skin rash, eye redness, swelling, etc.) alongside the user's provided context.
            
            USER CONTEXT: {symptoms_history}
            
            Provide a detailed assessment in the following JSON format:
            {{
                "analysis": "Detailed visual description of what you see in the image and how it relates to the context.",
                "possible_indications": ["Condition 1", "Condition 2"],
                "urgency": "Routine/Urgent/Emergency",
                "recommendation": "Specific actionable advice (e.g., 'Apply cold compress', 'See a dermatologist', 'Go to ER')."
            }}
            
            IMPORTANT: Focus on describing visual features like color, texture, shape, and distribution. 
            DISCLAIMER: Always include a note that this is an AI assessment and not a professional medical diagnosis.
            """

            response = self.groq_client.chat.completions.create(
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
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                response_format={"type": "json_object"}
            )

            import json
            analysis_data = json.loads(response.choices[0].message.content)
            
            return {
                "status": "success",
                "analysis": analysis_data.get("analysis", "No visual analysis available."),
                "possible_indications": analysis_data.get("possible_indications", []),
                "urgency": analysis_data.get("urgency", "Routine"),
                "recommendation": analysis_data.get("recommendation", "Please consult a doctor.")
            }

        except Exception as e:
            print(f"Vision Analysis Error: {e}")
            return {
                "status": "error",
                "message": f"Failed to analyze image: {str(e)}",
                "recommendation": "An error occurred during image analysis. Please describe your symptoms to the chatbot instead."
            }

_cam_analyzer_instance = None

def get_symptom_cam_analyzer() -> SymptomCamAnalyzer:
    global _cam_analyzer_instance
    if _cam_analyzer_instance is None:
        _cam_analyzer_instance = SymptomCamAnalyzer()
    return _cam_analyzer_instance
