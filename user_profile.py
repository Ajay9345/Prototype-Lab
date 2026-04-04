import json
import os
from typing import Optional, Dict, List
from datetime import datetime
from collections import Counter

class UserProfile:
    def __init__(self, 
                 age: Optional[int] = None,
                 conditions: Optional[List[str]] = None,
                 allergies: Optional[List[str]] = None,
                 medications: Optional[List[str]] = None,
                 goals: Optional[List[str]] = None,
                 chat_history: Optional[List[Dict]] = None,
                 prescriptions: Optional[List[Dict]] = None,
                 lab_reports: Optional[List[Dict]] = None,
                 settings: Optional[Dict] = None,
                 challenges: Optional[Dict] = None,
                 preferred_language: str = 'en',
                 gender: str = 'male'):
        self.age = age
        self.conditions = conditions or []
        self.allergies = allergies or []
        self.medications = medications or []
        self.goals = goals or []
        self.chat_history = chat_history or []
        self.prescriptions = prescriptions or []
        self.lab_reports = lab_reports or []
        self.preferred_language = preferred_language
        self.gender = gender
        self.challenges = challenges or {
            "active": {},
            "completed_history": [],
            "badges": [],
            "points": 0
        }
        # Load challenges from settings if they exist (migration support)
        if settings and 'challenges' in settings:
            self.challenges = settings.pop('challenges')
            
        self.settings = settings or {
            'theme': 'light',
            'notifications': True,
            'data_sharing': False
        }
    
    def add_chat_interaction(self, message: str, response: str, topic: Optional[str] = None):
        """Add a chat interaction to history"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'response': response,
            'topic': topic or self._extract_topic(message)
        }
        self.chat_history.append(interaction)
        
        # Keep only last 100 interactions to prevent unlimited growth
        if len(self.chat_history) > 100:
            self.chat_history = self.chat_history[-100:]
    
    def _extract_topic(self, message: str) -> str:
        """Extract topic from message (simple keyword matching)"""
        message_lower = message.lower()
        
        # Check for emergency first
        if any(word in message_lower for word in ['emergency', 'urgent', 'severe', 'chest pain', 'can\'t breathe']):
            return 'Emergency'
        # Check for symptoms
        elif any(word in message_lower for word in ['symptom', 'pain', 'ache', 'fever', 'cough', 'sick', 'ill']):
            return 'Symptoms & Diagnosis'
        elif any(word in message_lower for word in ['diet', 'food', 'eat', 'nutrition', 'meal']):
            return 'Diet & Nutrition'
        elif any(word in message_lower for word in ['exercise', 'workout', 'fitness', 'gym', 'run']):
            return 'Exercise & Fitness'
        elif any(word in message_lower for word in ['sleep', 'rest', 'insomnia', 'tired']):
            return 'Sleep & Rest'
        elif any(word in message_lower for word in ['stress', 'anxiety', 'mental', 'mood']):
            return 'Mental Health'
        elif any(word in message_lower for word in ['medicine', 'medication', 'drug', 'prescription']):
            return 'Medications'
        else:
            return 'General Health'
    
    def get_statistics(self) -> Dict:
        """Calculate user statistics"""
        total_chats = len(self.chat_history)
        
        # Count topics
        topics = [chat.get('topic', 'General Health') for chat in self.chat_history]
        topic_counts = Counter(topics)
        
        # Get recent interactions (last 5)
        recent_chats = self.chat_history[-5:] if self.chat_history else []
        
        # Calculate profile completion
        profile_fields = [self.age, self.conditions, self.allergies, self.medications, self.goals]
        filled_fields = sum(1 for field in profile_fields if field)
        profile_completion = int((filled_fields / len(profile_fields)) * 100)
        
        return {
            'total_conversations': total_chats,
            'topics': dict(topic_counts.most_common()),
            'recent_interactions': recent_chats,
            'profile_completion': profile_completion,
            'health_profile': {
                'age': self.age,
                'conditions_count': len(self.conditions),
                'allergies_count': len(self.allergies),
                'medications_count': len(self.medications),
                'goals_count': len(self.goals)
            }
        }
    
    def clear_chat_history(self):
        """Clear all chat history"""
        self.chat_history = []
    
    def add_prescription(self, prescription: Dict):
        """Add a prescription to the profile"""
        self.prescriptions.append(prescription)
    
    def get_prescriptions(self) -> List[Dict]:
        """Get all prescriptions"""
        return self.prescriptions
    
    def delete_prescription(self, prescription_id: str) -> bool:
        """Delete a prescription by ID"""
        for i, prescription in enumerate(self.prescriptions):
            if prescription.get('id') == prescription_id:
                self.prescriptions.pop(i)
                return True
        return False
    
    def add_lab_report(self, lab_report: Dict):
        """Add a lab report to the profile"""
        self.lab_reports.append(lab_report)
    
    def get_lab_reports(self) -> List[Dict]:
        """Get all lab reports"""
        return self.lab_reports
    
    def delete_lab_report(self, report_id: str) -> bool:
        """Delete a lab report by ID"""
        for i, report in enumerate(self.lab_reports):
            if report.get('id') == report_id:
                self.lab_reports.pop(i)
                return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return {
            'age': self.age,
            'conditions': self.conditions,
            'allergies': self.allergies,
            'medications': self.medications,
            'goals': self.goals,
            'chat_history': self.chat_history,
            'prescriptions': self.prescriptions,
            'lab_reports': self.lab_reports,
            'settings': self.settings,
            'challenges': self.challenges,
            'preferred_language': self.preferred_language,
            'gender': self.gender
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Create profile from dictionary"""
        return cls(
            age=data.get('age'),
            conditions=data.get('conditions', []),
            allergies=data.get('allergies', []),
            medications=data.get('medications', []),
            goals=data.get('goals', []),
            chat_history=data.get('chat_history', []),
            prescriptions=data.get('prescriptions'), # Changed from data.get('prescriptions', [])
            lab_reports=data.get('lab_reports'),     # Changed from data.get('lab_reports', [])
            preferred_language=data.get('preferred_language', 'en'),
            gender=data.get('gender', 'male'),
            settings=data.get('settings'),            # Changed from data.get('settings', {...})
            challenges=data.get('challenges')         # Added challenges
        )
    
    def to_context_string(self) -> str:
        """Format profile as context string for LLM"""
        if not any([self.age, self.conditions, self.allergies, self.medications, self.goals, self.prescriptions]):
            return ""
        
        context_parts = ["User Health Profile:"]
        
        if self.age:
            context_parts.append(f"- Age: {self.age} years old")
        
        if self.conditions:
            context_parts.append(f"- Medical Conditions: {', '.join(self.conditions)}")
        
        if self.allergies:
            context_parts.append(f"- Allergies: {', '.join(self.allergies)}")
        
        if self.medications:
            context_parts.append(f"- Current Medications: {', '.join(self.medications)}")
        
        if self.goals:
            context_parts.append(f"- Health Goals: {', '.join(self.goals)}")
        
        if self.prescriptions:
            context_parts.append("\nPrescriptions on File:")
            for i, prescription in enumerate(self.prescriptions, 1):
                context_parts.append(f"\nPrescription {i}:")
                if prescription.get('doctor_name'):
                    context_parts.append(f"  - Doctor: {prescription['doctor_name']}")
                if prescription.get('date'):
                    context_parts.append(f"  - Date: {prescription['date']}")
                if prescription.get('medications'):
                    context_parts.append(f"  - Medications: {', '.join(prescription['medications'][:5])}")
        
        return "\n".join(context_parts)


class ProfileManager:
    def __init__(self, storage_path: str = "user_profiles.json"):
        self.storage_path = storage_path
        self.profiles: Dict[str, UserProfile] = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Load profiles from JSON file"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.profiles = {
                        user_id: UserProfile.from_dict(profile_data)
                        for user_id, profile_data in data.items()
                    }
            except Exception as e:
                print(f"Error loading profiles: {e}")
                self.profiles = {}
    
    def save_profiles(self):
        """Save profiles to JSON file"""
        try:
            data = {
                user_id: profile.to_dict()
                for user_id, profile in self.profiles.items()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {e}")
    
    def get_profile(self, user_id: str = "default") -> UserProfile:
        """Get profile for user"""
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile()
        return self.profiles[user_id]
    
    def update_profile(self, profile_data: Dict, user_id: str = "default") -> UserProfile:
        """Update profile for user"""
        self.profiles[user_id] = UserProfile.from_dict(profile_data)
        self.save_profiles()
        return self.profiles[user_id]
