import json
import os
from typing import Dict, List, Optional, Tuple
from groq import Groq


# ── Reference data ─────────────────────────────────────────────────────────────

# Human-readable display names for each test parameter
PARAM_DISPLAY_NAMES: Dict[str, str] = {
    "hemoglobin":        "Hemoglobin (Hb)",
    "rbc":               "Red Blood Cells (RBC)",
    "wbc":               "White Blood Cells (WBC)",
    "platelets":         "Platelets",
    "hematocrit":        "Hematocrit (HCT)",
    "mcv":               "Mean Corpuscular Volume (MCV)",
    "mch":               "Mean Corpuscular Hemoglobin (MCH)",
    "mchc":              "Mean Corpuscular Hemoglobin Concentration (MCHC)",
    "total_cholesterol": "Total Cholesterol",
    "ldl":               "LDL Cholesterol (Bad Cholesterol)",
    "hdl":               "HDL Cholesterol (Good Cholesterol)",
    "triglycerides":     "Triglycerides",
    "vldl":              "VLDL Cholesterol",
    "fasting":           "Fasting Blood Sugar",
    "pp":                "Post-Prandial Blood Sugar",
    "random":            "Random Blood Sugar",
    "hba1c":             "HbA1c (Glycated Hemoglobin)",
    "tsh":               "Thyroid Stimulating Hormone (TSH)",
    "t3":                "Triiodothyronine (T3)",
    "t4":                "Thyroxine (T4)",
    "free_t3":           "Free T3",
    "free_t4":           "Free T4",
    "sgot":              "SGOT/AST",
    "sgpt":              "SGPT/ALT",
    "alp":               "Alkaline Phosphatase (ALP)",
    "bilirubin_total":   "Total Bilirubin",
    "bilirubin_direct":  "Direct Bilirubin",
    "bilirubin_indirect":"Indirect Bilirubin",
    "creatinine":        "Creatinine",
    "bun":               "Blood Urea Nitrogen (BUN)",
    "uric_acid":         "Uric Acid",
    "vitamin_d":         "Vitamin D",
    "vitamin_b12":       "Vitamin B12",
}

# What a LOW value means for each parameter
LOW_INTERPRETATIONS: Dict[str, str] = {
    "hemoglobin":  "possible anaemia or blood loss",
    "rbc":         "possible anaemia",
    "wbc":         "weakened immune system or bone marrow issues",
    "platelets":   "increased bleeding risk",
    "hdl":         "increased cardiovascular risk",
    "tsh":         "possible hyperthyroidism",
    "vitamin_d":   "vitamin D deficiency",
    "vitamin_b12": "vitamin B12 deficiency",
}

# What a HIGH value means for each parameter
HIGH_INTERPRETATIONS: Dict[str, str] = {
    "wbc":               "possible infection or inflammation",
    "platelets":         "increased clotting risk",
    "total_cholesterol": "increased cardiovascular risk",
    "ldl":               "increased risk of heart disease",
    "triglycerides":     "increased cardiovascular risk",
    "fasting":           "possible diabetes or prediabetes",
    "hba1c":             "poor blood sugar control",
    "tsh":               "possible hypothyroidism",
    "sgot":              "possible liver damage",
    "sgpt":              "possible liver damage",
    "creatinine":        "possible kidney dysfunction",
    "uric_acid":         "risk of gout",
}

# Lifestyle recommendations per parameter (shown when value is abnormal)
PARAM_RECOMMENDATIONS: Dict[str, List[str]] = {
    "hemoglobin":        ["Increase iron-rich foods (spinach, lentils, dates, pomegranate)", "Include vitamin C for better iron absorption", "Consider iron supplements after doctor consultation"],
    "total_cholesterol": ["Reduce saturated fats and trans fats", "Increase fibre intake (oats, beans, fruits)", "Exercise regularly (30 minutes daily)", "Maintain healthy weight"],
    "ldl":               ["Limit red meat and full-fat dairy", "Eat more nuts, fish, and olive oil", "Increase soluble fibre intake", "Regular physical activity"],
    "hdl":               ["Exercise regularly to increase HDL", "Include healthy fats (nuts, avocado, fish)", "Quit smoking if applicable", "Maintain healthy weight"],
    "triglycerides":     ["Reduce sugar and refined carbohydrates", "Limit alcohol consumption", "Increase omega-3 fatty acids (fish, flaxseeds)", "Regular exercise"],
    "fasting":           ["Reduce sugar and refined carbs", "Increase fibre intake", "Regular physical activity", "Maintain healthy weight", "Monitor blood sugar regularly"],
    "hba1c":             ["Follow diabetic diet plan", "Regular blood sugar monitoring", "Consistent meal timing", "Regular exercise", "Take medications as prescribed"],
    "tsh":               ["Follow up with endocrinologist", "Take thyroid medication as prescribed", "Regular monitoring of thyroid levels"],
    "sgot":              ["Avoid alcohol", "Maintain healthy weight", "Eat liver-friendly foods", "Regular exercise"],
    "sgpt":              ["Avoid alcohol", "Reduce fatty foods", "Maintain healthy weight", "Regular exercise"],
}

DEFAULT_RECOMMENDATIONS = [
    "Consult your doctor for personalised advice",
    "Follow a balanced, healthy diet",
    "Regular physical activity",
    "Adequate sleep and stress management",
]

# Groq model used for generating the AI summary
AI_SUMMARY_MODEL = "llama-3.1-8b-instant"


class LabTestAnalyzer:
    """
    Analyses parsed lab test values against reference ranges,
    determines status (normal / high / low / critical),
    and generates an AI-powered plain-language summary.
    """

    def __init__(self):
        self.normal_ranges = self._load_normal_ranges()
        try:
            api_key = os.getenv("GROQ_API_KEY")
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except Exception:
            self.groq_client = None

    # ── Public API ────────────────────────────────────────────────────────────

    def analyze_lab_report(
        self,
        test_values: Dict,
        test_category: str,
        gender: str = "male",
        age: Optional[int] = None,
        user_profile: Optional[Dict] = None,
    ) -> Dict:
        """
        Analyse all parameters in a lab report and return a structured result.

        Returns:
            Dict with test_category, overall_status, parameters list,
            AI summary, lifestyle_recommendations, when_to_consult_doctor,
            abnormal_count, total_parameters.
        """
        if not test_values:
            return {
                "test_category":  test_category,
                "overall_status": "No values to analyse",
                "parameters":     [],
                "summary":        "Unable to extract test values from the report.",
                "recommendations": [],
            }

        analyzed   = []
        abnormal   = 0
        critical   = 0

        for name, data in test_values.items():
            result = self._analyze_single_param(name, data, gender, age)
            if result:
                analyzed.append(result)
                if result["status"] in ("high", "low"):
                    abnormal += 1
                if result.get("is_critical"):
                    critical += 1

        # Determine overall status message
        if critical > 0:
            overall = "Critical — Immediate medical attention needed"
        elif abnormal > len(analyzed) / 2:
            overall = "Multiple abnormalities detected"
        elif abnormal > 0:
            overall = "Some values need attention"
        else:
            overall = "All values within normal range"

        ai_summary = self._generate_ai_summary(analyzed, test_category, user_profile)

        return {
            "test_category":          test_category,
            "overall_status":         overall,
            "parameters":             analyzed,
            "summary":                ai_summary.get("summary", ""),
            "lifestyle_recommendations": ai_summary.get("lifestyle_recommendations", []),
            "when_to_consult_doctor": ai_summary.get("when_to_consult_doctor", []),
            "abnormal_count":         abnormal,
            "total_parameters":       len(analyzed),
        }

    def get_parameter_trends(self, lab_reports: List[Dict]) -> Dict:
        """
        Build a trend history for each parameter across multiple lab reports.

        Returns:
            Dict mapping parameter name → {unit, history, summary}.
        """
        if not lab_reports:
            return {}

        sorted_reports = sorted(lab_reports, key=lambda r: r.get("upload_date", ""))
        trends: Dict[str, Dict] = {}

        for report in sorted_reports:
            date       = report.get("upload_date", "").split("T")[0]
            parameters = report.get("analysis", {}).get("parameters", [])

            for param in parameters:
                name = param.get("name")
                if not name:
                    continue
                if name not in trends:
                    trends[name] = {"unit": param.get("unit", ""), "history": []}
                trends[name]["history"].append({
                    "date":   date,
                    "value":  param.get("value"),
                    "status": param.get("status", "unknown"),
                })

        # Add a plain-language trend summary to each parameter
        for name, data in trends.items():
            data["summary"] = (
                self._trend_summary(name, data["history"])
                if len(data["history"]) > 1
                else "More data points needed to establish a trend."
            )

        return trends

    # ── Private helpers ───────────────────────────────────────────────────────

    def _load_normal_ranges(self) -> Dict:
        try:
            with open(os.path.join("data", "lab_test_ranges.json"), "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading normal ranges: {e}")
            return {}

    def _analyze_single_param(
        self,
        param_name: str,
        param_data: Dict,
        gender: str,
        age: Optional[int],
    ) -> Optional[Dict]:
        """Analyse one parameter and return its result dict, or None if no value."""
        value = param_data.get("value")
        if value is None:
            return None

        param_range = self._find_range(param_name, gender)

        if not param_range:
            return {
                "name":           PARAM_DISPLAY_NAMES.get(param_name, param_name.replace("_", " ").title()),
                "value":          value,
                "unit":           param_data.get("unit", ""),
                "normal_range":   "Not available",
                "status":         "unknown",
                "interpretation": "Normal range not available for this parameter.",
                "recommendations": [],
            }

        status, interpretation, is_critical = self._determine_status(param_name, value, param_range)

        return {
            "name":           PARAM_DISPLAY_NAMES.get(param_name, param_name.replace("_", " ").title()),
            "value":          value,
            "unit":           param_data.get("unit", param_range.get("unit", "")),
            "normal_range":   self._format_range(param_range),
            "status":         status,
            "interpretation": interpretation,
            "recommendations": PARAM_RECOMMENDATIONS.get(param_name, DEFAULT_RECOMMENDATIONS) if status != "normal" else [],
            "is_critical":    is_critical,
        }

    def _find_range(self, param_name: str, gender: str) -> Optional[Dict]:
        """Look up the reference range for a parameter, handling gender-specific ranges."""
        for _category, tests in self.normal_ranges.items():
            if param_name in tests:
                rng = tests[param_name]
                # If the range has gender sub-keys, return the appropriate one
                if isinstance(rng, dict) and gender in rng:
                    return rng[gender]
                return rng
        return None

    def _determine_status(
        self,
        param_name: str,
        value: float,
        param_range: Dict,
    ) -> Tuple[str, str, bool]:
        """
        Compare value against min/max and return (status, interpretation, is_critical).
        is_critical is True when the value is extremely far from the normal range.
        """
        min_val = param_range.get("min")
        max_val = param_range.get("max")

        # Critical thresholds: <50% of min or >200% of max
        is_critical = (
            (min_val is not None and value < min_val * 0.5)
            or (max_val is not None and value > max_val * 2)
        )

        if min_val is not None and value < min_val:
            interp = f"Below normal range. This indicates {LOW_INTERPRETATIONS.get(param_name, 'values below normal range')}."
            return ("low", interp, is_critical)

        if max_val is not None and value > max_val:
            interp = f"Above normal range. This indicates {HIGH_INTERPRETATIONS.get(param_name, 'values above normal range')}."
            return ("high", interp, is_critical)

        return ("normal", "Within normal range.", False)

    @staticmethod
    def _format_range(param_range: Dict) -> str:
        """Format a reference range dict as a readable string."""
        min_val = param_range.get("min")
        max_val = param_range.get("max")
        unit    = param_range.get("unit", "")

        if min_val is not None and max_val is not None:
            return f"{min_val}–{max_val} {unit}".strip()
        if max_val is not None:
            return f"< {max_val} {unit}".strip()
        if min_val is not None:
            return f"> {min_val} {unit}".strip()
        return "Range not available"

    def _generate_ai_summary(
        self,
        analyzed: List[Dict],
        test_category: str,
        user_profile: Optional[Dict],
    ) -> Dict:
        """
        Use Groq to generate a plain-language summary and recommendations
        for any abnormal parameters.  Falls back to static text if unavailable.
        """
        fallback = {
            "summary":                  "Analysis complete. Please review individual parameters.",
            "lifestyle_recommendations": [],
            "when_to_consult_doctor":   [],
        }

        if not self.groq_client or not analyzed:
            return fallback

        abnormal = [p for p in analyzed if p["status"] != "normal"]
        if not abnormal:
            return {
                "summary": "All your test values are within normal range. Keep up the healthy lifestyle!",
                "lifestyle_recommendations": ["Continue balanced diet", "Regular exercise", "Adequate sleep", "Stress management"],
                "when_to_consult_doctor": [],
            }

        # Build the prompt
        param_lines = "\n".join(
            f"- {p['name']}: {p['value']} {p['unit']} (Normal: {p['normal_range']}) — {p['status'].upper()}"
            for p in abnormal
        )
        prompt = (
            f"You are a medical assistant analysing lab test results.\n\n"
            f"Test Category: {test_category}\n\nAbnormal Parameters:\n{param_lines}\n\n"
            "Provide a brief, easy-to-understand summary (2–3 sentences) and 3–5 specific "
            "lifestyle recommendations. Also mention when the person should consult a doctor."
        )

        try:
            response = self.groq_client.chat.completions.create(
                model=AI_SUMMARY_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant. Use simple language. Always recommend consulting a doctor for abnormal values."},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            return self._parse_ai_response(response.choices[0].message.content)
        except Exception as e:
            print(f"AI summary error: {e}")
            return {
                "summary":                  "Some values are outside the normal range. Please review the details above.",
                "lifestyle_recommendations": [],
                "when_to_consult_doctor":   ["Consult your doctor to discuss these abnormal results"],
            }

    @staticmethod
    def _parse_ai_response(text: str) -> Dict:
        """
        Parse the free-text AI response into structured sections.
        Sections are detected by keywords in the line.
        """
        summary       = []
        recommendations = []
        doctor_advice = []
        section       = "summary"

        for raw_line in text.split("\n"):
            line = raw_line.strip()
            if not line:
                continue

            if "recommendation" in line.lower() or "lifestyle" in line.lower():
                section = "recommendations"
                continue
            if "doctor" in line.lower() or "consult" in line.lower():
                section = "doctor"
                continue

            if section == "summary" and not line.startswith("-"):
                summary.append(line)
            elif section == "recommendations" and (line.startswith(("-", "•")) or (line and line[0].isdigit())):
                recommendations.append(line.lstrip("-•0123456789. "))
            elif section == "doctor":
                doctor_advice.append(line.lstrip("-•0123456789. "))

        return {
            "summary":                  " ".join(summary) or "Please review the abnormal parameters above.",
            "lifestyle_recommendations": recommendations[:5],
            "when_to_consult_doctor":   doctor_advice or ["Consult your doctor to discuss these results"],
        }

    @staticmethod
    def _trend_summary(param_name: str, history: List[Dict]) -> str:
        """Generate a one-sentence trend description for a parameter."""
        first = history[0]["value"]
        last  = history[-1]["value"]

        if not isinstance(first, (int, float)) or not isinstance(last, (int, float)):
            return f"Trend available across {len(history)} records."

        diff    = last - first
        pct     = (diff / first * 100) if first != 0 else 0

        if abs(pct) < 2:
            return f"Stable: {param_name} is consistent at around {last}."

        direction = "increasing" if diff > 0 else "decreasing"
        magnitude = "significantly" if abs(pct) > 10 else "slightly"
        s_first   = history[0]["status"]
        s_last    = history[-1]["status"]

        if s_last == "normal" and s_first != "normal":
            return f"Improving: {param_name} has moved into the normal range."
        if s_last != "normal" and s_first == "normal":
            return f"Concerning: {param_name} has moved outside the normal range."

        return f"{magnitude.capitalize()} {direction}: {param_name} changed by {abs(pct):.1f}% since the first record."


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[LabTestAnalyzer] = None


def get_lab_test_analyzer() -> LabTestAnalyzer:
    """Return the shared LabTestAnalyzer instance."""
    global _instance
    if _instance is None:
        _instance = LabTestAnalyzer()
    return _instance
