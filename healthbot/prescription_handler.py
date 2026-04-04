"""
Prescription Handler Module
Handles prescription image upload, OCR text extraction, and parsing.
"""

import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image
import pytesseract
import re


class PrescriptionHandler:
    def __init__(self, upload_dir: str = "uploads/prescriptions"):
        self.upload_dir = upload_dir
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
    
    def process_prescription(self, image_file, user_id: str) -> Dict:
        """
        Process uploaded prescription image.
        
        Args:
            image_file: File object from Flask request
            user_id: User ID for organizing uploads
            
        Returns:
            Dictionary with prescription data
        """
        # Generate unique ID for this prescription
        prescription_id = str(uuid.uuid4())
        
        # Save the image
        user_dir = os.path.join(self.upload_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        # Get file extension
        filename = image_file.filename
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Save with unique name
        image_path = os.path.join(user_dir, f"{prescription_id}{file_ext}")
        image_file.save(image_path)
        
        # Extract text using OCR
        extracted_text = self._extract_text(image_path)
        
        # Parse the extracted text
        parsed_data = self._parse_prescription(extracted_text)
        
        # Create prescription record
        prescription = {
            'id': prescription_id,
            'filename': filename,
            'image_path': image_path,
            'upload_date': datetime.now().isoformat(),
            'extracted_text': extracted_text,
            'medications': parsed_data.get('medications', []),
            'doctor_name': parsed_data.get('doctor_name', ''),
            'date': parsed_data.get('date', ''),
            'notes': parsed_data.get('notes', '')
        }
        
        return prescription
    
    def _extract_text(self, image_path: str) -> str:
        """
        Extract text from prescription image using OCR.
        
        Args:
            image_path: Path to the prescription image
            
        Returns:
            Extracted text string
        """
        try:
            # Open image
            image = Image.open(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def _parse_prescription(self, text: str) -> Dict:
        """
        Parse extracted text to identify key information.
        
        Args:
            text: Extracted text from prescription
            
        Returns:
            Dictionary with parsed data
        """
        parsed = {
            'medications': [],
            'doctor_name': '',
            'date': '',
            'notes': ''
        }
        
        if not text:
            return parsed
        
        lines = text.split('\n')
        
        # Common medication-related keywords
        med_keywords = ['tab', 'tablet', 'cap', 'capsule', 'syrup', 'injection', 
                       'mg', 'ml', 'dose', 'dosage', 'take', 'times', 'daily']
        
        # Try to find medications
        medications = []
        for line in lines:
            line_lower = line.lower()
            # Check if line contains medication keywords
            if any(keyword in line_lower for keyword in med_keywords):
                # Clean and add to medications
                cleaned = line.strip()
                if cleaned and len(cleaned) > 3:
                    medications.append(cleaned)
        
        parsed['medications'] = medications[:10]  # Limit to 10 medications
        
        # Try to find doctor name (usually has "Dr." prefix)
        for line in lines:
            if 'dr.' in line.lower() or 'doctor' in line.lower():
                parsed['doctor_name'] = line.strip()
                break
        
        # Try to find date (simple pattern matching)
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        for line in lines:
            match = re.search(date_pattern, line)
            if match:
                parsed['date'] = match.group()
                break
        
        # Store full text as notes
        parsed['notes'] = text
        
        return parsed
    
    def delete_prescription(self, prescription_id: str, user_id: str) -> bool:
        """
        Delete a prescription image.
        
        Args:
            prescription_id: ID of the prescription to delete
            user_id: User ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        user_dir = os.path.join(self.upload_dir, user_id)
        
        # Find and delete the file
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            file_path = os.path.join(user_dir, f"{prescription_id}{ext}")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    return True
                except Exception as e:
                    print(f"Error deleting file: {e}")
                    return False
        
        return False


# Singleton instance
_prescription_handler_instance = None

def get_prescription_handler() -> PrescriptionHandler:
    """Get or create prescription handler instance."""
    global _prescription_handler_instance
    if _prescription_handler_instance is None:
        _prescription_handler_instance = PrescriptionHandler()
    return _prescription_handler_instance
