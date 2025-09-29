# E-commerce Platform - Microservices Architecture

A comprehensive e-commerce platform built with microservices architecture, featuring multiple services for product management, user authentication, shopping cart, order processing, and payment handling.

## 🏗️ Architecture Overview

The platform consists of the following microservices:

### Core Services
- **API Gateway** (Port 8080) - Central entry point for all API requests
- **Auth Service** (Port 5001) - User authentication and authorization
- **Product Service** (Port 5002) - Product catalog management
- **Cart Service** (Port 5003) - Shopping cart functionality
- **Order Service** (Port 5004) - Order management and processing
- **Payment Service** (Port 5005) - Payment processing

### AI Services (Planned)
- **Recommendation Service** (Port 5006) - Product recommendations
- **Visual Search Service** (Port 5007) - Image-based product search
- **Fraud Detection Service** (Port 5008) - Transaction fraud detection
- **Voice Assistant Service** (Port 5009) - Voice-based shopping assistant
- **Dynamic Pricing Service** (Port 5010) - AI-powered pricing optimization

### Infrastructure
- **MySQL Database** (Port 3306) - Primary data storage
- **Redis Cache** (Port 6379) - Caching and session storage
- **React Frontend** (Port 3000) - User interface

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.11+ (for local development)

### Running with Docker Compose
```bash
cd ecommerce-platform
docker-compose up -d
```

### API Gateway Access
The API Gateway is accessible at: **https://8080-ipljtdvqszg3uf8p57mc6-04dbd043.manusvm.computer**

## 📚 API Documentation

### Authentication Service (`/auth`)

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "address": "123 Main St, City, State"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get Profile
```http
GET /auth/profile
Authorization: Bearer <jwt_token>
```

### Product Service (`/products`)

#### Get All Products
```http
GET /products
```

#### Get Products with Filters
```http
GET /products?category=Electronics&search=phone&min_price=100&max_price=1000
```

#### Create Product
```http
POST /products
Content-Type: application/json

{
  "name": "Smartphone",
  "description": "Latest smartphone with advanced features",
  "price": 799.99,
  "category": "Electronics",
  "stock_quantity": 50,
  "image_url": "https://example.com/phone.jpg"
}
```

#### Get Product by ID
```http
GET /products/{product_id}
```

#### Update Product
```http
PUT /products/{product_id}
Content-Type: application/json

{
  "name": "Updated Product Name",
  "price": 899.99
}
```

#### Delete Product
```http
DELETE /products/{product_id}
```

### Cart Service (`/cart`)

#### Get Cart Items
```http
GET /cart
Authorization: Bearer <jwt_token>
```

#### Add Item to Cart
```http
POST /cart/add
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "product_id": "prod-1",
  "product_name": "Smartphone",
  "product_price": 799.99,
  "quantity": 1
}
```

#### Update Cart Item
```http
PUT /cart/update/{item_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "quantity": 2
}
```

#### Remove Cart Item
```http
DELETE /cart/remove/{item_id}
Authorization: Bearer <jwt_token>
```

#### Clear Cart
```http
DELETE /cart/clear
Authorization: Bearer <jwt_token>
```

### Order Service (`/orders`)

#### Create Order
```http
POST /orders
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "items": [
    {
      "product_id": "prod-1",
      "product_name": "Smartphone",
      "product_price": 799.99,
      "quantity": 1
    }
  ],
  "shipping_address": "123 Main St, City, State",
  "payment_method": "credit_card"
}
```

#### Get Orders
```http
GET /orders
Authorization: Bearer <jwt_token>
```

#### Get Order by ID
```http
GET /orders/{order_id}
Authorization: Bearer <jwt_token>
```

#### Update Order Status
```http
PUT /orders/{order_id}/status
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "status": "confirmed"
}
```

#### Cancel Order
```http
PUT /orders/{order_id}/cancel
Authorization: Bearer <jwt_token>
```

### Payment Service (`/payments`)

#### Process Payment
```http
POST /payments
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "order_id": "order-123",
  "amount": 799.99,
  "payment_method": "credit_card",
  "currency": "USD"
}
```

#### Get Payment by ID
```http
GET /payments/{payment_id}
Authorization: Bearer <jwt_token>
```

#### Get Payment by Order
```http
GET /payments/order/{order_id}
Authorization: Bearer <jwt_token>
```

#### Refund Payment
```http
POST /payments/{payment_id}/refund
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "amount": 799.99
}
```

## 🛠️ Development

### Service Structure
Each service follows a consistent structure:
```
service-name/
├── src/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   └── main.py         # Application entry point
├── Dockerfile
├── requirements.txt
└── venv/               # Virtual environment
```

### Adding New Services
1. Create service directory in `services/` or `ai-services/`
2. Use `manus-create-flask-app` to scaffold the service
3. Implement models and routes
4. Add service to `docker-compose.yml`
5. Update API Gateway routing

### Database Schema
The platform uses MySQL with the following main tables:
- `users` - User accounts and profiles
- `products` - Product catalog
- `cart_items` - Shopping cart items
- `orders` - Order records
- `order_items` - Order line items
- `payments` - Payment transactions

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL` - MySQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT signing key
- Service URLs for inter-service communication

### Security
- JWT-based authentication
- CORS enabled for frontend integration
- Input validation and sanitization
- Secure password hashing

## 📊 Features Implemented

### ✅ Completed
- User registration and authentication
- Product catalog with CRUD operations
- Shopping cart management
- Order processing and tracking
- Payment processing simulation
- API Gateway with service routing
- Docker containerization
- Database initialization
- CORS configuration

### 🔄 In Progress / Planned
- AI-powered product recommendations
- Visual search functionality
- Fraud detection system
- Voice shopping assistant
- Dynamic pricing optimization
- Frontend React application
- Real payment gateway integration
- Email notifications
- Admin dashboard

## 🚀 Deployment

The platform is designed for cloud deployment with:
- Docker Compose for local development
- Kubernetes manifests for production
- Load balancing and auto-scaling
- Monitoring and logging
- CI/CD pipeline integration

## 📞 Support

For questions or issues, please refer to the API documentation or contact the development team.

---

**Note**: This is a demonstration platform. For production use, additional security measures, monitoring, and testing should be implemented.

