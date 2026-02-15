# Get All Users API Documentation

## 📋 Overview

The Get All Users API retrieves a list of all users in the system. This endpoint requires authentication and is accessible to users with staff, manager, or admin roles. It returns user information including names, emails, and roles.

**Endpoint:** `GET /user/all`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token)

---

## 🔐 API Endpoints

### GET /user/all

Retrieves all users from the database with their basic information.

**URL:** `GET /user/all`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Get all users as staff:**
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Get all users as manager:**
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer MANAGER_JWT_TOKEN_HERE"
```

**Get all users as admin:**
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "user email": "alice.johnson@example.com",
    "users": [
      {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "staff"
      },
      {
        "id": 2,
        "name": "Bob Wilson",
        "email": "bob.wilson@example.com",
        "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "manager"
      },
      {
        "id": 3,
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "$2b$12$Mz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "admin"
      }
    ]
  }
}
```

**Empty Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "user email": "alice.johnson@example.com",
    "users": []
  }
}
```

**Error Response (401 Unauthorized)**
```json
{
  "detail": "Unauthorized to perform action, you are a unauthorized_role"
}
```

**Error Response (401 Unauthorized) - Invalid token:**
```json
{
  "detail": "Could not validate credentials"
}
```

#### Response Fields

| Field        | Type     | Description                                    |
|--------------|----------|------------------------------------------------|
| status       | string   | Response status ("success")                     |
| message      | object   | Contains current user email and users list      |
| user email   | string   | Email of the authenticated user making request |
| users        | array    | Array of user objects                          |
| id           | integer  | Unique user identifier                         |
| name         | string   | User's full name                               |
| email        | string   | User's email address                           |
| password     | string   | Hashed password (bcrypt)                       |
| role         | string   | User's role (staff, manager, admin)            |

---

## 🚀 Usage Examples

### 1. Staff User Getting All Users

**Request:**
```bash
# First login as staff user
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.johnson@example.com",
    "password": "StaffPass123!"
  }'

# Use the token to get all users
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZS5qb2huc29uQGV4YW1wbGUuY29tIiwicm9sZSI6InN0YWZmIiwiZXhwIjoxNzA1MjQyNDAwfQ.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "alice.johnson@example.com",
    "users": [
      {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "staff"
      },
      {
        "id": 2,
        "name": "Bob Wilson",
        "email": "bob.wilson@example.com",
        "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "manager"
      }
    ]
  }
}
```

### 2. Manager User Getting All Users

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Iud2lsc29uQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "bob.wilson@example.com",
    "users": [
      {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "staff"
      },
      {
        "id": 2,
        "name": "Bob Wilson",
        "email": "bob.wilson@example.com",
        "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "manager"
      },
      {
        "id": 3,
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "$2b$12$Mz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "admin"
      }
    ]
  }
}
```

### 3. Admin User Getting All Users

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "admin@example.com",
    "users": [
      {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "staff"
      },
      {
        "id": 2,
        "name": "Bob Wilson",
        "email": "bob.wilson@example.com",
        "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "manager"
      },
      {
        "id": 3,
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "$2b$12$Mz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
        "role": "admin"
      }
    ]
  }
}
```

### 4. Empty Users List

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "alice.johnson@example.com",
    "users": []
  }
}
```

---

## 🔧 Implementation Details

### Authorization Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked against allowed roles (staff, manager, admin)
3. **User Identification**: Current user's email is extracted from token
4. **Database Query**: All users are retrieved from the database
5. **Response Construction**: User list is formatted with current user context

### Role-Based Access Control

The following roles can access this endpoint:
- **staff**: Read-only access to view all users
- **manager**: Read-only access to view all users
- **admin**: Read-only access to view all users

### Security Considerations

1. **Password Exposure**: Hashed passwords are included in response (consider removing in production)
2. **User Enumeration**: All users are visible to authenticated users
3. **Data Privacy**: Consider filtering sensitive information in production
4. **Rate Limiting**: Can be implemented to prevent abuse

### Response Structure

- **status**: Always "success" for successful requests
- **message**: Object containing:
  - **user email**: Email of the authenticated user
  - **users**: Array of all user objects in the system

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Get authentication token for different roles
STAFF_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "staff@example.com", "password": "StaffPass123!"}' \
  | jq -r '.access_tokem')

MANAGER_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "manager@example.com", "password": "ManagerPass456@"}' \
  | jq -r '.access_tokem')

ADMIN_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "AdminPass789#"}' \
  | jq -r '.access_tokem')

# Test with staff token
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test with manager token
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer $MANAGER_TOKEN"

# Test with admin token
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test without token (should fail)
curl -X GET "http://127.0.0.1:5001/user/all"

# Test with invalid token (should fail)
curl -X GET "http://127.0.0.1:5001/user/all" \
  -H "Authorization: Bearer invalid_token"
```

### Python Testing Example

```python
import requests
import json

base_url = "http://127.0.0.1:5001"

def get_auth_token(email, password):
    """Helper function to get authentication token"""
    response = requests.post(f"{base_url}/user/login", json={
        "email": email,
        "password": password
    })
    return response.json()["access_tokem"]

def test_get_all_users():
    # Test with different user roles
    roles = [
        ("staff@example.com", "StaffPass123!"),
        ("manager@example.com", "ManagerPass456@"),
        ("admin@example.com", "AdminPass789#")
    ]
    
    for email, password in roles:
        print(f"\n=== Testing as {email} ===")
        
        # Get token
        token = get_auth_token(email, password)
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get all users
        response = requests.get(f"{base_url}/user/all", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    print("\n=== Testing without authentication ===")
    response = requests.get(f"{base_url}/user/all")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test with invalid token
    print("\n=== Testing with invalid token ===")
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{base_url}/user/all", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_get_all_users()
```

---

## 🐛 Error Handling

### Common Error Scenarios

1. **Missing Authentication Token**
   ```json
   {
     "detail": "Authorization header missing"
   }
   ```

2. **Invalid Token**
   ```json
   {
     "detail": "Could not validate credentials"
   }
   ```

3. **Expired Token**
   ```json
   {
     "detail": "Could not validate credentials"
   }
   ```

4. **Unauthorized Role**
   ```json
   {
     "detail": "Unauthorized to perform action, you are a unauthorized_role"
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Users retrieved successfully     |
| 401         | Unauthorized / Invalid token     |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **POST /user/register**: Create new user account
- **POST /user/login**: User authentication and token generation
- **PATCH /user/update**: Update user profile (manager/admin only)
- **DELETE /user/delete**: Delete user account (admin only)

---

## 📝 Notes

- The endpoint returns hashed passwords for all users - consider removing this in production
- All authenticated users (staff, manager, admin) can view all users in the system
- The response includes the current user's email for context
- Users are returned in the order they appear in the database
- Empty user lists return an empty array rather than null
- Consider implementing pagination for large user lists in production
- The endpoint does not support filtering or sorting - all users are returned
