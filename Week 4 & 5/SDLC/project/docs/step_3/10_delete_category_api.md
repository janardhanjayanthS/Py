# Delete Category API Documentation

## 📋 Overview

The Delete Category API allows authenticated admin users to permanently delete product categories from the system. This endpoint validates the admin's authentication token, checks admin permissions, and removes the specified category from the database.

**Endpoint:** `DELETE /category/delete`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Admin only)

---

## 🔐 API Endpoints

### DELETE /category/delete

Permanently deletes a product category from the system.

**URL:** `DELETE /category/delete?category_id={category_id}`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Query Parameters

| Parameter    | Type   | Required | Description                    |
|--------------|--------|----------|--------------------------------|
| category_id  | integer | Yes      | ID of the category to delete   |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Delete category with ID 1:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=1" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

**Delete category with ID 5:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=5" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "deleted category": {
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

**Error Response (401 Unauthorized) - Manager user:**
```json
{
  "detail": "Unauthorized to perform action, you are a manager"
}
```

**Error Response (401 Unauthorized) - Staff user:**
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

#### Response Fields

| Field            | Type     | Description                                    |
|------------------|----------|------------------------------------------------|
| status           | string   | Response status ("success" or "error")         |
| message          | object   | Contains deleted category data or error message|
| deleted category | object   | Complete category object that was deleted      |
| id               | integer  | Unique category identifier                     |
| name             | string   | Category name (lowercase, unique)              |

---

## 🚀 Usage Examples

### 1. Admin Deletes Category

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "deleted category": {
      "id": 1,
      "name": "electronics"
    }
  }
}
```

### 2. Admin Deletes Another Category

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=3" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "deleted category": {
      "id": 3,
      "name": "books"
    }
  }
}
```

### 3. Manager Attempts to Delete Category (Unauthorized)

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=2" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a manager"
}
```

### 4. Staff User Attempts to Delete Category (Unauthorized)

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=4" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

### 5. Admin Deletes Non-existent Category

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=999" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
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

### 6. Admin Deletes Category with Invalid ID Type

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=invalid" \
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
3. **Category ID Validation**: Query parameter is validated as integer
4. **Category Lookup**: Target category is found in database by ID
5. **Deletion Execution**: Category record is permanently removed
6. **Database Commit**: Transaction is committed to persist deletion
7. **Response**: Deleted category object and confirmation returned

### Security Considerations

1. **Admin Only**: Only users with admin role can delete categories
2. **Permanent Deletion**: This operation cannot be undone
3. **Referential Integrity**: Categories with associated products may cause database constraints
4. **Audit Trail**: Consider implementing audit logging for category deletions
5. **Input Validation**: Category ID is validated to prevent injection

### Cascade Effects

- **Products**: Products associated with the category may be affected depending on foreign key constraints
- **Database Constraints**: ON DELETE CASCADE may remove associated products
- **Data Integrity**: System maintains referential integrity

### Error Handling

- **Category Not Found**: Returns error status with descriptive message
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

# Get staff token (for testing unauthorized access)
STAFF_TOKEN=$(curl -s -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "staff@example.com", "password": "StaffPass123!"}' \
  | jq -r '.access_tokem')

# Test successful deletion
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=1" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test deletion of non-existent category
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=999" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test with invalid ID type
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=invalid" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test unauthorized access (manager)
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=2" \
  -H "Authorization: Bearer $MANAGER_TOKEN"

# Test unauthorized access (staff)
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=3" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test without authentication
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=4"

# Test with invalid token
curl -X DELETE "http://127.0.0.1:5001/category/delete?category_id=5" \
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

def test_delete_category():
    # Get admin token
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("=== Testing Admin Deletions ===")
    
    # Test successful deletion
    response = requests.delete(f"{base_url}/category/delete?category_id=1", headers=admin_headers)
    print(f"Successful Deletion: {json.dumps(response.json(), indent=2)}")
    
    # Test deletion of non-existent category
    response = requests.delete(f"{base_url}/category/delete?category_id=999", headers=admin_headers)
    print(f"Non-existent Category: {json.dumps(response.json(), indent=2)}")
    
    # Test invalid ID type
    response = requests.delete(f"{base_url}/category/delete?category_id=invalid", headers=admin_headers)
    print(f"Invalid ID Type: {json.dumps(response.json(), indent=2)}")
    
    # Test unauthorized access
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    
    print("\n=== Testing Unauthorized Access ===")
    
    response = requests.delete(f"{base_url}/category/delete?category_id=2", headers=manager_headers)
    print(f"Manager Attempt: {json.dumps(response.json(), indent=2)}")
    
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    
    response = requests.delete(f"{base_url}/category/delete?category_id=3", headers=staff_headers)
    print(f"Staff Attempt: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    print("\n=== Testing No Authentication ===")
    
    response = requests.delete(f"{base_url}/category/delete?category_id=4")
    print(f"No Auth: {json.dumps(response.json(), indent=2)}")
    
    # Test with invalid token
    print("\n=== Testing Invalid Token ===")
    
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.delete(f"{base_url}/category/delete?category_id=5", headers=invalid_headers)
    print(f"Invalid Token: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_delete_category()
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

4. **Invalid Category ID Type**
   ```json
   {
     "detail": "id should be type int but got type: str"
   }
   ```

5. **Category Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "Unable to find category with id - 999"
     }
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Category deleted successfully    |
| 200         | Category not found (error status)|
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid ID)    |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /category/all**: Get all categories
- **GET /category**: Get specific category by ID
- **POST /category**: Create new category (manager/admin only)
- **PUT /category/update**: Update category (manager/admin only)

---

## 📝 Notes

- This operation is permanent and cannot be undone
- Only admin users can delete categories
- Categories with associated products may cause database constraint violations
- Consider implementing soft deletes in production for better data recovery
- The response includes the complete deleted category object for audit purposes
- Category deletions should be logged for security and audit purposes
- Database foreign key constraints may prevent deletion of categories with products
- Consider implementing a confirmation step for critical category deletions
- The endpoint returns success even when category doesn't exist (with error status)
- Category ID validation prevents SQL injection attacks
- Admin-only access ensures system integrity and prevents accidental category removal
