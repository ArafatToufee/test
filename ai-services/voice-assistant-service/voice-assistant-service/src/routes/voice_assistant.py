from flask import Blueprint, jsonify

voice_assistant_bp = Blueprint("voice_assistant", __name__)

@voice_assistant_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

