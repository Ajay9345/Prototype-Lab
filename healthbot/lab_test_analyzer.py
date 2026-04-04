"""
Lab Test Analyzer Module
AI-powered analysis of lab test results with interpretations and recommendations.
"""

import json
import os
from typing import Dict, List, Optional
from groq import Groq


class LabTestAnalyzer:
    def __init__(self):
        # Load normal ranges
        self.normal_ranges = self._load_normal_ranges()
        
        # Initialize Groq client
        try:
            api_key = os.getenv('GROQ_API_KEY')
            self.groq_client = Groq(api_key=api_key) if api_key else None
        except:
            self.groq_client = None
    
    def _load_normal_ranges(self) -> Dict:
        """Load normal ranges from JSON file."""
        try:
            ranges_path = os.path.join('data', 'lab_test_ranges.json')
            with open(ranges_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading normal ranges: {e}")
            return {}
    
    def analyze_lab_report(
        self, 
        test_values: Dict, 
        test_category: str,
        gender: str = 'male',
        age: Optional[int] = None,
        user_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze lab test results and provide interpretations.
        
        Args:
            test_values: Dictionary of test parameters and values
            test_category: Category of the test
            gender: User's gender for gender-specific ranges
            age: User's age
            user_profile: User's health profile
            
        Returns:
            Dictionary with analysis results
        """
        if not test_values:
            return {
                'test_category': test_category,
                'overall_status': 'No values to analyze',
                'parameters': [],
                'summary': 'Unable to extract test values from the report.',
                'recommendations': []
            }
        
        # Analyze each parameter
        analyzed_parameters = []
        abnormal_count = 0
        critical_count = 0
        
        for param_name, param_data in test_values.items():
            analysis = self._analyze_parameter(
                param_name,
                param_data,
                gender,
                age
            )
            
            if analysis:
                analyzed_parameters.append(analysis)
                if analysis['status'] in ['high', 'low']:
                    abnormal_count += 1
                if analysis.get('is_critical', False):
                    critical_count += 1
        
        # Determine overall status
        if critical_count > 0:
            overall_status = 'Critical - Immediate medical attention needed'
        elif abnormal_count > len(analyzed_parameters) / 2:
            overall_status = 'Multiple abnormalities detected'
        elif abnormal_count > 0:
            overall_status = 'Some values need attention'
        else:
            overall_status = 'All values within normal range'
        
        # Generate AI-powered summary and recommendations
        ai_summary = self._generate_ai_summary(
            analyzed_parameters,
            test_category,
            user_profile
        )
        
        return {
            'test_category': test_category,
            'overall_status': overall_status,
            'parameters': analyzed_parameters,
            'summary': ai_summary.get('summary', ''),
            'lifestyle_recommendations': ai_summary.get('lifestyle_recommendations', []),
            'when_to_consult_doctor': ai_summary.get('when_to_consult_doctor', []),
            'abnormal_count': abnormal_count,
            'total_parameters': len(analyzed_parameters)
        }
    
    def _analyze_parameter(
        self,
        param_name: str,
        param_data: Dict,
        gender: str,
        age: Optional[int]
    ) -> Optional[Dict]:
        """
        Analyze a single test parameter.
        
        Returns:
            Dictionary with parameter analysis
        """
        value = param_data.get('value')
        if value is None:
            return None
        
        # Find the parameter in normal ranges
        param_range = self._find_parameter_range(param_name, gender)
        
        if not param_range:
            return {
                'name': self._format_parameter_name(param_name),
                'value': value,
                'unit': param_data.get('unit', ''),
                'normal_range': 'Not available',
                'status': 'unknown',
                'interpretation': 'Normal range not available for this parameter.',
                'recommendations': []
            }
        
        # Determine status
        status, interpretation, is_critical = self._determine_status(
            param_name,
            value,
            param_range
        )
        
        # Get recommendations
        recommendations = self._get_parameter_recommendations(
            param_name,
            status
        )
        
        # Format normal range
        normal_range_str = self._format_normal_range(param_range, gender)
        
        return {
            'name': self._format_parameter_name(param_name),
            'value': value,
            'unit': param_data.get('unit', param_range.get('unit', '')),
            'normal_range': normal_range_str,
            'status': status,
            'interpretation': interpretation,
            'recommendations': recommendations,
            'is_critical': is_critical
        }
    
    def _find_parameter_range(self, param_name: str, gender: str) -> Optional[Dict]:
        """Find the normal range for a parameter."""
        # Search through all test categories
        for category, tests in self.normal_ranges.items():
            if param_name in tests:
                param_range = tests[param_name]
                
                # Handle gender-specific ranges
                if isinstance(param_range, dict) and gender in param_range:
                    return param_range[gender]
                else:
                    return param_range
        
        return None
    
    def _determine_status(
        self,
        param_name: str,
        value: float,
        param_range: Dict
    ) -> tuple:
        """
        Determine if value is normal, high, or low.
        
        Returns:
            Tuple of (status, interpretation, is_critical)
        """
        min_val = param_range.get('min')
        max_val = param_range.get('max')
        
        is_critical = False
        
        # Check for critical values (very high or very low)
        if min_val and value < min_val * 0.5:
            is_critical = True
        if max_val and value > max_val * 2:
            is_critical = True
        
        # Determine status
        if min_val and max_val:
            if value < min_val:
                interpretation = f"Below normal range. This indicates {self._get_low_interpretation(param_name)}"
                return ('low', interpretation, is_critical)
            elif value > max_val:
                interpretation = f"Above normal range. This indicates {self._get_high_interpretation(param_name)}"
                return ('high', interpretation, is_critical)
            else:
                return ('normal', 'Within normal range', False)
        elif max_val:
            if value > max_val:
                interpretation = f"Above normal range. This indicates {self._get_high_interpretation(param_name)}"
                return ('high', interpretation, is_critical)
            else:
                return ('normal', 'Within normal range', False)
        elif min_val:
            if value < min_val:
                interpretation = f"Below normal range. This indicates {self._get_low_interpretation(param_name)}"
                return ('low', interpretation, is_critical)
            else:
                return ('normal', 'Within normal range', False)
        
        return ('unknown', 'Unable to determine status', False)
    
    def _get_low_interpretation(self, param_name: str) -> str:
        """Get interpretation for low values."""
        interpretations = {
            'hemoglobin': 'possible anemia or blood loss',
            'rbc': 'possible anemia',
            'wbc': 'weakened immune system or bone marrow issues',
            'platelets': 'increased bleeding risk',
            'hdl': 'increased cardiovascular risk',
            'tsh': 'possible hyperthyroidism',
            'vitamin_d': 'vitamin D deficiency',
            'vitamin_b12': 'vitamin B12 deficiency'
        }
        return interpretations.get(param_name, 'values below normal range')
    
    def _get_high_interpretation(self, param_name: str) -> str:
        """Get interpretation for high values."""
        interpretations = {
            'wbc': 'possible infection or inflammation',
            'platelets': 'increased clotting risk',
            'total_cholesterol': 'increased cardiovascular risk',
            'ldl': 'increased risk of heart disease',
            'triglycerides': 'increased cardiovascular risk',
            'fasting': 'possible diabetes or prediabetes',
            'hba1c': 'poor blood sugar control',
            'tsh': 'possible hypothyroidism',
            'sgot': 'possible liver damage',
            'sgpt': 'possible liver damage',
            'creatinine': 'possible kidney dysfunction',
            'uric_acid': 'risk of gout'
        }
        return interpretations.get(param_name, 'values above normal range')
    
    def _get_parameter_recommendations(self, param_name: str, status: str) -> List[str]:
        """Get lifestyle recommendations for abnormal values."""
        if status == 'normal':
            return []
        
        recommendations = {
            'hemoglobin': [
                'Increase iron-rich foods (spinach, lentils, dates, pomegranate)',
                'Include vitamin C for better iron absorption',
                'Consider iron supplements after doctor consultation'
            ],
            'total_cholesterol': [
                'Reduce saturated fats and trans fats',
                'Increase fiber intake (oats, beans, fruits)',
                'Exercise regularly (30 minutes daily)',
                'Maintain healthy weight'
            ],
            'ldl': [
                'Limit red meat and full-fat dairy',
                'Eat more nuts, fish, and olive oil',
                'Increase soluble fiber intake',
                'Regular physical activity'
            ],
            'hdl': [
                'Exercise regularly to increase HDL',
                'Include healthy fats (nuts, avocado, fish)',
                'Quit smoking if applicable',
                'Maintain healthy weight'
            ],
            'triglycerides': [
                'Reduce sugar and refined carbohydrates',
                'Limit alcohol consumption',
                'Increase omega-3 fatty acids (fish, flaxseeds)',
                'Regular exercise'
            ],
            'fasting': [
                'Reduce sugar and refined carbs',
                'Increase fiber intake',
                'Regular physical activity',
                'Maintain healthy weight',
                'Monitor blood sugar regularly'
            ],
            'hba1c': [
                'Follow diabetic diet plan',
                'Regular blood sugar monitoring',
                'Consistent meal timing',
                'Regular exercise',
                'Take medications as prescribed'
            ],
            'tsh': [
                'Follow up with endocrinologist',
                'Take thyroid medication as prescribed',
                'Regular monitoring of thyroid levels'
            ],
            'sgot': [
                'Avoid alcohol',
                'Maintain healthy weight',
                'Eat liver-friendly foods',
                'Regular exercise'
            ],
            'sgpt': [
                'Avoid alcohol',
                'Reduce fatty foods',
                'Maintain healthy weight',
                'Regular exercise'
            ]
        }
        
        return recommendations.get(param_name, [
            'Consult your doctor for personalized advice',
            'Follow a balanced, healthy diet',
            'Regular physical activity',
            'Adequate sleep and stress management'
        ])
    
    def _format_parameter_name(self, param_name: str) -> str:
        """Format parameter name for display."""
        name_map = {
            'hemoglobin': 'Hemoglobin (Hb)',
            'rbc': 'Red Blood Cells (RBC)',
            'wbc': 'White Blood Cells (WBC)',
            'platelets': 'Platelets',
            'hematocrit': 'Hematocrit (HCT)',
            'mcv': 'Mean Corpuscular Volume (MCV)',
            'mch': 'Mean Corpuscular Hemoglobin (MCH)',
            'mchc': 'Mean Corpuscular Hemoglobin Concentration (MCHC)',
            'total_cholesterol': 'Total Cholesterol',
            'ldl': 'LDL Cholesterol (Bad Cholesterol)',
            'hdl': 'HDL Cholesterol (Good Cholesterol)',
            'triglycerides': 'Triglycerides',
            'vldl': 'VLDL Cholesterol',
            'fasting': 'Fasting Blood Sugar',
            'pp': 'Post-Prandial Blood Sugar',
            'random': 'Random Blood Sugar',
            'hba1c': 'HbA1c (Glycated Hemoglobin)',
            'tsh': 'Thyroid Stimulating Hormone (TSH)',
            't3': 'Triiodothyronine (T3)',
            't4': 'Thyroxine (T4)',
            'free_t3': 'Free T3',
            'free_t4': 'Free T4',
            'sgot': 'SGOT/AST',
            'sgpt': 'SGPT/ALT',
            'alp': 'Alkaline Phosphatase (ALP)',
            'bilirubin_total': 'Total Bilirubin',
            'bilirubin_direct': 'Direct Bilirubin',
            'bilirubin_indirect': 'Indirect Bilirubin',
            'creatinine': 'Creatinine',
            'bun': 'Blood Urea Nitrogen (BUN)',
            'uric_acid': 'Uric Acid',
            'vitamin_d': 'Vitamin D',
            'vitamin_b12': 'Vitamin B12'
        }
        return name_map.get(param_name, param_name.replace('_', ' ').title())
    
    def _format_normal_range(self, param_range: Dict, gender: str) -> str:
        """Format normal range for display."""
        min_val = param_range.get('min')
        max_val = param_range.get('max')
        unit = param_range.get('unit', '')
        
        if min_val and max_val:
            return f"{min_val}-{max_val} {unit}"
        elif max_val:
            return f"< {max_val} {unit}"
        elif min_val:
            return f"> {min_val} {unit}"
        else:
            return "Range not available"
    
    def _generate_ai_summary(
        self,
        analyzed_parameters: List[Dict],
        test_category: str,
        user_profile: Optional[Dict]
    ) -> Dict:
        """Generate AI-powered summary and recommendations using Groq."""
        if not self.groq_client or not analyzed_parameters:
            return {
                'summary': 'Analysis complete. Please review individual parameters.',
                'lifestyle_recommendations': [],
                'when_to_consult_doctor': []
            }
        
        # Prepare data for AI
        abnormal_params = [p for p in analyzed_parameters if p['status'] != 'normal']
        
        if not abnormal_params:
            return {
                'summary': 'All your test values are within normal range. Keep maintaining your healthy lifestyle!',
                'lifestyle_recommendations': [
                    'Continue balanced diet',
                    'Regular exercise',
                    'Adequate sleep',
                    'Stress management'
                ],
                'when_to_consult_doctor': []
            }
        
        # Create prompt for AI
        prompt = f"""You are a medical assistant analyzing lab test results. 

Test Category: {test_category}

Abnormal Parameters:
"""
        for param in abnormal_params:
            prompt += f"\n- {param['name']}: {param['value']} {param['unit']} (Normal: {param['normal_range']}) - Status: {param['status'].upper()}"
        
        prompt += "\n\nProvide a brief, easy-to-understand summary (2-3 sentences) and 3-5 specific lifestyle recommendations. Also mention when the person should consult a doctor."
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant. Provide clear, simple explanations without medical jargon. Always recommend consulting a doctor for abnormal values."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response (simple parsing)
            lines = ai_response.split('\n')
            summary = []
            recommendations = []
            doctor_advice = []
            
            current_section = 'summary'
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if 'recommendation' in line.lower() or 'lifestyle' in line.lower():
                    current_section = 'recommendations'
                    continue
                elif 'doctor' in line.lower() or 'consult' in line.lower():
                    current_section = 'doctor'
                    continue
                
                if current_section == 'summary' and not line.startswith('-'):
                    summary.append(line)
                elif current_section == 'recommendations' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    recommendations.append(line.lstrip('-•0123456789. '))
                elif current_section == 'doctor':
                    doctor_advice.append(line.lstrip('-•0123456789. '))
            
            return {
                'summary': ' '.join(summary) if summary else 'Please review the abnormal parameters above.',
                'lifestyle_recommendations': recommendations[:5] if recommendations else [],
                'when_to_consult_doctor': doctor_advice if doctor_advice else ['Consult your doctor to discuss these results']
            }
            
        except Exception as e:
            print(f"Error generating AI summary: {e}")
            return {
                'summary': 'Some of your test values are outside the normal range. Please review the details above.',
                'lifestyle_recommendations': [],
                'when_to_consult_doctor': ['Consult your doctor to discuss these abnormal results']
            }


# Singleton instance
_lab_test_analyzer_instance = None

def get_lab_test_analyzer() -> LabTestAnalyzer:
    """Get or create lab test analyzer instance."""
    global _lab_test_analyzer_instance
    if _lab_test_analyzer_instance is None:
        _lab_test_analyzer_instance = LabTestAnalyzer()
    return _lab_test_analyzer_instance
