from typing import Dict, List, Optional


# ── Step-by-step first aid guides ─────────────────────────────────────────────
GUIDES: Dict[str, List[Dict]] = {
    "cpr": [
        {"step": 1, "text": "Check the scene for safety and the person for responsiveness.",          "visual": "scene_safety_icon"},
        {"step": 2, "text": "Call 108 (Emergency) and get an AED if available.",                      "visual": "call_108_icon"},
        {"step": 3, "text": "Place the heel of one hand on the centre of the chest.",                 "visual": "chest_center_overlay"},
        {"step": 4, "text": "Push hard and fast (100–120 compressions/min) to a depth of 2 inches.", "visual": "compression_depth_animation"},
        {"step": 5, "text": "Allow the chest to recoil completely between compressions.",             "visual": "recoil_overlay"},
    ],
    "heimlich": [
        {"step": 1, "text": "Stand behind the person with one foot forward for balance.",             "visual": "stance_overlay"},
        {"step": 2, "text": "Wrap your arms around their waist and tip them forward slightly.",       "visual": "wrap_arms_icon"},
        {"step": 3, "text": "Make a fist and place it just above the navel.",                         "visual": "fist_placement_icon"},
        {"step": 4, "text": "Grasp your fist with your other hand and give 5 quick upward thrusts.", "visual": "upward_thrust_animation"},
    ],
    "bleeding": [
        {"step": 1, "text": "Apply direct pressure with a clean cloth or bandage.",                   "visual": "apply_pressure_icon"},
        {"step": 2, "text": "Maintain pressure until the bleeding stops.",                            "visual": "steady_pressure_overlay"},
        {"step": 3, "text": "Do not remove the bandage if soaked — add more on top.",                 "visual": "add_bandage_icon"},
        {"step": 4, "text": "Seek emergency help if bleeding is severe or does not stop.",            "visual": "emergency_icon"},
    ],
}

FALLBACK_STEP = [{
    "step":   0,
    "text":   "No specific guide found. Follow general first aid protocols and call 108.",
    "visual": "general_warning",
}]


class ARFirstAidGuide:
    """
    Provides step-by-step first aid instructions for common emergencies
    (CPR, Heimlich manoeuvre, bleeding control).
    """

    def get_step_by_step(self, emergency_type: str) -> List[Dict]:
        """
        Return the first aid steps for the given emergency type.

        Args:
            emergency_type: A string like "cpr", "heimlich", or "bleeding".
                            Partial matches are accepted (e.g. "cpr emergency").

        Returns:
            List of step dicts, each with 'step', 'text', and 'visual' keys.
        """
        etype = emergency_type.lower()
        for key, steps in GUIDES.items():
            if key in etype:
                return steps
        return FALLBACK_STEP


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[ARFirstAidGuide] = None


def get_first_aid_guide() -> ARFirstAidGuide:
    """Return the shared ARFirstAidGuide instance."""
    global _instance
    if _instance is None:
        _instance = ARFirstAidGuide()
    return _instance
