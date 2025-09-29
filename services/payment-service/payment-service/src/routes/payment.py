from flask import Blueprint, request, jsonify
import jwt
import random
import time
from src.models.payment import db, Payment

payment_bp = Blueprint('payment', __name__)

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

def simulate_payment_processing(payment_method, amount):
    """Simulate payment processing with different outcomes"""
    # Simulate processing time
    time.sleep(1)
    
    # Simulate different payment outcomes based on amount
    if amount > 10000:  # Large amounts have higher failure rate
        success_rate = 0.7
    elif amount > 1000:
        success_rate = 0.9
    else:
        success_rate = 0.95
    
    if random.random() < success_rate:
        # Success
        transaction_id = f"TXN_{random.randint(100000, 999999)}"
        return True, transaction_id, None
    else:
        # Failure
        failure_reasons = [
            "Insufficient funds",
            "Card declined",
            "Invalid card details",
            "Payment processor error",
            "Network timeout"
        ]
        return False, None, random.choice(failure_reasons)

@payment_bp.route('/', methods=['POST'])
def process_payment():
    """Process a payment for an order"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['order_id', 'amount', 'payment_method']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400
    
    # Check if payment already exists for this order
    existing_payment = Payment.query.filter_by(order_id=data['order_id']).first()
    if existing_payment and existing_payment.status == 'completed':
        return jsonify({'error': 'Payment already completed for this order'}), 409
    
    # Create payment record
    payment = Payment(
        order_id=data['order_id'],
        user_id=user_id,
        amount=amount,
        currency=data.get('currency', 'USD'),
        payment_method=data['payment_method'],
        status='processing'
    )
    
    try:
        db.session.add(payment)
        db.session.commit()
        
        # Simulate payment processing
        success, transaction_id, failure_reason = simulate_payment_processing(
            data['payment_method'], amount
        )
        
        if success:
            payment.status = 'completed'
            payment.transaction_id = transaction_id
        else:
            payment.status = 'failed'
            payment.failure_reason = failure_reason
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment processed',
            'payment': payment.to_dict()
        }), 200 if success else 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process payment'}), 500

@payment_bp.route('/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Get payment details"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    payment = Payment.query.filter_by(id=payment_id, user_id=user_id).first()
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    return jsonify(payment.to_dict()), 200

@payment_bp.route('/order/<order_id>', methods=['GET'])
def get_payment_by_order(order_id):
    """Get payment details by order ID"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    payment = Payment.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not payment:
        return jsonify({'error': 'Payment not found for this order'}), 404
    
    return jsonify(payment.to_dict()), 200

@payment_bp.route('/', methods=['GET'])
def get_payments():
    """Get user's payment history"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Payment.query.filter_by(user_id=user_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    query = query.order_by(Payment.created_at.desc())
    
    # Pagination
    payments = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'payments': [payment.to_dict() for payment in payments.items],
        'total': payments.total,
        'pages': payments.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

@payment_bp.route('/<payment_id>/refund', methods=['POST'])
def refund_payment(payment_id):
    """Refund a completed payment"""
    user_id, error, status_code = get_user_from_token()
    if error:
        return jsonify(error), status_code
    
    payment = Payment.query.filter_by(id=payment_id, user_id=user_id).first()
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.status != 'completed':
        return jsonify({'error': 'Only completed payments can be refunded'}), 400
    
    data = request.get_json()
    refund_amount = data.get('amount', payment.amount) if data else payment.amount
    
    if refund_amount > payment.amount:
        return jsonify({'error': 'Refund amount cannot exceed payment amount'}), 400
    
    # Simulate refund processing (always successful for demo)
    payment.status = 'refunded'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Payment refunded successfully',
            'payment': payment.to_dict(),
            'refund_amount': refund_amount
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process refund'}), 500

@payment_bp.route('/methods', methods=['GET'])
def get_payment_methods():
    """Get available payment methods"""
    return jsonify({
        'payment_methods': [
            {'id': 'credit_card', 'name': 'Credit Card', 'enabled': True},
            {'id': 'debit_card', 'name': 'Debit Card', 'enabled': True},
            {'id': 'paypal', 'name': 'PayPal', 'enabled': True},
            {'id': 'apple_pay', 'name': 'Apple Pay', 'enabled': True},
            {'id': 'google_pay', 'name': 'Google Pay', 'enabled': True}
        ]
    }), 200

