# Todo List API - Assignment 8

## 📋 Overview

This is a comprehensive Todo List API built with FastAPI that supports user authentication, multiple lists, task management, and advanced features like deadline tracking and task prioritization.

## 🚀 Features

### ✅ Authentication & Security
- **Bearer Token Authentication**: JWT-based authentication system
- **User Registration**: Secure user registration with email validation
- **User Login**: Secure login with password hashing
- **Protected Endpoints**: All core API endpoints require authentication

### ✅ List Management
- Create, read, update, and delete lists
- View all lists with associated tasks
- Secure access with authentication

### ✅ Task Management
- Create, read, update, and delete tasks within lists
- Mark tasks as completed/uncompleted
- Set deadlines and priorities for tasks
- View tasks due this week across all lists
- Order tasks by deadline

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Database**: JSON file-based storage
- **Documentation**: Auto-generated with FastAPI

## 📁 Project Structure

```
assignment-8/
├── README-Final.md                    # This file
├── Todo-List-API.postman_collection.json  # Postman collection
├── requirements.txt                   # Python dependencies
├── run.py                           # Application entry point
├── app/
│   ├── main.py                      # FastAPI application setup
│   ├── api/
│   │   └── routes/
│   │       ├── auth_routes.py       # Authentication endpoints
│   │       ├── list_routes.py       # List management endpoints
│   │       └── task_routes.py       # Task management endpoints
│   ├── core/
│   │   └── config.py                # Application configuration
│   ├── db/
│   │   ├── database.py              # Database operations
│   │   ├── data.json                # Lists and tasks data
│   │   └── users.json               # Users data (auto-generated)
│   ├── models/
│   │   ├── list_model.py            # List data model
│   │   ├── task_model.py            # Task data model
│   │   └── user_model.py            # User data model
│   ├── schemas/
│   │   ├── auth_schema.py           # Authentication schemas
│   │   ├── list_schema.py           # List request/response schemas
│   │   └── task_schema.py           # Task request/response schemas
│   └── services/
│       ├── auth_service.py          # Authentication business logic
│       ├── list_service.py          # List business logic
│       └── task_service.py          # Task business logic
└── tests/                           # Test files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignment-8
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Documentation: `http://localhost:8000/docs`
   - Alternative Documentation: `http://localhost:8000/redoc`

## 🔐 Authentication Flow

### 1. Register a New User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Login to Get Access Token
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. Use Bearer Token for Protected Endpoints
```bash
curl -X GET "http://localhost:8000/api/lists" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📚 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/auth/me` | Get current user info | Yes |

### List Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/lists` | Get all lists | Yes |
| GET | `/api/lists/{list_id}` | Get specific list | Yes |
| POST | `/api/lists` | Create new list | Yes |
| PUT | `/api/lists/{list_id}` | Update list | Yes |
| DELETE | `/api/lists/{list_id}` | Delete list | Yes |

### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/lists/{list_id}/tasks` | Get all tasks in list | Yes |
| GET | `/api/lists/{list_id}/tasks/{task_id}` | Get specific task | Yes |
| POST | `/api/lists/{list_id}/tasks` | Create new task | Yes |
| PUT | `/api/lists/{list_id}/tasks/{task_id}` | Update task | Yes |
| DELETE | `/api/lists/{list_id}/tasks/{task_id}` | Delete task | Yes |
| PATCH | `/api/lists/{list_id}/tasks/{task_id}/complete` | Toggle task completion | Yes |

### Special Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/due-this-week` | Get tasks due this week | Yes |
| GET | `/api/lists/{list_id}/tasks/ordered` | Get tasks ordered by deadline | Yes |

## 📋 Request/Response Examples

### Create a List
**Request:**
```json
POST /api/lists
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Work Tasks",
  "description": "Tasks for work projects"
}
```

**Response:**
```json
{
  "id": "list-123",
  "name": "Work Tasks",
  "description": "Tasks for work projects",
  "tasks": []
}
```

### Create a Task
**Request:**
```json
POST /api/lists/list-123/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Complete API documentation",
  "description": "Write comprehensive API docs",
  "deadline": "2024-07-03T23:59:00Z",
  "priority": "high"
}
```

**Response:**
```json
{
  "id": "task-456",
  "title": "Complete API documentation",
  "description": "Write comprehensive API docs",
  "completed": false,
  "deadline": "2024-07-03T23:59:00Z",
  "priority": "high",
  "created_at": "2024-07-01T10:00:00Z"
}
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Test Coverage
- Unit tests for all services
- Integration tests for API endpoints
- Authentication flow tests

## 📦 Postman Collection

A comprehensive Postman collection is included: `Todo-List-API.postman_collection.json`

### Import Instructions:
1. Open Postman
2. Click "Import" button
3. Select the `Todo-List-API.postman_collection.json` file
4. Set up environment variables:
   - `base_url`: `http://localhost:8000`
   - `access_token`: (will be set after login)
   - `list_id`: (will be set after creating a list)
   - `task_id`: (will be set after creating a task)

### Collection Features:
- ✅ All authentication endpoints
- ✅ Complete CRUD operations for lists
- ✅ Complete CRUD operations for tasks
- ✅ Special task endpoints (due this week, ordered by deadline)
- ✅ Pre-configured request bodies with examples
- ✅ Proper authentication headers
- ✅ Environment variables for easy testing

## 🔧 Configuration

### Environment Variables
The application uses the following configuration (can be extended with environment variables):

- `APP_NAME`: "Todo List API"
- `API_PREFIX`: "/api"
- `SECRET_KEY`: JWT secret key (change in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30

### Default Admin User
A default admin user is automatically created:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

## 🚨 Security Considerations

### Production Deployment
1. **Change JWT Secret Key**: Update the secret key in `auth_service.py`
2. **Use Environment Variables**: Store sensitive data in environment variables
3. **Enable HTTPS**: Use HTTPS in production
4. **Database**: Consider using a proper database instead of JSON files
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **CORS**: Configure CORS properly for your frontend domain

### Security Features Implemented
- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Protected API endpoints
- ✅ Input validation with Pydantic
- ✅ Error handling and proper HTTP status codes

## 📊 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Schema
The API follows RESTful principles with:
- Consistent HTTP status codes
- JSON request/response format
- Proper error handling
- Comprehensive validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 License

This project is created for educational purposes as part of Binar Academy assignment.

## 🆘 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the test files for usage examples
3. Check the Postman collection for request examples

---

## ✅ Assignment 8 Checklist

### 1. Bearer Token Authentication ✅
- [x] User registration endpoint (`/api/auth/register`)
- [x] User login endpoint (`/api/auth/login`)
- [x] JWT token generation and validation
- [x] Password hashing with bcrypt
- [x] Protected API endpoints (Lists, Tasks)
- [x] Authentication middleware implementation

### 2. Comprehensive Postman Collection ✅
- [x] Complete API collection with all endpoints
- [x] Authentication requests (register, login, me)
- [x] List CRUD operations
- [x] Task CRUD operations
- [x] Special task endpoints (due this week, ordered)
- [x] Example request bodies and headers
- [x] Environment variables setup
- [x] Proper authentication headers

### 3. AI/Developer-Friendly README ✅
- [x] Clear project overview and features
- [x] Technology stack documentation
- [x] Installation and setup instructions
- [x] Authentication flow explanation
- [x] Complete API endpoint documentation
- [x] Request/response examples
- [x] Postman collection import instructions
- [x] Testing instructions
- [x] Security considerations
- [x] Production deployment guidelines

### 4. Additional Features ✅
- [x] User model with secure password handling
- [x] Authentication service with JWT
- [x] Protected routes with dependency injection
- [x] Comprehensive error handling
- [x] Input validation with Pydantic schemas
- [x] Auto-generated API documentation
- [x] Test coverage for all features

---

**🎉 Assignment 8 Complete! The API is ready for secure, real-world frontend consumption with comprehensive documentation and testing tools.** 