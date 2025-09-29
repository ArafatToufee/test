# Admin CRM Authentication & Authorization Design

## Overview
This document outlines the authentication and authorization system for the RefCommerce Admin CRM, ensuring secure access control with role-based permissions.

## Authentication Strategy

### JWT-Based Authentication
- **Token Type**: JSON Web Tokens (JWT)
- **Storage**: HTTP-only cookies for security
- **Expiration**: 24 hours for access tokens, 7 days for refresh tokens
- **Algorithm**: HS256 for token signing

### User Roles
1. **Super Admin**: Full system access, can create/manage admins and moderators
2. **Admin**: Full CRM access, can create/manage moderators
3. **Moderator**: Limited CRM access (read-only for some sections)

## Database Schema

### Admin Users Table
```sql
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'moderator',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES admin_users(id),
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP NULL
);
```

### Session Management Table
```sql
CREATE TABLE admin_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES admin_users(id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT
);
```

## Role-Based Permissions

### Super Admin Permissions
- Full system access
- Create/edit/delete admin users
- Create/edit/delete moderators
- Access all CRM modules
- System configuration
- Audit logs access

### Admin Permissions
- Full CRM access (dashboard, users, sellers, orders, products, analytics)
- Create/edit/delete moderators
- Cannot modify other admins
- Cannot access system configuration

### Moderator Permissions
- Dashboard access (read-only)
- Users management (limited actions)
- Orders management (status updates only)
- Products management (read-only)
- Cannot access user creation/deletion
- Cannot access analytics

## Security Features

### Password Security
- Minimum 8 characters
- Must contain uppercase, lowercase, number, and special character
- Bcrypt hashing with salt rounds = 12
- Password history (prevent reuse of last 5 passwords)

### Account Security
- Account lockout after 5 failed login attempts
- Lockout duration: 30 minutes
- Session timeout: 24 hours
- Concurrent session limit: 3 per user

### API Security
- Rate limiting: 100 requests per minute per IP
- CORS configuration for specific origins
- Request validation and sanitization
- SQL injection prevention
- XSS protection headers

## Authentication Flow

### Login Process
1. User submits username/password
2. Server validates credentials
3. Check account status (active, not locked)
4. Generate JWT access token
5. Set HTTP-only cookie
6. Return user info and permissions
7. Log successful login

### Token Validation
1. Extract token from cookie
2. Verify token signature
3. Check token expiration
4. Validate user exists and is active
5. Check session in database
6. Return user context

### Logout Process
1. Invalidate session in database
2. Clear HTTP-only cookie
3. Log logout event

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/change-password` - Change password

### User Management Endpoints
- `GET /api/admin/users` - List admin users (admin+ only)
- `POST /api/admin/users` - Create admin user (admin+ only)
- `PUT /api/admin/users/{id}` - Update admin user (admin+ only)
- `DELETE /api/admin/users/{id}` - Delete admin user (admin+ only)
- `POST /api/admin/users/{id}/reset-password` - Reset user password (admin+ only)

## Frontend Authentication

### Login Component
- Username/password form
- Remember me option
- Forgot password link
- Error handling and validation

### Route Protection
- Private route wrapper component
- Role-based route access
- Automatic redirect to login
- Permission-based UI rendering

### Session Management
- Automatic token refresh
- Logout on token expiration
- Session timeout warnings
- Concurrent session handling

## Default Admin Account

### Initial Setup
- Username: `admin`
- Email: `admin@refcommerce.com`
- Password: `Admin123!` (must be changed on first login)
- Role: `super_admin`
- Created during database initialization

## Security Considerations

### Data Protection
- Sensitive data encryption at rest
- Secure password storage (bcrypt)
- No plain text passwords in logs
- PII data anonymization in logs

### Network Security
- HTTPS enforcement
- Secure cookie flags
- CSRF protection
- Content Security Policy headers

### Monitoring & Auditing
- Login/logout events logging
- Failed authentication attempts
- Permission changes tracking
- Suspicious activity alerts

## Implementation Phases

### Phase 1: Backend Authentication
- User model and database setup
- JWT token generation/validation
- Login/logout endpoints
- Password hashing and validation

### Phase 2: Authorization System
- Role-based access control
- Permission middleware
- Protected route decorators
- User management APIs

### Phase 3: Frontend Integration
- Login form component
- Authentication context
- Protected routes
- Role-based UI rendering

### Phase 4: Security Hardening
- Rate limiting implementation
- Session management
- Security headers
- Audit logging

## Testing Strategy

### Unit Tests
- Authentication functions
- Password validation
- Token generation/validation
- Permission checking

### Integration Tests
- Login/logout flow
- Protected endpoint access
- Role-based permissions
- Session management

### Security Tests
- Brute force protection
- Token manipulation attempts
- SQL injection prevention
- XSS protection validation

This design ensures a robust, secure authentication and authorization system for the Admin CRM while maintaining usability and scalability.

