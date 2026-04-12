import os
from flask import Blueprint, request, jsonify
from flask import current_app as app
from utils.helpers import is_allowed_file, save_temp_image, remove_file_if_exists

records_bp = Blueprint("records", __name__)

FILE_ERROR_MSG = "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP"


def _services():
    return app.config["SERVICES"]


@records_bp.route("/upload-prescription", methods=["POST"])
def upload_prescription():
    svc = _services()
    user_id = request.form.get("user_id", "default")

    file = _get_uploaded_file(request, "prescription")
    if isinstance(file, tuple):
        return file

    try:
        prescription = svc["prescription_handler"].process_prescription(file, user_id)

        profile = svc["profile_manager"].get_profile(user_id)
        profile.add_prescription(prescription)
        svc["profile_manager"].save_profiles()

        safety_check = svc["medication_safety"].check_interactions(
            prescription.get("medications", []),
            profile.to_dict(),
        )

        return jsonify({"success": True, "prescription": prescription, "safety_check": safety_check})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/prescriptions", methods=["GET"])
def get_prescriptions():
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        prescriptions = profile.get_prescriptions()
        return jsonify({"prescriptions": prescriptions, "count": len(prescriptions)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/prescription/<prescription_id>", methods=["DELETE"])
def delete_prescription(prescription_id):
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        if profile.delete_prescription(prescription_id):
            svc["prescription_handler"].delete_prescription(prescription_id, user_id)
            svc["profile_manager"].save_profiles()
            return jsonify({"success": True, "message": "Prescription deleted successfully"})
        return jsonify({"error": "Prescription not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/upload-lab-report", methods=["POST"])
def upload_lab_report():
    svc = _services()
    user_id = request.form.get("user_id", "default")

    file = _get_uploaded_file(request, "lab_report")
    if isinstance(file, tuple):
        return file

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        lab_report = svc["lab_test_handler"].process_lab_report(file, user_id, profile.gender)

        analysis = svc["lab_test_analyzer"].analyze_lab_report(
            lab_report["test_values"],
            lab_report["test_category"],
            profile.gender,
            profile.age,
            profile.to_dict(),
        )
        lab_report["analysis"] = analysis

        profile.add_lab_report(lab_report)
        svc["profile_manager"].save_profiles()

        if profile.preferred_language != "en":
            analysis = svc["language_support"].translate_dict(analysis, "en", profile.preferred_language)

        return jsonify({
            "success": True,
            "lab_report": {
                "id":            lab_report["id"],
                "filename":      lab_report["filename"],
                "upload_date":   lab_report["upload_date"],
                "test_category": lab_report["test_category"],
                "analysis":      analysis,
            },
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/lab-reports", methods=["GET"])
def get_lab_reports():
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        lab_reports = profile.get_lab_reports()

        summaries = [
            {
                "id":             r["id"],
                "filename":       r["filename"],
                "upload_date":    r["upload_date"],
                "test_category":  r["test_category"],
                "overall_status": r.get("analysis", {}).get("overall_status", "Unknown"),
            }
            for r in lab_reports
        ]
        return jsonify({"lab_reports": summaries, "count": len(summaries)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/lab-report/<report_id>", methods=["GET"])
def get_lab_report_details(report_id):
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        report = next((r for r in profile.get_lab_reports() if r["id"] == report_id), None)

        if not report:
            return jsonify({"error": "Lab report not found"}), 404

        analysis = report.get("analysis", {})
        if profile.preferred_language != "en":
            analysis = svc["language_support"].translate_dict(analysis, "en", profile.preferred_language)

        return jsonify({
            "lab_report": {
                "id":            report["id"],
                "filename":      report["filename"],
                "upload_date":   report["upload_date"],
                "test_category": report["test_category"],
                "analysis":      analysis,
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/lab-report/<report_id>", methods=["DELETE"])
def delete_lab_report(report_id):
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        if profile.delete_lab_report(report_id):
            svc["lab_test_handler"].delete_lab_report(report_id, user_id)
            svc["profile_manager"].save_profiles()
            return jsonify({"success": True, "message": "Lab report deleted successfully"})
        return jsonify({"error": "Lab report not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@records_bp.route("/lab-trends", methods=["GET"])
def get_lab_trends():
    svc = _services()
    user_id = request.args.get("user_id", "default")

    try:
        profile = svc["profile_manager"].get_profile(user_id)
        lab_reports = profile.get_lab_reports()

        if not lab_reports:
            return jsonify({"trends": {}, "message": "No lab reports found for trend analysis."})

        trends = svc["lab_test_analyzer"].get_parameter_trends(lab_reports)
        return jsonify({"trends": trends, "count": len(lab_reports)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _get_uploaded_file(req, field_name: str):
    if field_name not in req.files:
        return jsonify({"error": "No file provided"}), 400

    file = req.files[field_name]

    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    if not is_allowed_file(file.filename):
        return jsonify({"error": FILE_ERROR_MSG}), 400

    return file
