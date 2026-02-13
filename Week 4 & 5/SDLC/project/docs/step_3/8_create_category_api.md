# Create Category API Documentation

## 📋 Overview

The Create Category API allows authenticated users with manager or admin roles to create new product categories. This endpoint validates the authentication token, checks user permissions, validates category data, and creates new category records in the database.

**Endpoint:** `POST /category`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Manager/Admin only)

---

## 🔐 API Endpoints

### POST /category

Creates a new product category in the system.

**URL:** `POST /category`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Body

| Parameter | Type   | Required | Description                    | Constraints                      |
|-----------|--------|----------|--------------------------------|-----------------------------------|
| id        | integer | No       | Category ID (optional)          | Unique if provided               |
| name      | string | Yes      | Category name                   | Max 25 characters, unique       |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Create category with name only:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "name": "electronics"
  }'
```

**Create category with ID and name:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "id": 10,
    "name": "sports"
  }'
```

**Create category as admin:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "name": "toys"
  }'
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "new category": {
      "id": 5,
      "name": "electronics"
    }
  }
}
```

**Error Response (401 Unauthorized) - Staff user:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

**Error Response (400 Bad Request) - Duplicate name:**
```json
{
  "detail": {
    "message": "Category with name - electronics - already exists in db"
  }
}
```

**Error Response (400 Bad Request) - Duplicate ID:**
```json
{
  "detail": {
    "message": "Category with id - 1 - already exists in db"
  }
}
```

#### Response Fields

| Field        | Type     | Description                                    |
|--------------|----------|------------------------------------------------|
| status       | string   | Response status ("success")                     |
| message      | object   | Contains created category data                 |
| new category | object   | Complete category object that was created      |
| id           | integer  | Unique category identifier                     |
| name         | string   | Category name (lowercase, unique)              |

---

## 🚀 Usage Examples

### 1. Manager Creates Category

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "name": "furniture"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "new category": {
      "id": 6,
      "name": "furniture"
    }
  }
}
```

### 2. Admin Creates Category with ID

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "id": 15,
    "name": "automotive"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "new category": {
      "id": 15,
      "name": "automotive"
    }
  }
}
```

### 3. Staff User Attempts Creation (Unauthorized)

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "name": "should-not-work"
  }'
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

### 4. Duplicate Category Name

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "name": "electronics"
  }'
```

**Response:**
```json
{
  "detail": {
    "message": "Category with name - electronics - already exists in db"
  }
}
```

### 5. Duplicate Category ID

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 1,
    "name": "new-category"
  }'
```

**Response:**
```json
{
  "detail": {
    "message": "Category with id - 1 - already exists in db"
  }
}
```

---

## 🔧 Implementation Details

### Creation Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked (must be manager or admin)
3. **Input Validation**: Pydantic schema validates category data
4. **Duplicate Checks**: Database queries check for existing name and ID
5. **Category Creation**: New category record is created and saved
6. **Database Commit**: Transaction is committed to persist the category
7. **Response**: Created category object is returned

### Validation Rules

- **Name**: Required, max 25 characters, unique across system
- **ID**: Optional, must be unique if provided
- **Case Handling**: Category names are stored in lowercase
- **Uniqueness**: Both name and ID must be unique if specified

### Security Features

1. **Role-Based Access**: Only managers and admins can create categories
2. **Input Validation**: All inputs are validated and sanitized
3. **Duplicate Prevention**: Database constraints prevent duplicates
4. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

### Data Processing

- **Name Normalization**: Category names are converted to lowercase
- **ID Generation**: Auto-generated if not provided
- **Error Logging**: Duplicate attempts are logged for monitoring

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Get manager token
MANAGER_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "manager@example.com", "password": "ManagerPass456@"}' \
  | jq -r '.access_tokem')

# Get admin token
ADMIN_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "AdminPass789#"}' \
  | jq -r '.access_tokem')

# Get staff token (for testing unauthorized access)
STAFF_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "staff@example.com", "password": "StaffPass123!"}' \
  | jq -r '.access_tokem')

# Test manager creates category
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"name": "test-category"}'

# Test admin creates category with ID
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"id": 20, "name": "admin-category"}'

# Test duplicate name
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"name": "test-category"}'

# Test duplicate ID
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"id": 1, "name": "duplicate-id"}'

# Test unauthorized access (staff)
curl -X POST "http://127.0.0.1:5001/category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{"name": "unauthorized"}'
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

def test_create_category():
    # Get tokens for different roles
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    
    print("=== Testing Manager Creation ===")
    
    # Test manager creates category
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    category_data = {"name": "test-manager-category"}
    response = requests.post(f"{base_url}/category", json=category_data, headers=manager_headers)
    print(f"Manager Creation: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Admin Creation ===")
    
    # Test admin creates category with ID
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    category_data = {"id": 25, "name": "test-admin-category"}
    response = requests.post(f"{base_url}/category", json=category_data, headers=admin_headers)
    print(f"Admin Creation: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Duplicate Name ===")
    
    # Test duplicate name
    category_data = {"name": "test-manager-category"}
    response = requests.post(f"{base_url}/category", json=category_data, headers=manager_headers)
    print(f"Duplicate Name: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Duplicate ID ===")
    
    # Test duplicate ID
    category_data = {"id": 1, "name": "duplicate-id-test"}
    response = requests.post(f"{base_url}/category", json=category_data, headers=admin_headers)
    print(f"Duplicate ID: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Unauthorized Access ===")
    
    # Test staff unauthorized access
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    category_data = {"name": "should-not-work"}
    response = requests.post(f"{base_url}/category", json=category_data, headers=staff_headers)
    print(f"Staff Unauthorized: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_create_category()
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

4. **Duplicate Category Name**
   ```json
   {
     "detail": {
       "message": "Category with name - electronics - already exists in db"
     }
   }
   ```

5. **Duplicate Category ID**
   ```json
   {
     "detail": {
       "message": "Category with id - 1 - already exists in db"
     }
   }
   ```

6. **Invalid Name Length**
   ```json
   {
     "detail": [
       {
         "type": "string_too_long",
         "loc": ["body", "name"],
         "msg": "String should have at most 25 characters",
         "input": "this-category-name-is-way-too-long-for-the-system"
       }
     ]
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Category created successfully    |
| 401         | Unauthorized / Invalid token     |
| 400         | Bad request (duplicate data)     |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /category/all**: Get all categories
- **GET /category**: Get specific category by ID
- **PUT /category/update**: Update category (manager/admin only)
- **DELETE /category/delete**: Delete category (admin only)

---

## 📝 Notes

- Only managers and admins can create categories
- Category names are automatically converted to lowercase
- Category IDs are auto-generated if not provided
- Category names must be unique across the entire system
- Category IDs must be unique if explicitly provided
- Created categories can be used immediately for product categorization
- Consider implementing category hierarchy in future versions
- The endpoint returns the complete created category object for confirmation
- Duplicate attempts are logged for security monitoring
- Categories with special characters are handled appropriately
