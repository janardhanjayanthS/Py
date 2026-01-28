# Update Product Category API Documentation

## 📋 Overview

The Update Product Category API allows authenticated users with manager or admin roles to update the category of existing products. This endpoint validates the authentication token, checks user permissions, validates product and category data, and updates the product's category assignment in the database.

**Endpoint:** `PATCH /product/update_category`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Manager/Admin only)

---

## 🔐 API Endpoints

### PATCH /product/update_category

Updates the category of an existing product.

**URL:** `PATCH /product/update_category`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Body

| Parameter    | Type    | Required | Description                    | Constraints                      |
|--------------|---------|----------|--------------------------------|-----------------------------------|
| product_id   | integer | Yes      | Product ID to update            | Must exist in database           |
| category_id  | integer | Yes      | New category ID                 | Must exist in database          |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Update product category:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "product_id": 1,
    "category_id": 2
  }'
```

**Update product category as admin:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "product_id": 3,
    "category_id": 1
  }'
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": {
    "user email": "bob.wilson@example.com",
    "updated product": {
      "id": 1,
      "name": "Laptop",
      "quantity": 10,
      "price": 999.99,
      "price_type": "regular",
      "category_id": 2
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

**Error Response (200 OK) - Category not found:**
```json
{
  "status": "error",
  "message": {
    "response": "Cannot find category with id: 999"
  }
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

| Field             | Type     | Description                                    |
|-------------------|----------|------------------------------------------------|
| status            | string   | Response status ("success" or "error")         |
| message           | object   | Contains user email and product data          |
| user email        | string   | Email of the authenticated user making request |
| updated product   | object   | Complete updated product object               |
| id                | integer  | Unique product identifier                     |
| name              | string   | Product name                                   |
| quantity          | integer  | Product quantity in stock                     |
| price             | float    | Product price                                  |
| price_type        | string   | Price type ("regular", "taxed", "discounted")  |
| category_id       | integer  | Updated category ID                            |

---

## 🚀 Usage Examples

### 1. Manager Updates Product Category

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "product_id": 1,
    "category_id": 2
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "bob.wilson@example.com",
    "updated product": {
      "id": 1,
      "name": "Laptop",
      "quantity": 10,
      "price": 999.99,
      "price_type": "regular",
      "category_id": 2
    }
  }
}
```

### 2. Admin Updates Product Category

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "product_id": 3,
    "category_id": 1
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "admin@example.com",
    "updated product": {
      "id": 3,
      "name": "T-Shirt",
      "quantity": 50,
      "price": 19.99,
      "price_type": "taxed",
      "category_id": 1
    }
  }
}
```

### 3. Product Not Found

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "product_id": 999,
    "category_id": 1
  }'
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

### 4. Category Not Found

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "product_id": 1,
    "category_id": 999
  }'
```

**Response:**
```json
{
  "status": "error",
  "message": {
    "response": "Cannot find category with id: 999"
  }
}
```

### 5. Staff User Attempts Category Update (Unauthorized)

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "product_id": 1,
    "category_id": 2
  }'
```

**Response:**
```json
{
  "detail": "Unauthorized to perform action, you are a staff"
}
```

### 6. Invalid Product ID Type

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "product_id": "invalid",
    "category_id": 1
  }'
```

**Response:**
```json
{
  "detail": "product_id should be type int but got type: str"
}
```

---

## 🔧 Implementation Details

### Update Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked (must be manager or admin)
3. **Input Validation**: Pydantic schema validates product and category IDs
4. **Product Lookup**: Target product is found in database by ID
5. **Category Validation**: Ensures new category exists
6. **Category Update**: Product's category_id field is updated and saved
7. **Database Commit**: Transaction is committed to persist changes
8. **Response**: Updated product object is returned

### Validation Rules

- **Product ID**: Required, must exist in database
- **Category ID**: Required, must exist in database
- **Both IDs**: Must be valid integers

### Security Features

1. **Role-Based Access**: Only managers and admins can update product categories
2. **Input Validation**: All inputs are validated and sanitized
3. **Existence Checks**: Product and category must exist before update
4. **Referential Integrity**: Maintains database relationships
5. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

### Data Processing

- **Atomic Update**: Category update is atomic and transactional
- **Category Migration**: Products can be moved between categories
- **Inventory Impact**: Category changes affect product organization
- **Audit Trail**: Consider logging category changes for tracking

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

# Test manager updates product category
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "product_id": 1,
    "category_id": 2
  }'

# Test admin updates product category
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "product_id": 2,
    "category_id": 1
  }'

# Test product not found
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "product_id": 999,
    "category_id": 1
  }'

# Test category not found
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "product_id": 1,
    "category_id": 999
  }'

# Test invalid product ID type
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "product_id": "invalid",
    "category_id": 1
  }'

# Test unauthorized access (staff)
curl -X PATCH "http://127.0.0.1:5001/product/update_category" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{
    "product_id": 1,
    "category_id": 2
  }'
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

def test_update_product_category():
    # Get tokens for different roles
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    
    print("=== Testing Manager Category Update ===")
    
    # Test manager updates product category
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    update_data = {
        "product_id": 1,
        "category_id": 2
    }
    response = requests.patch(f"{base_url}/product/update_category", json=update_data, headers=manager_headers)
    print(f"Manager Update: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Admin Category Update ===")
    
    # Test admin updates product category
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    update_data = {
        "product_id": 2,
        "category_id": 1
    }
    response = requests.patch(f"{base_url}/product/update_category", json=update_data, headers=admin_headers)
    print(f"Admin Update: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Product Not Found ===")
    
    # Test product not found
    update_data = {
        "product_id": 999,
        "category_id": 1
    }
    response = requests.patch(f"{base_url}/product/update_category", json=update_data, headers=manager_headers)
    print(f"Product Not Found: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Category Not Found ===")
    
    # Test category not found
    update_data = {
        "product_id": 1,
        "category_id": 999
    }
    response = requests.patch(f"{base_url}/product/update_category", json=update_data, headers=manager_headers)
    print(f"Category Not Found: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Invalid Product ID Type ===")
    
    # Test invalid product ID type
    update_data = {
        "product_id": "invalid",
        "category_id": 1
    }
    response = requests.patch(f"{base_url}/product/update_category", json=update_data, headers=manager_headers)
    print(f"Invalid ID Type: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Unauthorized Access ===")
    
    # Test staff unauthorized access
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    update_data = {
        "product_id": 1,
        "category_id": 2
    }
    response = requests.patch(f"{base_url}/product/update_category", json=update_data, headers=staff_headers)
    print(f"Staff Unauthorized: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_update_product_category()
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

4. **Product Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "product with id 999 not found"
     }
   }
   ```

5. **Category Not Found**
   ```json
   {
     "status": "error",
     "message": {
       "response": "Cannot find category with id: 999"
     }
   }
   ```

6. **Invalid Product ID Type**
   ```json
   {
     "detail": "product_id should be type int but got type: str"
   }
   ```

7. **Invalid Category ID Type**
   ```json
   {
     "detail": "category_id should be type int but got type: str"
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Category updated successfully    |
| 200         | Product not found (error status) |
| 200         | Category not found (error status)|
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /products**: Get products (with filtering)
- **POST /products**: Create new product (manager/admin only)
- **PUT /product**: Update existing product (manager/admin only)
- **DELETE /product**: Delete product (admin only)

---

## 📝 Notes

- Only managers and admins can update product categories
- Both product and category must exist before update can proceed
- This is a partial update - only the category_id field is changed
- The endpoint returns the complete updated product object for confirmation
- Category updates are atomic - either fully succeed or fail completely
- Consider implementing bulk category updates for efficiency
- Category changes affect product organization and filtering
- This endpoint is useful for product reorganization and inventory management
- The response includes the current user's email for audit purposes
- Consider logging category changes for tracking and analytics
- Product category updates do not affect other product attributes
- The operation maintains referential integrity in the database
