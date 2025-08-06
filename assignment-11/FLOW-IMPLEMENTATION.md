# Assignment 9 - Flow Implementation

## 🔄 **Authentication Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   App.tsx   │    │ AuthContainer│    │   Header    │      │
│  │             │    │             │    │             │      │
│  │ • Check     │───►│ • Login     │    │ • User Info │      │
│  │   Token     │    │ • Register  │    │ • Logout    │      │
│  │ • Route     │    │ • Switch    │    │ • Welcome   │      │
│  │   Guard     │    │   Forms     │    │   Message   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│           │                   │                   │          │
│           ▼                   ▼                   ▼          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  TodoApp    │    │   Login     │    │   Register  │      │
│  │             │    │   Form      │    │   Form      │      │
│  │ • Lists     │    │ • Username  │    │ • Username  │      │
│  │ • Tasks     │    │ • Password  │    │ • Email     │      │
│  │ • CRUD      │    │ • Submit    │    │ • Password  │      │
│  │   Ops       │    │ • Validation│    │ • Submit    │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API LAYER (Axios)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   api.ts    │    │ Interceptors│    │ Auth API    │      │
│  │             │    │             │    │             │      │
│  │ • Base URL  │    │ • Add Token │    │ • Login     │      │
│  │ • Headers   │    │ • Handle    │    │ • Register  │      │
│  │ • Config    │    │   401 Error │    │ • Get User  │      │
│  │             │    │ • Auto      │    │ • Logout    │      │
│  │             │    │   Logout    │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ auth_routes │    │auth_service │    │ user_model  │      │
│  │             │    │             │    │             │      │
│  │ • /register │    │ • Register  │    │ • Create    │      │
│  │ • /login    │    │ • Login     │    │   User      │      │
│  │ • /me       │    │ • Validate  │    │ • Verify    │      │
│  │ • JWT Auth  │    │ • Hash Pass │    │   Password  │      │
│  │             │    │ • Generate  │    │ • Save to   │      │
│  │             │    │   Token     │    │   JSON      │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│           │                   │                   │          │
│           ▼                   ▼                   ▼          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │list_routes  │    │task_routes  │    │  Database   │      │
│  │             │    │             │    │             │      │
│  │ • Protected │    │ • Protected │    │ • users.json│      │
│  │   Routes    │    │   Routes    │    │ • data.json │      │
│  │ • CRUD      │    │ • CRUD      │    │ • JSON      │      │
│  │   Lists     │    │   Tasks     │    │   Storage   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 **Step-by-Step Implementation**

### **Phase 1: Backend Authentication Setup**

#### **Step 1: User Model Implementation**
```bash
# 1. Create user_model.py
- Implement UserModel class
- Add password hashing with bcrypt
- Create JSON database for users
- Add user CRUD operations

# 2. Create auth_schema.py
- Define UserCreate, UserLogin, UserResponse schemas
- Add validation for email and password
- Set up Pydantic models for request/response
```

#### **Step 2: Authentication Service**
```bash
# 1. Create auth_service.py
- Implement AuthService class
- Add JWT token generation and validation
- Implement user registration logic
- Implement user login logic
- Add password verification

# 2. Configure JWT settings
- Set SECRET_KEY for token signing
- Configure token expiration time
- Set up algorithm (HS256)
```

#### **Step 3: Authentication Routes**
```bash
# 1. Create auth_routes.py
- Add /auth/register endpoint
- Add /auth/login endpoint
- Add /auth/me endpoint
- Implement error handling
- Add input validation

# 2. Update main.py
- Include auth router
- Add CORS configuration
- Set up middleware
```

### **Phase 2: Frontend Authentication Setup**

#### **Step 1: API Configuration**
```bash
# 1. Update api.ts
- Add authentication interfaces
- Implement authApi functions
- Add axios interceptors for token
- Handle 401 errors automatically
- Add localStorage token management
```

#### **Step 2: Authentication Components**
```bash
# 1. Create Login.tsx
- Build login form with validation
- Add password visibility toggle
- Implement error handling
- Add loading states
- Connect to authApi.login

# 2. Create Register.tsx
- Build registration form
- Add email validation
- Add password strength check
- Implement form validation
- Connect to authApi.register

# 3. Create AuthContainer.tsx
- Manage authentication state
- Switch between login/register
- Handle authentication success
- Provide unified auth interface
```

#### **Step 3: Protected App Structure**
```bash
# 1. Update App.tsx
- Add authentication state management
- Implement route protection
- Add logout functionality
- Integrate with Header component
- Handle token persistence

# 2. Create Header.tsx
- Display user information
- Add logout button
- Show welcome message
- Handle user data loading
```

### **Phase 3: Integration & Testing**

#### **Step 1: Backend Testing**
```bash
# 1. Test registration
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# 2. Test login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# 3. Test protected endpoint
curl -X GET "http://localhost:8000/api/lists" \
  -H "Authorization: Bearer <token>"
```

#### **Step 2: Frontend Testing**
```bash
# 1. Start frontend
cd frontend && npm run dev

# 2. Test registration flow
- Navigate to http://localhost:5173
- Click "Sign up"
- Fill registration form
- Submit and verify success

# 3. Test login flow
- Use registered credentials
- Login and verify token storage
- Check protected content access

# 4. Test logout flow
- Click logout button
- Verify token removal
- Check redirect to login
```

## 🔧 **Technical Implementation Details**

### **Backend Security Features**
- **Password Hashing**: bcrypt with salt rounds
- **JWT Tokens**: HS256 algorithm with expiration
- **Input Validation**: Pydantic schemas with constraints
- **Error Handling**: Proper HTTP status codes
- **Database**: JSON file with user data persistence

### **Frontend Security Features**
- **Token Storage**: localStorage with automatic cleanup
- **Auto Logout**: 401 error handling
- **Form Validation**: Client-side validation
- **Protected Routes**: Authentication state management
- **Error Boundaries**: Graceful error handling

### **API Security Features**
- **CORS Configuration**: Proper cross-origin handling
- **Request Interceptors**: Automatic token injection
- **Response Interceptors**: Automatic error handling
- **Type Safety**: TypeScript interfaces
- **Error Handling**: Consistent error responses

## 🎯 **Key Implementation Decisions**

### **1. Authentication Strategy**
- **JWT Tokens**: Stateless authentication
- **Local Storage**: Client-side token persistence
- **Auto Refresh**: Automatic token validation
- **Secure Logout**: Complete token removal

### **2. User Experience**
- **Form Validation**: Real-time validation feedback
- **Loading States**: Visual feedback during operations
- **Error Messages**: Clear error communication
- **Smooth Transitions**: Seamless auth state changes

### **3. Security Considerations**
- **Password Requirements**: Minimum 6 characters
- **Email Validation**: Proper email format checking
- **Token Expiration**: 30-minute token lifetime
- **Input Sanitization**: XSS prevention

## ✅ **Implementation Checklist**

### **Backend Implementation** ✅
- [x] User model with password hashing
- [x] Authentication service with JWT
- [x] Registration and login endpoints
- [x] Protected route middleware
- [x] Error handling and validation
- [x] Database persistence

### **Frontend Implementation** ✅
- [x] Authentication components (Login/Register)
- [x] API configuration with interceptors
- [x] Protected app structure
- [x] Token management
- [x] User interface integration
- [x] Error handling and loading states

### **Integration & Testing** ✅
- [x] Backend API testing
- [x] Frontend authentication flow
- [x] Protected route testing
- [x] Error scenario testing
- [x] User experience validation

## 🎉 **Assignment 9 Complete!**

Semua persyaratan Assignment 9 telah berhasil diimplementasikan dengan:

1. ✅ **Fitur Sign Up & Sign In** - Implementasi lengkap dengan validasi dan keamanan
2. ✅ **Integrasi Frontend** - UI yang user-friendly dengan protected routes
3. ✅ **Dokumentasi Flow** - Penjelasan teknis yang komprehensif dengan diagram

Aplikasi Task Manager sekarang memiliki sistem authentication yang aman, user-friendly, dan production-ready! 🚀 