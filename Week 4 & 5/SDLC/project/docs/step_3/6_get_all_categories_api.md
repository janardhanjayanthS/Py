# Get All Categories API Documentation

## 📋 Overview

The Get All Categories API retrieves a list of all product categories in the system. This endpoint requires authentication and is accessible to users with staff, manager, or admin roles. It returns category information including IDs and names.

**Endpoint:** `GET /category/all`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token)

---

## 🔐 API Endpoints

### GET /category/all

Retrieves all product categories from the database.

**URL:** `GET /category/all`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Get all categories as staff:**
```bash
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Get all categories as manager:**
```bash
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer MANAGER_JWT_TOKEN_HERE"
```

**Get all categories as admin:**
```bash
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "current user's email": "alice.johnson@example.com",
    "all categories": [
      {
        "id": 1,
        "name": "electronics"
      },
      {
        "id": 2,
        "name": "clothing"
      },
      {
        "id": 3,
        "name": "books"
      },
      {
        "id": 4,
        "name": "home & garden"
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
    "current user's email": "alice.johnson@example.com",
    "all categories": []
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

| Field                | Type     | Description                                    |
|----------------------|----------|------------------------------------------------|
| status               | string   | Response status ("success")                     |
| message              | object   | Contains current user email and categories list |
| current user's email | string   | Email of the authenticated user making request |
| all categories       | array    | Array of category objects                      |
| id                   | integer  | Unique category identifier                     |
| name                 | string   | Category name (lowercase, unique)              |

---

## 🚀 Usage Examples

### 1. Staff User Getting All Categories

**Request:**
```bash
# First login as staff user
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.johnson@example.com",
    "password": "StaffPass123!"
  }'

# Use the token to get all categories
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZS5qb2huc29uQGV4YW1wbGUuY29tIiwicm9sZSI6InN0YWZmIiwiZXhwIjoxNzA1MjQyNDAwfQ.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "current user's email": "alice.johnson@example.com",
    "all categories": [
      {
        "id": 1,
        "name": "electronics"
      },
      {
        "id": 2,
        "name": "clothing"
      },
      {
        "id": 3,
        "name": "books"
      }
    ]
  }
}
```

### 2. Manager User Getting All Categories

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Iud2lsc29uQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "current user's email": "bob.wilson@example.com",
    "all categories": [
      {
        "id": 1,
        "name": "electronics"
      },
      {
        "id": 2,
        "name": "clothing"
      },
      {
        "id": 3,
        "name": "books"
      },
      {
        "id": 4,
        "name": "home & garden"
      }
    ]
  }
}
```

### 3. Admin User Getting All Categories

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "current user's email": "admin@example.com",
    "all categories": [
      {
        "id": 1,
        "name": "electronics"
      },
      {
        "id": 2,
        "name": "clothing"
      },
      {
        "id": 3,
        "name": "books"
      },
      {
        "id": 4,
        "name": "home & garden"
      },
      {
        "id": 5,
        "name": "sports"
      }
    ]
  }
}
```

### 4. Empty Categories List

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "current user's email": "alice.johnson@example.com",
    "all categories": []
  }
}
```

---

## 🔧 Implementation Details

### Authorization Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked against allowed roles (staff, manager, admin)
3. **User Identification**: Current user's email is extracted from token
4. **Database Query**: All categories are retrieved from the database
5. **Response Construction**: Category list is formatted with current user context

### Role-Based Access Control

The following roles can access this endpoint:
- **staff**: Read-only access to view all categories
- **manager**: Read-only access to view all categories
- **admin**: Read-only access to view all categories

### Data Processing

- **Category Names**: Stored and returned in lowercase
- **Unique Constraint**: Category names are unique across the system
- **Sorting**: Categories are returned in database order (typically by ID)
- **Empty Handling**: Empty category lists return an empty array

### Response Structure

- **status**: Always "success" for successful requests
- **message**: Object containing:
  - **current user's email**: Email of the authenticated user
  - **all categories**: Array of all category objects in the system

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
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test with manager token
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer $MANAGER_TOKEN"

# Test with admin token
curl -X GET "http://127.0.0.1:5001/category/all" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test without token (should fail)
curl -X GET "http://127.0.0.1:5001/category/all"

# Test with invalid token (should fail)
curl -X GET "http://127.0.0.1:5001/category/all" \
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

def test_get_all_categories():
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
        
        # Get all categories
        response = requests.get(f"{base_url}/category/all", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    print("\n=== Testing without authentication ===")
    response = requests.get(f"{base_url}/category/all")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test with invalid token
    print("\n=== Testing with invalid token ===")
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{base_url}/category/all", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_get_all_categories()
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
| 200         | Categories retrieved successfully |
| 401         | Unauthorized / Invalid token     |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /category**: Get specific category by ID
- **POST /category**: Create new category (manager/admin only)
- **PUT /category/update**: Update category (manager/admin only)
- **DELETE /category/delete**: Delete category (admin only)

---

## 📝 Notes

- All authenticated users (staff, manager, admin) can view all categories
- Category names are returned in lowercase as stored in the database
- The response includes the current user's email for context
- Categories are returned in the order they appear in the database (typically by ID)
- Empty category lists return an empty array rather than null
- Category names are unique across the system
- This endpoint is useful for populating dropdown lists in user interfaces
- Consider implementing pagination for large category lists in production
- Categories with associated products cannot be deleted (referential integrity)
