from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import hashlib
import re
from src.models.admin_user import db, AdminUser, AdminSession
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('admin_token')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        current_user = AdminUser.verify_token(token)
        if not current_user:
            return jsonify({'success': False, 'message': 'Token is invalid or expired'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def permission_required(permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if not current_user.has_permission(permission):
                return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

@auth_bp.route('/login', methods=['POST'])
def login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Find user by username or email
        user = AdminUser.query.filter(
            (AdminUser.username == username) | (AdminUser.email == username)
        ).first()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Check if account is locked
        if user.is_locked():
            return jsonify({
                'success': False,
                'message': 'Account is temporarily locked due to multiple failed login attempts'
            }), 401
        
        # Check if account is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is deactivated'
            }), 401
        
        # Verify password
        if not user.check_password(password):
            user.increment_failed_attempts()
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Reset failed attempts on successful login
        user.reset_failed_attempts()
        user.update_last_login()
        
        # Generate token
        expires_in = 604800 if remember_me else 86400  # 7 days or 24 hours
        token = user.generate_token(expires_in)
        
        # Create session record
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        session = AdminSession(
            user_id=user.id,
            token_hash=token_hash,
            expires_in=expires_in,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        db.session.add(session)
        db.session.commit()
        
        # Create response with HTTP-only cookie
        response = make_response(jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }))
        
        response.set_cookie(
            'admin_token',
            token,
            max_age=expires_in,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax'
        )
        
        return response, 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Admin logout endpoint"""
    try:
        token = request.cookies.get('admin_token')
        if token:
            # Remove session from database
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            session = AdminSession.query.filter_by(
                user_id=current_user.id,
                token_hash=token_hash
            ).first()
            if session:
                db.session.delete(session)
                db.session.commit()
        
        # Clear cookie
        response = make_response(jsonify({
            'success': True,
            'message': 'Logout successful'
        }))
        response.set_cookie('admin_token', '', expires=0)
        
        return response, 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Logout failed: {str(e)}'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user information"""
    try:
        return jsonify({
            'success': True,
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching user info: {str(e)}'
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """Change user password"""
    try:
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'message': 'Current password and new password are required'
            }), 400
        
        # Verify current password
        if not current_user.check_password(current_password):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 400
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error changing password: {str(e)}'
        }), 500

@auth_bp.route('/users', methods=['GET'])
@token_required
@permission_required('manage_users')
def get_admin_users(current_user):
    """Get list of admin users"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        
        query = AdminUser.query
        
        # Filter by search if provided
        if search:
            query = query.filter(
                (AdminUser.username.contains(search)) |
                (AdminUser.email.contains(search))
            )
        
        # Pagination
        total = query.count()
        users = query.offset((page - 1) * limit).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in users],
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching admin users: {str(e)}'
        }), 500

@auth_bp.route('/users', methods=['POST'])
@token_required
@permission_required('create_moderator')
def create_admin_user(current_user):
    """Create new admin user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        role = data.get('role', 'moderator')
        
        # Validation
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'Username, email, and password are required'
            }), 400
        
        # Check if user can create this role
        if role == 'admin' and not current_user.has_permission('create_admin'):
            return jsonify({
                'success': False,
                'message': 'Insufficient permissions to create admin user'
            }), 403
        
        if role not in ['admin', 'moderator']:
            return jsonify({
                'success': False,
                'message': 'Invalid role specified'
            }), 400
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Check if username or email already exists
        existing_user = AdminUser.query.filter(
            (AdminUser.username == username) | (AdminUser.email == email)
        ).first()
        
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username or email already exists'
            }), 400
        
        # Create new user
        new_user = AdminUser(
            username=username,
            email=email,
            password=password,
            role=role,
            created_by=current_user.id
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{role.title()} user created successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating user: {str(e)}'
        }), 500

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@permission_required('manage_users')
def update_admin_user(current_user, user_id):
    """Update admin user"""
    try:
        target_user = AdminUser.query.get(user_id)
        if not target_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Check if current user can manage target user
        if not current_user.can_manage_user(target_user):
            return jsonify({
                'success': False,
                'message': 'Insufficient permissions to modify this user'
            }), 403
        
        data = request.get_json()
        
        # Update fields
        if 'username' in data:
            target_user.username = data['username'].strip()
        
        if 'email' in data:
            target_user.email = data['email'].strip()
        
        if 'is_active' in data:
            target_user.is_active = data['is_active']
        
        if 'role' in data and current_user.has_permission('create_admin'):
            if data['role'] in ['admin', 'moderator']:
                target_user.role = data['role']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': target_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating user: {str(e)}'
        }), 500

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@permission_required('delete_users')
def delete_admin_user(current_user, user_id):
    """Delete admin user"""
    try:
        target_user = AdminUser.query.get(user_id)
        if not target_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Prevent self-deletion
        if target_user.id == current_user.id:
            return jsonify({
                'success': False,
                'message': 'Cannot delete your own account'
            }), 400
        
        # Check if current user can manage target user
        if not current_user.can_manage_user(target_user):
            return jsonify({
                'success': False,
                'message': 'Insufficient permissions to delete this user'
            }), 403
        
        db.session.delete(target_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting user: {str(e)}'
        }), 500

@auth_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@token_required
@permission_required('manage_users')
def reset_user_password(current_user, user_id):
    """Reset user password"""
    try:
        target_user = AdminUser.query.get(user_id)
        if not target_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Check if current user can manage target user
        if not current_user.can_manage_user(target_user):
            return jsonify({
                'success': False,
                'message': 'Insufficient permissions to reset password for this user'
            }), 403
        
        data = request.get_json()
        new_password = data.get('new_password', '')
        
        if not new_password:
            return jsonify({
                'success': False,
                'message': 'New password is required'
            }), 400
        
        # Validate password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Update password
        target_user.set_password(new_password)
        target_user.unlock_account()  # Unlock if locked
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password reset successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error resetting password: {str(e)}'
        }), 500

@auth_bp.route('/cleanup-sessions', methods=['POST'])
@token_required
@permission_required('system_config')
def cleanup_expired_sessions(current_user):
    """Cleanup expired sessions"""
    try:
        count = AdminSession.cleanup_expired()
        return jsonify({
            'success': True,
            'message': f'Cleaned up {count} expired sessions'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error cleaning up sessions: {str(e)}'
        }), 500

