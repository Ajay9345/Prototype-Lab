import random
from datetime import datetime
from typing import Dict, List, Optional


# ── Static tip libraries ───────────────────────────────────────────────────────

GENERAL_TIPS = [
    "💧 Stay hydrated! Aim for 8 glasses of water daily.",
    "🚶 Take a 10-minute walk after meals to aid digestion.",
    "😴 Maintain a consistent sleep schedule for better rest.",
    "🧘 Practice deep breathing for 5 minutes to reduce stress.",
    "🥗 Include colourful vegetables in every meal for balanced nutrition.",
    "📱 Take regular breaks from screens to protect your eyes.",
    "🤸 Stretch for 5 minutes every hour if you sit for long periods.",
    "🌞 Get 15 minutes of sunlight daily for vitamin D.",
    "🧠 Practice mindfulness or meditation for mental clarity.",
    "👥 Stay connected with friends and family for emotional wellbeing.",
]

AGE_TIPS: Dict[str, List[str]] = {
    "young_adult": [   # 18–35
        "🏋️ Build muscle mass now — it's easier in your 20s and 30s!",
        "💪 Focus on building healthy habits that will last a lifetime.",
        "🎯 Set realistic fitness goals and track your progress.",
        "🥤 Limit sugary drinks and alcohol consumption.",
    ],
    "middle_age": [    # 36–60
        "🦴 Include calcium-rich foods for bone health.",
        "❤️ Monitor your blood pressure and cholesterol regularly.",
        "🏃 Maintain regular physical activity to prevent chronic diseases.",
        "🧘 Practice stress management techniques regularly.",
    ],
    "senior": [        # 60+
        "🦴 Focus on balance exercises to prevent falls.",
        "💊 Keep track of all medications and their schedules.",
        "🧠 Engage in mental exercises like puzzles or reading.",
        "👨‍⚕️ Schedule regular health check-ups and screenings.",
    ],
}

CONDITION_TIPS: Dict[str, List[str]] = {
    "diabetes": [
        "📊 Monitor your blood sugar levels regularly.",
        "🍽️ Eat small, frequent meals to maintain stable blood sugar.",
        "🚶 Regular exercise helps control blood sugar levels.",
        "👣 Check your feet daily for any cuts or sores.",
    ],
    "hypertension": [
        "🧂 Reduce salt intake to less than 5 g per day.",
        "🥗 Follow the DASH diet — rich in fruits and vegetables.",
        "😌 Practice stress-reduction techniques daily.",
        "⚖️ Maintain a healthy weight through diet and exercise.",
    ],
    "asthma": [
        "🌬️ Avoid triggers like smoke, dust, and strong odours.",
        "💨 Keep your inhaler with you at all times.",
        "🏠 Keep your living space clean and dust-free.",
        "🌡️ Monitor weather conditions that may trigger symptoms.",
    ],
    "arthritis": [
        "🏊 Try low-impact exercises like swimming or cycling.",
        "🔥 Apply heat or cold therapy to reduce pain.",
        "⚖️ Maintain a healthy weight to reduce joint stress.",
        "💊 Take medications as prescribed by your doctor.",
    ],
}

GOAL_TIPS: Dict[str, List[str]] = {
    "weight loss": [
        "📝 Keep a food diary to track your eating habits.",
        "🍽️ Use smaller plates to control portion sizes.",
        "🏃 Combine cardio and strength training for best results.",
        "💤 Get adequate sleep — it affects hunger hormones.",
    ],
    "better sleep": [
        "📵 Avoid screens 1 hour before bedtime.",
        "🌡️ Keep your bedroom cool, dark, and quiet.",
        "☕ Avoid caffeine after 2 PM.",
        "🛏️ Establish a relaxing bedtime routine.",
    ],
    "stress management": [
        "🧘 Practice meditation or yoga daily.",
        "📓 Journal your thoughts and feelings.",
        "🎵 Listen to calming music or nature sounds.",
        "🌳 Spend time in nature regularly.",
    ],
    "fitness": [
        "💪 Set SMART goals — Specific, Measurable, Achievable, Relevant, Time-bound.",
        "📅 Schedule workouts like important appointments.",
        "👯 Find a workout buddy for motivation.",
        "🎯 Mix different types of exercises to stay engaged.",
    ],
}

SEASONAL_TIPS: Dict[str, List[str]] = {
    "summer": [
        "☀️ Wear sunscreen with SPF 30+ when outdoors.",
        "💧 Increase water intake to prevent dehydration.",
        "🕶️ Protect your eyes with UV-blocking sunglasses.",
        "🌡️ Avoid outdoor activities during peak heat hours.",
    ],
    "monsoon": [
        "☔ Keep yourself dry to prevent infections.",
        "🦟 Use mosquito repellent to prevent dengue and malaria.",
        "🥗 Eat freshly cooked food and avoid street food.",
        "💧 Drink boiled or filtered water only.",
    ],
    "winter": [
        "🧥 Layer your clothing to stay warm.",
        "💧 Stay hydrated even if you don't feel thirsty.",
        "🧴 Moisturise your skin to prevent dryness.",
        "🏃 Stay active to maintain circulation and warmth.",
    ],
}

# Self-care tips per body-system category
SELF_CARE_TIPS: Dict[str, List[str]] = {
    "respiratory": [
        "💨 Use a humidifier to ease breathing.",
        "🍯 Try honey and warm water for throat relief.",
        "🛏️ Rest with your head elevated.",
        "🌡️ Monitor your temperature regularly.",
    ],
    "gastrointestinal": [
        "🍵 Drink ginger tea to ease nausea.",
        "🍚 Stick to bland foods like rice and bananas.",
        "💧 Stay hydrated with clear fluids.",
        "🚫 Avoid spicy and fatty foods.",
    ],
    "musculoskeletal": [
        "❄️ Apply ice for acute pain (first 48 hours).",
        "🔥 Use heat therapy for chronic pain.",
        "🧘 Gentle stretching can help relieve tension.",
        "💊 Over-the-counter pain relievers may help (consult pharmacist).",
    ],
    "neurological": [
        "😌 Rest in a quiet, dark room.",
        "💧 Stay well-hydrated.",
        "🧊 Apply a cold compress to your forehead.",
        "📵 Reduce screen time and bright lights.",
    ],
}

GENERAL_SELF_CARE = [
    "😴 Get adequate rest — 7–9 hours of sleep.",
    "💧 Stay well-hydrated throughout the day.",
    "🥗 Eat nutritious, balanced meals.",
    "🧘 Practice stress-reduction techniques.",
    "🚶 Light physical activity if you feel up to it.",
]


class WellnessGuide:
    """
    Provides personalised wellness tips, proactive health alerts,
    and self-care recommendations based on the user's profile.
    """

    def get_personalized_tips(
        self,
        user_profile: Optional[Dict] = None,
        count: int = 5,
    ) -> List[str]:
        """
        Build a personalised tip list from age, conditions, goals,
        and the current season.  Falls back to random general tips
        if no profile is provided.
        """
        if not user_profile:
            return random.sample(GENERAL_TIPS, min(count, len(GENERAL_TIPS)))

        tips: List[str] = []

        # Age-specific tips
        age = user_profile.get("age")
        if age:
            category = self._age_category(age)
            tips.extend(AGE_TIPS.get(category, []))

        # Condition-specific tips
        for condition in user_profile.get("conditions", []):
            cond_lower = condition.lower()
            for key, cond_tips in CONDITION_TIPS.items():
                if key in cond_lower:
                    tips.extend(cond_tips)

        # Goal-specific tips
        for goal in user_profile.get("goals", []):
            goal_lower = goal.lower()
            for key, goal_tips in GOAL_TIPS.items():
                if key in goal_lower or any(w in goal_lower for w in key.split()):
                    tips.extend(goal_tips)

        # Seasonal tips
        tips.extend(SEASONAL_TIPS.get(self._current_season(), []))

        # Pad with general tips and deduplicate
        tips.extend(GENERAL_TIPS)
        unique_tips = list(dict.fromkeys(tips))  # preserves insertion order
        return unique_tips[:count]

    def get_daily_wellness_tip(self, user_profile: Optional[Dict] = None) -> str:
        """Return a single personalised tip for the day."""
        tips = self.get_personalized_tips(user_profile, count=1)
        return tips[0] if tips else GENERAL_TIPS[0]

    def get_proactive_alerts(
        self,
        user_profile: Optional[Dict] = None,
        env_data: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Generate proactive health alerts based on the user's profile
        and optional environmental data (AQI, humidity, etc.).
        """
        if not user_profile:
            return []

        alerts: List[Dict] = []

        # Environmental alerts (requires env_data from EnvironmentalSync)
        if env_data:
            from services.environmental_sync import get_environmental_sync
            alerts.extend(get_environmental_sync().generate_alerts(env_data, user_profile))

        # Medication reminder
        medications = user_profile.get("medications", [])
        if medications:
            alerts.append({
                "type":     "medication",
                "priority": "high",
                "message":  f"💊 Remember to take your medications: {', '.join(medications)}",
                "action":   "Set a daily reminder",
            })

        # Health goals reminder
        goals = user_profile.get("goals", [])
        if goals:
            alerts.append({
                "type":     "goal",
                "priority": "medium",
                "message":  f"🎯 Stay focused on your health goals: {', '.join(goals)}",
                "action":   "Track your progress",
            })

        # Annual check-up reminder for users over 40
        age = user_profile.get("age")
        if age and age > 40:
            alerts.append({
                "type":     "checkup",
                "priority": "medium",
                "message":  "👨‍⚕️ Schedule your annual health check-up if you haven't already.",
                "action":   "Book an appointment",
            })

        # Condition monitoring reminder
        conditions = user_profile.get("conditions", [])
        if conditions:
            alerts.append({
                "type":     "monitoring",
                "priority": "high",
                "message":  f"📊 Monitor your {', '.join(conditions)} regularly and track any changes.",
                "action":   "Keep a health journal",
            })

        # Always include a hydration reminder
        alerts.append({
            "type":     "hydration",
            "priority": "low",
            "message":  "💧 Have you had enough water today? Aim for 8 glasses!",
            "action":   "Drink a glass of water now",
        })

        return alerts

    def get_self_care_recommendations(
        self,
        symptom_category: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> List[str]:
        """
        Return self-care tips for a given symptom category and risk level.
        High-risk symptoms always redirect to a doctor.
        """
        if risk_level == "high":
            return [
                "⚠️ These symptoms require medical attention. Please consult a doctor.",
                "Do not rely solely on self-care for serious symptoms.",
            ]

        tips = SELF_CARE_TIPS.get(symptom_category or "", [])
        return tips if tips else GENERAL_SELF_CARE

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _age_category(age: int) -> str:
        """Map an age to one of three broad categories."""
        if age < 36:
            return "young_adult"
        if age < 61:
            return "middle_age"
        return "senior"

    @staticmethod
    def _current_season() -> str:
        """Return the current Indian season based on the calendar month."""
        month = datetime.now().month
        if month in [3, 4, 5, 6]:
            return "summer"
        if month in [7, 8, 9]:
            return "monsoon"
        return "winter"


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[WellnessGuide] = None


def get_wellness_guide() -> WellnessGuide:
    """Return the shared WellnessGuide instance."""
    global _instance
    if _instance is None:
        _instance = WellnessGuide()
    return _instance
