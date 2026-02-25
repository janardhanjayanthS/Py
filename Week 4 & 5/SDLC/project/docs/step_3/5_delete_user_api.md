# Delete User API Documentation

## 📋 Overview

The Delete User API allows authenticated admin users to delete user accounts from the system. This endpoint validates the admin's authentication token, checks admin permissions, and permanently removes the specified user from the database.

**Endpoint:** `DELETE /user/delete`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Admin only)

---

## 🔐 API Endpoints

### DELETE /user/delete

Permanently deletes a user account from the system.

**URL:** `DELETE /user/delete?user_id={user_id}`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Query Parameters

| Parameter | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| user_id   | integer | Yes      | ID of the user to delete       |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Delete user with ID 1:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=1" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

**Delete user with ID 5:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=5" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "user email": "admin@example.com",
    "deleted account": {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "staff"
    }
  }
}
```

**Error Response (401 Unauthorized) - Non-admin user:**
```json
{
  "detail": "Unauthorized to perform action, you are a manager"
}
```

**Error Response (401 Unauthorized) - Invalid token:**
```json
{
  "detail": "Could not validate credentials"
}
```

**Error Response (200 OK) - User not found:**
```json
{
  "status": "error",
  "message": {
    "response": "Unable to find user with id: 999"
  }
}
```

#### Response Fields

| Field            | Type     | Description                                    |
|------------------|----------|------------------------------------------------|
| status           | string   | Response status ("success" or "error")         |
| message          | object   | Contains admin email and deleted user data     |
| user email       | string   | Email of the admin performing deletion         |
| deleted account  | object   | Complete user object that was deleted          |
| id               | integer  | Unique user identifier                         |
| name             | string   | User's full name                               |
| email            | string   | User's email address                           |
| password         | string   | Hashed password (bcrypt)                       |
| role             | string   | User's role                                    |

---

## 🚀 Usage Examples

### 1. Admin Deletes Staff User

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "admin@example.com",
    "deleted account": {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "staff"
    }
  }
}
```

### 2. Admin Deletes Manager User

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=2" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "admin@example.com",
    "deleted account": {
      "id": 2,
      "name": "Bob Wilson",
      "email": "bob.wilson@example.com",
      "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "manager"
    }
  }
}
```

### 3. Manager Attempts to Delete User (Unauthorized)

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=3" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a manager"
}
```

### 4. Admin Deletes Non-existent User

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=999" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "error",
  "message": {
    "response": "Unable to find user with id: 999"
  }
}
```

### 5. Admin Deletes User with Invalid ID Type

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=invalid" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

**Response:**
```json
{
  "detail": "id should be type int but got type: str"
}
```

---

## 🔧 Implementation Details

### Deletion Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked (must be admin)
3. **User ID Validation**: Query parameter is validated as integer
4. **User Lookup**: Target user is found in database by ID
5. **Deletion Execution**: User record is permanently removed
6. **Database Commit**: Transaction is committed to persist deletion
7. **Response**: Deleted user object and confirmation returned

### Security Considerations

1. **Admin Only**: Only users with admin role can delete users
2. **Permanent Deletion**: This operation cannot be undone
3. **Audit Trail**: Admin email is included in response for tracking
4. **Data Integrity**: Related records may be affected (cascade deletes)
5. **Input Validation**: User ID is validated to prevent injection

### Cascade Effects

- **Products**: User-owned products may be affected depending on foreign key constraints
- **Categories**: User-created categories may be affected
- **Sessions**: Active sessions for deleted user are invalidated

### Error Handling

- **User Not Found**: Returns error status with descriptive message
- **Invalid ID Type**: Returns validation error for non-integer IDs
- **Unauthorized Access**: Clear error message for non-admin users
- **Database Errors**: Proper error handling for database failures

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Get admin token
ADMIN_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "AdminPass789#"}' \
  | jq -r '.access_tokem')

# Get manager token (for testing unauthorized access)
MANAGER_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "manager@example.com", "password": "ManagerPass456@"}' \
  | jq -r '.access_tokem')

# Test successful deletion
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=1" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test deletion of non-existent user
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=999" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test with invalid ID type
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=invalid" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test unauthorized access (manager)
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=2" \
  -H "Authorization: Bearer $MANAGER_TOKEN"

# Test without authentication
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=3"

# Test with invalid token
curl -X DELETE "http://127.0.0.1:5001/user/delete?user_id=4" \
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

def test_delete_user():
    # Get admin token
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("=== Testing Admin Deletions ===")
    
    # Test successful deletion
    response = requests.delete(f"{base_url}/user/delete?user_id=1", headers=admin_headers)
    print(f"Successful Deletion: {json.dumps(response.json(), indent=2)}")
    
    # Test deletion of non-existent user
    response = requests.delete(f"{base_url}/user/delete?user_id=999", headers=admin_headers)
    print(f"Non-existent User: {json.dumps(response.json(), indent=2)}")
    
    # Test invalid ID type
    response = requests.delete(f"{base_url}/user/delete?user_id=invalid", headers=admin_headers)
    print(f"Invalid ID Type: {json.dumps(response.json(), indent=2)}")
    
    # Test unauthorized access
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    
    print("\n=== Testing Unauthorized Access ===")
    
    response = requests.delete(f"{base_url}/user/delete?user_id=2", headers=manager_headers)
    print(f"Manager Attempt: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    print("\n=== Testing No Authentication ===")
    
    response = requests.delete(f"{base_url}/user/delete?user_id=3")
    print(f"No Auth: {json.dumps(response.json(), indent=2)}")
    
    # Test with invalid token
    print("\n=== Testing Invalid Token ===")
    
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.delete(f"{base_url}/user/delete?user_id=4", headers=invalid_headers)
    print(f"Invalid Token: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_delete_user()
```

---

## 🐛 Error Handling

### Common Error Scenarios

1. **Unauthorized Role**
   ```json
   {
     "detail": "Unauthorized to perform action, you are a manager"
   }
   ```

2. **Missing Authentication Token**
   ```json
   {
     "detail": "Authorization header missing"
   }
   ```

3. **Invalid Token**
   ```json
   {
     "detail": "Could not validate credentials"
   }
   ```

4. **Invalid User ID Type**
   ```json
   {
     "detail": "id should be type int but got type: str"
   }
   ```

5. **User Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "Unable to find user with id: 999"
     }
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | User deleted successfully        |
| 200         | User not found (error status)    |
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid ID)    |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **POST /user/register**: Create new user account
- **POST /user/login**: User authentication and token generation
- **GET /user/all**: Get all users (requires authentication)
- **PATCH /user/update**: Update user profile (manager/admin only)

---

## 📝 Notes

- This operation is permanent and cannot be undone
- Only admin users can delete other users (including other admins)
- The admin cannot delete themselves through this endpoint
- Deleted users lose all access to the system immediately
- Related data (products, categories) may be affected by cascade deletes
- The response includes the complete deleted user object for audit purposes
- Consider implementing soft deletes in production for better data recovery
- Admin email is included in response for audit trail purposes
- User ID validation prevents SQL injection attacks
- The endpoint returns success even when user doesn't exist (with error status)
