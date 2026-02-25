# Delete Product API Documentation

## 📋 Overview

The Delete Product API allows authenticated admin users to permanently delete products from the inventory system. This endpoint validates the admin's authentication token, checks admin permissions, and removes the specified product from the database.

**Endpoint:** `DELETE /product`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Admin only)

---

## 🔐 API Endpoints

### DELETE /product

Permanently deletes a product from the inventory system.

**URL:** `DELETE /product?product_id={product_id}`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Query Parameters

| Parameter    | Type   | Required | Description                    |
|--------------|--------|----------|--------------------------------|
| product_id   | integer | Yes      | ID of the product to delete    |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Delete product with ID 1:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=1" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

**Delete product with ID 5:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=5" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "deleted product": {
      "id": 1,
      "name": "Laptop",
      "quantity": 10,
      "price": 999.99,
      "price_type": "regular",
      "category_id": 1
    }
  }
}
```

**Error Response (200 OK) - Product not found:**
```json
{
  "status": "error",
  "message": {
    "response": "product with id 999 not found"
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
| message          | object   | Contains deleted product data or error message|
| deleted product  | object   | Complete product object that was deleted      |
| id               | integer  | Unique product identifier                     |
| name             | string   | Product name                                   |
| quantity         | integer  | Product quantity in stock                     |
| price            | float    | Product price                                  |
| price_type       | string   | Price type ("regular", "taxed", "discounted")  |
| category_id      | integer  | Associated category ID                         |

---

## 🚀 Usage Examples

### 1. Admin Deletes Product

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "deleted product": {
      "id": 1,
      "name": "Laptop",
      "quantity": 10,
      "price": 999.99,
      "price_type": "regular",
      "category_id": 1
    }
  }
}
```

### 2. Admin Deletes Another Product

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=3" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "deleted product": {
      "id": 3,
      "name": "T-Shirt",
      "quantity": 50,
      "price": 19.99,
      "price_type": "taxed",
      "category_id": 2
    }
  }
}
```

### 3. Manager Attempts to Delete Product (Unauthorized)

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=2" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a manager"
}
```

### 4. Staff User Attempts to Delete Product (Unauthorized)

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=4" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

### 5. Admin Deletes Non-existent Product

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=999" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE"
```

**Response:**
```json
{
  "status": "error",
  "message": {
    "response": "product with id 999 not found"
  }
}
```

### 6. Admin Deletes Product with Invalid ID Type

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:5001/product?product_id=invalid" \
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
3. **Product ID Validation**: Query parameter is validated as integer
4. **Product Lookup**: Target product is found in database by ID
5. **Deletion Execution**: Product record is permanently removed
6. **Database Commit**: Transaction is committed to persist deletion
7. **Response**: Deleted product object and confirmation returned

### Security Considerations

1. **Admin Only**: Only users with admin role can delete products
2. **Permanent Deletion**: This operation cannot be undone
3. **Inventory Impact**: Deleting products affects inventory records
4. **Audit Trail**: Consider implementing audit logging for product deletions
5. **Input Validation**: Product ID is validated to prevent injection

### Cascade Effects

- **Inventory Records**: Product deletion removes inventory entries
- **Category Relationships**: Product-category relationships are removed
- **Data Integrity**: System maintains referential integrity
- **Historical Data**: Consider soft deletes for historical tracking

### Error Handling

- **Product Not Found**: Returns error status with descriptive message
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
curl -X DELETE "http://127.0.0.1:5001/product?product_id=1" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test deletion of non-existent product
curl -X DELETE "http://127.0.0.1:5001/product?product_id=999" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test with invalid ID type
curl -X DELETE "http://127.0.0.1:5001/product?product_id=invalid" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test unauthorized access (manager)
curl -X DELETE "http://127.0.0.1:5001/product?product_id=2" \
  -H "Authorization: Bearer $MANAGER_TOKEN"

# Test unauthorized access (staff)
curl -X DELETE "http://127.0.0.1:5001/product?product_id=3" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test without authentication
curl -X DELETE "http://127.0.0.1:5001/product?product_id=4"

# Test with invalid token
curl -X DELETE "http://127.0.0.1:5001/product?product_id=5" \
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

def test_delete_product():
    # Get admin token
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("=== Testing Admin Deletions ===")
    
    # Test successful deletion
    response = requests.delete(f"{base_url}/product?product_id=1", headers=admin_headers)
    print(f"Successful Deletion: {json.dumps(response.json(), indent=2)}")
    
    # Test deletion of non-existent product
    response = requests.delete(f"{base_url}/product?product_id=999", headers=admin_headers)
    print(f"Non-existent Product: {json.dumps(response.json(), indent=2)}")
    
    # Test invalid ID type
    response = requests.delete(f"{base_url}/product?product_id=invalid", headers=admin_headers)
    print(f"Invalid ID Type: {json.dumps(response.json(), indent=2)}")
    
    # Test unauthorized access
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    
    print("\n=== Testing Unauthorized Access ===")
    
    response = requests.delete(f"{base_url}/product?product_id=2", headers=manager_headers)
    print(f"Manager Attempt: {json.dumps(response.json(), indent=2)}")
    
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    
    response = requests.delete(f"{base_url}/product?product_id=3", headers=staff_headers)
    print(f"Staff Attempt: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    print("\n=== Testing No Authentication ===")
    
    response = requests.delete(f"{base_url}/product?product_id=4")
    print(f"No Auth: {json.dumps(response.json(), indent=2)}")
    
    # Test with invalid token
    print("\n=== Testing Invalid Token ===")
    
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.delete(f"{base_url}/product?product_id=5", headers=invalid_headers)
    print(f"Invalid Token: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_delete_product()
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

4. **Invalid Product ID Type**
   ```json
   {
     "detail": "id should be type int but got type: str"
   }
   ```

5. **Product Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "product with id 999 not found"
     }
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Product deleted successfully     |
| 200         | Product not found (error status) |
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid ID)    |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /products**: Get products (with filtering)
- **POST /products**: Create new product (manager/admin only)
- **PUT /product**: Update existing product (manager/admin only)
- **PATCH /product/update_category**: Update product category (manager/admin only)

---

## 📝 Notes

- This operation is permanent and cannot be undone
- Only admin users can delete products
- Product deletions affect inventory records and stock levels
- Consider implementing soft deletes in production for better data recovery
- The response includes the complete deleted product object for audit purposes
- Product deletions should be logged for security and audit purposes
- Consider implementing a confirmation step for critical product deletions
- The endpoint returns success even when product doesn't exist (with error status)
- Product ID validation prevents SQL injection attacks
- Admin-only access ensures system integrity and prevents accidental product removal
- Consider checking for active orders or dependencies before deletion
- Product deletion may affect reporting and analytics data
