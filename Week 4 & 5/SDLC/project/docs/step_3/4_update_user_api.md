# Update User API Documentation

## 📋 Overview

The Update User API allows authenticated users with manager or admin roles to update their own profile information including name and password. This endpoint validates the authentication token, checks user permissions, and updates user data in the database.

**Endpoint:** `PATCH /user/update`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token)

---

## 🔐 API Endpoints

### PATCH /user/update

Updates the authenticated user's profile information (name and/or password).

**URL:** `PATCH /user/update`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Body

| Parameter     | Type   | Required | Description                    | Constraints                      |
|---------------|--------|----------|--------------------------------|-----------------------------------|
| new_name      | string | No       | New user name                  | 5-100 characters, unique         |
| new_password  | string | No       | New user password              | Strong password (8+ chars, mixed case, numbers, special chars) |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Update user name only:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "new_name": "Alice Johnson Smith"
  }'
```

**Update password only:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "new_password": "NewSecurePass456@"
  }'
```

**Update both name and password:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "new_name": "Alice Johnson Smith",
    "new_password": "NewSecurePass456@"
  }'
```

**Update with no changes (valid request):**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{}'
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "update status": "updated user's name to Alice Johnson Smith. password updated",
    "updated user detail": {
      "id": 2,
      "name": "Alice Johnson Smith",
      "email": "alice.johnson@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "manager"
    }
  }
}
```

**Success Response - No Changes:**
```json
{
  "status": "success",
  "message": {
    "update status": "existing name and new name are same. same password",
    "updated user detail": {
      "id": 2,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "manager"
    }
  }
}
```

**Error Response (401 Unauthorized)**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

**Error Response (401 Unauthorized) - Invalid token:**
```json
{
  "detail": "Could not validate credentials"
}
```

**Error Response (400 Bad Request) - Weak password:**
```json
{
  "detail": "Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: weak"
}
```

#### Response Fields

| Field                | Type     | Description                                    |
|----------------------|----------|------------------------------------------------|
| status               | string   | Response status ("success")                     |
| message              | object   | Contains update status and user data           |
| update status        | string   | Description of what was updated                |
| updated user detail  | object   | Complete updated user object                   |
| id                   | integer  | Unique user identifier                         |
| name                 | string   | User's updated name                            |
| email                | string   | User's email address                           |
| password             | string   | Updated hashed password (bcrypt)               |
| role                 | string   | User's role                                    |

---

## 🚀 Usage Examples

### 1. Manager Updates Name Only

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Iud2lsc29uQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "new_name": "Robert Wilson Jr."
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "update status": "updated user's name to Robert Wilson Jr. ",
    "updated user detail": {
      "id": 2,
      "name": "Robert Wilson Jr.",
      "email": "bob.wilson@example.com",
      "password": "$2b$12$Kz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "manager"
    }
  }
}
```

### 2. Admin Updates Password Only

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "new_password": "AdminNewPass789#"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "update status": "existing name and new name are same. password updated",
    "updated user detail": {
      "id": 3,
      "name": "Admin User",
      "email": "admin@example.com",
      "password": "$2b$12$Mz9XjQ8yZ7vN6mK5lJ4HpOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "admin"
    }
  }
}
```

### 3. Manager Updates Both Name and Password

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Iud2lsc29uQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "new_name": "Robert Wilson Senior",
    "new_password": "ManagerNewPass456@"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "update status": "updated user's name to Robert Wilson Senior. password updated",
    "updated user detail": {
      "id": 2,
      "name": "Robert Wilson Senior",
      "email": "bob.wilson@example.com",
      "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
      "role": "manager"
    }
  }
}
```

### 4. Staff User Attempts Update (Unauthorized)

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZS5qb2huc29uQGV4YW1wbGUuY29tIiwicm9sZSI6InN0YWZmIiwiZXhwIjoxNzA1MjQyNDAwfQ.signature" \
  -d '{
    "new_name": "Alice Updated"
  }'
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

### 5. Update with Weak Password

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "new_password": "weak"
  }'
```

**Response:**
```json
{
  "detail": "Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: weak"
}
```

---

## 🔧 Implementation Details

### Update Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked (must be manager or admin)
3. **User Retrieval**: Current user object is fetched from database
4. **Input Validation**: Pydantic schema validates new name and/or password
5. **Password Strength Check**: New password must meet security requirements
6. **Field Updates**: Only provided fields are updated (partial update)
7. **Database Commit**: Changes are saved to database
8. **Response**: Updated user object and status message returned

### Update Logic

- **Name Update**: Only updates if new name is different from current name
- **Password Update**: Only updates if new password is different from current hash
- **No Changes**: Returns success message indicating no changes were made
- **Partial Updates**: Supports updating only name, only password, or both

### Security Features

1. **Role-Based Access**: Only managers and admins can update profiles
2. **Password Validation**: New passwords must meet strength requirements
3. **Password Hashing**: New passwords are hashed using bcrypt
4. **Self-Update Only**: Users can only update their own profiles
5. **Input Sanitization**: All inputs are validated and sanitized

### Password Requirements

The new password must meet the same criteria as registration:
- **Minimum length**: 8 characters
- **Lowercase letter**: At least one (a-z)
- **Uppercase letter**: At least one (A-Z)
- **Digit**: At least one (0-9)
- **Special character**: At least one (!@#$%^&*(),.?":{}|<>)

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Get authentication token for manager
MANAGER_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "manager@example.com", "password": "ManagerPass456@"}' \
  | jq -r '.access_tokem')

# Test name update
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"new_name": "Updated Manager Name"}'

# Test password update
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"new_password": "NewManagerPass456@"}'

# Test both name and password update
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"new_name": "Final Manager Name", "new_password": "FinalManagerPass789#"}'

# Test with staff token (should fail)
STAFF_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "staff@example.com", "password": "StaffPass123!"}' \
  | jq -r '.access_tokem')

curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{"new_name": "Should Not Work"}'

# Test weak password
curl -X PATCH "http://127.0.0.1:5001/user/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"new_password": "weak"}'
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

def test_update_user():
    # Test with manager token
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    headers = {"Authorization": f"Bearer {manager_token}"}
    
    print("=== Testing Manager Updates ===")
    
    # Test name update
    update_data = {"new_name": "Updated Manager Name"}
    response = requests.patch(f"{base_url}/user/update", json=update_data, headers=headers)
    print(f"Name Update: {json.dumps(response.json(), indent=2)}")
    
    # Test password update
    update_data = {"new_password": "NewManagerPass456@"}
    response = requests.patch(f"{base_url}/user/update", json=update_data, headers=headers)
    print(f"Password Update: {json.dumps(response.json(), indent=2)}")
    
    # Test both updates
    update_data = {
        "new_name": "Final Manager Name",
        "new_password": "FinalManagerPass789#"
    }
    response = requests.patch(f"{base_url}/user/update", json=update_data, headers=headers)
    print(f"Both Updates: {json.dumps(response.json(), indent=2)}")
    
    # Test with admin token
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("\n=== Testing Admin Updates ===")
    
    update_data = {"new_name": "Updated Admin Name"}
    response = requests.patch(f"{base_url}/user/update", json=update_data, headers=admin_headers)
    print(f"Admin Update: {json.dumps(response.json(), indent=2)}")
    
    # Test with staff token (should fail)
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    
    print("\n=== Testing Staff Unauthorized Access ===")
    
    update_data = {"new_name": "Should Not Work"}
    response = requests.patch(f"{base_url}/user/update", json=update_data, headers=staff_headers)
    print(f"Staff Attempt: {json.dumps(response.json(), indent=2)}")
    
    # Test weak password
    print("\n=== Testing Weak Password Validation ===")
    
    update_data = {"new_password": "weak"}
    response = requests.patch(f"{base_url}/user/update", json=update_data, headers=headers)
    print(f"Weak Password: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_update_user()
```

---

## 🐛 Error Handling

### Common Error Scenarios

1. **Unauthorized Role**
   ```json
   {
     "detail": "Unauthorized to perform action, you are a staff"
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

4. **Weak Password**
   ```json
   {
     "detail": "Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: weak"
   }
   ```

5. **Invalid Name Length**
   ```json
   {
     "detail": [
       {
         "type": "value_error",
         "loc": ["body", "new_name"],
         "msg": "String should have at least 5 characters",
         "input": "abc"
       }
     ]
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | User updated successfully        |
| 401         | Unauthorized / Invalid token     |
| 400         | Bad request (weak password)      |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **POST /user/register**: Create new user account
- **POST /user/login**: User authentication and token generation
- **GET /user/all**: Get all users (requires authentication)
- **DELETE /user/delete**: Delete user account (admin only)

---

## 📝 Notes

- Users can only update their own profiles, not other users' profiles
- The endpoint uses PATCH method to support partial updates
- Password changes require the new password to meet the same strength requirements as registration
- Name changes must maintain uniqueness across the system
- The response includes a descriptive status message indicating what was updated
- Users with staff role cannot update their profiles - only managers and admins
- After password update, the user will need to login again with the new password
- The endpoint returns the complete updated user object including the hashed password
