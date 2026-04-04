"""
Verification Script for Phase 3 Features
"""
import json
import os
from triage_engine import get_triage_engine
from symptom_cam_analyzer import get_symptom_cam_analyzer

def test_triage_engine():
    print("Testing Virtual Triage Engine...")
    engine = get_triage_engine()
    
    symptom_analysis = {
        "has_symptoms": True,
        "symptoms": ["Chest Pain", "Shortness of breath"],
        "risk_level": "high"
    }
    profile = {
        "age": 55,
        "conditions": ["Hypertension"]
    }
    
    # This will use LLM if available
    result = engine.conduct_triage(symptom_analysis, profile)
    print(f"Triage Urgency: {result.get('urgency_level')}")
    print(f"Recommended Specialist: {result.get('recommended_specialist')}")
    print(f"Follow-up Questions: {result.get('follow_up_questions', [])[:2]}")
    print("Triage Engine check initiated.")

def test_symptom_cam():
    print("\nTesting Symptom Cam Analyzer...")
    analyzer = get_symptom_cam_analyzer()
    
    # Create a dummy image file for testing
    dummy_path = "dummy_symptom.jpg"
    with open(dummy_path, "wb") as f:
        f.write(b"dummy image data")
    
    result = analyzer.analyze_symptom_image(dummy_path, "Rash")
    print(f"Visual Assessment: {result.get('visual_assessment', {}).get('detected_features')}")
    print(f"Recommendation: {result.get('visual_assessment', {}).get('recommendation')}")
    
    # Clean up
    if os.path.exists(dummy_path):
        os.remove(dummy_path)
    print("Symptom Cam check initiated.")

if __name__ == "__main__":
    try:
        test_triage_engine()
        test_symptom_cam()
        print("\nAll Phase 3 verifications initiated successfully.")
    except Exception as e:
        print(f"Verification failed: {e}")
