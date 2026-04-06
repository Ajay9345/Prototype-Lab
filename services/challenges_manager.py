from datetime import datetime
from typing import Dict, List, Optional


# ── Challenge definitions ──────────────────────────────────────────────────────
CHALLENGES_CATALOG: Dict[str, Dict] = {
    "hydration_7_day":  {"id": "hydration_7_day",  "name": "7-Day Hydration",   "description": "Drink 8 glasses of water every day for a week.",          "duration_days": 7,  "category": "hydration",   "icon": "💧", "points_per_day": 10, "completion_bonus": 100, "badge_id": "hydration_master"},
    "steps_10k_streak": {"id": "steps_10k_streak", "name": "10k Steps Streak",  "description": "Walk 10,000 steps daily to keep your heart healthy.",      "duration_days": 30, "category": "activity",    "icon": "👣", "points_per_day": 15, "completion_bonus": 300, "badge_id": "step_champion"},
    "sugar_control":    {"id": "sugar_control",    "name": "Sugar Control",     "description": "Avoid added sugars and sweets for 14 days.",               "duration_days": 14, "category": "nutrition",   "icon": "🥗", "points_per_day": 20, "completion_bonus": 200, "badge_id": "sugar_slayer"},
    "yoga_streak":      {"id": "yoga_streak",      "name": "Yoga Streak",       "description": "Practice yoga for at least 20 minutes daily.",             "duration_days": 21, "category": "mindfulness", "icon": "🧘", "points_per_day": 15, "completion_bonus": 250, "badge_id": "zen_master"},
    "sleep_improvement":{"id": "sleep_improvement","name": "Sleep Improvement", "description": "Get at least 7 hours of quality sleep every night.",       "duration_days": 7,  "category": "sleep",       "icon": "😴", "points_per_day": 10, "completion_bonus": 100, "badge_id": "sleep_guru"},
}

BADGES_CATALOG: Dict[str, Dict] = {
    "hydration_master": {"name": "Hydration Master", "icon": "💧", "description": "Completed the 7-Day Hydration Challenge"},
    "step_champion":    {"name": "Step Champion",    "icon": "👟", "description": "Walked 10k steps for 30 days"},
    "sugar_slayer":     {"name": "Sugar Slayer",     "icon": "🍬", "description": "Controlled sugar intake for 14 days"},
    "zen_master":       {"name": "Zen Master",       "icon": "🧘", "description": "Completed 21 days of Yoga"},
    "sleep_guru":       {"name": "Sleep Guru",       "icon": "🌙", "description": "Achieved 7 days of good sleep"},
}


class ChallengesManager:
    """
    Manages health challenges: joining, logging daily progress,
    awarding points/badges, and completing challenges.
    """

    def get_all_challenges(self) -> List[Dict]:
        """Return all available challenges as a list."""
        return list(CHALLENGES_CATALOG.values())

    def get_challenge_details(self, challenge_id: str) -> Optional[Dict]:
        """Return details for a single challenge, or None if not found."""
        return CHALLENGES_CATALOG.get(challenge_id)

    def join_challenge(self, user_profile, challenge_id: str) -> Dict:
        """
        Add a challenge to the user's active list.

        Returns:
            {"success": True, "challenge": ...} or {"success": False, "error": ...}
        """
        if challenge_id not in CHALLENGES_CATALOG:
            return {"success": False, "error": "Challenge not found"}

        active = user_profile.challenges.setdefault("active", {})
        if challenge_id in active:
            return {"success": False, "error": "Already participating in this challenge"}

        challenge_data = {
            "id":             challenge_id,
            "started_at":     datetime.now().isoformat(),
            "days_completed": 0,
            "last_log_date":  None,
            "history":        [],
        }
        active[challenge_id] = challenge_data
        return {"success": True, "challenge": challenge_data}

    def log_progress(self, user_profile, challenge_id: str) -> Dict:
        """
        Record one day of progress for an active challenge.
        Awards daily points and checks for completion.

        Returns:
            Result dict with success, points_earned, days_completed, etc.
        """
        active = user_profile.challenges.get("active", {})
        if challenge_id not in active:
            return {"success": False, "error": "Challenge not active"}

        definition     = CHALLENGES_CATALOG[challenge_id]
        user_challenge = active[challenge_id]
        today          = datetime.now().date().isoformat()

        if user_challenge["last_log_date"] == today:
            return {"success": False, "error": "Already logged progress for today"}

        # Update progress
        user_challenge["last_log_date"]  = today
        user_challenge["days_completed"] += 1
        user_challenge["history"].append(today)

        # Award daily points
        points = definition["points_per_day"]
        user_profile.challenges["points"] = user_profile.challenges.get("points", 0) + points

        result = {
            "success":       True,
            "points_earned": points,
            "days_completed": user_challenge["days_completed"],
            "total_days":    definition["duration_days"],
            "completed":     False,
        }

        # Check if the challenge is now complete
        if user_challenge["days_completed"] >= definition["duration_days"]:
            self._complete_challenge(user_profile, challenge_id)
            result["completed"]    = True
            result["bonus_points"] = definition["completion_bonus"]
            result["badge"]        = BADGES_CATALOG[definition["badge_id"]]

        return result

    def leave_challenge(self, user_profile, challenge_id: str) -> Dict:
        """Remove a challenge from the user's active list."""
        active = user_profile.challenges.get("active", {})
        if challenge_id in active:
            del active[challenge_id]
            return {"success": True}
        return {"success": False, "error": "Challenge not active"}

    # ── Private helpers ───────────────────────────────────────────────────────

    def _complete_challenge(self, user_profile, challenge_id: str) -> None:
        """Move a finished challenge to history and award bonus points + badge."""
        definition     = CHALLENGES_CATALOG[challenge_id]
        user_challenge = user_profile.challenges["active"].pop(challenge_id)
        user_challenge["completed_at"] = datetime.now().isoformat()

        # Move to completed history
        history = user_profile.challenges.setdefault("completed_history", [])
        history.append(user_challenge)

        # Award bonus points
        user_profile.challenges["points"] = (
            user_profile.challenges.get("points", 0) + definition["completion_bonus"]
        )

        # Award badge (if not already earned)
        badges   = user_profile.challenges.setdefault("badges", [])
        badge_id = definition["badge_id"]
        if badge_id not in badges:
            badges.append(badge_id)


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[ChallengesManager] = None


def get_challenges_manager() -> ChallengesManager:
    """Return the shared ChallengesManager instance."""
    global _instance
    if _instance is None:
        _instance = ChallengesManager()
    return _instance
