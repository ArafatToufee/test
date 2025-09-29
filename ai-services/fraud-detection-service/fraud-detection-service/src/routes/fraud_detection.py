from flask import Blueprint, jsonify, request
import random
import json
from datetime import datetime, timedelta
import hashlib
import re

fraud_detection_bp = Blueprint("fraud_detection", __name__)

# Risk scoring thresholds
RISK_THRESHOLDS = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}

# Suspicious patterns database
SUSPICIOUS_PATTERNS = {
    'email_domains': ['tempmail.com', '10minutemail.com', 'guerrillamail.com'],
    'high_risk_countries': ['XX', 'YY', 'ZZ'],  # Placeholder country codes
    'velocity_limits': {
        'transactions_per_hour': 10,
        'amount_per_hour': 5000,
        'cards_per_day': 3
    }
}

@fraud_detection_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Fraud Detection Service"}), 200

@fraud_detection_bp.route("/analyze-transaction", methods=["POST"])
def analyze_transaction():
    """Analyze a transaction for fraud risk"""
    try:
        data = request.get_json() or {}
        
        # Extract transaction details
        transaction = {
            'id': data.get('transaction_id'),
            'user_id': data.get('user_id'),
            'amount': data.get('amount', 0),
            'currency': data.get('currency', 'USD'),
            'payment_method': data.get('payment_method'),
            'billing_address': data.get('billing_address', {}),
            'shipping_address': data.get('shipping_address', {}),
            'user_agent': data.get('user_agent', ''),
            'ip_address': data.get('ip_address', ''),
            'timestamp': data.get('timestamp', datetime.now().isoformat())
        }
        
        # Perform comprehensive fraud analysis
        risk_analysis = _perform_fraud_analysis(transaction)
        
        # Calculate overall risk score
        overall_risk = _calculate_overall_risk(risk_analysis)
        
        # Determine risk level and recommendation
        risk_level, recommendation = _get_risk_assessment(overall_risk)
        
        return jsonify({
            "status": "success",
            "transaction_id": transaction['id'],
            "risk_analysis": risk_analysis,
            "overall_risk_score": overall_risk,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "algorithm": "Multi-layer AI Fraud Detection",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@fraud_detection_bp.route("/analyze-user-behavior", methods=["POST"])
def analyze_user_behavior():
    """Analyze user behavior patterns for anomalies"""
    try:
        data = request.get_json() or {}
        
        user_id = data.get('user_id')
        behavior_data = {
            'login_history': data.get('login_history', []),
            'purchase_history': data.get('purchase_history', []),
            'browsing_patterns': data.get('browsing_patterns', {}),
            'device_fingerprint': data.get('device_fingerprint', {}),
            'location_history': data.get('location_history', [])
        }
        
        # Analyze behavior patterns
        behavior_analysis = _analyze_behavior_patterns(behavior_data)
        
        # Calculate anomaly score
        anomaly_score = _calculate_anomaly_score(behavior_analysis)
        
        # Generate insights and recommendations
        insights = _generate_behavior_insights(behavior_analysis)
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "behavior_analysis": behavior_analysis,
            "anomaly_score": anomaly_score,
            "insights": insights,
            "algorithm": "Behavioral Analytics & Machine Learning",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@fraud_detection_bp.route("/check-payment-method", methods=["POST"])
def check_payment_method():
    """Analyze payment method for fraud indicators"""
    try:
        data = request.get_json() or {}
        
        payment_info = {
            'card_number': data.get('card_number', ''),
            'cardholder_name': data.get('cardholder_name', ''),
            'billing_address': data.get('billing_address', {}),
            'cvv': data.get('cvv', ''),
            'expiry_date': data.get('expiry_date', '')
        }
        
        # Analyze payment method
        payment_analysis = _analyze_payment_method(payment_info)
        
        # Check against known fraud patterns
        fraud_indicators = _check_fraud_indicators(payment_info)
        
        # Calculate payment risk score
        payment_risk = _calculate_payment_risk(payment_analysis, fraud_indicators)
        
        return jsonify({
            "status": "success",
            "payment_analysis": payment_analysis,
            "fraud_indicators": fraud_indicators,
            "payment_risk_score": payment_risk,
            "algorithm": "Payment Method Fraud Detection",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@fraud_detection_bp.route("/velocity-check", methods=["POST"])
def velocity_check():
    """Check transaction velocity for suspicious patterns"""
    try:
        data = request.get_json() or {}
        
        user_id = data.get('user_id')
        time_window = data.get('time_window', 'hour')  # hour, day, week
        transactions = data.get('recent_transactions', [])
        
        # Perform velocity analysis
        velocity_analysis = _analyze_transaction_velocity(transactions, time_window)
        
        # Check against velocity limits
        velocity_violations = _check_velocity_limits(velocity_analysis)
        
        # Calculate velocity risk
        velocity_risk = _calculate_velocity_risk(velocity_analysis, velocity_violations)
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "time_window": time_window,
            "velocity_analysis": velocity_analysis,
            "velocity_violations": velocity_violations,
            "velocity_risk_score": velocity_risk,
            "algorithm": "Transaction Velocity Analysis",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@fraud_detection_bp.route("/device-fingerprint", methods=["POST"])
def analyze_device_fingerprint():
    """Analyze device fingerprint for fraud detection"""
    try:
        data = request.get_json() or {}
        
        device_info = {
            'user_agent': data.get('user_agent', ''),
            'screen_resolution': data.get('screen_resolution', ''),
            'timezone': data.get('timezone', ''),
            'language': data.get('language', ''),
            'plugins': data.get('plugins', []),
            'canvas_fingerprint': data.get('canvas_fingerprint', ''),
            'webgl_fingerprint': data.get('webgl_fingerprint', '')
        }
        
        # Analyze device fingerprint
        device_analysis = _analyze_device_fingerprint(device_info)
        
        # Check for suspicious device characteristics
        device_risk_factors = _check_device_risk_factors(device_info)
        
        # Calculate device risk score
        device_risk = _calculate_device_risk(device_analysis, device_risk_factors)
        
        return jsonify({
            "status": "success",
            "device_analysis": device_analysis,
            "risk_factors": device_risk_factors,
            "device_risk_score": device_risk,
            "algorithm": "Device Fingerprinting & Risk Analysis",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@fraud_detection_bp.route("/ml-prediction", methods=["POST"])
def ml_fraud_prediction():
    """Machine learning-based fraud prediction"""
    try:
        data = request.get_json() or {}
        
        # Extract features for ML model
        features = {
            'transaction_amount': data.get('amount', 0),
            'hour_of_day': datetime.now().hour,
            'day_of_week': datetime.now().weekday(),
            'user_age_days': data.get('user_age_days', 0),
            'previous_transactions': data.get('previous_transactions', 0),
            'avg_transaction_amount': data.get('avg_transaction_amount', 0),
            'location_risk_score': data.get('location_risk_score', 0),
            'payment_method_risk': data.get('payment_method_risk', 0)
        }
        
        # Simulate ML model prediction
        ml_prediction = _simulate_ml_prediction(features)
        
        # Generate feature importance
        feature_importance = _calculate_feature_importance(features)
        
        # Generate explanation
        explanation = _generate_ml_explanation(ml_prediction, feature_importance)
        
        return jsonify({
            "status": "success",
            "ml_prediction": ml_prediction,
            "feature_importance": feature_importance,
            "explanation": explanation,
            "model_version": "RefFraudNet-v2.1",
            "algorithm": "Gradient Boosting Classifier",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def _perform_fraud_analysis(transaction):
    """Perform comprehensive fraud analysis"""
    analysis = {}
    
    # Amount analysis
    analysis['amount_analysis'] = {
        'amount': transaction['amount'],
        'is_high_value': transaction['amount'] > 1000,
        'is_round_number': transaction['amount'] % 100 == 0,
        'risk_score': min(transaction['amount'] / 5000, 1.0)
    }
    
    # Geographic analysis
    analysis['geographic_analysis'] = {
        'billing_country': transaction['billing_address'].get('country', 'US'),
        'shipping_country': transaction['shipping_address'].get('country', 'US'),
        'address_mismatch': transaction['billing_address'].get('country') != transaction['shipping_address'].get('country'),
        'high_risk_location': random.choice([True, False])  # Simulate
    }
    
    # Temporal analysis
    analysis['temporal_analysis'] = {
        'hour': datetime.now().hour,
        'is_unusual_hour': datetime.now().hour < 6 or datetime.now().hour > 23,
        'is_weekend': datetime.now().weekday() >= 5,
        'velocity_risk': random.uniform(0, 1)
    }
    
    # User analysis
    analysis['user_analysis'] = {
        'user_id': transaction['user_id'],
        'is_new_user': random.choice([True, False]),
        'account_age_days': random.randint(1, 365),
        'previous_fraud_attempts': random.randint(0, 3)
    }
    
    return analysis

def _calculate_overall_risk(risk_analysis):
    """Calculate overall risk score from analysis components"""
    weights = {
        'amount_analysis': 0.25,
        'geographic_analysis': 0.20,
        'temporal_analysis': 0.15,
        'user_analysis': 0.40
    }
    
    total_risk = 0
    for component, weight in weights.items():
        if component in risk_analysis:
            component_risk = _extract_component_risk(risk_analysis[component])
            total_risk += component_risk * weight
    
    return round(total_risk, 3)

def _extract_component_risk(component_data):
    """Extract risk score from component analysis"""
    if 'risk_score' in component_data:
        return component_data['risk_score']
    
    # Calculate based on boolean flags
    risk_factors = [v for k, v in component_data.items() if isinstance(v, bool) and v]
    return len(risk_factors) / len(component_data)

def _get_risk_assessment(risk_score):
    """Get risk level and recommendation based on score"""
    if risk_score < RISK_THRESHOLDS['low']:
        return 'low', 'approve'
    elif risk_score < RISK_THRESHOLDS['medium']:
        return 'medium', 'review'
    elif risk_score < RISK_THRESHOLDS['high']:
        return 'high', 'manual_review'
    else:
        return 'critical', 'decline'

def _analyze_behavior_patterns(behavior_data):
    """Analyze user behavior patterns"""
    analysis = {}
    
    # Login pattern analysis
    login_history = behavior_data.get('login_history', [])
    analysis['login_patterns'] = {
        'total_logins': len(login_history),
        'unique_locations': len(set(l.get('location', '') for l in login_history)),
        'unusual_times': sum(1 for l in login_history if _is_unusual_time(l.get('timestamp', ''))),
        'failed_attempts': sum(1 for l in login_history if not l.get('successful', True))
    }
    
    # Purchase pattern analysis
    purchase_history = behavior_data.get('purchase_history', [])
    analysis['purchase_patterns'] = {
        'total_purchases': len(purchase_history),
        'avg_amount': sum(p.get('amount', 0) for p in purchase_history) / max(len(purchase_history), 1),
        'category_diversity': len(set(p.get('category', '') for p in purchase_history)),
        'recent_spike': _detect_purchase_spike(purchase_history)
    }
    
    return analysis

def _calculate_anomaly_score(behavior_analysis):
    """Calculate anomaly score from behavior analysis"""
    score = 0
    
    # Check login anomalies
    login_patterns = behavior_analysis.get('login_patterns', {})
    if login_patterns.get('unusual_times', 0) > 5:
        score += 0.3
    if login_patterns.get('failed_attempts', 0) > 3:
        score += 0.4
    
    # Check purchase anomalies
    purchase_patterns = behavior_analysis.get('purchase_patterns', {})
    if purchase_patterns.get('recent_spike', False):
        score += 0.5
    
    return round(min(score, 1.0), 3)

def _generate_behavior_insights(behavior_analysis):
    """Generate insights from behavior analysis"""
    insights = []
    
    login_patterns = behavior_analysis.get('login_patterns', {})
    if login_patterns.get('unusual_times', 0) > 3:
        insights.append("User frequently logs in during unusual hours")
    
    if login_patterns.get('failed_attempts', 0) > 2:
        insights.append("Multiple failed login attempts detected")
    
    purchase_patterns = behavior_analysis.get('purchase_patterns', {})
    if purchase_patterns.get('recent_spike', False):
        insights.append("Unusual spike in purchase activity")
    
    return insights

def _analyze_payment_method(payment_info):
    """Analyze payment method for fraud indicators"""
    analysis = {}
    
    card_number = payment_info.get('card_number', '')
    
    # Basic card validation
    analysis['card_validation'] = {
        'is_valid_length': len(card_number.replace(' ', '')) in [13, 14, 15, 16, 17, 18, 19],
        'passes_luhn': _luhn_check(card_number),
        'card_type': _detect_card_type(card_number)
    }
    
    # Name analysis
    cardholder_name = payment_info.get('cardholder_name', '')
    analysis['name_analysis'] = {
        'has_name': bool(cardholder_name.strip()),
        'name_length': len(cardholder_name),
        'suspicious_patterns': _check_name_patterns(cardholder_name)
    }
    
    return analysis

def _check_fraud_indicators(payment_info):
    """Check for known fraud indicators"""
    indicators = []
    
    card_number = payment_info.get('card_number', '')
    if card_number.startswith('4111'):  # Test card pattern
        indicators.append("Test card number detected")
    
    cardholder_name = payment_info.get('cardholder_name', '').lower()
    if any(word in cardholder_name for word in ['test', 'fake', 'fraud']):
        indicators.append("Suspicious cardholder name")
    
    return indicators

def _calculate_payment_risk(payment_analysis, fraud_indicators):
    """Calculate payment method risk score"""
    risk = 0
    
    # Card validation issues
    card_validation = payment_analysis.get('card_validation', {})
    if not card_validation.get('is_valid_length', True):
        risk += 0.4
    if not card_validation.get('passes_luhn', True):
        risk += 0.5
    
    # Fraud indicators
    risk += len(fraud_indicators) * 0.3
    
    return round(min(risk, 1.0), 3)

def _analyze_transaction_velocity(transactions, time_window):
    """Analyze transaction velocity"""
    now = datetime.now()
    
    if time_window == 'hour':
        cutoff = now - timedelta(hours=1)
    elif time_window == 'day':
        cutoff = now - timedelta(days=1)
    else:
        cutoff = now - timedelta(weeks=1)
    
    recent_transactions = [
        t for t in transactions 
        if datetime.fromisoformat(t.get('timestamp', now.isoformat())) > cutoff
    ]
    
    return {
        'transaction_count': len(recent_transactions),
        'total_amount': sum(t.get('amount', 0) for t in recent_transactions),
        'unique_cards': len(set(t.get('card_last4', '') for t in recent_transactions)),
        'avg_amount': sum(t.get('amount', 0) for t in recent_transactions) / max(len(recent_transactions), 1)
    }

def _check_velocity_limits(velocity_analysis):
    """Check velocity against limits"""
    violations = []
    
    if velocity_analysis['transaction_count'] > SUSPICIOUS_PATTERNS['velocity_limits']['transactions_per_hour']:
        violations.append("Excessive transaction count")
    
    if velocity_analysis['total_amount'] > SUSPICIOUS_PATTERNS['velocity_limits']['amount_per_hour']:
        violations.append("Excessive transaction amount")
    
    return violations

def _calculate_velocity_risk(velocity_analysis, violations):
    """Calculate velocity risk score"""
    risk = len(violations) * 0.4
    
    # Additional risk based on velocity metrics
    if velocity_analysis['transaction_count'] > 5:
        risk += 0.2
    
    return round(min(risk, 1.0), 3)

def _analyze_device_fingerprint(device_info):
    """Analyze device fingerprint"""
    return {
        'browser_info': _extract_browser_info(device_info.get('user_agent', '')),
        'screen_info': device_info.get('screen_resolution', ''),
        'timezone': device_info.get('timezone', ''),
        'language': device_info.get('language', ''),
        'plugin_count': len(device_info.get('plugins', []))
    }

def _check_device_risk_factors(device_info):
    """Check for device-based risk factors"""
    risk_factors = []
    
    user_agent = device_info.get('user_agent', '').lower()
    if 'bot' in user_agent or 'crawler' in user_agent:
        risk_factors.append("Bot-like user agent")
    
    if not device_info.get('plugins'):
        risk_factors.append("No browser plugins detected")
    
    return risk_factors

def _calculate_device_risk(device_analysis, risk_factors):
    """Calculate device risk score"""
    risk = len(risk_factors) * 0.3
    
    # Additional risk factors
    if device_analysis.get('plugin_count', 0) == 0:
        risk += 0.2
    
    return round(min(risk, 1.0), 3)

def _simulate_ml_prediction(features):
    """Simulate ML model prediction"""
    # Simple simulation based on features
    risk_score = 0
    
    # Amount-based risk
    if features['transaction_amount'] > 1000:
        risk_score += 0.3
    
    # Time-based risk
    if features['hour_of_day'] < 6 or features['hour_of_day'] > 22:
        risk_score += 0.2
    
    # User history risk
    if features['user_age_days'] < 30:
        risk_score += 0.4
    
    # Add some randomness
    risk_score += random.uniform(-0.1, 0.1)
    
    return {
        'fraud_probability': round(max(0, min(risk_score, 1.0)), 3),
        'confidence': round(random.uniform(0.8, 0.95), 3),
        'prediction': 'fraud' if risk_score > 0.5 else 'legitimate'
    }

def _calculate_feature_importance(features):
    """Calculate feature importance for ML explanation"""
    importance = {}
    total_features = len(features)
    
    for feature, value in features.items():
        # Simulate importance based on feature type
        if 'amount' in feature:
            importance[feature] = round(random.uniform(0.15, 0.25), 3)
        elif 'age' in feature or 'history' in feature:
            importance[feature] = round(random.uniform(0.10, 0.20), 3)
        else:
            importance[feature] = round(random.uniform(0.05, 0.15), 3)
    
    # Normalize to sum to 1
    total_importance = sum(importance.values())
    for feature in importance:
        importance[feature] = round(importance[feature] / total_importance, 3)
    
    return importance

def _generate_ml_explanation(prediction, feature_importance):
    """Generate explanation for ML prediction"""
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
    
    explanation = f"Prediction: {prediction['prediction']} (confidence: {prediction['confidence']})\n"
    explanation += "Top contributing factors:\n"
    
    for feature, importance in top_features:
        explanation += f"- {feature}: {importance:.1%} importance\n"
    
    return explanation

# Helper functions
def _is_unusual_time(timestamp_str):
    """Check if timestamp represents unusual time"""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.hour < 6 or dt.hour > 23
    except:
        return False

def _detect_purchase_spike(purchase_history):
    """Detect if there's a recent spike in purchases"""
    if len(purchase_history) < 5:
        return False
    
    recent_count = sum(1 for p in purchase_history[-5:])
    return recent_count > 3

def _luhn_check(card_number):
    """Perform Luhn algorithm check"""
    digits = [int(d) for d in card_number.replace(' ', '') if d.isdigit()]
    if len(digits) < 13:
        return False
    
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    
    return checksum % 10 == 0

def _detect_card_type(card_number):
    """Detect card type from number"""
    card_number = card_number.replace(' ', '')
    
    if card_number.startswith('4'):
        return 'Visa'
    elif card_number.startswith('5') or card_number.startswith('2'):
        return 'Mastercard'
    elif card_number.startswith('3'):
        return 'American Express'
    else:
        return 'Unknown'

def _check_name_patterns(name):
    """Check for suspicious name patterns"""
    suspicious = []
    
    if len(name.split()) < 2:
        suspicious.append("Single name only")
    
    if any(char.isdigit() for char in name):
        suspicious.append("Contains numbers")
    
    return suspicious

def _extract_browser_info(user_agent):
    """Extract browser information from user agent"""
    if 'Chrome' in user_agent:
        return 'Chrome'
    elif 'Firefox' in user_agent:
        return 'Firefox'
    elif 'Safari' in user_agent:
        return 'Safari'
    else:
        return 'Unknown'

