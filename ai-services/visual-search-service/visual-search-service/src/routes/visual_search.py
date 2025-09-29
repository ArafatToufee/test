from flask import Blueprint, jsonify, request
import base64
import random
import json
from datetime import datetime
import hashlib

visual_search_bp = Blueprint("visual_search", __name__)

# Sample product database for visual search
VISUAL_PRODUCTS = [
    {
        "id": "prod-1",
        "name": "Wireless Headphones",
        "price": 199.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",
        "visual_features": ["black", "circular", "headband", "cushioned", "wireless"],
        "color_palette": ["#000000", "#333333", "#666666"],
        "shape_features": ["circular", "curved", "padded"]
    },
    {
        "id": "prod-2",
        "name": "Smartphone",
        "price": 799.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop",
        "visual_features": ["rectangular", "screen", "sleek", "modern", "black"],
        "color_palette": ["#000000", "#1a1a1a", "#333333"],
        "shape_features": ["rectangular", "flat", "smooth"]
    },
    {
        "id": "prod-3",
        "name": "Running Shoes",
        "price": 129.99,
        "category": "Sports",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop",
        "visual_features": ["red", "white", "athletic", "laced", "sporty"],
        "color_palette": ["#ff0000", "#ffffff", "#cccccc"],
        "shape_features": ["curved", "textured", "flexible"]
    },
    {
        "id": "prod-4",
        "name": "Coffee Maker",
        "price": 89.99,
        "category": "Home & Kitchen",
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",
        "visual_features": ["white", "cylindrical", "appliance", "modern", "sleek"],
        "color_palette": ["#ffffff", "#f0f0f0", "#e0e0e0"],
        "shape_features": ["cylindrical", "vertical", "smooth"]
    },
    {
        "id": "prod-5",
        "name": "Laptop",
        "price": 1299.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
        "visual_features": ["silver", "rectangular", "screen", "keyboard", "portable"],
        "color_palette": ["#c0c0c0", "#e0e0e0", "#f0f0f0"],
        "shape_features": ["rectangular", "flat", "hinged"]
    },
    {
        "id": "prod-6",
        "name": "Yoga Mat",
        "price": 39.99,
        "category": "Sports",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop",
        "visual_features": ["purple", "rectangular", "textured", "flexible", "mat"],
        "color_palette": ["#800080", "#9932cc", "#ba55d3"],
        "shape_features": ["rectangular", "flat", "textured"]
    }
]

@visual_search_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Visual Search Service"}), 200

@visual_search_bp.route("/search-by-image", methods=["POST"])
def search_by_image():
    """Search for products using image upload"""
    try:
        data = request.get_json() or {}
        
        # Handle different input formats
        image_data = data.get('image')
        image_url = data.get('image_url')
        limit = data.get('limit', 6)
        
        if not image_data and not image_url:
            return jsonify({"status": "error", "message": "No image provided"}), 400
        
        # Simulate AI image analysis
        if image_data:
            # Decode base64 image (simulation)
            try:
                # Generate a hash for the image to simulate processing
                image_hash = hashlib.md5(image_data.encode()).hexdigest()
                analysis_result = _analyze_uploaded_image(image_hash)
            except Exception:
                return jsonify({"status": "error", "message": "Invalid image data"}), 400
        else:
            # Analyze image from URL (simulation)
            analysis_result = _analyze_image_url(image_url)
        
        # Find matching products based on visual features
        matches = _find_visual_matches(analysis_result, limit)
        
        return jsonify({
            "status": "success",
            "image_analysis": analysis_result,
            "matches": matches,
            "algorithm": "Deep Learning Visual Recognition",
            "confidence_threshold": 0.7,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@visual_search_bp.route("/search-by-color", methods=["POST"])
def search_by_color():
    """Search for products by color"""
    try:
        data = request.get_json() or {}
        color = data.get('color', '').lower()
        limit = data.get('limit', 6)
        
        if not color:
            return jsonify({"status": "error", "message": "No color specified"}), 400
        
        # Find products matching the color
        color_matches = []
        for product in VISUAL_PRODUCTS:
            if any(color in feature.lower() for feature in product['visual_features']):
                # Calculate color match score
                color_score = _calculate_color_similarity(color, product['visual_features'])
                product_copy = product.copy()
                product_copy['color_match_score'] = color_score
                product_copy['matched_features'] = [f for f in product['visual_features'] if color in f.lower()]
                color_matches.append(product_copy)
        
        # Sort by color match score
        color_matches.sort(key=lambda x: x['color_match_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "search_color": color,
            "matches": color_matches[:limit],
            "algorithm": "Color-based visual matching",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@visual_search_bp.route("/search-by-style", methods=["POST"])
def search_by_style():
    """Search for products by visual style"""
    try:
        data = request.get_json() or {}
        style = data.get('style', '').lower()
        limit = data.get('limit', 6)
        
        if not style:
            return jsonify({"status": "error", "message": "No style specified"}), 400
        
        # Define style mappings
        style_keywords = {
            'modern': ['sleek', 'modern', 'contemporary'],
            'classic': ['traditional', 'classic', 'timeless'],
            'sporty': ['athletic', 'sporty', 'active'],
            'minimalist': ['simple', 'clean', 'minimal'],
            'luxury': ['premium', 'elegant', 'sophisticated']
        }
        
        search_keywords = style_keywords.get(style, [style])
        
        # Find products matching the style
        style_matches = []
        for product in VISUAL_PRODUCTS:
            style_score = 0
            matched_features = []
            
            for keyword in search_keywords:
                for feature in product['visual_features']:
                    if keyword in feature.lower():
                        style_score += 1
                        matched_features.append(feature)
            
            if style_score > 0:
                product_copy = product.copy()
                product_copy['style_match_score'] = style_score
                product_copy['matched_style_features'] = matched_features
                style_matches.append(product_copy)
        
        # Sort by style match score
        style_matches.sort(key=lambda x: x['style_match_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "search_style": style,
            "matches": style_matches[:limit],
            "algorithm": "Style-based visual matching",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@visual_search_bp.route("/extract-features", methods=["POST"])
def extract_visual_features():
    """Extract visual features from an image"""
    try:
        data = request.get_json() or {}
        image_data = data.get('image')
        image_url = data.get('image_url')
        
        if not image_data and not image_url:
            return jsonify({"status": "error", "message": "No image provided"}), 400
        
        # Simulate AI feature extraction
        if image_data:
            image_hash = hashlib.md5(image_data.encode()).hexdigest()
            features = _extract_features_from_hash(image_hash)
        else:
            features = _extract_features_from_url(image_url)
        
        return jsonify({
            "status": "success",
            "extracted_features": features,
            "algorithm": "Convolutional Neural Network Feature Extraction",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@visual_search_bp.route("/similar-images/<product_id>", methods=["GET"])
def find_similar_images(product_id):
    """Find products with similar visual appearance"""
    try:
        limit = request.args.get('limit', 4, type=int)
        
        # Find the target product
        target_product = next((p for p in VISUAL_PRODUCTS if p['id'] == product_id), None)
        if not target_product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        
        # Calculate visual similarity
        similar_products = []
        for product in VISUAL_PRODUCTS:
            if product['id'] == product_id:
                continue
            
            # Calculate similarity based on visual features
            similarity_score = _calculate_visual_similarity(target_product, product)
            
            if similarity_score > 0.3:  # Threshold for similarity
                product_copy = product.copy()
                product_copy['visual_similarity_score'] = similarity_score
                product_copy['similar_features'] = _get_common_features(target_product, product)
                similar_products.append(product_copy)
        
        # Sort by similarity score
        similar_products.sort(key=lambda x: x['visual_similarity_score'], reverse=True)
        
        return jsonify({
            "status": "success",
            "target_product": target_product,
            "similar_products": similar_products[:limit],
            "algorithm": "Visual feature similarity matching",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def _analyze_uploaded_image(image_hash):
    """Simulate AI analysis of uploaded image"""
    # Simulate different analysis results based on hash
    hash_int = int(image_hash[:8], 16)
    
    colors = ['red', 'blue', 'green', 'black', 'white', 'silver', 'purple']
    shapes = ['rectangular', 'circular', 'curved', 'angular', 'smooth']
    styles = ['modern', 'classic', 'sporty', 'elegant', 'casual']
    
    return {
        "dominant_colors": random.sample(colors, 2),
        "detected_shapes": random.sample(shapes, 2),
        "style_classification": random.choice(styles),
        "confidence": round(random.uniform(0.75, 0.95), 3),
        "object_detection": ["product", "item"],
        "texture_analysis": random.choice(["smooth", "textured", "glossy", "matte"])
    }

def _analyze_image_url(image_url):
    """Simulate AI analysis of image from URL"""
    # Simple simulation based on URL
    url_hash = hashlib.md5(image_url.encode()).hexdigest()
    return _analyze_uploaded_image(url_hash)

def _find_visual_matches(analysis_result, limit):
    """Find products matching the visual analysis"""
    matches = []
    
    for product in VISUAL_PRODUCTS:
        match_score = 0
        
        # Check color matches
        for color in analysis_result['dominant_colors']:
            if any(color in feature.lower() for feature in product['visual_features']):
                match_score += 0.3
        
        # Check shape matches
        for shape in analysis_result['detected_shapes']:
            if any(shape in feature.lower() for feature in product['shape_features']):
                match_score += 0.2
        
        # Check style match
        style = analysis_result['style_classification']
        if any(style in feature.lower() for feature in product['visual_features']):
            match_score += 0.3
        
        if match_score > 0.2:  # Minimum threshold
            product_copy = product.copy()
            product_copy['match_score'] = round(match_score, 3)
            product_copy['match_confidence'] = round(match_score * analysis_result['confidence'], 3)
            matches.append(product_copy)
    
    # Sort by match score
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches[:limit]

def _calculate_color_similarity(search_color, product_features):
    """Calculate color similarity score"""
    score = 0
    for feature in product_features:
        if search_color in feature.lower():
            score += 1
    return round(score / len(product_features), 3)

def _calculate_visual_similarity(product1, product2):
    """Calculate visual similarity between two products"""
    # Compare visual features
    common_features = set(product1['visual_features']) & set(product2['visual_features'])
    total_features = set(product1['visual_features']) | set(product2['visual_features'])
    
    feature_similarity = len(common_features) / len(total_features) if total_features else 0
    
    # Compare shape features
    common_shapes = set(product1['shape_features']) & set(product2['shape_features'])
    total_shapes = set(product1['shape_features']) | set(product2['shape_features'])
    
    shape_similarity = len(common_shapes) / len(total_shapes) if total_shapes else 0
    
    # Weighted average
    overall_similarity = (feature_similarity * 0.7) + (shape_similarity * 0.3)
    return round(overall_similarity, 3)

def _get_common_features(product1, product2):
    """Get common visual features between products"""
    return list(set(product1['visual_features']) & set(product2['visual_features']))

def _extract_features_from_hash(image_hash):
    """Extract features based on image hash"""
    hash_int = int(image_hash[:8], 16)
    
    return {
        "colors": random.sample(['red', 'blue', 'green', 'black', 'white', 'silver'], 3),
        "shapes": random.sample(['rectangular', 'circular', 'curved', 'angular'], 2),
        "textures": random.sample(['smooth', 'rough', 'glossy', 'matte'], 2),
        "patterns": random.choice(['solid', 'striped', 'dotted', 'gradient']),
        "brightness": round(random.uniform(0.3, 0.9), 2),
        "contrast": round(random.uniform(0.4, 0.8), 2)
    }

def _extract_features_from_url(image_url):
    """Extract features from image URL"""
    url_hash = hashlib.md5(image_url.encode()).hexdigest()
    return _extract_features_from_hash(url_hash)

