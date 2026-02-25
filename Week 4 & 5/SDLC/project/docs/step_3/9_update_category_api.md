# Update Category API Documentation

## 📋 Overview

The Update Category API allows authenticated users with manager or admin roles to update existing product categories. This endpoint validates the authentication token, checks user permissions, validates category data, and updates category records in the database.

**Endpoint:** `PUT /category/update`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Manager/Admin only)

---

## 🔐 API Endpoints

### PUT /category/update

Updates an existing product category in the system.

**URL:** `PUT /category/update`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Body

| Parameter | Type   | Required | Description                    | Constraints                      |
|-----------|--------|----------|--------------------------------|-----------------------------------|
| id        | integer | Yes      | Category ID to update           | Must exist in database           |
| name      | string | Yes      | New category name               | Max 25 characters, unique       |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Update category name:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 1,
    "name": "electronics-updated"
  }'
```

**Update category as admin:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "id": 2,
    "name": "clothing-new"
  }'
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "updated category details": {
      "id": 1,
      "name": "electronics-updated"
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

**Error Response (200 OK) - Duplicate name:**
```json
{
  "status": "error",
  "message": {
    "response": "found existing category with same name",
    "category": {
      "id": 2,
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

#### Response Fields

| Field                    | Type     | Description                                    |
|--------------------------|----------|------------------------------------------------|
| status                   | string   | Response status ("success" or "error")         |
| message                  | object   | Contains update status and category data       |
| updated category details | object   | Updated category object (success response)     |
| id                       | integer  | Unique category identifier                     |
| name                     | string   | Updated category name (lowercase, unique)      |

---

## 🚀 Usage Examples

### 1. Manager Updates Category

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "id": 1,
    "name": "electronics-modern"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "updated category details": {
      "id": 1,
      "name": "electronics-modern"
    }
  }
}
```

### 2. Admin Updates Category

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "id": 3,
    "name": "books-updated"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "updated category details": {
      "id": 3,
      "name": "books-updated"
    }
  }
}
```

### 3. Category Not Found

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 999,
    "name": "nonexistent"
  }'
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

### 4. Duplicate Category Name

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 1,
    "name": "clothing"
  }'
```

**Response:**
```json
{
  "status": "error",
  "message": {
    "response": "found existing category with same name",
    "category": {
      "id": 2,
      "name": "clothing"
    }
  }
}
```

### 5. Staff User Attempts Update (Unauthorized)

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "id": 1,
    "name": "should-not-work"
  }'
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

---

## 🔧 Implementation Details

### Update Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked (must be manager or admin)
3. **Input Validation**: Pydantic schema validates category data
4. **Category Lookup**: Target category is found in database by ID
5. **Duplicate Check**: Database query checks for existing name (excluding current category)
6. **Category Update**: Category name is updated and saved
7. **Database Commit**: Transaction is committed to persist changes
8. **Response**: Updated category object is returned

### Validation Rules

- **ID**: Required, must exist in database
- **Name**: Required, max 25 characters, unique across system (excluding current category)
- **Case Handling**: Category names are stored in lowercase
- **Uniqueness**: Name must be unique among all categories

### Security Features

1. **Role-Based Access**: Only managers and admins can update categories
2. **Input Validation**: All inputs are validated and sanitized
3. **Duplicate Prevention**: Database constraints prevent duplicate names
4. **Existence Check**: Category must exist before update
5. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

### Data Processing

- **Name Normalization**: Category names are converted to lowercase
- **Duplicate Exclusion**: Current category is excluded from duplicate name check
- **Atomic Update**: Update operation is atomic and transactional

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

# Test manager updates category
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"id": 1, "name": "updated-electronics"}'

# Test admin updates category
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"id": 2, "name": "updated-clothing"}'

# Test category not found
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"id": 999, "name": "nonexistent"}'

# Test duplicate name
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{"id": 1, "name": "clothing"}'

# Test unauthorized access (staff)
curl -X PUT "http://127.0.0.1:5001/category/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{"id": 1, "name": "unauthorized"}'
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

def test_update_category():
    # Get tokens for different roles
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    
    print("=== Testing Manager Update ===")
    
    # Test manager updates category
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    category_data = {"id": 1, "name": "manager-updated"}
    response = requests.put(f"{base_url}/category/update", json=category_data, headers=manager_headers)
    print(f"Manager Update: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Admin Update ===")
    
    # Test admin updates category
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    category_data = {"id": 2, "name": "admin-updated"}
    response = requests.put(f"{base_url}/category/update", json=category_data, headers=admin_headers)
    print(f"Admin Update: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Category Not Found ===")
    
    # Test category not found
    category_data = {"id": 999, "name": "nonexistent"}
    response = requests.put(f"{base_url}/category/update", json=category_data, headers=manager_headers)
    print(f"Not Found: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Duplicate Name ===")
    
    # Test duplicate name
    category_data = {"id": 1, "name": "clothing"}
    response = requests.put(f"{base_url}/category/update", json=category_data, headers=manager_headers)
    print(f"Duplicate Name: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Unauthorized Access ===")
    
    # Test staff unauthorized access
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    category_data = {"id": 1, "name": "should-not-work"}
    response = requests.put(f"{base_url}/category/update", json=category_data, headers=staff_headers)
    print(f"Staff Unauthorized: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_update_category()
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

4. **Category Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "Unable to find category with id - 999"
     }
   }
   ```

5. **Duplicate Category Name**
   ```json
   {
     "status": "error",
     "message": {
       "response": "found existing category with same name",
       "category": {
         "id": 2,
         "name": "electronics"
       }
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
| 200         | Category updated successfully    |
| 200         | Category not found (error status)|
| 200         | Duplicate name (error status)    |
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /category/all**: Get all categories
- **GET /category**: Get specific category by ID
- **POST /category**: Create new category (manager/admin only)
- **DELETE /category/delete**: Delete category (admin only)

---

## 📝 Notes

- Only managers and admins can update categories
- Category names are automatically converted to lowercase
- Category must exist before it can be updated
- Category names must be unique across the entire system
- The current category is excluded from duplicate name checks
- Updated category names are immediately reflected in the system
- Consider implementing category versioning for audit trails
- The endpoint returns the complete updated category object for confirmation
- Products associated with the category are not affected by name changes
- Category updates are atomic - either fully succeed or fail completely
