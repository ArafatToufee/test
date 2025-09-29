from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import random
import time
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

# Sample product data for demonstration
SAMPLE_PRODUCTS = [
    {"id": "1", "name": "Wireless Headphones", "price": 199.99, "category": "Electronics", "stock": 50},
    {"id": "2", "name": "Smartphone", "price": 799.99, "category": "Electronics", "stock": 25},
    {"id": "3", "name": "Running Shoes", "price": 129.99, "category": "Sports", "stock": 100},
    {"id": "4", "name": "Coffee Maker", "price": 89.99, "category": "Home & Kitchen", "stock": 30},
    {"id": "5", "name": "Laptop", "price": 1299.99, "category": "Electronics", "stock": 15},
    {"id": "6", "name": "Yoga Mat", "price": 39.99, "category": "Sports", "stock": 75}
]

# Sample order data
SAMPLE_ORDERS = [
    {"id": "ORD001", "status": "shipped", "total": 199.99, "items": ["Wireless Headphones"]},
    {"id": "ORD002", "status": "processing", "total": 929.98, "items": ["Smartphone", "Running Shoes"]},
    {"id": "ORD003", "status": "delivered", "total": 89.99, "items": ["Coffee Maker"]}
]

# FAQ responses
FAQ_RESPONSES = {
    "shipping": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, and express shipping takes 1-2 business days.",
    "returns": "You can return items within 30 days of purchase. Items must be in original condition with tags attached.",
    "payment": "We accept all major credit cards, PayPal, and Apple Pay. Your payment information is securely encrypted.",
    "support": "Our customer support team is available 24/7. You can reach us via chat, email at support@refcommerce.com, or phone at 1-800-REF-SHOP.",
    "account": "You can create an account to track orders, save favorites, and get personalized recommendations. Account creation is free and takes less than a minute.",
    "warranty": "All electronics come with a 1-year manufacturer warranty. Extended warranties are available for purchase."
}

def get_intent_and_entities(message):
    """Simple intent recognition and entity extraction"""
    message_lower = message.lower()
    
    # Product search intent
    if any(word in message_lower for word in ["find", "search", "looking for", "show me", "product"]):
        # Extract product category or name
        for product in SAMPLE_PRODUCTS:
            if product["name"].lower() in message_lower or product["category"].lower() in message_lower:
                return "product_search", {"product": product}
        return "product_search", {"query": message}
    
    # Order status intent
    if any(word in message_lower for word in ["order", "tracking", "status", "ord"]):
        # Extract order ID if present
        for order in SAMPLE_ORDERS:
            if order["id"].lower() in message_lower:
                return "order_status", {"order": order}
        return "order_status", {"query": message}
    
    # FAQ intents
    if any(word in message_lower for word in ["shipping", "delivery", "ship"]):
        return "faq", {"topic": "shipping"}
    elif any(word in message_lower for word in ["return", "refund", "exchange"]):
        return "faq", {"topic": "returns"}
    elif any(word in message_lower for word in ["payment", "pay", "credit card", "paypal"]):
        return "faq", {"topic": "payment"}
    elif any(word in message_lower for word in ["support", "help", "contact"]):
        return "faq", {"topic": "support"}
    elif any(word in message_lower for word in ["account", "register", "sign up", "login"]):
        return "faq", {"topic": "account"}
    elif any(word in message_lower for word in ["warranty", "guarantee"]):
        return "faq", {"topic": "warranty"}
    
    # Greeting intent
    if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "greeting", {}
    
    # Default fallback
    return "fallback", {}

def generate_response(intent, entities, user_message):
    """Generate appropriate response based on intent and entities"""
    
    if intent == "greeting":
        greetings = [
            "Hello! Welcome to RefCommerce! How can I help you today?",
            "Hi there! I'm here to assist you with your shopping needs. What can I do for you?",
            "Welcome! I'm your AI shopping assistant. Feel free to ask me about products, orders, or any questions you have!"
        ]
        return random.choice(greetings)
    
    elif intent == "product_search":
        if "product" in entities:
            product = entities["product"]
            return f"I found the {product['name']} for ${product['price']}. It's in the {product['category']} category and we have {product['stock']} in stock. Would you like to know more about this product?"
        else:
            # Return multiple products
            products_text = "Here are some popular products:\n"
            for product in SAMPLE_PRODUCTS[:3]:
                products_text += f"• {product['name']} - ${product['price']} ({product['category']})\n"
            products_text += "\nWould you like more details about any of these products?"
            return products_text
    
    elif intent == "order_status":
        if "order" in entities:
            order = entities["order"]
            return f"Your order {order['id']} is currently {order['status']}. Total: ${order['total']}. Items: {', '.join(order['items'])}."
        else:
            return "I can help you check your order status. Please provide your order ID (e.g., ORD001) or log into your account to view all orders."
    
    elif intent == "faq":
        topic = entities.get("topic", "support")
        return FAQ_RESPONSES.get(topic, FAQ_RESPONSES["support"])
    
    else:  # fallback
        return "I'm here to help! You can ask me about:\n• Product information and search\n• Order status and tracking\n• Shipping and returns\n• Payment methods\n• Account help\n\nWhat would you like to know?"

@chatbot_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({
                'error': 'Message is required'
            }), 400
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Get intent and entities
        intent, entities = get_intent_and_entities(user_message)
        
        # Generate response
        response_text = generate_response(intent, entities, user_message)
        
        # Prepare response
        response = {
            'response': response_text,
            'intent': intent,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'confidence': random.uniform(0.8, 0.95)  # Simulated confidence score
        }
        
        # Add suggested actions based on intent
        if intent == "product_search":
            response['suggested_actions'] = [
                {'text': 'View all Electronics', 'action': 'browse_category', 'data': 'Electronics'},
                {'text': 'Show me deals', 'action': 'show_deals', 'data': None}
            ]
        elif intent == "order_status":
            response['suggested_actions'] = [
                {'text': 'Track another order', 'action': 'track_order', 'data': None},
                {'text': 'Contact support', 'action': 'contact_support', 'data': None}
            ]
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred processing your request',
            'details': str(e)
        }), 500

@chatbot_bp.route('/chat/suggestions', methods=['GET'])
@cross_origin()
def get_suggestions():
    """Get suggested conversation starters"""
    suggestions = [
        "Show me electronics",
        "What's your return policy?",
        "Track my order ORD001",
        "How does shipping work?",
        "Help me find running shoes",
        "What payment methods do you accept?"
    ]
    
    return jsonify({
        'suggestions': random.sample(suggestions, 4)
    })

@chatbot_bp.route('/chat/feedback', methods=['POST'])
@cross_origin()
def chat_feedback():
    """Receive feedback on chatbot responses"""
    try:
        data = request.get_json()
        feedback_type = data.get('type')  # 'positive' or 'negative'
        message_id = data.get('message_id')
        comment = data.get('comment', '')
        
        # In a real implementation, this would be stored in a database
        # For now, we'll just acknowledge the feedback
        
        return jsonify({
            'message': 'Thank you for your feedback! It helps us improve.',
            'feedback_received': True
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to process feedback',
            'details': str(e)
        }), 500

@chatbot_bp.route('/chat/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'RefCommerce AI Chatbot',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

