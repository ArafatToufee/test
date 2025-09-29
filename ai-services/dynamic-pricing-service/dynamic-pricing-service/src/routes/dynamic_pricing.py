from flask import Blueprint, jsonify

dynamic_pricing_bp = Blueprint("dynamic_pricing", __name__)

@dynamic_pricing_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

