from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from rag_engine import RAGEngine
from user_profile import ProfileManager
from symptom_analyzer import get_symptom_analyzer
from emergency_support import get_emergency_support
from wellness_guide import get_wellness_guide
from prescription_handler import get_prescription_handler
from language_support import get_language_support
from lab_test_handler import get_lab_test_handler
from lab_test_analyzer import get_lab_test_analyzer
from challenges_manager import get_challenges_manager
import os
import json

app = Flask(__name__)

try:
    rag_engine = RAGEngine()
except Exception as e:
    print(f"Warning: RAG Engine not initialized: {e}")
    rag_engine = None

profile_manager = ProfileManager()
symptom_analyzer = get_symptom_analyzer()
emergency_support = get_emergency_support()
wellness_guide = get_wellness_guide()
prescription_handler = get_prescription_handler()
language_support = get_language_support()
lab_test_handler = get_lab_test_handler()
lab_test_analyzer = get_lab_test_analyzer()
challenges_manager = get_challenges_manager()

UPLOAD_FOLDER = 'uploads/prescriptions'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not rag_engine:
        return jsonify({"error": "RAG Engine not initialized. Please check server logs."}), 500
    
    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 'default')
    user_language = data.get('language')  
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        
        profile = profile_manager.get_profile(user_id)
        
        
        if not user_language:
            user_language = language_support.detect_language(user_message)
        
        
        if user_language != profile.preferred_language:
            profile.preferred_language = user_language
            profile_manager.save_profiles()
        
        
        message_in_english = language_support.translate_to_english(
            user_message, 
            user_language
        )
        
        
        if symptom_analyzer.check_emergency(message_in_english):
            guidance = emergency_support.get_emergency_guidance()
            
            if user_language != 'en':
                guidance = language_support.translate_dict(guidance, 'en', user_language)
                
            return jsonify({
                "response": "🚨 EMERGENCY DETECTED. Please go to the nearest hospital immediately.",
                "is_emergency": True,
                "emergency_guidance": guidance,
                "detected_language": user_language
            })

        # Get profile context
        profile_context = profile.to_context_string()
        
        # Analyze message for symptoms (using English translation)
        symptom_analysis = symptom_analyzer.analyze_message(
            message_in_english, 
            profile.to_dict()
        )
        
        # Generate response with profile context and conversation history
        response_in_english = rag_engine.generate_response(
            message_in_english, 
            profile_context,
            conversation_history=profile.chat_history
        )
        
        # Translate response back to user's language
        response = language_support.translate_from_english(
            response_in_english,
            user_language
        )
        
        # Translate symptom analysis if present
        if symptom_analysis and user_language != 'en':
            symptom_analysis = language_support.translate_dict(
                symptom_analysis,
                'en',
                user_language
            )
        
        # Track chat interaction (store in user's language)
        profile.add_chat_interaction(user_message, response)
        profile_manager.save_profiles()
        
        return jsonify({
            "response": response,
            "symptom_analysis": symptom_analysis,
            "detected_language": user_language
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    """Analyze symptoms from user message."""
    data = request.json
    message = data.get('message')
    user_id = data.get('user_id', 'default')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        profile = profile_manager.get_profile(user_id)
        analysis = symptom_analyzer.analyze_message(message, profile.to_dict())
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emergency-check', methods=['POST'])
def emergency_check():
    """Check if message contains emergency indicators."""
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        is_emergency = symptom_analyzer.check_emergency(message)
        
        if is_emergency:
            guidance = emergency_support.get_emergency_guidance()
            return jsonify({
                "is_emergency": True,
                "guidance": guidance
            })
        else:
            return jsonify({"is_emergency": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nearby-hospitals', methods=['GET'])
def nearby_hospitals():
    """Get nearby hospitals based on coordinates."""
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        max_results = int(request.args.get('max_results', 5))
        
        hospitals = emergency_support.find_nearby_hospitals(lat, lon, max_results)
        
        return jsonify({
            "hospitals": hospitals,
            "count": len(hospitals)
        })
    except (TypeError, ValueError) as e:
        return jsonify({"error": "Invalid coordinates provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nearby-pharmacies', methods=['GET'])
def nearby_pharmacies():
    """Get nearby 24/7 pharmacies based on coordinates."""
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        max_results = int(request.args.get('max_results', 5))
        
        pharmacies = emergency_support.find_nearby_pharmacies(lat, lon, max_results)
        
        return jsonify({
            "pharmacies": pharmacies,
            "count": len(pharmacies)
        })
    except (TypeError, ValueError) as e:
        return jsonify({"error": "Invalid coordinates provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emergency-contacts', methods=['GET'])
def emergency_contacts():
    """Get emergency contact numbers."""
    try:
        contacts = emergency_support.get_emergency_contacts()
        return jsonify({"contacts": contacts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/wellness-tips', methods=['GET'])
def wellness_tips():
    """Get personalized wellness tips."""
    user_id = request.args.get('user_id', 'default')
    count = int(request.args.get('count', 5))
    
    try:
        profile = profile_manager.get_profile(user_id)
        tips = wellness_guide.get_personalized_tips(profile.to_dict(), count)
        
        return jsonify({
            "tips": tips,
            "count": len(tips)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/daily-tip', methods=['GET'])
def daily_tip():
    """Get daily wellness tip."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        tip = wellness_guide.get_daily_wellness_tip(profile.to_dict())
        
        return jsonify({"tip": tip})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/proactive-alerts', methods=['GET'])
def proactive_alerts():
    """Get proactive health alerts."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        alerts = wellness_guide.get_proactive_alerts(profile.to_dict())
        
        return jsonify({
            "alerts": alerts,
            "count": len(alerts)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/self-care', methods=['GET'])
def self_care():
    """Get self-care recommendations."""
    category = request.args.get('category')
    risk_level = request.args.get('risk_level')
    
    try:
        recommendations = wellness_guide.get_self_care_recommendations(
            category, risk_level
        )
        
        return jsonify({
            "recommendations": recommendations,
            "count": len(recommendations)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id', 'default')
    profile = profile_manager.get_profile(user_id)
    return jsonify(profile.to_dict())

@app.route('/profile', methods=['POST'])
def update_profile():
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        
        # Get existing profile
        profile = profile_manager.get_profile(user_id)
        
        # Update fields
        if 'age' in data:
            profile.age = data.get('age')
        if 'conditions' in data:
            profile.conditions = data.get('conditions', [])
        if 'allergies' in data:
            profile.allergies = data.get('allergies', [])
        if 'medications' in data:
            profile.medications = data.get('medications', [])
        if 'goals' in data:
            profile.goals = data.get('goals', [])
            
        # Save changes
        profile_manager.save_profiles()
        
        return jsonify({"success": True, "profile": profile.to_dict()})
    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    user_id = request.args.get('user_id', 'default')
    profile = profile_manager.get_profile(user_id)
    stats = profile.get_statistics()
    return jsonify(stats)

@app.route('/settings', methods=['GET'])
def get_settings():
    user_id = request.args.get('user_id', 'default')
    profile = profile_manager.get_profile(user_id)
    return jsonify(profile.settings)

@app.route('/settings', methods=['POST'])
def update_settings():
    data = request.json
    user_id = data.get('user_id', 'default')
    
    profile = profile_manager.get_profile(user_id)
    profile.settings.update(data.get('settings', {}))
    profile_manager.save_profiles()
    
    return jsonify({"success": True, "settings": profile.settings})

@app.route('/clear-history', methods=['POST'])
def clear_history():
    data = request.json
    user_id = data.get('user_id', 'default')
    
    profile = profile_manager.get_profile(user_id)
    profile.clear_chat_history()
    profile_manager.save_profiles()
    
    return jsonify({"success": True, "message": "Chat history cleared"})

@app.route('/upload-prescription', methods=['POST'])
def upload_prescription():
    """Upload and process a prescription image."""
    user_id = request.form.get('user_id', 'default')
    
    # Check if file is present
    if 'prescription' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['prescription']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP"}), 400
    
    try:
        # Process the prescription
        prescription = prescription_handler.process_prescription(file, user_id)
        
        # Add to user profile
        profile = profile_manager.get_profile(user_id)
        profile.add_prescription(prescription)
        profile_manager.save_profiles()
        
        return jsonify({
            "success": True,
            "prescription": prescription
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    """Get all prescriptions for a user."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        prescriptions = profile.get_prescriptions()
        
        return jsonify({
            "prescriptions": prescriptions,
            "count": len(prescriptions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/prescription/<prescription_id>', methods=['DELETE'])
def delete_prescription(prescription_id):
    """Delete a prescription."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        
        # Delete from profile
        if profile.delete_prescription(prescription_id):
            # Delete the file
            prescription_handler.delete_prescription(prescription_id, user_id)
            profile_manager.save_profiles()
            
            return jsonify({
                "success": True,
                "message": "Prescription deleted successfully"
            })
        else:
            return jsonify({"error": "Prescription not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/supported-languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages."""
    try:
        languages = language_support.get_supported_languages()
        return jsonify({"languages": languages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/set-language', methods=['POST'])
def set_language():
    """Set user's preferred language."""
    data = request.json
    user_id = data.get('user_id', 'default')
    language = data.get('language', 'en')
    
    try:
        # Validate language
        if not language_support.is_supported_language(language):
            return jsonify({"error": "Unsupported language"}), 400
        
        # Update user profile
        profile = profile_manager.get_profile(user_id)
        profile.preferred_language = language
        profile_manager.save_profiles()
        
        return jsonify({
            "success": True,
            "language": language,
            "language_name": language_support.get_language_name(language)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-language', methods=['GET'])
def get_language():
    """Get user's current language preference."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        return jsonify({
            "language": profile.preferred_language,
            "language_name": language_support.get_language_name(profile.preferred_language),
            "native_name": language_support.get_native_name(profile.preferred_language)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload-lab-report', methods=['POST'])
def upload_lab_report():
    """Upload and process a lab report image."""
    user_id = request.form.get('user_id', 'default')
    
    # Check if file is present
    if 'lab_report' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['lab_report']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP"}), 400
    
    try:
        # Get user profile for gender
        profile = profile_manager.get_profile(user_id)
        
        # Process the lab report
        lab_report = lab_test_handler.process_lab_report(file, user_id, profile.gender)
        
        # Analyze the results
        analysis = lab_test_analyzer.analyze_lab_report(
            lab_report['test_values'],
            lab_report['test_category'],
            profile.gender,
            profile.age,
            profile.to_dict()
        )
        
        # Add analysis to lab report
        lab_report['analysis'] = analysis
        
        # Add to user profile
        profile.add_lab_report(lab_report)
        profile_manager.save_profiles()
        
        # Translate analysis if needed
        if profile.preferred_language != 'en':
            analysis = language_support.translate_dict(
                analysis,
                'en',
                profile.preferred_language
            )
        
        return jsonify({
            "success": True,
            "lab_report": {
                'id': lab_report['id'],
                'filename': lab_report['filename'],
                'upload_date': lab_report['upload_date'],
                'test_category': lab_report['test_category'],
                'analysis': analysis
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lab-reports', methods=['GET'])
def get_lab_reports():
    """Get all lab reports for a user."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        lab_reports = profile.get_lab_reports()
        
        # Return summary info (not full analysis to keep response small)
        reports_summary = []
        for report in lab_reports:
            reports_summary.append({
                'id': report['id'],
                'filename': report['filename'],
                'upload_date': report['upload_date'],
                'test_category': report['test_category'],
                'overall_status': report.get('analysis', {}).get('overall_status', 'Unknown')
            })
        
        return jsonify({
            "lab_reports": reports_summary,
            "count": len(reports_summary)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lab-report/<report_id>', methods=['GET'])
def get_lab_report_details(report_id):
    """Get detailed analysis of a specific lab report."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        lab_reports = profile.get_lab_reports()
        
        # Find the specific report
        report = next((r for r in lab_reports if r['id'] == report_id), None)
        
        if not report:
            return jsonify({"error": "Lab report not found"}), 404
        
        # Translate if needed
        analysis = report.get('analysis', {})
        if profile.preferred_language != 'en':
            analysis = language_support.translate_dict(
                analysis,
                'en',
                profile.preferred_language
            )
        
        return jsonify({
            "lab_report": {
                'id': report['id'],
                'filename': report['filename'],
                'upload_date': report['upload_date'],
                'test_category': report['test_category'],
                'analysis': analysis
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lab-report/<report_id>', methods=['DELETE'])
def delete_lab_report(report_id):
    """Delete a lab report."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        
        # Delete from profile
        if profile.delete_lab_report(report_id):
            # Delete the file
            lab_test_handler.delete_lab_report(report_id, user_id)
            profile_manager.save_profiles()
            
            return jsonify({
                "success": True,
                "message": "Lab report deleted successfully"
            })
        else:
            return jsonify({"error": "Lab report not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lab-test-chat', methods=['POST'])
def lab_test_chat():
    """Dedicated chat endpoint for lab test questions."""
    if not rag_engine:
        return jsonify({"error": "RAG Engine not initialized"}), 500
    
    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 'default')
    report_id = data.get('report_id')  # Optional: specific report context
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        profile = profile_manager.get_profile(user_id)
        user_language = profile.preferred_language
        
        # Translate message to English if needed
        message_in_english = language_support.translate_to_english(
            user_message,
            user_language
        )
        
        # Build context from lab reports
        lab_context = ""
        if report_id:
            # Get specific report
            lab_reports = profile.get_lab_reports()
            report = next((r for r in lab_reports if r['id'] == report_id), None)
            if report:
                lab_context = f"\n\nUser's Lab Test ({report['test_category']}):\n"
                analysis = report.get('analysis', {})
                for param in analysis.get('parameters', []):
                    lab_context += f"- {param['name']}: {param['value']} {param['unit']} (Normal: {param['normal_range']}) - {param['status']}\n"
        else:
            # Use most recent report
            lab_reports = profile.get_lab_reports()
            if lab_reports:
                recent_report = lab_reports[-1]
                lab_context = f"\n\nUser's Most Recent Lab Test ({recent_report['test_category']}):\n"
                analysis = recent_report.get('analysis', {})
                for param in analysis.get('parameters', []):
                    lab_context += f"- {param['name']}: {param['value']} {param['unit']} (Normal: {param['normal_range']}) - {param['status']}\n"
        
        # Generate response
        response_in_english = rag_engine.generate_response(
            message_in_english,
            profile.to_context_string() + lab_context,
            conversation_history=profile.chat_history
        )
        
        # Translate back
        response = language_support.translate_from_english(
            response_in_english,
            user_language
        )
        
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/challenges', methods=['GET'])
def get_challenges():
    """Get all challenges and user status."""
    user_id = request.args.get('user_id', 'default')
    
    try:
        profile = profile_manager.get_profile(user_id)
        all_challenges = challenges_manager.get_all_challenges()
        
        # Enrich with user status
        active_challenges = profile.challenges.get('active', {})
        completed_history = profile.challenges.get('completed_history', [])
        completed_ids = [c['id'] for c in completed_history]
        
        enriched_challenges = []
        for challenge in all_challenges:
            c_data = challenge.copy()
            c_id = c_data['id']
            
            if c_id in active_challenges:
                c_data['status'] = 'active'
                c_data['progress'] = active_challenges[c_id]
            elif c_id in completed_ids:
                c_data['status'] = 'completed'
            else:
                c_data['status'] = 'available'
                
            enriched_challenges.append(c_data)
            
        return jsonify({
            "challenges": enriched_challenges,
            "user_stats": {
                "points": profile.challenges.get('points', 0),
                "badges": profile.challenges.get('badges', []),
                "active_count": len(active_challenges),
                "completed_count": len(completed_history)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/challenges/join', methods=['POST'])
def join_challenge():
    """Join a challenge."""
    data = request.json
    user_id = data.get('user_id', 'default')
    challenge_id = data.get('challenge_id')
    
    try:
        profile = profile_manager.get_profile(user_id)
        result = challenges_manager.join_challenge(profile, challenge_id)
        
        if result['success']:
            profile_manager.save_profiles()
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/challenges/leave', methods=['POST'])
def leave_challenge():
    """Leave a challenge."""
    data = request.json
    user_id = data.get('user_id', 'default')
    challenge_id = data.get('challenge_id')
    
    try:
        profile = profile_manager.get_profile(user_id)
        result = challenges_manager.leave_challenge(profile, challenge_id)
        
        if result['success']:
            profile_manager.save_profiles()
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/challenges/log', methods=['POST'])
def log_challenge_progress():
    """Log daily progress for a challenge."""
    data = request.json
    user_id = data.get('user_id', 'default')
    challenge_id = data.get('challenge_id')
    
    try:
        profile = profile_manager.get_profile(user_id)
        result = challenges_manager.log_progress(profile, challenge_id)
        
        if result['success']:
            profile_manager.save_profiles()
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=5000)
