import json
import os
from typing import Dict, Optional
from groq import Groq

SIMULATION_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are a health simulation engine. "
    "Provide evidence-based predictions. Return valid JSON only."
)


class HealthDigitalTwin:
    """
    Simulates predictive health outcomes for 'What If' lifestyle scenarios.
    Example: "What if I quit smoking for 1 year?"
    """

    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    def simulate_outcome(self, user_profile: Dict, scenario: str) -> Dict:
        """
        Predict health outcomes for a given lifestyle scenario.

        Args:
            user_profile: User's health profile dict.
            scenario:     Description of the hypothetical change (e.g. "Stop smoking").

        Returns:
            Dict with expected_physical_changes, timeline, risk_reduction,
            visual_preview_desc.
        """
        if not scenario:
            return {"status": "error", "message": "No scenario provided for simulation."}

        if not self.groq_client:
            return {
                "status":     "fallback",
                "simulation": "Prediction requires AI model. General advice: Quitting smoking improves heart health within weeks.",
            }

        age        = user_profile.get("age", "Unknown")
        conditions = ", ".join(user_profile.get("conditions", [])) or "None"
        meds       = ", ".join(user_profile.get("medications", [])) or "None"

        prompt = (
            f"You are a predictive health scientist. Generate a Digital Twin Simulation.\n\n"
            f"Scenario: {scenario}\n\n"
            f"User Profile:\n- Age: {age}\n- Conditions: {conditions}\n- Medications: {meds}\n\n"
            "Provide:\n"
            '1. "expected_physical_changes": List of metabolic/physiological changes.\n'
            '2. "timeline": Changes at 1 week, 1 month, 6 months, 1 year.\n'
            '3. "risk_reduction": Percentage risk reduction for their conditions.\n'
            '4. "visual_preview_desc": One sentence describing the body change.\n\n'
            "Return valid JSON only."
        )

        try:
            response = self.groq_client.chat.completions.create(
                model=SIMULATION_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"status": "error", "message": f"Simulation failed: {e}"}


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[HealthDigitalTwin] = None


def get_digital_twin() -> HealthDigitalTwin:
    """Return the shared HealthDigitalTwin instance."""
    global _instance
    if _instance is None:
        _instance = HealthDigitalTwin()
    return _instance
