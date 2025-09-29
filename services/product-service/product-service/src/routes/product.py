from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime

product_bp = Blueprint("product", __name__)

# In-memory storage for demo purposes (in production, use a database)
products = {}

@product_bp.route("/", methods=["GET"])
def get_products():
    """Get all products with optional filtering"""
    category = request.args.get('category')
    search = request.args.get('search')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    filtered_products = list(products.values())
    
    if category:
        filtered_products = [p for p in filtered_products if p.get('category', '').lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        filtered_products = [p for p in filtered_products 
                           if search_lower in p.get('name', '').lower() 
                           or search_lower in p.get('description', '').lower()]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.get('price', 0) >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p.get('price', 0) <= max_price]
    
    return jsonify({
        "products": filtered_products,
        "total": len(filtered_products)
    }), 200

@product_bp.route("/", methods=["POST"])
def create_product():
    """Create a new product"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required_fields = ['name', 'price', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    product_id = str(uuid.uuid4())
    product = {
        "id": product_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "price": float(data["price"]),
        "category": data["category"],
        "stock_quantity": data.get("stock_quantity", 0),
        "image_url": data.get("image_url", ""),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    products[product_id] = product
    
    return jsonify(product), 201

@product_bp.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    """Get a specific product by ID"""
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(products[product_id]), 200

@product_bp.route("/<product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a specific product"""
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    product = products[product_id]
    
    # Update allowed fields
    updatable_fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'image_url']
    for field in updatable_fields:
        if field in data:
            if field == 'price':
                product[field] = float(data[field])
            else:
                product[field] = data[field]
    
    product["updated_at"] = datetime.utcnow().isoformat()
    
    return jsonify(product), 200

@product_bp.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a specific product"""
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404
    
    deleted_product = products.pop(product_id)
    
    return jsonify({
        "message": "Product deleted successfully",
        "deleted_product": deleted_product
    }), 200

@product_bp.route("/categories", methods=["GET"])
def get_categories():
    """Get all unique product categories"""
    categories = list(set(p.get('category', '') for p in products.values() if p.get('category')))
    return jsonify({"categories": categories}), 200

@product_bp.route("/search", methods=["GET"])
def search_products():
    """Advanced product search"""
    query = request.args.get('q', '')
    category = request.args.get('category')
    sort_by = request.args.get('sort_by', 'name')  # name, price, created_at
    sort_order = request.args.get('sort_order', 'asc')  # asc, desc
    
    filtered_products = list(products.values())
    
    if query:
        query_lower = query.lower()
        filtered_products = [p for p in filtered_products 
                           if query_lower in p.get('name', '').lower() 
                           or query_lower in p.get('description', '').lower()]
    
    if category:
        filtered_products = [p for p in filtered_products if p.get('category', '').lower() == category.lower()]
    
    # Sort products
    reverse = sort_order == 'desc'
    if sort_by in ['name', 'category']:
        filtered_products.sort(key=lambda x: x.get(sort_by, '').lower(), reverse=reverse)
    elif sort_by in ['price', 'stock_quantity']:
        filtered_products.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    elif sort_by == 'created_at':
        filtered_products.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
    
    return jsonify({
        "products": filtered_products,
        "total": len(filtered_products),
        "query": query,
        "category": category,
        "sort_by": sort_by,
        "sort_order": sort_order
    }), 200


