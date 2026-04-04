import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ChallengesManager:
    def __init__(self):
        # Static definition of available challenges
        self.challenges_catalog = {
            "hydration_7_day": {
                "id": "hydration_7_day",
                "name": "7-Day Hydration",
                "description": "Drink 8 glasses of water every day for a week.",
                "duration_days": 7,
                "category": "hydration",
                "icon": "💧",
                "points_per_day": 10,
                "completion_bonus": 100,
                "badge_id": "hydration_master"
            },
            "steps_10k_streak": {
                "id": "steps_10k_streak",
                "name": "10k Steps Streak",
                "description": "Walk 10,000 steps daily to keep your heart healthy.",
                "duration_days": 30,
                "category": "activity",
                "icon": "👣",
                "points_per_day": 15,
                "completion_bonus": 300,
                "badge_id": "step_champion"
            },
            "sugar_control": {
                "id": "sugar_control",
                "name": "Sugar Control",
                "description": "Avoid added sugars and sweets for 14 days.",
                "duration_days": 14,
                "category": "nutrition",
                "icon": "🥗",
                "points_per_day": 20,
                "completion_bonus": 200,
                "badge_id": "sugar_slayer"
            },
            "yoga_streak": {
                "id": "yoga_streak",
                "name": "Yoga Streak",
                "description": "Practice yoga for at least 20 minutes daily.",
                "duration_days": 21,
                "category": "mindfulness",
                "icon": "🧘",
                "points_per_day": 15,
                "completion_bonus": 250,
                "badge_id": "zen_master"
            },
            "sleep_improvement": {
                "id": "sleep_improvement",
                "name": "Sleep Improvement",
                "description": "Get at least 7 hours of quality sleep every night.",
                "duration_days": 7,
                "category": "sleep",
                "icon": "😴",
                "points_per_day": 10,
                "completion_bonus": 100,
                "badge_id": "sleep_guru"
            }
        }

        self.badges_catalog = {
            "hydration_master": {"name": "Hydration Master", "icon": "💧", "description": "Completed the 7-Day Hydration Challenge"},
            "step_champion": {"name": "Step Champion", "icon": "👟", "description": "Walked 10k steps for 30 days"},
            "sugar_slayer": {"name": "Sugar Slayer", "icon": "🍬", "description": "Controlled sugar intake for 14 days"},
            "zen_master": {"name": "Zen Master", "icon": "🧘", "description": "Completed 21 days of Yoga"},
            "sleep_guru": {"name": "Sleep Guru", "icon": "🌙", "description": "Achieved 7 days of good sleep"}
        }

    def get_all_challenges(self) -> List[Dict]:
        """Return list of all available challenges"""
        return list(self.challenges_catalog.values())

    def get_challenge_details(self, challenge_id: str) -> Optional[Dict]:
        """Get details for a specific challenge"""
        return self.challenges_catalog.get(challenge_id)

    def join_challenge(self, user_profile, challenge_id: str) -> Dict:
        """
        Add a challenge to user's active challenges.
        Returns updated challenge status or error.
        """
        if challenge_id not in self.challenges_catalog:
            return {"success": False, "error": "Challenge not found"}

        if challenge_id in user_profile.challenges.get("active", {}):
            return {"success": False, "error": "Already participating in this challenge"}

        # Initialize challenge progress
        challenge_data = {
            "id": challenge_id,
            "started_at": datetime.now().isoformat(),
            "days_completed": 0,
            "last_log_date": None,
            "history": [] # List of dates when progress was logged
        }

        if "active" not in user_profile.challenges:
            user_profile.challenges["active"] = {}
        
        user_profile.challenges["active"][challenge_id] = challenge_data
        return {"success": True, "challenge": challenge_data}

    def log_progress(self, user_profile, challenge_id: str) -> Dict:
        """
        Log daily progress for a challenge.
        Updates streak, points, and checks for completion.
        """
        if "active" not in user_profile.challenges or challenge_id not in user_profile.challenges["active"]:
            return {"success": False, "error": "Challenge not active"}

        challenge_def = self.challenges_catalog[challenge_id]
        user_challenge = user_profile.challenges["active"][challenge_id]
        
        today = datetime.now().date().isoformat()
        
        # Check if already logged today
        if user_challenge["last_log_date"] == today:
            return {"success": False, "error": "Already logged progress for today"}

        # Update progress
        user_challenge["last_log_date"] = today
        user_challenge["days_completed"] += 1
        user_challenge["history"].append(today)

        # Award daily points
        points_earned = challenge_def["points_per_day"]
        user_profile.challenges["points"] = user_profile.challenges.get("points", 0) + points_earned

        result = {
            "success": True,
            "points_earned": points_earned,
            "days_completed": user_challenge["days_completed"],
            "total_days": challenge_def["duration_days"],
            "completed": False
        }

        # Check for completion
        if user_challenge["days_completed"] >= challenge_def["duration_days"]:
            self._complete_challenge(user_profile, challenge_id)
            result["completed"] = True
            result["bonus_points"] = challenge_def["completion_bonus"]
            result["badge"] = self.badges_catalog[challenge_def["badge_id"]]

        return result

    def _complete_challenge(self, user_profile, challenge_id: str):
        """Handle challenge completion: move to history, award bonus/badge"""
        challenge_def = self.challenges_catalog[challenge_id]
        user_challenge = user_profile.challenges["active"].pop(challenge_id)
        
        # Add completion metadata
        user_challenge["completed_at"] = datetime.now().isoformat()
        
        # Move to completed history
        if "completed_history" not in user_profile.challenges:
            user_profile.challenges["completed_history"] = []
        user_profile.challenges["completed_history"].append(user_challenge)

        # Award bonus points
        user_profile.challenges["points"] += challenge_def["completion_bonus"]

        # Award badge
        badge_id = challenge_def["badge_id"]
        if "badges" not in user_profile.challenges:
            user_profile.challenges["badges"] = []
        
        if badge_id not in user_profile.challenges["badges"]:
            user_profile.challenges["badges"].append(badge_id)

    def leave_challenge(self, user_profile, challenge_id: str) -> Dict:
        """Remove a challenge from active list"""
        if "active" in user_profile.challenges and challenge_id in user_profile.challenges["active"]:
            del user_profile.challenges["active"][challenge_id]
            return {"success": True}
        return {"success": False, "error": "Challenge not active"}

# Singleton instance
_challenges_manager = ChallengesManager()

def get_challenges_manager():
    return _challenges_manager
