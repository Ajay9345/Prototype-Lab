"""
Verification Script for Phase 2 Features
"""
import json
from food_safety_scanner import get_food_safety_scanner
from grocery_auditor import get_grocery_auditor

def test_food_scanner():
    print("Testing Food Safety Scanner...")
    scanner = get_food_safety_scanner()
    
    ingredients = "Sugar, Palm Oil, Cocoa Solids, Wheat Flour, Emulsifier (Soy Lecithin), Artificial Flavour (Vanillin)."
    profile = {
        "conditions": ["Diabetes"],
        "allergies": ["Soy"]
    }
    
    # This will use LLM if available
    result = scanner.audit_ingredients(ingredients, profile)
    print(f"Food Audit Grade: {result.get('grade')}")
    print(f"Risks identified: {result.get('risks', [])}")
    print("Food Scanner check initiated.")

def test_grocery_auditor():
    print("\nTesting Grocery Auditor...")
    auditor = get_grocery_auditor()
    
    receipt = """
    1x Whole Milk 1L
    2x Coca Cola 500ml
    1x Lay's Classic Chips
    1x Fresh Spinach 200g
    1x Apples 1kg
    """
    profile = {
        "goals": ["Weight Loss"],
        "conditions": ["Hypertension"]
    }
    
    # This will use LLM if available
    result = auditor.analyze_receipt(receipt, profile)
    print(f"Basket Health Score: {result.get('health_score')}")
    print(f"Red Flags: {result.get('red_flags', [])}")
    print("Grocery Auditor check initiated.")

if __name__ == "__main__":
    try:
        test_food_scanner()
        test_grocery_auditor()
        print("\nAll Phase 2 verifications initiated successfully.")
    except Exception as e:
        print(f"Verification failed: {e}")
