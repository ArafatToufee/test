import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from src.models.order import db
from src.routes.order import order_bp

app = Flask(__name__)

# 配置
app.config["SECRET_KEY"] = "ecommerce-platform-order-secret-key-2025"

# 启用CORS
CORS(app, origins="*")

# 注册蓝图
app.register_blueprint(order_bp, url_prefix="/orders")

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy", "service": "order-service"}, 200

@app.route("/", methods=["GET"])
def index():
    return {"message": "Order Service is running", "service": "order-service"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
