# User Registration API Documentation

## 📋 Overview

The User Registration API allows new users to create an account in the Inventory Management System. This endpoint validates user input, ensures password strength, checks for existing users, and creates a new user record with appropriate role assignment.

**Endpoint:** `POST /user/register`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Not Required

---

## 🔐 API Endpoints

### POST /user/register

Creates a new user account with validated credentials and assigns a role.

**URL:** `POST /user/register`  
**Content-Type:** `application/json`  
**Authentication:** None

#### Request Body

| Parameter | Type   | Required | Description                    | Constraints                      |
|-----------|--------|----------|--------------------------------|-----------------------------------|
| name      | string | Yes      | User's full name               | 5-100 characters, unique         |
| email     | string | Yes      | User's email address           | Valid email format, unique       |
| password  | string | Yes      | User's password                | Strong password (8+ chars, mixed case, numbers, special chars) |
| role      | string | Yes      | User's role in system          | "staff", "manager", or "admin"   |

#### Request Examples

**Basic user registration:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123!",
    "role": "staff"
  }'
```

**Manager registration:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "password": "ManagerPass456@",
    "role": "manager"
  }'
```

**Admin registration:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "AdminPass789#",
    "role": "admin"
  }'
```

#### Response

**Success Response (201 Created)**
```json
{
  "status": "success",
  "message": {
    "registered user": {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "staff"
    }
  }
}
```

**Error Response (400 Bad Request) - Email already exists:**
```json
{
  "detail": "User with email john.doe@example.com already exists"
}
```

**Error Response (400 Bad Request) - Weak password:**
```json
{
  "detail": "Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: weak"
}
```

**Error Response (422 Unprocessable Entity) - Invalid email:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "input": "invalid-email"
    }
  ]
}
```

#### Response Fields

| Field        | Type     | Description                                    |
|--------------|----------|------------------------------------------------|
| status       | string   | Response status ("success")                     |
| message      | object   | Contains registered user data                  |
| id           | integer  | Unique user identifier                         |
| name         | string   | User's full name                               |
| email        | string   | User's email address                           |
| password     | string   | Hashed password (bcrypt)                       |
| role         | string   | User's assigned role                           |

---

## 🚀 Usage Examples

### 1. Successful Staff Registration

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "password": "StaffPass123!",
    "role": "staff"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "registered user": {
      "id": 2,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "staff"
    }
  }
}
```

### 2. Manager Registration

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Wilson",
    "email": "bob.wilson@example.com",
    "password": "ManagerPass456@",
    "role": "manager"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "registered user": {
      "id": 3,
      "name": "Bob Wilson",
      "email": "bob.wilson@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "manager"
    }
  }
}
```

### 3. Duplicate Email Registration

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Another User",
    "email": "alice.johnson@example.com",
    "password": "AnotherPass123!",
    "role": "staff"
  }'
```

**Response:**
```json
{
  "detail": "User with email alice.johnson@example.com already exists"
}
```

### 4. Weak Password Registration

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weak User",
    "email": "weak@example.com",
    "password": "123",
    "role": "staff"
  }'
```

**Response:**
```json
{
  "detail": "Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: 123"
}
```

---

## 🔧 Implementation Details

### Registration Process

1. **Input Validation**: Pydantic schemas validate all input fields
2. **Password Strength Check**: Custom validator ensures strong passwords
3. **Email Uniqueness**: Database query checks if email already exists
4. **Password Hashing**: Password is hashed using bcrypt before storage
5. **User Creation**: New user record is created with all provided data
6. **Database Commit**: Transaction is committed to persist the user

### Password Requirements

The password must meet the following criteria:
- **Minimum length**: 8 characters
- **Lowercase letter**: At least one (a-z)
- **Uppercase letter**: At least one (A-Z)
- **Digit**: At least one (0-9)
- **Special character**: At least one (!@#$%^&*(),.?":{}|<>)

### Role System

Three roles are available with different permission levels:
- **staff**: Read-only access (GET operations only)
- **manager**: Read and write access (GET, POST, PUT, PATCH)
- **admin**: Full access (GET, POST, PUT, PATCH, DELETE)

### Security Features

1. **Password Hashing**: Uses bcrypt with automatic salt generation
2. **Input Sanitization**: All inputs are validated and sanitized
3. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
4. **Email Validation**: Pydantic EmailStr validates email format
5. **Rate Limiting**: Can be implemented at the FastAPI level

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Test successful registration
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPass123!",
    "role": "staff"
  }'

# Test duplicate email
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User 2",
    "email": "test@example.com",
    "password": "TestPass456!",
    "role": "staff"
  }'

# Test weak password
curl -X POST "http://127.0.0.1:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weak User",
    "email": "weak@example.com",
    "password": "weak",
    "role": "staff"
  }'
```

### Python Testing Example

```python
import requests
import json

base_url = "http://127.0.0.1:5001"

def test_user_registration():
    # Successful registration
    user_data = {
        "name": "Python Test User",
        "email": "python@example.com",
        "password": "PythonTest123!",
        "role": "staff"
    }
    
    response = requests.post(f"{base_url}/user/register", json=user_data)
    print("Registration response:", json.dumps(response.json(), indent=2))
    
    # Test duplicate email
    response = requests.post(f"{base_url}/user/register", json=user_data)
    print("Duplicate email response:", json.dumps(response.json(), indent=2))
    
    # Test weak password
    weak_data = {
        "name": "Weak User",
        "email": "weak@example.com",
        "password": "weak",
        "role": "staff"
    }
    response = requests.post(f"{base_url}/user/register", json=weak_data)
    print("Weak password response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_user_registration()
```

---

## 🐛 Error Handling

### Common Error Scenarios

1. **Email Already Exists**
   ```json
   {
     "detail": "User with email user@example.com already exists"
   }
   ```

2. **Weak Password**
   ```json
   {
     "detail": "Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: weakpass"
   }
   ```

3. **Invalid Email Format**
   ```json
   {
     "detail": [
       {
         "type": "value_error",
         "loc": ["body", "email"],
         "msg": "value is not a valid email address",
         "input": "invalid-email"
       }
     ]
   }
   ```

4. **Invalid Role**
   ```json
   {
     "detail": [
       {
         "type": "enum",
         "loc": ["body", "role"],
         "msg": "Input should be 'staff', 'manager', or 'admin'",
         "input": "invalid_role"
       }
     ]
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 201         | User created successfully        |
| 400         | Bad request (duplicate email, weak password) |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **POST /user/login**: User authentication and token generation
- **GET /user/all**: Get all users (requires authentication)
- **PATCH /user/update**: Update user profile (requires authentication)
- **DELETE /user/delete**: Delete user account (admin only)

---

## 📝 Notes

- Passwords are never stored in plain text - always hashed with bcrypt
- Email addresses are case-insensitive for uniqueness checks
- User names must be unique across the system
- Role assignment is final during registration - changes require admin intervention
- The endpoint returns the full user object including the hashed password for confirmation
- All validation errors provide detailed feedback to help users correct their input
- The system automatically generates a unique ID for each new user
