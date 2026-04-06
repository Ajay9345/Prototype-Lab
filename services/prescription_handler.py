import os
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image
import pytesseract

# Keywords that suggest a line in the prescription contains a medication
MED_KEYWORDS = [
    "tab", "tablet", "cap", "capsule", "syrup", "injection",
    "mg", "ml", "dose", "dosage", "take", "times", "daily",
]

# Regex to find dates like 12/05/2024 or 5-3-24
DATE_PATTERN = r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}"


class PrescriptionHandler:
    """
    Handles prescription image uploads:
    saves the file, extracts text via OCR, and parses key fields.
    """

    def __init__(self, upload_dir: str = "uploads/prescriptions"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    # ── Public API ────────────────────────────────────────────────────────────

    def process_prescription(self, image_file, user_id: str) -> Dict:
        """
        Save the uploaded image, run OCR, and return a prescription record.

        Args:
            image_file: Flask FileStorage object.
            user_id:    ID of the user uploading the file.

        Returns:
            Dict with id, filename, image_path, upload_date,
            extracted_text, medications, doctor_name, date, notes.
        """
        prescription_id = str(uuid.uuid4())

        # Save image to a user-specific sub-folder
        user_dir   = os.path.join(self.upload_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        file_ext   = os.path.splitext(image_file.filename)[1].lower()
        image_path = os.path.join(user_dir, f"{prescription_id}{file_ext}")
        image_file.save(image_path)

        # OCR → parse
        text   = self._extract_text(image_path)
        parsed = self._parse_prescription(text)

        return {
            "id":             prescription_id,
            "filename":       image_file.filename,
            "image_path":     image_path,
            "upload_date":    datetime.now().isoformat(),
            "extracted_text": text,
            "medications":    parsed["medications"],
            "doctor_name":    parsed["doctor_name"],
            "date":           parsed["date"],
            "notes":          parsed["notes"],
        }

    def delete_prescription(self, prescription_id: str, user_id: str) -> bool:
        """Delete the image file for a prescription. Returns True on success."""
        user_dir = os.path.join(self.upload_dir, user_id)
        for ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
            path = os.path.join(user_dir, f"{prescription_id}{ext}")
            if os.path.exists(path):
                try:
                    os.remove(path)
                    return True
                except Exception as e:
                    print(f"Error deleting prescription file: {e}")
                    return False
        return False

    # ── Private helpers ───────────────────────────────────────────────────────

    def _extract_text(self, image_path: str) -> str:
        """Run Tesseract OCR on the image and return the extracted text."""
        try:
            return pytesseract.image_to_string(Image.open(image_path)).strip()
        except Exception as e:
            print(f"OCR error: {e}")
            return ""

    def _parse_prescription(self, text: str) -> Dict:
        """
        Parse OCR text to extract medications, doctor name, and date.

        Returns a dict with keys: medications, doctor_name, date, notes.
        """
        result = {"medications": [], "doctor_name": "", "date": "", "notes": text}

        if not text:
            return result

        lines = text.split("\n")

        # Medications: lines that contain medication-related keywords
        meds = [
            line.strip()
            for line in lines
            if any(kw in line.lower() for kw in MED_KEYWORDS)
            and len(line.strip()) > 3
        ]
        result["medications"] = meds[:10]  # cap at 10

        # Doctor name: first line containing "dr." or "doctor"
        for line in lines:
            if "dr." in line.lower() or "doctor" in line.lower():
                result["doctor_name"] = line.strip()
                break

        # Date: first line matching the date pattern
        for line in lines:
            match = re.search(DATE_PATTERN, line)
            if match:
                result["date"] = match.group()
                break

        return result


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[PrescriptionHandler] = None


def get_prescription_handler() -> PrescriptionHandler:
    """Return the shared PrescriptionHandler instance."""
    global _instance
    if _instance is None:
        _instance = PrescriptionHandler()
    return _instance
