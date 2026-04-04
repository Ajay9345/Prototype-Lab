"""
Verification Script for Phase 4 Features
"""
import json
from digital_twin import get_digital_twin
from insurance_concierge import get_insurance_concierge
from first_aid_guide import get_first_aid_guide
from emergency_support import get_emergency_support

def test_emergency_distress():
    print("Testing Emergency Distress Detection...")
    support = get_emergency_support()
    
    msg1 = "I am fine, just hungry."
    msg2 = "Bacho! Help, I'm falling!"
    
    assert support.detect_distress_keywords(msg1) == False
    assert support.detect_distress_keywords(msg2) == True
    print("Emergency Distress Detection passed.")

def test_digital_twin():
    print("\nTesting Digital Twin...")
    twin = get_digital_twin()
    
    profile = {"age": 30, "conditions": []}
    # This will use LLM if available
    result = twin.simulate_outcome(profile, "Stop smoking for 1 year")
    print(f"Simulation physical changes: {result.get('expected_physical_changes', 'Fallback result')}")
    print("Digital Twin check initiated.")

def test_insurance_concierge():
    print("\nTesting Insurance Concierge...")
    concierge = get_insurance_concierge()
    
    policy = "Health Insurance Plan: Covers MRI scans up to 80%. Pre-authorization required."
    # This will use LLM if available
    result = concierge.analyze_coverage(policy, "MRI Scan")
    print(f"Is Covered: {result.get('is_covered')}")
    print("Insurance Concierge check initiated.")

def test_first_aid():
    print("\nTesting AR First Aid...")
    guide = get_first_aid_guide()
    
    steps = guide.get_step_by_step("cpr")
    print(f"CPR Step 1: {steps[0]['text']}")
    assert len(steps) > 1
    print("AR First Aid passed.")

if __name__ == "__main__":
    try:
        test_emergency_distress()
        test_digital_twin()
        test_insurance_concierge()
        test_first_aid()
        print("\nAll Phase 4 verifications initiated successfully.")
    except Exception as e:
        print(f"Verification failed: {e}")
