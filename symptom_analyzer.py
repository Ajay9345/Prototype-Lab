"""
Symptom Analyzer Module
Analyzes user messages for health symptoms, assesses risk levels,
and generates follow-up questions.
"""

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class SymptomAnalyzer:
    def __init__(self):
        # Emergency keywords that require immediate attention
        self.emergency_keywords = [
            'chest pain', 'heart attack', 'stroke', 'can\'t breathe', 'cannot breathe',
            'difficulty breathing', 'severe bleeding', 'uncontrolled bleeding',
            'unconscious', 'seizure', 'severe burn', 'poisoning', 'overdose',
            'severe head injury', 'broken bone', 'severe allergic reaction',
            'anaphylaxis', 'choking', 'severe abdominal pain', 'coughing blood',
            'vomiting blood', 'suicidal', 'severe chest pressure'
        ]
        
        # High risk symptoms
        self.high_risk_keywords = [
            'severe pain', 'intense pain', 'unbearable pain', 'sharp pain',
            'sudden pain', 'high fever', 'persistent vomiting', 'blood in stool',
            'blood in urine', 'severe headache', 'vision loss', 'slurred speech',
            'numbness', 'paralysis', 'confusion', 'disorientation', 'fainting',
            'dizziness', 'rapid heartbeat', 'irregular heartbeat', 'shortness of breath'
        ]
        
        # Medium risk symptoms
        self.medium_risk_keywords = [
            'fever', 'cough', 'sore throat', 'body ache', 'fatigue', 'weakness',
            'nausea', 'vomiting', 'diarrhea', 'abdominal pain', 'headache',
            'muscle pain', 'joint pain', 'rash', 'swelling', 'persistent pain',
            'loss of appetite', 'weight loss', 'night sweats', 'chills'
        ]
        
        # Low risk symptoms
        self.low_risk_keywords = [
            'mild headache', 'slight fever', 'runny nose', 'sneezing', 'tired',
            'sleepy', 'mild cough', 'dry throat', 'minor ache', 'slight pain',
            'feeling unwell', 'low energy', 'mild discomfort'
        ]
        
        # Symptom categories for topic extraction
        self.symptom_categories = {
            'respiratory': ['cough', 'breathing', 'breath', 'chest', 'lung', 'throat', 'wheeze'],
            'cardiovascular': ['heart', 'chest pain', 'palpitation', 'heartbeat', 'blood pressure'],
            'gastrointestinal': ['stomach', 'abdominal', 'nausea', 'vomit', 'diarrhea', 'constipation'],
            'neurological': ['headache', 'dizzy', 'numbness', 'seizure', 'confusion', 'memory'],
            'musculoskeletal': ['joint', 'muscle', 'bone', 'back pain', 'neck pain', 'arthritis'],
            'dermatological': ['rash', 'skin', 'itch', 'burn', 'wound', 'bruise'],
            'general': ['fever', 'fatigue', 'weakness', 'tired', 'pain', 'ache']
        }
    
    def analyze_message(self, message: str, user_profile: Optional[Dict] = None) -> Dict:
        """
        Analyze a message for symptoms and assess risk level.
        
        Args:
            message: User's message
            user_profile: Optional user profile for personalized analysis
            
        Returns:
            Dictionary containing analysis results
        """
        message_lower = message.lower()
        
        # Detect if message contains symptoms
        has_symptoms = self._contains_symptoms(message_lower)
        
        if not has_symptoms:
            return {
                'has_symptoms': False,
                'risk_level': 'none',
                'symptoms': [],
                'is_emergency': False
            }
        
        # Extract symptoms
        symptoms = self._extract_symptoms(message_lower)
        
        # Assess risk level
        risk_level, is_emergency = self._assess_risk(message_lower, user_profile)
        
        # Get symptom category
        category = self._categorize_symptoms(message_lower)
        
        # Generate follow-up questions
        follow_up_questions = self._generate_follow_up_questions(
            symptoms, risk_level, category, user_profile
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, is_emergency, category)
        
        return {
            'has_symptoms': True,
            'symptoms': symptoms,
            'risk_level': risk_level,
            'is_emergency': is_emergency,
            'category': category,
            'follow_up_questions': follow_up_questions,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _contains_symptoms(self, message: str) -> bool:
        """Check if message contains symptom-related content."""
        symptom_indicators = [
            'pain', 'ache', 'hurt', 'feel', 'symptom', 'sick', 'ill', 'unwell',
            'fever', 'cough', 'bleeding', 'swelling', 'rash', 'dizzy', 'nausea',
            'vomit', 'headache', 'tired', 'fatigue', 'weak', 'sore'
        ]
        return any(indicator in message for indicator in symptom_indicators)
    
    def _extract_symptoms(self, message: str) -> List[str]:
        """Extract specific symptoms from message."""
        symptoms = []
        
        # Combine all symptom keywords
        all_keywords = (
            self.emergency_keywords + 
            self.high_risk_keywords + 
            self.medium_risk_keywords + 
            self.low_risk_keywords
        )
        
        for keyword in all_keywords:
            if keyword in message:
                symptoms.append(keyword)
        
        # Remove duplicates and return
        return list(set(symptoms))
    
    def _assess_risk(self, message: str, user_profile: Optional[Dict] = None) -> Tuple[str, bool]:
        """
        Assess risk level based on symptoms and user profile.
        
        Returns:
            Tuple of (risk_level, is_emergency)
        """
        # Check for emergency keywords first
        for keyword in self.emergency_keywords:
            if keyword in message:
                return ('high', True)
        
        # Check for high risk keywords
        for keyword in self.high_risk_keywords:
            if keyword in message:
                # Consider user profile for risk adjustment
                if user_profile:
                    # Higher risk for elderly or those with conditions
                    age = user_profile.get('age') or 0
                    conditions = user_profile.get('conditions', [])
                    if age > 65 or len(conditions) > 0:
                        return ('high', True)
                return ('high', False)
        
        # Check for medium risk keywords
        for keyword in self.medium_risk_keywords:
            if keyword in message:
                # Check for severity modifiers
                if any(mod in message for mod in ['severe', 'intense', 'persistent', 'chronic']):
                    return ('high', False)
                return ('medium', False)
        
        # Check for low risk keywords
        for keyword in self.low_risk_keywords:
            if keyword in message:
                return ('low', False)
        
        # Default to low risk if symptoms detected but no specific match
        return ('low', False)
    
    def _categorize_symptoms(self, message: str) -> str:
        """Categorize symptoms into body system."""
        for category, keywords in self.symptom_categories.items():
            if any(keyword in message for keyword in keywords):
                return category
        return 'general'
    
    def _generate_follow_up_questions(
        self, 
        symptoms: List[str], 
        risk_level: str, 
        category: str,
        user_profile: Optional[Dict] = None
    ) -> List[str]:
        """Generate contextual follow-up questions."""
        questions = []
        
        if risk_level == 'high' or risk_level == 'emergency':
            questions.extend([
                "How long have you been experiencing these symptoms?",
                "Are the symptoms getting worse?",
                "Have you taken any medication for this?"
            ])
        elif risk_level == 'medium':
            questions.extend([
                "When did these symptoms start?",
                "Have you experienced this before?",
                "Are there any other symptoms you're experiencing?"
            ])
        else:  # low risk
            questions.extend([
                "How long have you had these symptoms?",
                "Have you tried any home remedies?",
                "Is there anything that makes it better or worse?"
            ])
        
        # Category-specific questions
        if category == 'respiratory':
            questions.append("Do you have any difficulty breathing or chest tightness?")
        elif category == 'cardiovascular':
            questions.append("Do you have any history of heart problems?")
        elif category == 'gastrointestinal':
            questions.append("Have you noticed any changes in your diet recently?")
        
        return questions[:3]  # Return top 3 questions
    
    def _generate_recommendations(self, risk_level: str, is_emergency: bool, category: str) -> List[str]:
        """Generate recommendations based on risk level."""
        recommendations = []
        
        if is_emergency:
            recommendations.extend([
                "🚨 This appears to be a medical emergency. Call 108 immediately.",
                "Do not delay seeking emergency medical care.",
                "If possible, have someone stay with you until help arrives."
            ])
        elif risk_level == 'high':
            recommendations.extend([
                "⚠️ These symptoms require medical attention. Please consult a doctor soon.",
                "Consider visiting a nearby hospital or clinic within 24 hours.",
                "Monitor your symptoms closely and seek immediate care if they worsen."
            ])
        elif risk_level == 'medium':
            recommendations.extend([
                "📋 Schedule an appointment with your doctor if symptoms persist.",
                "Keep track of your symptoms and any changes.",
                "Rest and stay hydrated while monitoring your condition."
            ])
        else:  # low risk
            recommendations.extend([
                "💡 These symptoms are typically mild and may resolve on their own.",
                "Try rest, hydration, and over-the-counter remedies if appropriate.",
                "Consult a doctor if symptoms persist for more than a few days."
            ])
        
        return recommendations
    
    def check_emergency(self, message: str) -> bool:
        """Quick check if message contains emergency keywords."""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.emergency_keywords)


# Singleton instance
_analyzer_instance = None

def get_symptom_analyzer() -> SymptomAnalyzer:
    """Get or create symptom analyzer instance."""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = SymptomAnalyzer()
    return _analyzer_instance
