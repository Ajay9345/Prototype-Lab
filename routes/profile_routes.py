from flask import Blueprint, request, jsonify
from flask import current_app as app

profile_bp = Blueprint("profile", __name__)


def _services():
    return app.config["SERVICES"]


@profile_bp.route("/profile", methods=["GET"])
def get_profile():
    svc = _services()
    user_id = request.args.get("user_id", "default")
    profile = svc["profile_manager"].get_profile(user_id)
    return jsonify(profile.to_dict())


@profile_bp.route("/profile", methods=["POST"])
def update_profile():
    svc = _services()
    data = request.json

    try:
        user_id = data.get("user_id", "default")
        profile = svc["profile_manager"].get_profile(user_id)

        updatable_fields = ["age", "conditions", "allergies", "medications", "goals"]
        for field in updatable_fields:
            if field in data:
                setattr(profile, field, data[field])

        svc["profile_manager"].save_profiles()
        return jsonify({"success": True, "profile": profile.to_dict()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@profile_bp.route("/stats", methods=["GET"])
def get_stats():
    svc = _services()
    user_id = request.args.get("user_id", "default")
    profile = svc["profile_manager"].get_profile(user_id)
    return jsonify(profile.get_statistics())


@profile_bp.route("/settings", methods=["GET"])
def get_settings():
    svc = _services()
    user_id = request.args.get("user_id", "default")
    profile = svc["profile_manager"].get_profile(user_id)
    return jsonify(profile.settings)


@profile_bp.route("/settings", methods=["POST"])
def update_settings():
    svc = _services()
    data = request.json

    user_id = data.get("user_id", "default")
    profile = svc["profile_manager"].get_profile(user_id)
    profile.settings.update(data.get("settings", {}))
    svc["profile_manager"].save_profiles()

    return jsonify({"success": True, "settings": profile.settings})


@profile_bp.route("/clear-history", methods=["POST"])
def clear_history():
    svc = _services()
    data = request.json
    user_id = data.get("user_id", "default")

    profile = svc["profile_manager"].get_profile(user_id)
    profile.clear_chat_history()
    svc["profile_manager"].save_profiles()

    return jsonify({"success": True, "message": "Chat history cleared"})
