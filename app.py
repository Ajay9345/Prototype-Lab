"""
app.py — Application entry point.

Initialises all services, registers Flask Blueprints, and starts the server.
Run with:  python app.py
"""
import os
from flask import Flask, render_template

# ── Core engine ───────────────────────────────────────────────────────────────
from core.rag_engine import RAGEngine

# ── Data model ────────────────────────────────────────────────────────────────
from models.user_profile import ProfileManager

# ── Feature services ──────────────────────────────────────────────────────────
from services.symptom_analyzer    import get_symptom_analyzer
from services.emergency_support   import get_emergency_support
from services.wellness_guide      import get_wellness_guide
from services.prescription_handler import get_prescription_handler
from services.language_support    import get_language_support
from services.lab_test_handler    import get_lab_test_handler
from services.lab_test_analyzer   import get_lab_test_analyzer
from services.challenges_manager  import get_challenges_manager
from services.medication_safety   import get_medication_safety_checker
from services.environmental_sync  import get_environmental_sync
from services.food_safety_scanner import get_food_safety_scanner
from services.grocery_auditor     import get_grocery_auditor
from services.triage_engine       import get_triage_engine
from services.symptom_cam_analyzer import get_symptom_cam_analyzer
from services.digital_twin        import get_digital_twin
from services.insurance_concierge import get_insurance_concierge
from services.first_aid_guide     import get_first_aid_guide

# ── Route Blueprints ──────────────────────────────────────────────────────────
from routes.chat_routes    import chat_bp
from routes.profile_routes import profile_bp
from routes.health_routes  import health_bp
from routes.records_routes import records_bp
from routes.ai_routes      import ai_bp

# ── Configuration ─────────────────────────────────────────────────────────────
UPLOAD_FOLDER    = "uploads/prescriptions"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


def create_app() -> Flask:
    """
    Application factory.

    Creates the Flask app, initialises all services, stores them in
    app.config["SERVICES"] so Blueprints can access them via current_app,
    and registers all route Blueprints.
    """
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"]      = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

    # ── Initialise RAG engine (may fail if FAISS index is missing) ────────────
    rag_engine = None
    try:
        rag_engine = RAGEngine()
    except Exception as e:
        print(f"Warning: RAG Engine not initialised — {e}")

    # ── Bundle all services into a single dict for easy Blueprint access ──────
    app.config["SERVICES"] = {
        "rag_engine":           rag_engine,
        "profile_manager":      ProfileManager(),
        "symptom_analyzer":     get_symptom_analyzer(),
        "emergency_support":    get_emergency_support(),
        "wellness_guide":       get_wellness_guide(),
        "prescription_handler": get_prescription_handler(),
        "language_support":     get_language_support(),
        "lab_test_handler":     get_lab_test_handler(),
        "lab_test_analyzer":    get_lab_test_analyzer(),
        "challenges_manager":   get_challenges_manager(),
        "medication_safety":    get_medication_safety_checker(),
        "env_sync":             get_environmental_sync(),
        "food_scanner":         get_food_safety_scanner(),
        "grocery_auditor":      get_grocery_auditor(),
        "triage_engine":        get_triage_engine(),
        "symptom_cam":          get_symptom_cam_analyzer(),
        "digital_twin":         get_digital_twin(),
        "insurance_concierge":  get_insurance_concierge(),
        "first_aid":            get_first_aid_guide(),
    }

    # ── Register Blueprints ───────────────────────────────────────────────────
    app.register_blueprint(chat_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(ai_bp)

    # ── Home route ────────────────────────────────────────────────────────────
    @app.route("/")
    def home():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    flask_app = create_app()
    flask_app.run(debug=True, port=5000)
