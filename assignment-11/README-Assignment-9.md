# Assignment 9 - Authentication Implementation

## 📋 Overview

Assignment 9 berfokus pada implementasi fitur otentikasi (Sign Up & Sign In) yang dapat digunakan pada aplikasi Task Manager, serta menjelaskan langkah teknis implementasinya baik di backend maupun frontend.

## ✅ **Requirements Checklist**

### **1. Tambahkan Fitur Sign Up & Sign In** ✅
- [x] Implementasi login dan register menggunakan email & password
- [x] Data disimpan dan tervalidasi di backend
- [x] JWT token authentication
- [x] Password hashing dengan bcrypt
- [x] User registration dengan validasi
- [x] User login dengan token generation

### **2. Integrasikan dengan Frontend** ✅
- [x] Tampilan form login & register
- [x] API otentikasi untuk mengatur alur akses aplikasi
- [x] Protected routes di frontend
- [x] Token management di localStorage
- [x] Auto-logout pada token expiration
- [x] User info display di header

### **3. Jelaskan Flow Implementasi** ✅
- [x] Diagram alur authentication
- [x] Langkah-langkah implementasi
- [x] Catatan teknis backend dan frontend

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │    │   (FastAPI)     │    │   (JSON)        │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Login Form    │◄──►│ • /auth/login   │◄──►│ • users.json    │
│ • Register Form │    │ • /auth/register│    │ • data.json     │
│ • Protected UI  │    │ • /auth/me      │    │                 │
│ • Token Storage │    │ • JWT Auth      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔐 **Authentication Flow**

### **1. User Registration Flow**
```
1. User fills registration form
   ├── Username (required)
   ├── Email (required, validated)
   └── Password (required, min 6 chars)

2. Frontend sends POST /api/auth/register
   ├── Validates form data
   └── Sends to backend

3. Backend processes registration
   ├── Validates input data
   ├── Checks for existing username/email
   ├── Hashes password with bcrypt
   ├── Creates user in database
   └── Returns user data (without password)

4. Frontend handles response
   ├── Shows success message
   ├── Switches to login form
   └── User can now login
```

### **2. User Login Flow**
```
1. User fills login form
   ├── Username
   └── Password

2. Frontend sends POST /api/auth/login
   ├── Validates form data
   └── Sends to backend

3. Backend processes login
   ├── Validates credentials
   ├── Verifies password hash
   ├── Generates JWT token
   └── Returns token + user info

4. Frontend handles response
   ├── Stores token in localStorage
   ├── Redirects to main app
   └── Sets authenticated state
```

### **3. Protected Route Flow**
```
1. User accesses protected route
   ├── App checks localStorage for token
   └── If no token → redirect to login

2. API requests include token
   ├── Axios interceptor adds Authorization header
   └── Bearer token sent with requests

3. Backend validates token
   ├── Verifies JWT signature
   ├── Checks token expiration
   ├── Extracts user info
   └── Allows/denies access

4. Frontend handles responses
   ├── 401 errors → auto logout
   ├── Success → display protected content
   └── User info displayed in header
```

## 🛠️ **Technical Implementation**

### **Backend Implementation**

#### **1. Authentication Service (`auth_service.py`)**
```python
class AuthService:
    def __init__(self):
        self.user_model = UserModel()
    
    def register_user(self, user_data: UserCreate) -> dict:
        # Validates username/email uniqueness
        # Hashes password with bcrypt
        # Creates user in database
        # Returns user data
    
    def login_user(self, user_data: UserLogin) -> dict:
        # Validates credentials
        # Verifies password hash
        # Generates JWT token
        # Returns token + user info
    
    def get_current_user(self, credentials) -> dict:
        # Validates JWT token
        # Returns current user data
```

#### **2. User Model (`user_model.py`)**
```python
class UserModel:
    def __init__(self):
        self.users_file = "app/db/users.json"
    
    def create_user(self, username, email, hashed_password):
        # Creates new user with UUID
        # Saves to JSON database
    
    def verify_password(self, plain_password, hashed_password):
        # Uses bcrypt to verify password
    
    def get_password_hash(self, password):
        # Uses bcrypt to hash password
```

#### **3. Authentication Routes (`auth_routes.py`)**
```python
@router.post("/register")
async def register(user_data: UserCreate):
    # Handles user registration

@router.post("/login")
async def login(user_data: UserLogin):
    # Handles user login

@router.get("/me")
async def get_current_user_info(current_user):
    # Returns current user info
```

### **Frontend Implementation**

#### **1. API Configuration (`api.ts`)**
```typescript
// Authentication interceptors
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

#### **2. Authentication Components**
```typescript
// Login Component
export function Login({ onSwitchToRegister, onLoginSuccess }) {
  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access_token);
      onLoginSuccess();
    }
  });
}

// Register Component
export function Register({ onSwitchToLogin, onRegisterSuccess }) {
  const registerMutation = useMutation({
    mutationFn: authApi.register,
    onSuccess: () => {
      onRegisterSuccess();
    }
  });
}
```

#### **3. Protected App Structure**
```typescript
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  if (!isAuthenticated) {
    return <AuthContainer onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div>
      <Header onLogout={handleLogout} />
      <TodoApp />
    </div>
  );
}
```

## 📁 **File Structure**

```
assignment-9/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   │   ├── auth_routes.py      # Authentication endpoints
│   │   │   ├── list_routes.py      # Protected list endpoints
│   │   │   └── task_routes.py      # Protected task endpoints
│   │   ├── models/
│   │   │   └── user_model.py       # User data model
│   │   ├── services/
│   │   │   └── auth_service.py     # Authentication logic
│   │   └── schemas/
│   │       └── auth_schema.py      # Auth request/response schemas
│   └── app/db/
│       └── users.json              # User database
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Login.tsx           # Login form component
│       │   ├── Register.tsx        # Register form component
│       │   ├── AuthContainer.tsx   # Auth state management
│       │   └── Header.tsx          # Header with user info
│       ├── api.ts                  # API configuration with auth
│       └── App.tsx                 # Main app with auth flow
└── README-Assignment-9.md          # This documentation
```

## 🔧 **Setup Instructions**

### **Backend Setup**
```bash
cd assignment-9/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### **Frontend Setup**
```bash
cd assignment-9/frontend
npm install
npm run dev
```

### **Testing Authentication**
1. **Register a new user:**
   - Go to http://localhost:5173
   - Click "Don't have an account? Sign up"
   - Fill in username, email, and password
   - Submit registration

2. **Login with existing user:**
   - Use the credentials from registration
   - Or use default admin user:
     - Username: `admin`
     - Password: `admin123`

3. **Test protected features:**
   - Create lists and tasks
   - Verify user info in header
   - Test logout functionality

## 🚀 **Key Features Implemented**

### **Security Features**
- ✅ JWT token-based authentication
- ✅ Password hashing with bcrypt
- ✅ Protected API endpoints
- ✅ Auto-logout on token expiration
- ✅ Input validation and sanitization
- ✅ Error handling for authentication failures

### **User Experience**
- ✅ Clean login/register forms
- ✅ Form validation with error messages
- ✅ Loading states during authentication
- ✅ Smooth transitions between auth states
- ✅ User info display in header
- ✅ Logout functionality

### **Technical Features**
- ✅ React Query for state management
- ✅ Axios interceptors for token handling
- ✅ TypeScript for type safety
- ✅ Responsive design with Tailwind CSS
- ✅ Error boundary handling
- ✅ Persistent authentication state

## 📊 **API Endpoints**

### **Authentication Endpoints**
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/auth/me` | Get current user info | Yes |

### **Protected Endpoints**
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/lists` | Get all lists | Yes |
| POST | `/api/lists` | Create new list | Yes |
| GET | `/api/lists/{id}/tasks` | Get tasks in list | Yes |
| POST | `/api/lists/{id}/tasks` | Create new task | Yes |

## 🎯 **Assignment 9 Complete!**

Semua persyaratan Assignment 9 telah berhasil diimplementasikan:

1. ✅ **Fitur Sign Up & Sign In** - Implementasi lengkap dengan validasi
2. ✅ **Integrasi Frontend** - UI yang user-friendly dengan protected routes
3. ✅ **Dokumentasi Flow** - Penjelasan teknis yang komprehensif

Aplikasi Task Manager sekarang memiliki sistem authentication yang aman dan user-friendly! 🎉 