from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import sqlite3
import os
import random
from src.routes.auth import token_required, permission_required

admin_bp = Blueprint('admin', __name__)

# Mock data for demonstration
def get_mock_analytics():
    """Generate mock analytics data"""
    return {
        "total_users": 15847,
        "total_sellers": 2341,
        "total_orders": 8923,
        "total_revenue": 1247893.45,
        "monthly_growth": 12.5,
        "active_users_today": 1234,
        "pending_orders": 156,
        "refund_requests": 23
    }

def get_mock_users():
    """Generate mock user data"""
    users = []
    for i in range(1, 21):
        users.append({
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "status": random.choice(["active", "inactive", "suspended"]),
            "registration_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "total_orders": random.randint(0, 50),
            "total_spent": round(random.uniform(0, 5000), 2)
        })
    return users

def get_mock_sellers():
    """Generate mock seller data"""
    sellers = []
    for i in range(1, 16):
        sellers.append({
            "id": i,
            "name": f"Seller {i}",
            "email": f"seller{i}@example.com",
            "status": random.choice(["active", "pending", "suspended"]),
            "registration_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "total_products": random.randint(1, 100),
            "total_sales": round(random.uniform(1000, 50000), 2),
            "commission_rate": round(random.uniform(5, 15), 1)
        })
    return sellers

def get_mock_orders():
    """Generate mock order data"""
    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled", "refunded"]
    for i in range(1, 26):
        orders.append({
            "id": f"ORD{i:04d}",
            "customer_name": f"Customer {i}",
            "seller_name": f"Seller {random.randint(1, 15)}",
            "amount": round(random.uniform(20, 500), 2),
            "status": random.choice(statuses),
            "order_date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M"),
            "items_count": random.randint(1, 5)
        })
    return orders

def get_mock_products():
    """Generate mock product data"""
    products = []
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Beauty"]
    for i in range(1, 31):
        products.append({
            "id": i,
            "name": f"Product {i}",
            "category": random.choice(categories),
            "seller_name": f"Seller {random.randint(1, 15)}",
            "price": round(random.uniform(10, 1000), 2),
            "stock": random.randint(0, 100),
            "status": random.choice(["active", "inactive", "out_of_stock"]),
            "created_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
        })
    return products

@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@permission_required('view_dashboard')
def get_dashboard(current_user):
    """Get dashboard analytics"""
    try:
        analytics = get_mock_analytics()
        return jsonify({
            "success": True,
            "data": analytics
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching dashboard data: {str(e)}"
        }), 500

@admin_bp.route('/users', methods=['GET'])
@token_required
@permission_required('view_users')
def get_users(current_user):
    """Get all users with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        
        users = get_mock_users()
        
        # Filter by search if provided
        if search:
            users = [user for user in users if search.lower() in user['name'].lower() or search.lower() in user['email'].lower()]
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_users = users[start:end]
        
        return jsonify({
            "success": True,
            "data": {
                "users": paginated_users,
                "total": len(users),
                "page": page,
                "limit": limit,
                "total_pages": (len(users) + limit - 1) // limit
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching users: {str(e)}"
        }), 500

@admin_bp.route('/sellers', methods=['GET'])
@token_required
@permission_required('manage_sellers')
def get_sellers(current_user):
    """Get all sellers with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        
        sellers = get_mock_sellers()
        
        # Filter by search if provided
        if search:
            sellers = [seller for seller in sellers if search.lower() in seller['name'].lower() or search.lower() in seller['email'].lower()]
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_sellers = sellers[start:end]
        
        return jsonify({
            "success": True,
            "data": {
                "sellers": paginated_sellers,
                "total": len(sellers),
                "page": page,
                "limit": limit,
                "total_pages": (len(sellers) + limit - 1) // limit
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching sellers: {str(e)}"
        }), 500

@admin_bp.route('/orders', methods=['GET'])
@token_required
@permission_required('manage_orders')
def get_orders(current_user):
    """Get all orders with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        status = request.args.get('status', '')
        
        orders = get_mock_orders()
        
        # Filter by status if provided
        if status:
            orders = [order for order in orders if order['status'] == status]
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_orders = orders[start:end]
        
        return jsonify({
            "success": True,
            "data": {
                "orders": paginated_orders,
                "total": len(orders),
                "page": page,
                "limit": limit,
                "total_pages": (len(orders) + limit - 1) // limit
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching orders: {str(e)}"
        }), 500

@admin_bp.route('/products', methods=['GET'])
@token_required
@permission_required('view_products')
def get_products(current_user):
    """Get all products with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        category = request.args.get('category', '')
        
        products = get_mock_products()
        
        # Filter by category if provided
        if category:
            products = [product for product in products if product['category'] == category]
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_products = products[start:end]
        
        return jsonify({
            "success": True,
            "data": {
                "products": paginated_products,
                "total": len(products),
                "page": page,
                "limit": limit,
                "total_pages": (len(products) + limit - 1) // limit
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching products: {str(e)}"
        }), 500

@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@token_required
@permission_required('manage_users')
def update_user_status(current_user, user_id):
    """Update user status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['active', 'inactive', 'suspended']:
            return jsonify({
                "success": False,
                "message": "Invalid status. Must be 'active', 'inactive', or 'suspended'"
            }), 400
        
        # In a real application, you would update the database here
        return jsonify({
            "success": True,
            "message": f"User {user_id} status updated to {new_status}"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating user status: {str(e)}"
        }), 500

@admin_bp.route('/sellers/<int:seller_id>/status', methods=['PUT'])
@token_required
@permission_required('manage_sellers')
def update_seller_status(current_user, seller_id):
    """Update seller status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['active', 'pending', 'suspended']:
            return jsonify({
                "success": False,
                "message": "Invalid status. Must be 'active', 'pending', or 'suspended'"
            }), 400
        
        # In a real application, you would update the database here
        return jsonify({
            "success": True,
            "message": f"Seller {seller_id} status updated to {new_status}"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating seller status: {str(e)}"
        }), 500

@admin_bp.route('/orders/<order_id>/status', methods=['PUT'])
@token_required
@permission_required('manage_orders')
def update_order_status(current_user, order_id):
    """Update order status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded']
        if new_status not in valid_statuses:
            return jsonify({
                "success": False,
                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            }), 400
        
        # In a real application, you would update the database here
        return jsonify({
            "success": True,
            "message": f"Order {order_id} status updated to {new_status}"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating order status: {str(e)}"
        }), 500

@admin_bp.route('/analytics/revenue', methods=['GET'])
@token_required
@permission_required('view_analytics')
def get_revenue_analytics(current_user):
    """Get revenue analytics"""
    try:
        # Generate mock revenue data for the last 12 months
        months = []
        revenue_data = []
        
        for i in range(12):
            month_date = datetime.now() - timedelta(days=30 * i)
            months.insert(0, month_date.strftime("%Y-%m"))
            revenue_data.insert(0, round(random.uniform(80000, 150000), 2))
        
        return jsonify({
            "success": True,
            "data": {
                "months": months,
                "revenue": revenue_data,
                "total_revenue": sum(revenue_data),
                "average_monthly": round(sum(revenue_data) / len(revenue_data), 2)
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching revenue analytics: {str(e)}"
        }), 500

@admin_bp.route('/analytics/users', methods=['GET'])
@token_required
@permission_required('view_analytics')
def get_user_analytics(current_user):
    """Get user analytics"""
    try:
        # Generate mock user growth data
        months = []
        user_data = []
        
        for i in range(12):
            month_date = datetime.now() - timedelta(days=30 * i)
            months.insert(0, month_date.strftime("%Y-%m"))
            user_data.insert(0, random.randint(800, 1500))
        
        return jsonify({
            "success": True,
            "data": {
                "months": months,
                "new_users": user_data,
                "total_new_users": sum(user_data),
                "average_monthly": round(sum(user_data) / len(user_data), 2)
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching user analytics: {str(e)}"
        }), 500

@admin_bp.route('/reports/sales', methods=['GET'])
@token_required
@permission_required('view_analytics')
def get_sales_report(current_user):
    """Get sales report"""
    try:
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        end_date = request.args.get('end_date', datetime.now().strftime("%Y-%m-%d"))
        
        # Generate mock sales report data
        report_data = {
            "period": f"{start_date} to {end_date}",
            "total_sales": round(random.uniform(50000, 100000), 2),
            "total_orders": random.randint(500, 1000),
            "average_order_value": round(random.uniform(80, 150), 2),
            "top_selling_categories": [
                {"category": "Electronics", "sales": round(random.uniform(15000, 25000), 2)},
                {"category": "Clothing", "sales": round(random.uniform(10000, 20000), 2)},
                {"category": "Home & Garden", "sales": round(random.uniform(8000, 15000), 2)},
                {"category": "Sports", "sales": round(random.uniform(5000, 12000), 2)},
                {"category": "Books", "sales": round(random.uniform(3000, 8000), 2)}
            ],
            "top_sellers": [
                {"seller": "Seller 1", "sales": round(random.uniform(8000, 15000), 2)},
                {"seller": "Seller 3", "sales": round(random.uniform(7000, 12000), 2)},
                {"seller": "Seller 7", "sales": round(random.uniform(6000, 10000), 2)},
                {"seller": "Seller 12", "sales": round(random.uniform(5000, 9000), 2)},
                {"seller": "Seller 5", "sales": round(random.uniform(4000, 8000), 2)}
            ]
        }
        
        return jsonify({
            "success": True,
            "data": report_data
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error generating sales report: {str(e)}"
        }), 500

@admin_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "Admin CRM API is running",
        "timestamp": datetime.now().isoformat()
    }), 200

