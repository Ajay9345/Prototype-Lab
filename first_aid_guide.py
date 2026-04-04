"""
AR First Aid Guide Module
Provides step-by-step visual and text-based instructions for 
common medical emergencies, optimized for low-latency AR display.
"""

from typing import List, Dict

class ARFirstAidGuide:
    def __init__(self):
        self.guides = {
            "cpr": [
                {"step": 1, "text": "Check the scene for safety and the person for responsiveness.", "visual": "scene_safety_icon"},
                {"step": 2, "text": "Call 108 (Emergency) and get an AED if available.", "visual": "call_108_icon"},
                {"step": 3, "text": "Place the heel of one hand on the center of the chest.", "visual": "chest_center_overlay"},
                {"step": 4, "text": "Push hard and fast (100-120 compressions/min) with a depth of 2 inches.", "visual": "compression_depth_animation"},
                {"step": 5, "text": "Allow the chest to recoil completely between compressions.", "visual": "recoil_overlay"}
            ],
            "heimlich": [
                {"step": 1, "text": "Stand behind the person with one foot forward for balance.", "visual": "stance_overlay"},
                {"step": 2, "text": "Wrap your arms around their waist and tip them forward slightly.", "visual": "wrap_arms_icon"},
                {"step": 3, "text": "Make a fist with one hand and place it just above the navel.", "visual": "fist_placement_icon"},
                {"step": 4, "text": "Grasp your fist with your other hand and give 5 quick upward thrusts.", "visual": "upward_thrust_animation"}
            ],
            "bleeding": [
                {"step": 1, "text": "Apply direct pressure with a clean cloth or bandage.", "visual": "apply_pressure_icon"},
                {"step": 2, "text": "Maintain pressure until the bleeding stops.", "visual": "steady_pressure_overlay"},
                {"step": 3, "text": "Do not remove the bandage if it becomes soaked; add more on top.", "visual": "add_bandage_icon"},
                {"step": 4, "text": "Seek emergency medical help if the bleeding is severe or doesn't stop.", "visual": "emergency_icon"}
            ]
        }

    def get_step_by_step(self, emergency_type: str) -> List[Dict]:
        """
        Return the first aid steps for a given emergency type.
        """
        for key in self.guides:
            if key in emergency_type.lower():
                return self.guides[key]
        return [{"step": 0, "text": "No specific guide found for this emergency. Please follow general first aid protocols and call 108.", "visual": "general_warning"}]

_first_aid_instance = None

def get_first_aid_guide() -> ARFirstAidGuide:
    global _first_aid_instance
    if _first_aid_instance is None:
        _first_aid_instance = ARFirstAidGuide()
    return _first_aid_instance
