# Update Product API Documentation

## 📋 Overview

The Update Product API allows authenticated users with manager or admin roles to update existing products in the inventory system. This endpoint validates the authentication token, checks user permissions, validates product data, and updates product records in the database.

**Endpoint:** `PUT /product`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Manager/Admin only)

---

## 🔐 API Endpoints

### PUT /product

Updates an existing product in the inventory system.

**URL:** `PUT /product`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Body

| Parameter    | Type    | Required | Description                    | Constraints                      |
|--------------|---------|----------|--------------------------------|-----------------------------------|
| id           | integer | Yes      | Product ID to update            | Must exist in database           |
| name         | string  | Yes      | Updated product name            | Max 100 characters              |
| quantity     | integer | Yes      | Updated product quantity        | Positive integer                |
| price        | float   | Yes      | Updated product price           | Positive float                  |
| category_id  | integer | Yes      | Updated category ID             | Must exist in database          |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Update product:**
```bash
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 1,
    "name": "Updated Laptop",
    "quantity": 15,
    "price": 1099.99,
    "category_id": 1
  }'
```

**Update product as admin:**
```bash
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "id": 2,
    "name": "Premium Mouse",
    "quantity": 30,
    "price": 39.99,
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
      "name": "Updated Laptop",
      "quantity": 15,
      "price": 1099.99,
      "price_type": "regular",
      "category_id": 1
    }
  }
}
```

**Success Response (200 OK) - With Price Adjustment:**
```json
{
  "status": "success",
  "message": {
    "user email": "admin@example.com",
    "updated product": {
      "id": 2,
      "name": "Premium Mouse",
      "quantity": 30,
      "price": 31.992,
      "price_type": "discounted",
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

**Error Response (400 Bad Request) - Category not found:**
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

#### Response Fields

| Field             | Type     | Description                                    |
|-------------------|----------|------------------------------------------------|
| status            | string   | Response status ("success" or "error")         |
| message           | object   | Contains user email and product data          |
| user email        | string   | Email of the authenticated user making request |
| updated product   | object   | Complete updated product object               |
| id                | integer  | Unique product identifier                     |
| name              | string   | Updated product name                           |
| quantity          | integer  | Updated product quantity in stock             |
| price             | float    | Updated product price (may be adjusted)       |
| price_type        | string   | Price type ("regular", "taxed", "discounted")  |
| category_id       | integer  | Updated category ID                            |

---

## 🚀 Usage Examples

### 1. Manager Updates Product

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "id": 1,
    "name": "Gaming Laptop Pro",
    "quantity": 12,
    "price": 1299.99,
    "category_id": 1
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
      "name": "Gaming Laptop Pro",
      "quantity": 12,
      "price": 1299.99,
      "price_type": "regular",
      "category_id": 1
    }
  }
}
```

### 2. Admin Updates Product with Price Adjustment

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "id": 2,
    "name": "Wireless Mouse Elite",
    "quantity": 35,
    "price": 49.99,
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
      "id": 2,
      "name": "Wireless Mouse Elite",
      "quantity": 35,
      "price": 59.988,
      "price_type": "taxed",
      "category_id": 1
    }
  }
}
```

### 3. Product Not Found

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 999,
    "name": "Nonexistent Product",
    "quantity": 10,
    "price": 29.99,
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
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "id": 1,
    "name": "Updated Product",
    "quantity": 20,
    "price": 39.99,
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

### 5. Staff User Attempts Update (Unauthorized)

**Request:**
```bash
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "id": 1,
    "name": "Should Not Work",
    "quantity": 10,
    "price": 19.99,
    "category_id": 1
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
3. **Input Validation**: Pydantic schema validates product data
4. **Product Lookup**: Target product is found in database by ID
5. **Category Validation**: Ensures new category exists
6. **Price Processing**: Applies tax or discount based on product ID
7. **Product Update**: Product fields are updated and saved
8. **Database Commit**: Transaction is committed to persist changes
9. **Response**: Updated product object is returned

### Price Adjustment Logic

- **Even Product ID**: 20% tax applied, price_type = "taxed"
- **Odd Product ID**: 20% discount applied, price_type = "discounted"
- **Price adjustments are applied during updates based on the product's ID**

### Validation Rules

- **ID**: Required, must exist in database
- **Name**: Required, max 100 characters
- **Quantity**: Required, positive integer
- **Price**: Required, positive float
- **Category ID**: Required, must exist in database

### Security Features

1. **Role-Based Access**: Only managers and admins can update products
2. **Input Validation**: All inputs are validated and sanitized
3. **Existence Checks**: Product and category must exist before update
4. **Referential Integrity**: Maintains database relationships
5. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

### Data Processing

- **Atomic Update**: Update operation is atomic and transactional
- **Price Calculation**: Automatic price adjustments based on business rules
- **Category Migration**: Products can be moved between categories
- **Inventory Tracking**: Quantity updates affect stock levels

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

# Test manager updates product
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "id": 1,
    "name": "Manager Updated Product",
    "quantity": 20,
    "price": 89.99,
    "category_id": 1
  }'

# Test admin updates product (price adjustment)
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "id": 2,
    "name": "Admin Updated Product",
    "quantity": 25,
    "price": 99.99,
    "category_id": 1
  }'

# Test product not found
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "id": 999,
    "name": "Nonexistent",
    "quantity": 10,
    "price": 29.99,
    "category_id": 1
  }'

# Test category not found
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "id": 1,
    "name": "Invalid Category",
    "quantity": 15,
    "price": 39.99,
    "category_id": 999
  }'

# Test unauthorized access (staff)
curl -X PUT "http://127.0.0.1:5001/product" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{
    "id": 1,
    "name": "Unauthorized Update",
    "quantity": 5,
    "price": 19.99,
    "category_id": 1
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

def test_update_product():
    # Get tokens for different roles
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    
    print("=== Testing Manager Update ===")
    
    # Test manager updates product
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    product_data = {
        "id": 1,
        "name": "Manager Updated Product",
        "quantity": 20,
        "price": 89.99,
        "category_id": 1
    }
    response = requests.put(f"{base_url}/product", json=product_data, headers=manager_headers)
    print(f"Manager Update: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Admin Update (price adjustment) ===")
    
    # Test admin updates product
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    product_data = {
        "id": 2,
        "name": "Admin Updated Product",
        "quantity": 25,
        "price": 99.99,
        "category_id": 1
    }
    response = requests.put(f"{base_url}/product", json=product_data, headers=admin_headers)
    print(f"Admin Update: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Product Not Found ===")
    
    # Test product not found
    product_data = {
        "id": 999,
        "name": "Nonexistent Product",
        "quantity": 10,
        "price": 29.99,
        "category_id": 1
    }
    response = requests.put(f"{base_url}/product", json=product_data, headers=manager_headers)
    print(f"Not Found: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Category Not Found ===")
    
    # Test category not found
    product_data = {
        "id": 1,
        "name": "Invalid Category Product",
        "quantity": 15,
        "price": 39.99,
        "category_id": 999
    }
    response = requests.put(f"{base_url}/product", json=product_data, headers=manager_headers)
    print(f"Invalid Category: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Unauthorized Access ===")
    
    # Test staff unauthorized access
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    product_data = {
        "id": 1,
        "name": "Unauthorized Update",
        "quantity": 5,
        "price": 19.99,
        "category_id": 1
    }
    response = requests.put(f"{base_url}/product", json=product_data, headers=staff_headers)
    print(f"Staff Unauthorized: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_update_product()
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

6. **Invalid Quantity**
   ```json
   {
     "detail": [
       {
         "type": "value_error",
         "loc": ["body", "quantity"],
         "msg": "Input should be greater than 0",
         "input": -5
       }
     ]
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Product updated successfully     |
| 200         | Product not found (error status) |
| 200         | Category not found (error status)|
| 400         | Bad request (invalid data)        |
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /products**: Get products (with filtering)
- **POST /products**: Create new product (manager/admin only)
- **DELETE /product**: Delete product (admin only)
- **PATCH /product/update_category**: Update product category (manager/admin only)

---

## 📝 Notes

- Only managers and admins can update products
- All product fields must be provided in the update request
- Price adjustments are automatically applied based on product ID:
  - Even IDs: 20% tax added
  - Odd IDs: 20% discount applied
- Product must exist before it can be updated
- Category must exist before product can be assigned to it
- Quantity must be a positive integer
- Price must be a positive float
- The endpoint returns the complete updated product object for confirmation
- Product updates are atomic - either fully succeed or fail completely
- Consider implementing partial updates for better user experience
- Price type indicates if special pricing was applied during update
- Inventory management should track quantity changes over time
