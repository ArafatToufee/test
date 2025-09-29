from flask import Blueprint, request, jsonify
import jwt
from src.models.order import db, Order, OrderItem

order_bp = Blueprint('order', __name__)

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

@order_bp.route('/', methods=['GET'])
def get_orders():
    """Get user's orders with optional filtering"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Order.query.filter_by(user_id=user_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    query = query.order_by(Order.created_at.desc())
    
    # Pagination
    orders = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [order.to_dict() for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

@order_bp.route('/', methods=['POST'])
def create_order():
    """Create a new order"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['items', 'shipping_address', 'payment_method']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if not data['items'] or len(data['items']) == 0:
        return jsonify({'error': 'Order must contain at least one item'}), 400
    
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item_data in data['items']:
        required_item_fields = ['product_id', 'product_name', 'product_price', 'quantity']
        for field in required_item_fields:
            if field not in item_data:
                return jsonify({'error': f'Missing required item field: {field}'}), 400
        
        quantity = item_data['quantity']
        price = float(item_data['product_price'])
        subtotal = quantity * price
        total_amount += subtotal
        
        order_items.append({
            'product_id': item_data['product_id'],
            'product_name': item_data['product_name'],
            'product_price': price,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    # Create order
    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        shipping_address=data['shipping_address'],
        payment_method=data['payment_method'],
        status='pending',
        payment_status='pending'
    )
    
    try:
        db.session.add(new_order)
        db.session.flush()  # Get the order ID
        
        # Create order items
        for item_data in order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                product_price=item_data['product_price'],
                quantity=item_data['quantity'],
                subtotal=item_data['subtotal']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': new_order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order'}), 500

@order_bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict()), 200

@order_bp.route('/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Prevent status changes for delivered or cancelled orders
    if order.status in ['delivered', 'cancelled']:
        return jsonify({'error': f'Cannot change status of {order.status} order'}), 400
    
    order.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Order status updated',
            'order': order.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update order status'}), 500

@order_bp.route('/<order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    """Cancel an order"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Only allow cancellation of pending or confirmed orders
    if order.status not in ['pending', 'confirmed']:
        return jsonify({'error': f'Cannot cancel {order.status} order'}), 400
    
    order.status = 'cancelled'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel order'}), 500

@order_bp.route('/stats', methods=['GET'])
def get_order_stats():
    """Get user's order statistics"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    total_orders = Order.query.filter_by(user_id=user_id).count()
    pending_orders = Order.query.filter_by(user_id=user_id, status='pending').count()
    confirmed_orders = Order.query.filter_by(user_id=user_id, status='confirmed').count()
    shipped_orders = Order.query.filter_by(user_id=user_id, status='shipped').count()
    delivered_orders = Order.query.filter_by(user_id=user_id, status='delivered').count()
    cancelled_orders = Order.query.filter_by(user_id=user_id, status='cancelled').count()
    
    total_spent = db.session.query(db.func.sum(Order.total_amount)).filter_by(
        user_id=user_id, 
        status='delivered'
    ).scalar() or 0
    
    return jsonify({
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'total_spent': total_spent
    }), 200

