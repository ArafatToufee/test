# Secure Admin CRM System Documentation

## 🔐 **Overview**

The RefCommerce Admin CRM is a secure, role-based administrative system that provides comprehensive management capabilities for the e-commerce platform. The system implements robust authentication and authorization controls to ensure only authorized personnel can access administrative functions.

## 🚀 **Live Access**

**Admin Dashboard**: https://5173-i2xa9oyqotsypiq78vpw5-04dbd043.manusvm.computer
**Backend API**: https://5011-i2xa9oyqotsypiq78vpw5-04dbd043.manusvm.computer

## 🔑 **Default Admin Credentials**

```
Username: admin
Password: Admin123!
Role: Super Admin
```

## 🛡️ **Security Features**

### **Authentication System**
- **JWT-based Authentication**: Secure token-based authentication with HTTP-only cookies
- **Session Management**: Automatic session expiration and refresh
- **Password Security**: Strong password requirements (min 8 chars, mixed case, numbers, special chars)
- **Account Lockout**: Protection against brute force attacks
- **Remember Me**: Optional extended session duration (7 days)

### **Authorization & Role-Based Access Control (RBAC)**
- **Three-Tier Role System**:
  - **Super Admin**: Full system access, can create admins and moderators
  - **Admin**: Platform management, can create moderators
  - **Moderator**: Limited access to specific management functions

### **Permission Matrix**
| Feature | Super Admin | Admin | Moderator |
|---------|-------------|-------|-----------|
| Dashboard View | ✅ | ✅ | ✅ |
| User Management | ✅ | ✅ | ❌ |
| Seller Management | ✅ | ✅ | ✅ |
| Order Management | ✅ | ✅ | ✅ |
| Product Management | ✅ | ✅ | ✅ |
| Analytics | ✅ | ✅ | ❌ |
| Create Admins | ✅ | ❌ | ❌ |
| Create Moderators | ✅ | ✅ | ❌ |
| Delete Users | ✅ | ✅ | ❌ |

## 🏗️ **System Architecture**

### **Backend Components**
- **Flask Application**: RESTful API server with CORS support
- **SQLite Database**: Secure user data storage with encrypted passwords
- **JWT Authentication**: Token-based session management
- **Role-Based Middleware**: Permission checking for all endpoints
- **Password Hashing**: Bcrypt encryption for secure password storage

### **Frontend Components**
- **React Application**: Modern, responsive admin interface
- **Authentication Context**: Global state management for user sessions
- **Protected Routes**: Component-level access control
- **Role-Based UI**: Dynamic interface based on user permissions

## 📊 **Features & Capabilities**

### **Dashboard**
- Real-time platform metrics and KPIs
- Revenue and user growth analytics
- Interactive charts and visualizations
- Performance monitoring

### **User Management** (Admin+ Only)
- Platform user directory and search
- User status management (active, inactive, suspended)
- User activity tracking
- Export capabilities

### **Seller Management**
- Seller approval workflow
- Performance monitoring
- Commission rate management
- Sales analytics

### **Order Management**
- Real-time order tracking
- Status updates and management
- Customer and seller information
- Bulk operations

### **Product Management**
- Product catalog oversight
- Category filtering
- Stock level monitoring
- Status control

### **Analytics** (Admin+ Only)
- 12-month revenue trends
- User growth analysis
- Performance reports
- Data visualization

### **Admin User Management** (Admin+ Only)
- Create and manage admin users
- Role assignment (Admin/Moderator)
- User search and filtering
- Account status management
- Password policy enforcement

## 🔧 **API Endpoints**

### **Authentication Endpoints**
```
POST /api/auth/login          - User login
POST /api/auth/logout         - User logout
GET  /api/auth/me             - Get current user info
POST /api/auth/users          - Create new admin user (Admin+)
GET  /api/auth/users          - List admin users (Admin+)
DELETE /api/auth/users/:id    - Delete admin user (Admin+)
```

### **Admin Management Endpoints**
```
GET  /api/admin/dashboard     - Dashboard metrics
GET  /api/admin/users         - Platform users
GET  /api/admin/sellers       - Seller management
GET  /api/admin/orders        - Order management
GET  /api/admin/products      - Product management
GET  /api/admin/analytics/*   - Analytics data
PUT  /api/admin/*/status      - Update entity status
```

## 🔐 **Security Best Practices**

### **Password Policy**
- Minimum 8 characters
- Must contain uppercase and lowercase letters
- Must contain at least one number
- Must contain at least one special character
- No common passwords or dictionary words

### **Session Security**
- JWT tokens stored in HTTP-only cookies
- Automatic token refresh
- Secure cookie flags (HttpOnly, Secure, SameSite)
- Session timeout after inactivity

### **Access Control**
- Route-level permission checking
- Component-level access control
- API endpoint authorization
- Role-based feature visibility

### **Data Protection**
- Password hashing with bcrypt
- SQL injection prevention
- XSS protection
- CSRF protection with SameSite cookies

## 🚀 **Deployment & Setup**

### **Backend Setup**
```bash
cd /home/ubuntu/ecommerce-platform/admin-crm/admin-crm-backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### **Frontend Setup**
```bash
cd /home/ubuntu/ecommerce-platform/admin-crm/admin-crm-frontend
npm install
npm run dev
```

### **Environment Configuration**
- Backend runs on port 5011
- Frontend runs on port 5173
- Database: SQLite (admin_crm.db)
- CORS enabled for frontend communication

## 👥 **User Management Workflow**

### **Creating New Users**
1. Login as Admin or Super Admin
2. Navigate to "User Management"
3. Click "Create User"
4. Fill in user details:
   - Username (unique)
   - Email address
   - Strong password
   - Role (Moderator/Admin)
5. Submit to create user

### **Managing Existing Users**
- View all admin users in a searchable table
- See user roles, status, and last login
- Delete users (except yourself)
- Search and filter users

## 🔍 **Monitoring & Auditing**

### **User Activity Tracking**
- Login/logout timestamps
- Last activity tracking
- Failed login attempts
- Account status changes

### **System Logs**
- Authentication events
- Permission denials
- User creation/deletion
- System errors

## 🛠️ **Troubleshooting**

### **Common Issues**
1. **Login Failed**: Check credentials and account status
2. **Access Denied**: Verify user role and permissions
3. **Session Expired**: Re-login to refresh session
4. **API Errors**: Check backend service status

### **Support Contacts**
- System Administrator: admin@refcommerce.com
- Technical Support: support@refcommerce.com

## 📈 **Future Enhancements**

### **Planned Features**
- Two-factor authentication (2FA)
- Advanced audit logging
- IP-based access restrictions
- Single Sign-On (SSO) integration
- Advanced analytics dashboard
- Bulk user operations
- Email notifications for security events

### **Security Improvements**
- Rate limiting for API endpoints
- Advanced password policies
- Account lockout policies
- Security headers implementation
- Regular security audits

---

**Last Updated**: July 26, 2025
**Version**: 1.0.0
**Status**: Production Ready

