"""
Verification Script for Phase 1 Features
"""
import os
import json
from lab_test_analyzer import get_lab_test_analyzer
from medication_safety import get_medication_safety_checker
from environmental_sync import get_environmental_sync

def test_lab_trends():
    print("Testing Lab Trends...")
    analyzer = get_lab_test_analyzer()
    
    mock_reports = [
        {
            "upload_date": "2024-01-01T10:00:00",
            "analysis": {
                "parameters": [
                    {"name": "hemoglobin", "value": 12.5, "unit": "g/dL", "status": "low"}
                ]
            }
        },
        {
            "upload_date": "2024-03-01T10:00:00",
            "analysis": {
                "parameters": [
                    {"name": "hemoglobin", "value": 14.2, "unit": "g/dL", "status": "normal"}
                ]
            }
        }
    ]
    
    trends = analyzer.get_parameter_trends(mock_reports)
    assert 'hemoglobin' in trends
    assert len(trends['hemoglobin']['history']) == 2
    print(f"Trend Summary: {trends['hemoglobin']['summary']}")
    print("Lab Trends passed.")

def test_medication_safety():
    print("\nTesting Medication Safety...")
    checker = get_medication_safety_checker()
    
    profile = {
        "medications": ["Lipitor"],
        "allergies": ["Penicillin"],
        "conditions": ["Diabetes"]
    }
    
    # This will use the LLM if GROQ_API_KEY is available
    result = checker.check_interactions(["Amoxicillin"], profile)
    print(f"Safety Check Result: {result.get('status')} - Warnings: {result.get('warnings')}")
    print("Medication Safety check triggered.")

def test_environmental_sync():
    print("\nTesting Environmental Sync...")
    sync = get_environmental_sync()
    
    data = sync.get_environmental_data(19.076, 72.877) # Mumbai
    print(f"Current Env Data (AQI): {data.get('aqi')} - {data.get('status')}")
    
    profile = {"conditions": ["Asthma"]}
    alerts = sync.generate_alerts(data, profile)
    for alert in alerts:
        print(f"Alert: {alert['message']}")
    print("Environmental Sync passed.")

if __name__ == "__main__":
    try:
        test_lab_trends()
        test_medication_safety()
        test_environmental_sync()
        print("\nAll Phase 1 verifications initiated successfully.")
    except Exception as e:
        print(f"Verification failed: {e}")
