import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from routes.product import product_bp

app = Flask(__name__)

# 配置
app.config["SECRET_KEY"] = "ecommerce-platform-product-secret-key-2025"

# 启用CORS
CORS(app, origins="*")

# 注册蓝图
app.register_blueprint(product_bp, url_prefix="/")

@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy", "service": "product-service"}, 200

@app.route("/", methods=["GET"])
def index():
    return {"message": "Product Service is running", "service": "product-service"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


