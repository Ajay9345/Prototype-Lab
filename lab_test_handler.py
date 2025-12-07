"""
Lab Test Handler Module
Handles lab report image upload, OCR text extraction, and value parsing.
Supports: CBC, Lipid Profile, Blood Sugar, Thyroid, Liver Function, Kidney Function tests.
"""

import os
import uuid
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from PIL import Image
import pytesseract


class LabTestHandler:
    def __init__(self, upload_dir: str = "uploads/lab_reports"):
        self.upload_dir = upload_dir
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        # Load normal ranges
        self.normal_ranges = self._load_normal_ranges()
    
    def _load_normal_ranges(self) -> Dict:
        """Load normal ranges from JSON file."""
        try:
            ranges_path = os.path.join('data', 'lab_test_ranges.json')
            with open(ranges_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading normal ranges: {e}")
            return {}
    
    def process_lab_report(self, image_file, user_id: str, gender: str = 'male') -> Dict:
        """
        Process uploaded lab report image.
        
        Args:
            image_file: File object from Flask request
            user_id: User ID for organizing uploads
            gender: User's gender for gender-specific ranges
            
        Returns:
            Dictionary with lab report data
        """
        # Generate unique ID for this report
        report_id = str(uuid.uuid4())
        
        # Save the image
        user_dir = os.path.join(self.upload_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        # Get file extension
        filename = image_file.filename
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Save with unique name
        image_path = os.path.join(user_dir, f"{report_id}{file_ext}")
        image_file.save(image_path)
        
        # Extract text using OCR
        extracted_text = self._extract_text(image_path)
        
        # Parse the extracted text
        parsed_values = self.parse_test_values(extracted_text)
        
        # Determine test category
        test_category = self.get_test_category(parsed_values)
        
        # Create lab report record
        lab_report = {
            'id': report_id,
            'filename': filename,
            'image_path': image_path,
            'upload_date': datetime.now().isoformat(),
            'extracted_text': extracted_text,
            'test_category': test_category,
            'test_values': parsed_values,
            'gender': gender
        }
        
        return lab_report
    
    def _extract_text(self, image_path: str) -> str:
        """
        Extract text from lab report image using OCR.
        
        Args:
            image_path: Path to the lab report image
            
        Returns:
            Extracted text string
        """
        try:
            # Open image
            image = Image.open(image_path)
            
            # Perform OCR with better configuration for lab reports
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def parse_test_values(self, text: str) -> Dict[str, Dict]:
        """
        Parse extracted text to identify test parameters and values.
        
        Args:
            text: Extracted text from lab report
            
        Returns:
            Dictionary with test names as keys and value/unit as values
        """
        parsed_values = {}
        
        if not text:
            return parsed_values
        
        lines = text.split('\n')
        
        # Common test name patterns (case-insensitive)
        test_patterns = {
            # CBC
            r'hemo?globin|hb': 'hemoglobin',
            r'\brbc\b|red\s+blood\s+cell': 'rbc',
            r'\bwbc\b|white\s+blood\s+cell': 'wbc',
            r'platelet': 'platelets',
            r'hematocrit|hct|pcv': 'hematocrit',
            r'\bmcv\b': 'mcv',
            r'\bmch\b': 'mch',
            r'\bmchc\b': 'mchc',
            
            # Lipid Profile
            r'total\s+cholesterol|cholesterol\s+total': 'total_cholesterol',
            r'\bldl\b|ldl\s+cholesterol': 'ldl',
            r'\bhdl\b|hdl\s+cholesterol': 'hdl',
            r'triglyceride': 'triglycerides',
            r'\bvldl\b': 'vldl',
            
            # Blood Sugar
            r'fasting\s+(?:blood\s+)?(?:sugar|glucose)|fbs': 'fasting',
            r'(?:post\s+prandial|pp)\s+(?:blood\s+)?(?:sugar|glucose)|ppbs': 'pp',
            r'random\s+(?:blood\s+)?(?:sugar|glucose)|rbs': 'random',
            r'hba1c|glycated\s+hemoglobin': 'hba1c',
            
            # Thyroid
            r'\btsh\b|thyroid\s+stimulating': 'tsh',
            r'\bt3\b|triiodothyronine': 't3',
            r'\bt4\b|thyroxine': 't4',
            r'free\s+t3|ft3': 'free_t3',
            r'free\s+t4|ft4': 'free_t4',
            
            # Liver Function
            r'\bsgot\b|ast\b|aspartate': 'sgot',
            r'\bsgpt\b|alt\b|alanine': 'sgpt',
            r'\balp\b|alkaline\s+phosphatase': 'alp',
            r'bilirubin\s+total|total\s+bilirubin': 'bilirubin_total',
            r'bilirubin\s+direct|direct\s+bilirubin': 'bilirubin_direct',
            r'bilirubin\s+indirect|indirect\s+bilirubin': 'bilirubin_indirect',
            r'total\s+protein': 'total_protein',
            r'\balbumin\b': 'albumin',
            r'\bglobulin\b': 'globulin',
            r'a/?g\s+ratio': 'ag_ratio',
            
            # Kidney Function
            r'\bcreatinine\b': 'creatinine',
            r'\bbun\b|blood\s+urea\s+nitrogen': 'bun',
            r'uric\s+acid': 'uric_acid',
            r'\bsodium\b|\bna\b': 'sodium',
            r'\bpotassium\b|\bk\b': 'potassium',
            r'\bchloride\b|\bcl\b': 'chloride',
            
            # Vitamins
            r'vitamin\s+d|25\s*-?\s*oh\s+d': 'vitamin_d',
            r'vitamin\s+b12|b12': 'vitamin_b12',
            r'folate|folic\s+acid': 'folate'
        }
        
        # Value pattern: number (with optional decimal) followed by optional unit
        value_pattern = r'(\d+\.?\d*)\s*([a-zA-Z/%μ]+)?'
        
        for line in lines:
            line_lower = line.lower()
            
            # Try to match test name patterns
            for pattern, test_name in test_patterns.items():
                if re.search(pattern, line_lower):
                    # Extract value from the same line
                    value_match = re.search(value_pattern, line)
                    if value_match:
                        value = float(value_match.group(1))
                        unit = value_match.group(2) if value_match.group(2) else ''
                        
                        parsed_values[test_name] = {
                            'value': value,
                            'unit': unit,
                            'raw_line': line.strip()
                        }
                    break
        
        return parsed_values
    
    def get_test_category(self, parsed_values: Dict) -> str:
        """
        Determine the category of lab test based on parsed values.
        
        Args:
            parsed_values: Dictionary of parsed test values
            
        Returns:
            Test category string
        """
        if not parsed_values:
            return 'unknown'
        
        test_keys = set(parsed_values.keys())
        
        # Check for CBC markers
        cbc_markers = {'hemoglobin', 'wbc', 'rbc', 'platelets'}
        if len(test_keys & cbc_markers) >= 2:
            return 'Complete Blood Count (CBC)'
        
        # Check for lipid profile markers
        lipid_markers = {'total_cholesterol', 'ldl', 'hdl', 'triglycerides'}
        if len(test_keys & lipid_markers) >= 2:
            return 'Lipid Profile'
        
        # Check for blood sugar markers
        sugar_markers = {'fasting', 'pp', 'random', 'hba1c'}
        if len(test_keys & sugar_markers) >= 1:
            return 'Blood Sugar Test'
        
        # Check for thyroid markers
        thyroid_markers = {'tsh', 't3', 't4', 'free_t3', 'free_t4'}
        if len(test_keys & thyroid_markers) >= 1:
            return 'Thyroid Function Test'
        
        # Check for liver function markers
        liver_markers = {'sgot', 'sgpt', 'alp', 'bilirubin_total'}
        if len(test_keys & liver_markers) >= 2:
            return 'Liver Function Test'
        
        # Check for kidney function markers
        kidney_markers = {'creatinine', 'bun', 'uric_acid'}
        if len(test_keys & kidney_markers) >= 1:
            return 'Kidney Function Test'
        
        return 'General Lab Test'
    
    def delete_lab_report(self, report_id: str, user_id: str) -> bool:
        """
        Delete a lab report image.
        
        Args:
            report_id: ID of the report to delete
            user_id: User ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        user_dir = os.path.join(self.upload_dir, user_id)
        
        # Find and delete the file
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf']:
            file_path = os.path.join(user_dir, f"{report_id}{ext}")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    return True
                except Exception as e:
                    print(f"Error deleting file: {e}")
                    return False
        
        return False


# Singleton instance
_lab_test_handler_instance = None

def get_lab_test_handler() -> LabTestHandler:
    """Get or create lab test handler instance."""
    global _lab_test_handler_instance
    if _lab_test_handler_instance is None:
        _lab_test_handler_instance = LabTestHandler()
    return _lab_test_handler_instance
