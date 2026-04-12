import json
import os
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image
import pytesseract

TEST_PATTERNS: Dict[str, str] = {
    r"hemo?globin|hb":                          "hemoglobin",
    r"\brbc\b|red\s+blood\s+cell":              "rbc",
    r"\bwbc\b|white\s+blood\s+cell":            "wbc",
    r"platelet":                                "platelets",
    r"hematocrit|hct|pcv":                      "hematocrit",
    r"\bmcv\b":                                 "mcv",
    r"\bmch\b":                                 "mch",
    r"\bmchc\b":                                "mchc",
    r"total\s+cholesterol|cholesterol\s+total": "total_cholesterol",
    r"\bldl\b|ldl\s+cholesterol":               "ldl",
    r"\bhdl\b|hdl\s+cholesterol":               "hdl",
    r"triglyceride":                            "triglycerides",
    r"\bvldl\b":                                "vldl",
    r"fasting\s+(?:blood\s+)?(?:sugar|glucose)|fbs":          "fasting",
    r"(?:post\s+prandial|pp)\s+(?:blood\s+)?(?:sugar|glucose)|ppbs": "pp",
    r"random\s+(?:blood\s+)?(?:sugar|glucose)|rbs":           "random",
    r"hba1c|glycated\s+hemoglobin":             "hba1c",
    r"\btsh\b|thyroid\s+stimulating":           "tsh",
    r"\bt3\b|triiodothyronine":                 "t3",
    r"\bt4\b|thyroxine":                        "t4",
    r"free\s+t3|ft3":                           "free_t3",
    r"free\s+t4|ft4":                           "free_t4",
    r"\bsgot\b|ast\b|aspartate":                "sgot",
    r"\bsgpt\b|alt\b|alanine":                  "sgpt",
    r"\balp\b|alkaline\s+phosphatase":          "alp",
    r"bilirubin\s+total|total\s+bilirubin":     "bilirubin_total",
    r"bilirubin\s+direct|direct\s+bilirubin":   "bilirubin_direct",
    r"bilirubin\s+indirect|indirect\s+bilirubin": "bilirubin_indirect",
    r"total\s+protein":                         "total_protein",
    r"\balbumin\b":                             "albumin",
    r"\bglobulin\b":                            "globulin",
    r"a/?g\s+ratio":                            "ag_ratio",
    r"\bcreatinine\b":                          "creatinine",
    r"\bbun\b|blood\s+urea\s+nitrogen":         "bun",
    r"uric\s+acid":                             "uric_acid",
    r"\bsodium\b|\bna\b":                       "sodium",
    r"\bpotassium\b|\bk\b":                     "potassium",
    r"\bchloride\b|\bcl\b":                     "chloride",
    r"vitamin\s+d|25\s*-?\s*oh\s+d":           "vitamin_d",
    r"vitamin\s+b12|b12":                       "vitamin_b12",
    r"folate|folic\s+acid":                     "folate",
}

CATEGORY_MARKERS: Dict[str, tuple] = {
    "Complete Blood Count (CBC)": ({"hemoglobin", "wbc", "rbc", "platelets"}, 2),
    "Lipid Profile":              ({"total_cholesterol", "ldl", "hdl", "triglycerides"}, 2),
    "Blood Sugar Test":           ({"fasting", "pp", "random", "hba1c"}, 1),
    "Thyroid Function Test":      ({"tsh", "t3", "t4", "free_t3", "free_t4"}, 1),
    "Liver Function Test":        ({"sgot", "sgpt", "alp", "bilirubin_total"}, 2),
    "Kidney Function Test":       ({"creatinine", "bun", "uric_acid"}, 1),
}

VALUE_PATTERN = r"(\d+\.?\d*)\s*([a-zA-Z/%μ]+)?"


class LabTestHandler:
    def __init__(self, upload_dir: str = "uploads/lab_reports"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
        self.normal_ranges = self._load_normal_ranges()

    def process_lab_report(self, image_file, user_id: str, gender: str = "male") -> Dict:
        report_id = str(uuid.uuid4())

        user_dir = os.path.join(self.upload_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        file_ext = os.path.splitext(image_file.filename)[1].lower()
        image_path = os.path.join(user_dir, f"{report_id}{file_ext}")
        image_file.save(image_path)

        text = self._extract_text(image_path)
        test_values = self.parse_test_values(text)
        test_category = self.get_test_category(test_values)

        return {
            "id":             report_id,
            "filename":       image_file.filename,
            "image_path":     image_path,
            "upload_date":    datetime.now().isoformat(),
            "extracted_text": text,
            "test_category":  test_category,
            "test_values":    test_values,
            "gender":         gender,
        }

    def parse_test_values(self, text: str) -> Dict[str, Dict]:
        parsed: Dict[str, Dict] = {}
        if not text:
            return parsed

        for line in text.split("\n"):
            line_lower = line.lower()
            for pattern, test_name in TEST_PATTERNS.items():
                if re.search(pattern, line_lower):
                    match = re.search(VALUE_PATTERN, line)
                    if match:
                        parsed[test_name] = {
                            "value":    float(match.group(1)),
                            "unit":     match.group(2) or "",
                            "raw_line": line.strip(),
                        }
                    break

        return parsed

    def get_test_category(self, parsed_values: Dict) -> str:
        if not parsed_values:
            return "unknown"

        keys = set(parsed_values.keys())
        for category, (markers, min_overlap) in CATEGORY_MARKERS.items():
            if len(keys & markers) >= min_overlap:
                return category

        return "General Lab Test"

    def delete_lab_report(self, report_id: str, user_id: str) -> bool:
        user_dir = os.path.join(self.upload_dir, user_id)
        for ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".pdf"]:
            path = os.path.join(user_dir, f"{report_id}{ext}")
            if os.path.exists(path):
                try:
                    os.remove(path)
                    return True
                except Exception as e:
                    print(f"Error deleting lab report file: {e}")
                    return False
        return False

    def _load_normal_ranges(self) -> Dict:
        try:
            with open(os.path.join("data", "lab_test_ranges.json"), "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading normal ranges: {e}")
            return {}

    def _extract_text(self, image_path: str) -> str:
        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image, config="--oem 3 --psm 6").strip()
        except Exception as e:
            print(f"OCR error: {e}")
            return ""


_instance: Optional[LabTestHandler] = None


def get_lab_test_handler() -> LabTestHandler:
    global _instance
    if _instance is None:
        _instance = LabTestHandler()
    return _instance
