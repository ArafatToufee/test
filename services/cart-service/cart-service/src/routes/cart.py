from flask import Blueprint, request, jsonify
import jwt
from src.models.cart import db, CartItem

cart_bp = Blueprint('cart', __name__)

SECRET_KEY = "ecommerce-platform-auth-secret-key-2025"  # Should match auth service

def get_user_from_token():
    """Extract user ID from JWT token in Authorization header"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {'error': 'Authorization token required'}, 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id'], None, None
    except jwt.ExpiredSignatureError:
        return None, {'error': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return None, {'error': 'Invalid token'}, 401

@cart_bp.route('/', methods=['GET'])
def get_cart():
    """Get user's cart items"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    total_amount = sum(item.product_price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    return jsonify({
        'cart_items': [item.to_dict() for item in cart_items],
        'total_items': total_items,
        'total_amount': total_amount
    }), 200

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['product_id', 'product_name', 'product_price']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    quantity = data.get('quantity', 1)
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be greater than 0'}), 400
    
    # Check if item already exists in cart
    existing_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=data['product_id']
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += quantity
        existing_item.product_price = data['product_price']  # Update price in case it changed
        existing_item.product_name = data['product_name']  # Update name in case it changed
        db.session.commit()
        
        return jsonify({
            'message': 'Item quantity updated in cart',
            'cart_item': existing_item.to_dict()
        }), 200
    else:
        # Add new item
        new_item = CartItem(
            user_id=user_id,
            product_id=data['product_id'],
            product_name=data['product_name'],
            product_price=float(data['product_price']),
            quantity=quantity
        )
        
        try:
            db.session.add(new_item)
            db.session.commit()
            
            return jsonify({
                'message': 'Item added to cart',
                'cart_item': new_item.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to add item to cart'}), 500

@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Quantity is required'}), 400
    
    quantity = data['quantity']
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be greater than 0'}), 400
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    cart_item.quantity = quantity
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Cart item updated',
            'cart_item': cart_item.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update cart item'}), 500

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_cart_item(item_id):
    """Remove item from cart"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item removed from cart',
            'removed_item': cart_item.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove cart item'}), 500

@cart_bp.route('/clear', methods=['DELETE'])
def clear_cart():
    """Clear all items from user's cart"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    try:
        deleted_count = CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'message': f'Cart cleared. {deleted_count} items removed.'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to clear cart'}), 500

@cart_bp.route('/count', methods=['GET'])
def get_cart_count():
    """Get total number of items in user's cart"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    total_items = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=user_id).scalar() or 0
    
    return jsonify({
        'total_items': total_items
    }), 200

