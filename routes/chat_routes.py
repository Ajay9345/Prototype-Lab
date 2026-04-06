"""
Chat routes — main conversation endpoint and lab-test chat.
"""
from flask import Blueprint, request, jsonify

chat_bp = Blueprint("chat", __name__)

# Services and managers are injected via app context (set in app.py)
from flask import current_app as app


def _services():
    """Convenience accessor for the shared service container."""
    return app.config["SERVICES"]


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.
    Detects language, checks for emergencies, generates an AI response,
    and runs a proactive medication safety check.
    """
    svc = _services()

    if not svc["rag_engine"]:
        return jsonify({"error": "RAG Engine not initialised. Check server logs."}), 500

    data         = request.json
    user_message = data.get("message")
    user_id      = data.get("user_id", "default")
    user_language = data.get("language")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        profile = svc["profile_manager"].get_profile(user_id)

        # Detect language if not supplied by the client
        if not user_language:
            user_language = svc["language_support"].detect_language(user_message)

        # Persist language preference if it changed
        if user_language != profile.preferred_language:
            profile.preferred_language = user_language
            svc["profile_manager"].save_profiles()

        # Translate to English for processing
        english_message = svc["language_support"].translate_to_english(user_message, user_language)

        # Emergency check — short-circuit with guidance if detected
        if svc["symptom_analyzer"].check_emergency(english_message):
            guidance = svc["emergency_support"].get_emergency_guidance()
            if user_language != "en":
                guidance = svc["language_support"].translate_dict(guidance, "en", user_language)
            return jsonify({
                "response":          "🚨 EMERGENCY DETECTED. Please go to the nearest hospital immediately.",
                "is_emergency":      True,
                "emergency_guidance": guidance,
                "detected_language": user_language,
            })

        # Symptom analysis
        symptom_analysis = svc["symptom_analyzer"].analyze_message(english_message, profile.to_dict())

        # Generate AI response
        english_response = svc["rag_engine"].generate_response(
            english_message,
            profile.to_context_string(),
            conversation_history=profile.chat_history,
        )

        # Translate response back to user's language
        response = svc["language_support"].translate_from_english(english_response, user_language)

        # Translate symptom analysis if needed
        if symptom_analysis and user_language != "en":
            symptom_analysis = svc["language_support"].translate_dict(symptom_analysis, "en", user_language)

        # Save chat interaction
        profile.add_chat_interaction(user_message, response)

        # Ambient distress detection
        distress_detected = svc["emergency_support"].detect_distress_keywords(english_message)

        # Proactive medication safety check
        safety_analysis = None
        med_keywords = ["take", "start", "medication", "drug"]
        if any(kw in english_message.lower() for kw in med_keywords):
            safety_analysis = svc["medication_safety"].check_interactions(
                [english_message], profile.to_dict()
            )

        svc["profile_manager"].save_profiles()

        return jsonify({
            "response":          response,
            "symptom_analysis":  symptom_analysis,
            "safety_analysis":   safety_analysis,
            "distress_detected": distress_detected,
            "detected_language": user_language,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/lab-test-chat", methods=["POST"])
def lab_test_chat():
    """
    Dedicated chat endpoint for questions about a user's lab results.
    Injects the relevant lab report data into the RAG context.
    """
    svc = _services()

    if not svc["rag_engine"]:
        return jsonify({"error": "RAG Engine not initialised"}), 500

    data         = request.json
    user_message = data.get("message")
    user_id      = data.get("user_id", "default")
    report_id    = data.get("report_id")  # optional: focus on a specific report

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        profile       = svc["profile_manager"].get_profile(user_id)
        user_language = profile.preferred_language
        english_msg   = svc["language_support"].translate_to_english(user_message, user_language)

        # Build lab context string from the relevant report
        lab_context = _build_lab_context(profile, report_id)

        english_response = svc["rag_engine"].generate_response(
            english_msg,
            profile.to_context_string() + lab_context,
            conversation_history=profile.chat_history,
        )

        response = svc["language_support"].translate_from_english(english_response, user_language)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _build_lab_context(profile, report_id: str) -> str:
    """
    Build a text block summarising the relevant lab report parameters
    to inject into the RAG prompt.
    """
    lab_reports = profile.get_lab_reports()
    if not lab_reports:
        return ""

    # Use the specified report or fall back to the most recent one
    if report_id:
        report = next((r for r in lab_reports if r["id"] == report_id), None)
    else:
        report = lab_reports[-1]

    if not report:
        return ""

    lines = [f"\n\nUser's Lab Test ({report['test_category']}):"]
    for param in report.get("analysis", {}).get("parameters", []):
        lines.append(
            f"- {param['name']}: {param['value']} {param['unit']} "
            f"(Normal: {param['normal_range']}) — {param['status']}"
        )
    return "\n".join(lines)
