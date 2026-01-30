# Create Product API Documentation

## 📋 Overview

The Create Product API allows authenticated users with manager or admin roles to create new products in the inventory system. This endpoint validates the authentication token, checks user permissions, validates product data, and creates new product records in the database.

**Endpoint:** `POST /products`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token - Manager/Admin only)

---

## 🔐 API Endpoints

### POST /products

Creates a new product in the inventory system.

**URL:** `POST /products`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Request Body

| Parameter    | Type    | Required | Description                    | Constraints                      |
|--------------|---------|----------|--------------------------------|-----------------------------------|
| id           | integer | No       | Product ID (optional)           | Unique if provided               |
| name         | string  | Yes      | Product name                    | Max 100 characters              |
| quantity     | integer | Yes      | Product quantity                | Positive integer                |
| price        | float   | Yes      | Product price                   | Positive float                  |
| category_id  | integer | Yes      | Associated category ID          | Must exist in database          |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Create product without ID:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "name": "Wireless Mouse",
    "quantity": 50,
    "price": 29.99,
    "category_id": 1
  }'
```

**Create product with ID:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "id": 15,
    "name": "Gaming Keyboard",
    "quantity": 25,
    "price": 89.99,
    "category_id": 1
  }'
```

**Create product as admin:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "name": "USB-C Hub",
    "quantity": 30,
    "price": 45.99,
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
    "inserted product": {
      "id": 5,
      "name": "Wireless Mouse",
      "quantity": 50,
      "price": 29.99,
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
    "inserted product": {
      "id": 16,
      "name": "Gaming Keyboard",
      "quantity": 25,
      "price": 71.992,
      "price_type": "discounted",
      "category_id": 1
    }
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

**Error Response (400 Bad Request) - Duplicate product name:**
```json
{
  "detail": {
    "message": "product with name Wireless Mouse already exists"
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
| inserted product  | object   | Complete product object that was created      |
| id                | integer  | Unique product identifier                     |
| name              | string   | Product name                                   |
| quantity          | integer  | Product quantity in stock                     |
| price             | float    | Product price (may be adjusted)               |
| price_type        | string   | Price type ("regular", "taxed", "discounted")  |
| category_id       | integer  | Associated category ID                         |

---

## 🚀 Usage Examples

### 1. Manager Creates Product

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature" \
  -d '{
    "name": "Bluetooth Headphones",
    "quantity": 40,
    "price": 79.99,
    "category_id": 1
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "bob.wilson@example.com",
    "inserted product": {
      "id": 6,
      "name": "Bluetooth Headphones",
      "quantity": 40,
      "price": 79.99,
      "price_type": "regular",
      "category_id": 1
    }
  }
}
```

### 2. Admin Creates Product with ID and Price Adjustment

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
    "id": 20,
    "name": "Monitor Stand",
    "quantity": 15,
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
    "inserted product": {
      "id": 20,
      "name": "Monitor Stand",
      "quantity": 15,
      "price": 59.988,
      "price_type": "taxed",
      "category_id": 1
    }
  }
}
```

### 3. Staff User Attempts Creation (Unauthorized)

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFmZkBleGFtcGxlLmNvbSIsInJvbGUiOiJzdGFmZiIsImV4cCI6MTcwNTI0MjQwMH0.signature" \
  -d '{
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

### 4. Category Not Found

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "name": "Test Product",
    "quantity": 10,
    "price": 29.99,
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

### 5. Duplicate Product Name

**Request:**
```bash
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MANAGER_JWT_TOKEN_HERE" \
  -d '{
    "name": "Bluetooth Headphones",
    "quantity": 20,
    "price": 69.99,
    "category_id": 1
  }'
```

**Response:**
```json
{
  "detail": {
    "message": "product with name Bluetooth Headphones already exists"
  }
}
```

---

## 🔧 Implementation Details

### Creation Process

1. **Token Validation**: JWT token is decoded and validated
2. **Role Verification**: User role is checked (must be manager or admin)
3. **Input Validation**: Pydantic schema validates product data
4. **Duplicate Checks**: Database queries check for existing product name and ID
5. **Category Validation**: Ensures category exists before product creation
6. **Price Processing**: Applies tax or discount if ID is provided
7. **Product Creation**: New product record is created and saved
8. **Database Commit**: Transaction is committed to persist the product
9. **Response**: Created product object is returned

### Price Adjustment Logic

- **No ID Provided**: Price remains unchanged, price_type = "regular"
- **Even ID**: 20% tax applied, price_type = "taxed"
- **Odd ID**: 20% discount applied, price_type = "discounted"

### Validation Rules

- **Name**: Required, max 100 characters, unique across system
- **Quantity**: Required, positive integer
- **Price**: Required, positive float
- **Category ID**: Required, must exist in database
- **ID**: Optional, must be unique if provided

### Security Features

1. **Role-Based Access**: Only managers and admins can create products
2. **Input Validation**: All inputs are validated and sanitized
3. **Duplicate Prevention**: Database constraints prevent duplicates
4. **Category Validation**: Ensures referential integrity
5. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

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

# Test manager creates product
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "name": "Test Product Manager",
    "quantity": 25,
    "price": 39.99,
    "category_id": 1
  }'

# Test admin creates product with ID (price adjustment)
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "id": 100,
    "name": "Test Product Admin",
    "quantity": 15,
    "price": 59.99,
    "category_id": 1
  }'

# Test category not found
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "name": "Invalid Category",
    "quantity": 10,
    "price": 29.99,
    "category_id": 999
  }'

# Test duplicate name
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -d '{
    "name": "Test Product Manager",
    "quantity": 20,
    "price": 34.99,
    "category_id": 1
  }'

# Test unauthorized access (staff)
curl -X POST "http://127.0.0.1:5001/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{
    "name": "Unauthorized Product",
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

def test_create_product():
    # Get tokens for different roles
    manager_token = get_auth_token("manager@example.com", "ManagerPass456@")
    admin_token = get_auth_token("admin@example.com", "AdminPass789#")
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    
    print("=== Testing Manager Creation ===")
    
    # Test manager creates product
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    product_data = {
        "name": "Manager Test Product",
        "quantity": 25,
        "price": 39.99,
        "category_id": 1
    }
    response = requests.post(f"{base_url}/products", json=product_data, headers=manager_headers)
    print(f"Manager Creation: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Admin Creation (with price adjustment) ===")
    
    # Test admin creates product with ID
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    product_data = {
        "id": 50,
        "name": "Admin Test Product",
        "quantity": 15,
        "price": 59.99,
        "category_id": 1
    }
    response = requests.post(f"{base_url}/products", json=product_data, headers=admin_headers)
    print(f"Admin Creation: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Category Not Found ===")
    
    # Test category not found
    product_data = {
        "name": "Invalid Category Product",
        "quantity": 10,
        "price": 29.99,
        "category_id": 999
    }
    response = requests.post(f"{base_url}/products", json=product_data, headers=manager_headers)
    print(f"Invalid Category: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Duplicate Name ===")
    
    # Test duplicate name
    product_data = {
        "name": "Manager Test Product",
        "quantity": 20,
        "price": 34.99,
        "category_id": 1
    }
    response = requests.post(f"{base_url}/products", json=product_data, headers=manager_headers)
    print(f"Duplicate Name: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing Unauthorized Access ===")
    
    # Test staff unauthorized access
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    product_data = {
        "name": "Unauthorized Product",
        "quantity": 5,
        "price": 19.99,
        "category_id": 1
    }
    response = requests.post(f"{base_url}/products", json=product_data, headers=staff_headers)
    print(f"Staff Unauthorized: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_create_product()
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
       "response": "Cannot find category with id: 999"
     }
   }
   ```

5. **Duplicate Product Name**
   ```json
   {
     "detail": {
       "message": "product with name Test Product already exists"
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
| 200         | Product created successfully     |
| 400         | Bad request (invalid data)        |
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid input) |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **GET /products**: Get products (with filtering)
- **PUT /product**: Update existing product (manager/admin only)
- **DELETE /product**: Delete product (admin only)
- **PATCH /product/update_category**: Update product category (manager/admin only)

---

## 📝 Notes

- Only managers and admins can create products
- Product names must be unique across the entire system
- Product IDs are auto-generated if not provided
- Price adjustments are applied when ID is explicitly provided:
  - Even IDs: 20% tax added
  - Odd IDs: 20% discount applied
- Category must exist before product can be created
- Quantity must be a positive integer
- Price must be a positive float
- The endpoint returns the complete created product object for confirmation
- Price type indicates if special pricing was applied
- Consider implementing inventory validation for negative quantities
- Product creation is atomic - either fully succeeds or fails completely
