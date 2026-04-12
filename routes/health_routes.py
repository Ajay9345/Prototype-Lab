from flask import Blueprint, request, jsonify
from flask import current_app as app

health_bp = Blueprint("health", __name__)


def _services():
    return app.config["SERVICES"]


@health_bp.route("/analyze-symptoms", methods=["POST"])
def analyze_symptoms():
    svc = _services()
    data = request.json

    message = data.get("message")
    user_id = data.get("user_id", "default")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        analysis = svc["symptom_analyzer"].analyze_message(message, profile.to_dict())
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/emergency-check", methods=["POST"])
def emergency_check():
    svc = _services()
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        is_emergency = svc["symptom_analyzer"].check_emergency(message)
        if is_emergency:
            guidance = svc["emergency_support"].get_emergency_guidance()
            return jsonify({"is_emergency": True, "guidance": guidance})
        return jsonify({"is_emergency": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/nearby-hospitals", methods=["GET"])
def nearby_hospitals():
    svc = _services()
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        max_results = int(request.args.get("max_results", 5))
        hospitals = svc["emergency_support"].find_nearby_hospitals(lat, lon, max_results)
        return jsonify({"hospitals": hospitals, "count": len(hospitals)})
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid coordinates provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/nearby-pharmacies", methods=["GET"])
def nearby_pharmacies():
    svc = _services()
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        max_results = int(request.args.get("max_results", 5))
        pharmacies = svc["emergency_support"].find_nearby_pharmacies(lat, lon, max_results)
        return jsonify({"pharmacies": pharmacies, "count": len(pharmacies)})
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid coordinates provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/emergency-contacts", methods=["GET"])
def emergency_contacts():
    svc = _services()
    try:
        contacts = svc["emergency_support"].get_emergency_contacts()
        return jsonify({"contacts": contacts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/wellness-tips", methods=["GET"])
def wellness_tips():
    svc = _services()
    user_id = request.args.get("user_id", "default")
    count = int(request.args.get("count", 5))

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        tips = svc["wellness_guide"].get_personalized_tips(profile.to_dict(), count)
        return jsonify({"tips": tips, "count": len(tips)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/daily-tip", methods=["GET"])
def daily_tip():
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        tip = svc["wellness_guide"].get_daily_wellness_tip(profile.to_dict())
        return jsonify({"tip": tip})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/proactive-alerts", methods=["GET"])
def proactive_alerts():
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        lat, lon = request.args.get("lat"), request.args.get("lon")

        env_data = None
        if lat and lon:
            env_data = svc["env_sync"].get_environmental_data(float(lat), float(lon))

        alerts = svc["wellness_guide"].get_proactive_alerts(profile.to_dict(), env_data)
        return jsonify({
            "alerts":                alerts,
            "count":                 len(alerts),
            "environmental_context": env_data or "No location provided",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/self-care", methods=["GET"])
def self_care():
    svc = _services()
    category = request.args.get("category")
    risk_level = request.args.get("risk_level")

    try:
        recs = svc["wellness_guide"].get_self_care_recommendations(category, risk_level)
        return jsonify({"recommendations": recs, "count": len(recs)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/triage", methods=["POST"])
def triage():
    svc = _services()
    data = request.json

    user_id = data.get("user_id", "default")
    symptom_analysis = data.get("symptom_analysis")

    if not symptom_analysis:
        return jsonify({"error": "No symptom analysis provided"}), 400

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        triage_report = svc["triage_engine"].conduct_triage(symptom_analysis, profile.to_dict())
        return jsonify(triage_report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@health_bp.route("/first-aid", methods=["GET"])
def get_first_aid():
    svc = _services()
    emergency_type = request.args.get("type", "general")
    steps = svc["first_aid"].get_step_by_step(emergency_type)
    return jsonify({"emergency_type": emergency_type, "steps": steps})
