from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# 配置
app.config["SECRET_KEY"] = "ecommerce-platform-api-gateway-secret-key-2025"

# 启用CORS
CORS(app, origins="*")

def proxy_request(service_url_env, method, path, json_data=None):
    base_url = os.getenv(service_url_env)
    if not base_url:
        return jsonify({"error": f"Service URL not configured: {service_url_env}"}), 500

    url = f"{base_url}{path}"
    try:
        if method == "GET":
            resp = requests.get(url, params=request.args)
        elif method == "POST":
            resp = requests.post(url, json=json_data)
        elif method == "PUT":
            resp = requests.put(url, json=json_data)
        elif method == "DELETE":
            resp = requests.delete(url)
        else:
            return jsonify({"error": "Method not allowed"}), 405

        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Service unavailable: {str(e)}"}), 503

@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy", "service": "api-gateway"}, 200

@app.route("/", methods=["GET"])
def index():
    return {"message": "API Gateway is running", "service": "api-gateway"}, 200

# Product Service routes
@app.route("/products", methods=["GET", "POST"])
@app.route("/products/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def product_service_proxy(path=""):
    if path:
        return proxy_request("PRODUCT_SERVICE_URL", request.method, f"/{path}", request.get_json())
    else:
        return proxy_request("PRODUCT_SERVICE_URL", request.method, "/", request.get_json())


# Auth Service routes
@app.route("/auth/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def auth_service_proxy(path):
    return proxy_request("AUTH_SERVICE_URL", request.method, f"/auth/{path}", request.get_json())





# Cart Service routes
@app.route("/cart", methods=["GET", "POST"])
@app.route("/cart/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def cart_service_proxy(path=""):
    return proxy_request("CART_SERVICE_URL", request.method, f"/cart/{path}", request.get_json())





# Order Service routes
@app.route("/orders", methods=["GET", "POST"])
@app.route("/orders/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def order_service_proxy(path=""):
    return proxy_request("ORDER_SERVICE_URL", request.method, f"/orders/{path}", request.get_json())





# Payment Service routes
@app.route("/payments", methods=["GET", "POST"])
@app.route("/payments/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def payment_service_proxy(path=""):
    return proxy_request("PAYMENT_SERVICE_URL", request.method, f"/payments/{path}", request.get_json())





# Recommendation Service routes
@app.route("/recommendations", methods=["GET", "POST"])
@app.route("/recommendations/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def recommendation_service_proxy(path=""):
    return proxy_request("RECOMMENDATION_SERVICE_URL", request.method, f"/recommendations/{path}", request.get_json())





# Visual Search Service routes
@app.route("/visual-search", methods=["GET", "POST"])
@app.route("/visual-search/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def visual_search_service_proxy(path=""):
    return proxy_request("VISUAL_SEARCH_SERVICE_URL", request.method, f"/visual-search/{path}", request.get_json())





# Fraud Detection Service routes
@app.route("/fraud-detection", methods=["GET", "POST"])
@app.route("/fraud-detection/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def fraud_detection_service_proxy(path=""):
    return proxy_request("FRAUD_DETECTION_SERVICE_URL", request.method, f"/fraud-detection/{path}", request.get_json())





# Voice Assistant Service routes
@app.route("/voice-assistant", methods=["GET", "POST"])
@app.route("/voice-assistant/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def voice_assistant_service_proxy(path=""):
    return proxy_request("VOICE_ASSISTANT_SERVICE_URL", request.method, f"/voice-assistant/{path}", request.get_json())





# Dynamic Pricing Service routes
@app.route("/dynamic-pricing", methods=["GET", "POST"])
@app.route("/dynamic-pricing/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def dynamic_pricing_service_proxy(path=""):
    return proxy_request("DYNAMIC_PRICING_SERVICE_URL", request.method, f"/dynamic-pricing/{path}", request.get_json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


