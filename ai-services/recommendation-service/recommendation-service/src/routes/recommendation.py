from flask import Blueprint, jsonify, request
import random
import json
from datetime import datetime, timedelta

recommendation_bp = Blueprint("recommendation", __name__)

# Sample product data for recommendations
SAMPLE_PRODUCTS = [
    {
        "id": "prod-1",
        "name": "Wireless Headphones",
        "price": 199.99,
        "category": "Electronics",
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",
        "tags": ["audio", "wireless", "music", "noise-cancelling"]
    },
    {
        "id": "prod-2",
        "name": "Smartphone",
        "price": 799.99,
        "category": "Electronics",
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop",
        "tags": ["mobile", "communication", "camera", "apps"]
    },
    {
        "id": "prod-3",
        "name": "Running Shoes",
        "price": 129.99,
        "category": "Sports",
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop",
        "tags": ["fitness", "running", "comfort", "athletic"]
    },
    {
        "id": "prod-4",
        "name": "Coffee Maker",
        "price": 89.99,
        "category": "Home & Kitchen",
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",
        "tags": ["coffee", "kitchen", "appliance", "brewing"]
    },
    {
        "id": "prod-5",
        "name": "Laptop",
        "price": 1299.99,
        "category": "Electronics",
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
        "tags": ["computer", "work", "productivity", "portable"]
    },
    {
        "id": "prod-6",
        "name": "Yoga Mat",
        "price": 39.99,
        "category": "Sports",
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop",
        "tags": ["yoga", "fitness", "exercise", "meditation"]
    },
    {
        "id": "prod-7",
        "name": "Bluetooth Speaker",
        "price": 79.99,
        "category": "Electronics",
        "rating": 4.1,
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop",
        "tags": ["audio", "portable", "wireless", "music"]
    },
    {
        "id": "prod-8",
        "name": "Kitchen Knife Set",
        "price": 149.99,
        "category": "Home & Kitchen",
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?w=400&h=300&fit=crop",
        "tags": ["cooking", "kitchen", "tools", "sharp"]
    }
]

@recommendation_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Recommendation Service"}), 200

@recommendation_bp.route("/personalized", methods=["POST"])
def get_personalized_recommendations():
    """Get personalized product recommendations based on user behavior"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        viewed_products = data.get('viewed_products', [])
        purchased_products = data.get('purchased_products', [])
        cart_items = data.get('cart_items', [])
        limit = data.get('limit', 6)
        
        # AI-powered recommendation algorithm simulation
        recommendations = []
        
        # Collaborative filtering simulation
        if viewed_products or purchased_products:
            # Find products in similar categories
            user_categories = set()
            for product_id in viewed_products + purchased_products:
                product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
                if product:
                    user_categories.add(product['category'])
            
            # Recommend products from preferred categories
            category_recommendations = [
                p for p in SAMPLE_PRODUCTS 
                if p['category'] in user_categories and p['id'] not in viewed_products + purchased_products
            ]
            recommendations.extend(category_recommendations[:limit//2])
        
        # Content-based filtering simulation
        if cart_items:
            # Find products with similar tags
            cart_tags = set()
            for item_id in cart_items:
                product = next((p for p in SAMPLE_PRODUCTS if p['id'] == item_id), None)
                if product:
                    cart_tags.update(product['tags'])
            
            # Recommend products with similar tags
            tag_recommendations = [
                p for p in SAMPLE_PRODUCTS 
                if any(tag in p['tags'] for tag in cart_tags) and p['id'] not in cart_items
            ]
            recommendations.extend(tag_recommendations[:limit//2])
        
        # Fill remaining slots with trending products
        remaining_slots = limit - len(recommendations)
        if remaining_slots > 0:
            trending = sorted(SAMPLE_PRODUCTS, key=lambda x: x['rating'], reverse=True)
            for product in trending:
                if product not in recommendations and len(recommendations) < limit:
                    recommendations.append(product)
        
        # Add recommendation scores and reasons
        for i, product in enumerate(recommendations):
            product['recommendation_score'] = round(0.95 - (i * 0.05), 2)
            product['recommendation_reason'] = _get_recommendation_reason(product, user_categories if 'user_categories' in locals() else set())
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "recommendations": recommendations[:limit],
            "algorithm": "Hybrid (Collaborative + Content-based)",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@recommendation_bp.route("/similar/<product_id>", methods=["GET"])
def get_similar_products(product_id):
    """Get products similar to a specific product"""
    try:
        limit = request.args.get('limit', 4, type=int)
        
        # Find the target product
        target_product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
        if not target_product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        
        # Find similar products based on category and tags
        similar_products = []
        
        for product in SAMPLE_PRODUCTS:
            if product['id'] == product_id:
                continue
                
            similarity_score = 0
            
            # Category similarity (40% weight)
            if product['category'] == target_product['category']:
                similarity_score += 0.4
            
            # Tag similarity (40% weight)
            common_tags = set(product['tags']) & set(target_product['tags'])
            tag_similarity = len(common_tags) / len(set(product['tags']) | set(target_product['tags']))
            similarity_score += tag_similarity * 0.4
            
            # Price similarity (20% weight)
            price_diff = abs(product['price'] - target_product['price']) / max(product['price'], target_product['price'])
            price_similarity = 1 - min(price_diff, 1)
            similarity_score += price_similarity * 0.2
            
            product['similarity_score'] = round(similarity_score, 3)
            similar_products.append(product)
        
        # Sort by similarity score and return top results
        similar_products.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "target_product": target_product,
            "similar_products": similar_products[:limit],
            "algorithm": "Content-based similarity",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@recommendation_bp.route("/trending", methods=["GET"])
def get_trending_products():
    """Get trending products based on AI analysis"""
    try:
        limit = request.args.get('limit', 6, type=int)
        category = request.args.get('category')
        
        # Simulate trending algorithm based on rating, recent views, and sales
        trending_products = SAMPLE_PRODUCTS.copy()
        
        # Filter by category if specified
        if category:
            trending_products = [p for p in trending_products if p['category'].lower() == category.lower()]
        
        # Add trending metrics
        for product in trending_products:
            # Simulate trending score based on multiple factors
            base_score = product['rating'] / 5.0  # Normalize rating
            view_boost = random.uniform(0.1, 0.3)  # Simulated recent view boost
            sales_boost = random.uniform(0.05, 0.25)  # Simulated sales boost
            
            product['trending_score'] = round(base_score + view_boost + sales_boost, 3)
            product['trend_reason'] = _get_trend_reason()
        
        # Sort by trending score
        trending_products.sort(key=lambda x: x['trending_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "trending_products": trending_products[:limit],
            "category_filter": category,
            "algorithm": "Multi-factor trending analysis",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@recommendation_bp.route("/cross-sell/<product_id>", methods=["GET"])
def get_cross_sell_recommendations(product_id):
    """Get cross-sell recommendations for a product"""
    try:
        limit = request.args.get('limit', 4, type=int)
        
        # Find the target product
        target_product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
        if not target_product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        
        # Cross-sell logic based on product category and complementary items
        cross_sell_rules = {
            "Electronics": ["Electronics", "Home & Kitchen"],
            "Sports": ["Sports", "Home & Kitchen"],
            "Home & Kitchen": ["Home & Kitchen", "Electronics"]
        }
        
        target_categories = cross_sell_rules.get(target_product['category'], [target_product['category']])
        
        cross_sell_products = []
        for product in SAMPLE_PRODUCTS:
            if product['id'] != product_id and product['category'] in target_categories:
                # Calculate cross-sell score
                score = random.uniform(0.6, 0.9)
                product['cross_sell_score'] = round(score, 3)
                product['cross_sell_reason'] = _get_cross_sell_reason(target_product, product)
                cross_sell_products.append(product)
        
        # Sort by cross-sell score
        cross_sell_products.sort(key=lambda x: x['cross_sell_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "target_product": target_product,
            "cross_sell_products": cross_sell_products[:limit],
            "algorithm": "Rule-based cross-selling",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@recommendation_bp.route("/bundle", methods=["POST"])
def get_bundle_recommendations():
    """Get product bundle recommendations"""
    try:
        data = request.get_json() or {}
        product_ids = data.get('product_ids', [])
        
        if not product_ids:
            return jsonify({"status": "error", "message": "No product IDs provided"}), 400
        
        # Find products in the bundle
        bundle_products = [p for p in SAMPLE_PRODUCTS if p['id'] in product_ids]
        
        if not bundle_products:
            return jsonify({"status": "error", "message": "No valid products found"}), 404
        
        # Calculate bundle metrics
        total_price = sum(p['price'] for p in bundle_products)
        avg_rating = sum(p['rating'] for p in bundle_products) / len(bundle_products)
        
        # Suggest discount based on bundle size
        discount_percentage = min(len(bundle_products) * 5, 20)  # Max 20% discount
        discounted_price = total_price * (1 - discount_percentage / 100)
        
        # Find complementary products for the bundle
        bundle_categories = set(p['category'] for p in bundle_products)
        complementary_products = []
        
        for product in SAMPLE_PRODUCTS:
            if product['id'] not in product_ids:
                # Check if product complements the bundle
                if product['category'] in bundle_categories or len(bundle_categories) == 1:
                    product['bundle_fit_score'] = round(random.uniform(0.7, 0.95), 3)
                    complementary_products.append(product)
        
        complementary_products.sort(key=lambda x: x['bundle_fit_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "bundle": {
                "products": bundle_products,
                "total_price": round(total_price, 2),
                "discounted_price": round(discounted_price, 2),
                "discount_percentage": discount_percentage,
                "savings": round(total_price - discounted_price, 2),
                "avg_rating": round(avg_rating, 2)
            },
            "complementary_products": complementary_products[:4],
            "algorithm": "Bundle optimization with complementary analysis",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def _get_recommendation_reason(product, user_categories):
    """Generate recommendation reason"""
    reasons = [
        f"Popular in {product['category']}",
        f"Highly rated ({product['rating']}/5)",
        "Trending now",
        "Customers also bought",
        "Based on your interests"
    ]
    
    if product['category'] in user_categories:
        return f"Based on your interest in {product['category']}"
    
    return random.choice(reasons)

def _get_trend_reason():
    """Generate trending reason"""
    reasons = [
        "High recent sales",
        "Increasing search volume",
        "Social media buzz",
        "Seasonal popularity",
        "Customer reviews spike"
    ]
    return random.choice(reasons)

def _get_cross_sell_reason(target_product, recommended_product):
    """Generate cross-sell reason"""
    if target_product['category'] == recommended_product['category']:
        return f"Complements your {target_product['name']}"
    else:
        return f"Often bought with {target_product['category']} items"

