"""
Wellness Guide Module
Provides personalized wellness tips, proactive health monitoring,
and self-care recommendations.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random


class WellnessGuide:
    def __init__(self):
        # General wellness tips
        self.general_tips = [
            "💧 Stay hydrated! Aim for 8 glasses of water daily.",
            "🚶 Take a 10-minute walk after meals to aid digestion.",
            "😴 Maintain a consistent sleep schedule for better rest.",
            "🧘 Practice deep breathing for 5 minutes to reduce stress.",
            "🥗 Include colorful vegetables in every meal for balanced nutrition.",
            "📱 Take regular breaks from screens to protect your eyes.",
            "🤸 Stretch for 5 minutes every hour if you sit for long periods.",
            "🌞 Get 15 minutes of sunlight daily for vitamin D.",
            "🧠 Practice mindfulness or meditation for mental clarity.",
            "👥 Stay connected with friends and family for emotional wellbeing."
        ]
        
        # Age-specific tips
        self.age_specific_tips = {
            'young_adult': [  # 18-35
                "🏋️ Build muscle mass now - it's easier in your 20s and 30s!",
                "💪 Focus on building healthy habits that will last a lifetime.",
                "🎯 Set realistic fitness goals and track your progress.",
                "🥤 Limit sugary drinks and alcohol consumption."
            ],
            'middle_age': [  # 36-60
                "🦴 Include calcium-rich foods for bone health.",
                "❤️ Monitor your blood pressure and cholesterol regularly.",
                "🏃 Maintain regular physical activity to prevent chronic diseases.",
                "🧘 Practice stress management techniques regularly."
            ],
            'senior': [  # 60+
                "🦴 Focus on balance exercises to prevent falls.",
                "💊 Keep track of all medications and their schedules.",
                "🧠 Engage in mental exercises like puzzles or reading.",
                "👨‍⚕️ Schedule regular health check-ups and screenings."
            ]
        }
        
        # Condition-specific tips
        self.condition_tips = {
            'diabetes': [
                "📊 Monitor your blood sugar levels regularly.",
                "🍽️ Eat small, frequent meals to maintain stable blood sugar.",
                "🚶 Regular exercise helps control blood sugar levels.",
                "👣 Check your feet daily for any cuts or sores."
            ],
            'hypertension': [
                "🧂 Reduce salt intake to less than 5g per day.",
                "🥗 Follow the DASH diet - rich in fruits and vegetables.",
                "😌 Practice stress-reduction techniques daily.",
                "⚖️ Maintain a healthy weight through diet and exercise."
            ],
            'asthma': [
                "🌬️ Avoid triggers like smoke, dust, and strong odors.",
                "💨 Keep your inhaler with you at all times.",
                "🏠 Keep your living space clean and dust-free.",
                "🌡️ Monitor weather conditions that may trigger symptoms."
            ],
            'arthritis': [
                "🏊 Try low-impact exercises like swimming or cycling.",
                "🔥 Apply heat or cold therapy to reduce pain.",
                "⚖️ Maintain a healthy weight to reduce joint stress.",
                "💊 Take medications as prescribed by your doctor."
            ]
        }
        
        # Goal-specific tips
        self.goal_tips = {
            'weight loss': [
                "📝 Keep a food diary to track your eating habits.",
                "🍽️ Use smaller plates to control portion sizes.",
                "🏃 Combine cardio and strength training for best results.",
                "💤 Get adequate sleep - it affects hunger hormones."
            ],
            'better sleep': [
                "📵 Avoid screens 1 hour before bedtime.",
                "🌡️ Keep your bedroom cool, dark, and quiet.",
                "☕ Avoid caffeine after 2 PM.",
                "🛏️ Establish a relaxing bedtime routine."
            ],
            'stress management': [
                "🧘 Practice meditation or yoga daily.",
                "📓 Journal your thoughts and feelings.",
                "🎵 Listen to calming music or nature sounds.",
                "🌳 Spend time in nature regularly."
            ],
            'fitness': [
                "💪 Set SMART goals - Specific, Measurable, Achievable, Relevant, Time-bound.",
                "📅 Schedule workouts like important appointments.",
                "👯 Find a workout buddy for motivation.",
                "🎯 Mix different types of exercises to stay engaged."
            ]
        }
        
        # Seasonal wellness tips
        self.seasonal_tips = {
            'summer': [
                "☀️ Wear sunscreen with SPF 30+ when outdoors.",
                "💧 Increase water intake to prevent dehydration.",
                "🕶️ Protect your eyes with UV-blocking sunglasses.",
                "🌡️ Avoid outdoor activities during peak heat hours."
            ],
            'monsoon': [
                "☔ Keep yourself dry to prevent infections.",
                "🦟 Use mosquito repellent to prevent dengue and malaria.",
                "🥗 Eat freshly cooked food and avoid street food.",
                "💧 Drink boiled or filtered water only."
            ],
            'winter': [
                "🧥 Layer your clothing to stay warm.",
                "💧 Stay hydrated even if you don't feel thirsty.",
                "🧴 Moisturize your skin to prevent dryness.",
                "🏃 Stay active to maintain circulation and warmth."
            ]
        }
    
    def get_personalized_tips(
        self, 
        user_profile: Optional[Dict] = None,
        count: int = 5
    ) -> List[str]:
        """
        Get personalized wellness tips based on user profile.
        
        Args:
            user_profile: User's health profile
            count: Number of tips to return
            
        Returns:
            List of personalized wellness tips
        """
        tips = []
        
        if not user_profile:
            # Return random general tips if no profile
            return random.sample(self.general_tips, min(count, len(self.general_tips)))
        
        # Add age-specific tips
        age = user_profile.get('age')
        if age:
            age_category = self._get_age_category(age)
            if age_category in self.age_specific_tips:
                tips.extend(self.age_specific_tips[age_category])
        
        # Add condition-specific tips
        conditions = user_profile.get('conditions', [])
        for condition in conditions:
            condition_lower = condition.lower()
            for key, condition_tips in self.condition_tips.items():
                if key in condition_lower:
                    tips.extend(condition_tips)
        
        # Add goal-specific tips
        goals = user_profile.get('goals', [])
        for goal in goals:
            goal_lower = goal.lower()
            for key, goal_tips in self.goal_tips.items():
                if key in goal_lower or any(word in goal_lower for word in key.split()):
                    tips.extend(goal_tips)
        
        # Add seasonal tips
        current_season = self._get_current_season()
        if current_season in self.seasonal_tips:
            tips.extend(self.seasonal_tips[current_season])
        
        # Add general tips to fill up
        tips.extend(self.general_tips)
        
        # Remove duplicates and return requested count
        unique_tips = list(dict.fromkeys(tips))  # Preserves order
        return unique_tips[:count]
    
    def get_daily_wellness_tip(self, user_profile: Optional[Dict] = None) -> str:
        """Get a single daily wellness tip."""
        tips = self.get_personalized_tips(user_profile, count=1)
        return tips[0] if tips else self.general_tips[0]
    
    def get_proactive_alerts(self, user_profile: Optional[Dict] = None) -> List[Dict]:
        """
        Generate proactive health alerts based on user profile and history.
        
        Returns:
            List of alert dictionaries with type, message, and priority
        """
        alerts = []
        
        if not user_profile:
            return alerts
        
        # Check medication reminders
        medications = user_profile.get('medications', [])
        if medications:
            alerts.append({
                'type': 'medication',
                'priority': 'high',
                'message': f"💊 Remember to take your medications: {', '.join(medications)}",
                'action': 'Set a daily reminder'
            })
        
        # Check for health goals progress
        goals = user_profile.get('goals', [])
        if goals:
            alerts.append({
                'type': 'goal',
                'priority': 'medium',
                'message': f"🎯 Stay focused on your health goals: {', '.join(goals)}",
                'action': 'Track your progress'
            })
        
        # Check for regular check-ups (based on age and conditions)
        age = user_profile.get('age')
        conditions = user_profile.get('conditions', [])
        
        if age and age > 40:
            alerts.append({
                'type': 'checkup',
                'priority': 'medium',
                'message': "👨‍⚕️ Schedule your annual health check-up if you haven't already.",
                'action': 'Book an appointment'
            })
        
        if conditions:
            alerts.append({
                'type': 'monitoring',
                'priority': 'high',
                'message': f"📊 Monitor your {', '.join(conditions)} regularly and track any changes.",
                'action': 'Keep a health journal'
            })
        
        # Hydration reminder
        alerts.append({
            'type': 'hydration',
            'priority': 'low',
            'message': "💧 Have you had enough water today? Aim for 8 glasses!",
            'action': 'Drink a glass of water now'
        })
        
        return alerts
    
    def get_self_care_recommendations(
        self, 
        symptom_category: Optional[str] = None,
        risk_level: Optional[str] = None
    ) -> List[str]:
        """
        Get self-care recommendations based on symptoms or general wellness.
        
        Args:
            symptom_category: Category of symptoms (if any)
            risk_level: Risk level of symptoms (if any)
            
        Returns:
            List of self-care recommendations
        """
        recommendations = []
        
        # If high risk, recommend medical attention
        if risk_level == 'high':
            return [
                "⚠️ These symptoms require medical attention. Please consult a doctor.",
                "Do not rely solely on self-care for serious symptoms."
            ]
        
        # Category-specific self-care
        if symptom_category:
            if symptom_category == 'respiratory':
                recommendations.extend([
                    "💨 Use a humidifier to ease breathing.",
                    "🍯 Try honey and warm water for throat relief.",
                    "🛏️ Rest with your head elevated.",
                    "🌡️ Monitor your temperature regularly."
                ])
            elif symptom_category == 'gastrointestinal':
                recommendations.extend([
                    "🍵 Drink ginger tea to ease nausea.",
                    "🍚 Stick to bland foods like rice and bananas.",
                    "💧 Stay hydrated with clear fluids.",
                    "🚫 Avoid spicy and fatty foods."
                ])
            elif symptom_category == 'musculoskeletal':
                recommendations.extend([
                    "❄️ Apply ice for acute pain (first 48 hours).",
                    "🔥 Use heat therapy for chronic pain.",
                    "🧘 Gentle stretching can help relieve tension.",
                    "💊 Over-the-counter pain relievers may help (consult pharmacist)."
                ])
            elif symptom_category == 'neurological':
                recommendations.extend([
                    "😌 Rest in a quiet, dark room.",
                    "💧 Stay well-hydrated.",
                    "🧊 Apply a cold compress to your forehead.",
                    "📵 Reduce screen time and bright lights."
                ])
        
        # General self-care recommendations
        if not recommendations:
            recommendations.extend([
                "😴 Get adequate rest - 7-9 hours of sleep.",
                "💧 Stay well-hydrated throughout the day.",
                "🥗 Eat nutritious, balanced meals.",
                "🧘 Practice stress-reduction techniques.",
                "🚶 Light physical activity if you feel up to it."
            ])
        
        return recommendations
    
    def _get_age_category(self, age: int) -> str:
        """Categorize age into groups."""
        if age < 36:
            return 'young_adult'
        elif age < 61:
            return 'middle_age'
        else:
            return 'senior'
    
    def _get_current_season(self) -> str:
        """Determine current season (India-specific)."""
        month = datetime.now().month
        
        # Indian seasons (approximate)
        if month in [3, 4, 5, 6]:
            return 'summer'
        elif month in [7, 8, 9]:
            return 'monsoon'
        else:  # [10, 11, 12, 1, 2]
            return 'winter'


# Singleton instance
_wellness_guide_instance = None

def get_wellness_guide() -> WellnessGuide:
    """Get or create wellness guide instance."""
    global _wellness_guide_instance
    if _wellness_guide_instance is None:
        _wellness_guide_instance = WellnessGuide()
    return _wellness_guide_instance
