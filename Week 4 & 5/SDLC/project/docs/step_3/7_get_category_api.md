# Get Category API Documentation

## 📋 Overview

The Get Category API retrieves a specific product category by its ID. This endpoint requires authentication and is accessible to users with staff, manager, or admin roles. It returns detailed information about the requested category.

**Endpoint:** `GET /category`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token)

---

## 🔐 API Endpoints

### GET /category

Retrieves a specific product category by ID.

**URL:** `GET /category?category_id={category_id}`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Query Parameters

| Parameter    | Type   | Required | Description                    |
|--------------|--------|----------|--------------------------------|
| category_id  | integer | Yes      | ID of the category to retrieve  |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Get category with ID 1:**
```bash
curl -X GET "http://127.0.0.1:5001/category?category_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Get category with ID 3:**
```bash
curl -X GET "http://127.0.0.1:5001/category?category_id=3" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "requested category": {
      "id": 1,
      "name": "electronics"
    }
  }
}
```

**Error Response (200 OK) - Category not found:**
```json
{
  "status": "error",
  "message": {
    "response": "Unable to find category with id - 999"
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

| Field               | Type     | Description                                    |
|---------------------|----------|------------------------------------------------|
| status              | string   | Response status ("success" or "error")         |
| message             | object   | Contains category data or error message        |
| requested category  | object   | Category object (success response)             |
| id                  | integer  | Unique category identifier                     |
| name                | string   | Category name (lowercase, unique)              |

---

## 🚀 Usage Examples

### 1. Staff User Gets Category

**Request:**
```bash
# First login as staff user
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.johnson@example.com",
    "password": "StaffPass123!"
  }'

# Use the token to get category
curl -X GET "http://127.0.0.1:5001/category?category_id=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZS5qb2huc29uQGV4YW1wbGUuY29tIiwicm9sZSI6InN0YWZmIiwiZXhwIjoxNzA1MjQyNDAwfQ.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "requested category": {
      "id": 1,
      "name": "electronics"
    }
  }
}
```

### 2. Manager User Gets Category

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category?category_id=2" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Iud2lsc29uQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "requested category": {
      "id": 2,
      "name": "clothing"
    }
  }
}
```

### 3. Admin User Gets Category

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category?category_id=3" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "requested category": {
      "id": 3,
      "name": "books"
    }
  }
}
```

### 4. Category Not Found

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category?category_id=999" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Response:**
```json
{
  "status": "error",
  "message": {
    "response": "Unable to find category with id - 999"
  }
}
```

### 5. Invalid Category ID Type

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/category?category_id=invalid" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Response:**
```json
{
  "detail": "id should be type int but got type: str"
}
```

---

## 🔧 Implementation Details

### Retrieval Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked against allowed roles (staff, manager, admin)
3. **Category ID Validation**: Query parameter is validated as integer
4. **Database Query**: Category is retrieved from database by ID
5. **Response Construction**: Category data is formatted and returned

### Role-Based Access Control

The following roles can access this endpoint:
- **staff**: Read-only access to view specific categories
- **manager**: Read-only access to view specific categories
- **admin**: Read-only access to view specific categories

### Data Processing

- **Category Lookup**: Uses SQLAlchemy ORM to find category by primary key
- **Error Handling**: Returns error status for non-existent categories
- **Type Validation**: Ensures category_id is a valid integer
- **Response Format**: Consistent with other category endpoints

### Response Structure

- **Success**: Contains category object with id and name
- **Error**: Contains descriptive error message
- **Status**: Indicates success or error state

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Get authentication token
STAFF_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "staff@example.com", "password": "StaffPass123!"}' \
  | jq -r '.access_tokem')

# Test successful retrieval
curl -X GET "http://127.0.0.1:5001/category?category_id=1" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test category not found
curl -X GET "http://127.0.0.1:5001/category?category_id=999" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test invalid ID type
curl -X GET "http://127.0.0.1:5001/category?category_id=invalid" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test without authentication
curl -X GET "http://127.0.0.1:5001/category?category_id=1"

# Test with invalid token
curl -X GET "http://127.0.0.1:5001/category?category_id=1" \
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

def test_get_category():
    # Get staff token
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    headers = {"Authorization": f"Bearer {staff_token}"}
    
    print("=== Testing Category Retrieval ===")
    
    # Test successful retrieval
    response = requests.get(f"{base_url}/category?category_id=1", headers=headers)
    print(f"Category 1: {json.dumps(response.json(), indent=2)}")
    
    # Test another category
    response = requests.get(f"{base_url}/category?category_id=2", headers=headers)
    print(f"Category 2: {json.dumps(response.json(), indent=2)}")
    
    # Test category not found
    response = requests.get(f"{base_url}/category?category_id=999", headers=headers)
    print(f"Category Not Found: {json.dumps(response.json(), indent=2)}")
    
    # Test invalid ID type
    response = requests.get(f"{base_url}/category?category_id=invalid", headers=headers)
    print(f"Invalid ID Type: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    print("\n=== Testing Without Authentication ===")
    response = requests.get(f"{base_url}/category?category_id=1")
    print(f"No Auth: {json.dumps(response.json(), indent=2)}")
    
    # Test with invalid token
    print("\n=== Testing Invalid Token ===")
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{base_url}/category?category_id=1", headers=invalid_headers)
    print(f"Invalid Token: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_get_category()
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

3. **Invalid Category ID Type**
   ```json
   {
     "detail": "id should be type int but got type: str"
   }
   ```

4. **Category Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "Unable to find category with id - 999"
     }
   }
   ```

5. **Unauthorized Role**
   ```json
   {
     "detail": "Unauthorized to perform action, you are a unauthorized_role"
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Category retrieved successfully  |
| 200         | Category not found (error status)|
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid ID)    |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /category/all**: Get all categories
- **POST /category**: Create new category (manager/admin only)
- **PUT /category/update**: Update category (manager/admin only)
- **DELETE /category/delete**: Delete category (admin only)

---

## 📝 Notes

- All authenticated users (staff, manager, admin) can view specific categories
- Category names are returned in lowercase as stored in the database
- The endpoint returns error status (200 OK) when category is not found
- Category IDs must be positive integers
- This endpoint is useful for validating category existence before product operations
- Consider implementing caching for frequently accessed categories
- Categories with associated products can still be retrieved (deletion is separate)
