"""
AI features routes — food scanner, grocery auditor, symptom cam,
digital twin, insurance concierge, and language settings.
"""
import os
from flask import Blueprint, request, jsonify

ai_bp = Blueprint("ai", __name__)

from flask import current_app as app
from utils.helpers import save_temp_image, remove_file_if_exists


def _services():
    return app.config["SERVICES"]


# ── Food & nutrition ──────────────────────────────────────────────────────────

@ai_bp.route("/scan-food", methods=["POST"])
def scan_food():
    """Analyse a food ingredient label photo and return a safety audit."""
    svc     = _services()
    user_id = request.form.get("user_id", "default")

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    temp_path = save_temp_image(request.files["image"], "uploads/nutrition", prefix="food_")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        result  = svc["food_scanner"].audit_food_image(temp_path, profile.to_dict())
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        remove_file_if_exists(temp_path)


@ai_bp.route("/audit-receipt", methods=["POST"])
def audit_receipt():
    """Analyse a grocery receipt photo and return a basket health score."""
    svc     = _services()
    user_id = request.form.get("user_id", "default")

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    temp_path = save_temp_image(request.files["image"], "uploads/nutrition", prefix="receipt_")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        result  = svc["grocery_auditor"].analyze_receipt_image(temp_path, profile.to_dict())
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        remove_file_if_exists(temp_path)


# ── Symptom camera ────────────────────────────────────────────────────────────

@ai_bp.route("/symptom-cam", methods=["POST"])
def symptom_cam_analysis():
    """Analyse a photo of a symptomatic area using vision AI."""
    svc              = _services()
    symptoms_history = request.form.get("symptoms_history", "")

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    temp_path = save_temp_image(request.files["image"], "uploads/symptoms", prefix="temp_")

    try:
        result = svc["symptom_cam"].analyze_symptom_image(temp_path, symptoms_history)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        remove_file_if_exists(temp_path)


# ── Digital twin ──────────────────────────────────────────────────────────────

@ai_bp.route("/simulate-health", methods=["POST"])
def simulate_health():
    """Simulate health outcomes for a 'What If' lifestyle scenario."""
    svc  = _services()
    data = request.json

    user_id  = data.get("user_id", "default")
    scenario = data.get("scenario")

    if not scenario:
        return jsonify({"error": "No scenario provided"}), 400

    try:
        profile    = svc["profile_manager"].get_profile(user_id)
        simulation = svc["digital_twin"].simulate_outcome(profile.to_dict(), scenario)
        return jsonify(simulation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Insurance concierge ───────────────────────────────────────────────────────

@ai_bp.route("/insurance-check", methods=["POST"])
def insurance_check():
    """Audit an insurance policy for coverage of a specific treatment."""
    svc         = _services()
    policy_text = request.form.get("policy_text")
    treatment   = request.form.get("treatment")

    if not policy_text or not treatment:
        return jsonify({"error": "Policy text and treatment name are required"}), 400

    try:
        result = svc["insurance_concierge"].analyze_coverage(policy_text, treatment)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Language settings ─────────────────────────────────────────────────────────

@ai_bp.route("/supported-languages", methods=["GET"])
def get_supported_languages():
    """Return all supported languages with metadata."""
    svc = _services()
    try:
        return jsonify({"languages": svc["language_support"].get_supported_languages()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_bp.route("/set-language", methods=["POST"])
def set_language():
    """Set the preferred language for a user."""
    svc  = _services()
    data = request.json

    user_id  = data.get("user_id", "default")
    language = data.get("language", "en")

    try:
        if not svc["language_support"].is_supported_language(language):
            return jsonify({"error": "Unsupported language"}), 400

        profile = svc["profile_manager"].get_profile(user_id)
        profile.preferred_language = language
        svc["profile_manager"].save_profiles()

        return jsonify({
            "success":       True,
            "language":      language,
            "language_name": svc["language_support"].get_language_name(language),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_bp.route("/get-language", methods=["GET"])
def get_language():
    """Return the current language preference for a user."""
    svc     = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        lang    = profile.preferred_language
        return jsonify({
            "language":      lang,
            "language_name": svc["language_support"].get_language_name(lang),
            "native_name":   svc["language_support"].get_native_name(lang),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Challenges ────────────────────────────────────────────────────────────────

@ai_bp.route("/challenges", methods=["GET"])
def get_challenges():
    """Return all challenges enriched with the user's current status."""
    svc     = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile           = svc["profile_manager"].get_profile(user_id)
        all_challenges    = svc["challenges_manager"].get_all_challenges()
        active            = profile.challenges.get("active", {})
        completed_history = profile.challenges.get("completed_history", [])
        completed_ids     = {c["id"] for c in completed_history}

        enriched = []
        for challenge in all_challenges:
            c = dict(challenge)
            cid = c["id"]
            if cid in active:
                c["status"]   = "active"
                c["progress"] = active[cid]
            elif cid in completed_ids:
                c["status"] = "completed"
            else:
                c["status"] = "available"
            enriched.append(c)

        return jsonify({
            "challenges": enriched,
            "user_stats": {
                "points":          profile.challenges.get("points", 0),
                "badges":          profile.challenges.get("badges", []),
                "active_count":    len(active),
                "completed_count": len(completed_history),
            },
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_bp.route("/challenges/join", methods=["POST"])
def join_challenge():
    """Join a health challenge."""
    svc  = _services()
    data = request.json

    user_id      = data.get("user_id", "default")
    challenge_id = data.get("challenge_id")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        result  = svc["challenges_manager"].join_challenge(profile, challenge_id)
        if result["success"]:
            svc["profile_manager"].save_profiles()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_bp.route("/challenges/leave", methods=["POST"])
def leave_challenge():
    """Leave an active health challenge."""
    svc  = _services()
    data = request.json

    user_id      = data.get("user_id", "default")
    challenge_id = data.get("challenge_id")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        result  = svc["challenges_manager"].leave_challenge(profile, challenge_id)
        if result["success"]:
            svc["profile_manager"].save_profiles()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_bp.route("/challenges/log", methods=["POST"])
def log_challenge_progress():
    """Log one day of progress for an active challenge."""
    svc  = _services()
    data = request.json

    user_id      = data.get("user_id", "default")
    challenge_id = data.get("challenge_id")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        result  = svc["challenges_manager"].log_progress(profile, challenge_id)
        if result["success"]:
            svc["profile_manager"].save_profiles()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
