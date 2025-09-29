from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

db = SQLAlchemy()

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='moderator')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    created_users = db.relationship('AdminUser', backref=db.backref('creator', remote_side=[id]))
    sessions = db.relationship('AdminSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, role='moderator', created_by=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        self.created_by = created_by
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_locked(self):
        """Check if account is locked"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def lock_account(self):
        """Lock account for 30 minutes"""
        self.locked_until = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
    
    def unlock_account(self):
        """Unlock account and reset failed attempts"""
        self.locked_until = None
        self.failed_login_attempts = 0
        db.session.commit()
    
    def increment_failed_attempts(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account()
        else:
            db.session.commit()
    
    def reset_failed_attempts(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
        db.session.commit()
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def generate_token(self, expires_in=86400):  # 24 hours
        """Generate JWT token"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'role': self.role,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, os.environ.get('SECRET_KEY', 'admin_crm_secret_key_2024'), algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'admin_crm_secret_key_2024'), algorithms=['HS256'])
            user = AdminUser.query.get(payload['user_id'])
            if user and user.is_active and not user.is_locked():
                return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return None
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        permissions = {
            'super_admin': [
                'view_dashboard', 'manage_users', 'manage_sellers', 'manage_orders', 
                'manage_products', 'view_analytics', 'create_admin', 'create_moderator',
                'delete_users', 'system_config', 'audit_logs'
            ],
            'admin': [
                'view_dashboard', 'manage_users', 'manage_sellers', 'manage_orders',
                'manage_products', 'view_analytics', 'create_moderator', 'delete_moderator'
            ],
            'moderator': [
                'view_dashboard', 'view_users', 'manage_orders', 'view_products'
            ]
        }
        return permission in permissions.get(self.role, [])
    
    def can_manage_user(self, target_user):
        """Check if user can manage another user"""
        if self.role == 'super_admin':
            return True
        elif self.role == 'admin':
            return target_user.role in ['moderator']
        return False
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_locked': self.is_locked()
        }


class AdminSession(db.Model):
    __tablename__ = 'admin_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    def __init__(self, user_id, token_hash, expires_in=86400, ip_address=None, user_agent=None):
        self.user_id = user_id
        self.token_hash = token_hash
        self.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    def is_expired(self):
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    @staticmethod
    def cleanup_expired():
        """Remove expired sessions"""
        expired_sessions = AdminSession.query.filter(AdminSession.expires_at < datetime.utcnow()).all()
        for session in expired_sessions:
            db.session.delete(session)
        db.session.commit()
        return len(expired_sessions)

