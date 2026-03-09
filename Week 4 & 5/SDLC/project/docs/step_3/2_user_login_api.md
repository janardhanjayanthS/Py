# User Login API Documentation

## 📋 Overview

The User Login API authenticates users and provides JWT tokens for accessing protected endpoints. This endpoint validates user credentials, generates a JWT token with 30-minute expiration, and returns the token for subsequent API calls.

**Endpoint:** `POST /user/login`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Not Required

---

## 🔐 API Endpoints

### POST /user/login

Authenticates a user with email and password, returning a JWT access token.

**URL:** `POST /user/login`  
**Content-Type:** `application/json`  
**Authentication:** None

#### Request Body

| Parameter | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| email     | string | Yes      | User's email address           |
| password  | string | Yes      | User's password                |

#### Request Examples

**Standard user login:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

**Manager login:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.smith@example.com",
    "password": "ManagerPass456@"
  }'
```

**Admin login:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "AdminPass789#"
  }'
```

#### Response

**Success Response (200 OK)**
```json
{
  "access_tokem": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature",
  "token_type": "Bearer"
}
```

**Error Response (401 Unauthorized) - Invalid credentials:**
```json
{
  "detail": "Incorrect email or password"
}
```

**Error Response (401 Unauthorized) - User not found:**
```json
{
  "detail": "Incorrect email or password"
}
```

#### Response Fields

| Field        | Type   | Description                                    |
|--------------|--------|------------------------------------------------|
| access_tokem | string | JWT access token (note: typo in original field name) |
| token_type   | string | Token type ("Bearer")                          |

---

## 🚀 Usage Examples

### 1. Successful Staff Login

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.johnson@example.com",
    "password": "StaffPass123!"
  }'
```

**Response:**
```json
{
  "access_tokem": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZS5qb2huc29uQGV4YW1wbGUuY29tIiwicm9sZSI6InN0YWZmIiwiZXhwIjoxNzA1MjQyNDAwfQ.signature",
  "token_type": "Bearer"
}
```

### 2. Manager Login

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob.wilson@example.com",
    "password": "ManagerPass456@"
  }'
```

**Response:**
```json
{
  "access_tokem": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Iud2lsc29uQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature",
  "token_type": "Bearer"
}
```

### 3. Admin Login

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "AdminPass789#"
  }'
```

**Response:**
```json
{
  "access_tokem": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature",
  "token_type": "Bearer"
}
```

### 4. Invalid Email Login

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@example.com",
    "password": "SomePass123!"
  }'
```

**Response:**
```json
{
  "detail": "Incorrect email or password"
}
```

### 5. Invalid Password Login

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.johnson@example.com",
    "password": "WrongPassword123!"
  }'
```

**Response:**
```json
{
  "detail": "Incorrect email or password"
}
```

---

## 🔧 Implementation Details

### Authentication Process

1. **Input Validation**: Pydantic schema validates email and password fields
2. **User Lookup**: Database query finds user by email
3. **Password Verification**: bcrypt compares provided password with stored hash
4. **Token Generation**: JWT token is created with user email and role
5. **Token Expiration**: Default 30-minute expiration is set
6. **Response**: Token and token type are returned to client

### JWT Token Structure

The JWT token contains the following claims:
- **sub (subject)**: User's email address
- **role**: User's role (staff, manager, admin)
- **exp (expiration)**: Token expiration timestamp
- **iat (issued at)**: Token creation timestamp (automatically added)

### Security Features

1. **Password Verification**: Uses bcrypt for secure password comparison
2. **JWT Signing**: Tokens are signed with HS256 algorithm using secret key
3. **Token Expiration**: 30-minute expiration prevents token abuse
4. **Universal Error**: Same error message for both invalid email and password (prevents user enumeration)
5. **Rate Limiting**: Can be implemented at the FastAPI level

### Token Usage

After successful login, use the token in the Authorization header:
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Test successful login
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'

# Test invalid email
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@example.com",
    "password": "TestPass123!"
  }'

# Test invalid password
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "WrongPassword123!"
  }'

# Store token for subsequent requests
TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "TestPass123!"}' \
  | jq -r '.access_tokem')

# Use token to access protected endpoint
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer $TOKEN"
```

### Python Testing Example

```python
import requests
import json
import time

base_url = "http://127.0.0.1:5001"

def test_user_login():
    # Successful login
    login_data = {
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{base_url}/user/login", json=login_data)
    print("Login response:", json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        token = response.json()["access_tokem"]
        
        # Test token usage
        headers = {"Authorization": f"Bearer {token}"}
        users_response = requests.get(f"{base_url}/user/all", headers=headers)
        print("Protected endpoint response:", json.dumps(users_response.json(), indent=2))
    
    # Test invalid credentials
    invalid_data = {
        "email": "test@example.com",
        "password": "WrongPassword123!"
    }
    response = requests.post(f"{base_url}/user/login", json=invalid_data)
    print("Invalid credentials response:", json.dumps(response.json(), indent=2))
    
    # Test nonexistent user
    nonexistent_data = {
        "email": "nonexistent@example.com",
        "password": "TestPass123!"
    }
    response = requests.post(f"{base_url}/user/login", json=nonexistent_data)
    print("Nonexistent user response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_user_login()
```

---

## 🐛 Error Handling

### Common Error Scenarios

1. **Invalid Email or Password**
   ```json
   {
     "detail": "Incorrect email or password"
   }
   ```

2. **Missing Required Fields**
   ```json
   {
     "detail": [
       {
         "type": "missing",
         "loc": ["body", "email"],
         "msg": "Field required"
       }
     ]
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

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Login successful                 |
| 401         | Invalid credentials              |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **POST /user/register**: Create new user account
- **GET /user/all**: Get all users (requires authentication)
- **PATCH /user/update**: Update user profile (requires authentication)
- **DELETE /user/delete**: Delete user account (admin only)

---

## 📝 Notes

- The response field name has a typo: "access_tokem" instead of "access_token"
- Token expiration is set to 30 minutes by default
- The same error message is returned for both invalid email and password to prevent user enumeration
- Tokens should be stored securely on the client side (e.g., in memory or secure storage)
- Expired tokens will be rejected by protected endpoints
- The JWT secret key should be kept secure and environment-specific
- Password verification uses bcrypt with constant-time comparison to prevent timing attacks
