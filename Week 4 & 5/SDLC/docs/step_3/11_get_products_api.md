# Get Products API Documentation

## 📋 Overview

The Get Products API retrieves product information from the system with flexible filtering options. This endpoint requires authentication and is accessible to users with staff, manager, or admin roles. It supports filtering by specific product ID or category ID.

**Endpoint:** `GET /products`  
**Base URL:** `http://127.0.0.1:5001`  
**Authentication:** Required (JWT Bearer Token)

---

## 🔐 API Endpoints

### GET /products

Retrieves products with optional filtering by product ID or category ID.

**URL:** `GET /products?product_id={product_id}&category_id={category_id}`  
**Content-Type:** `application/json`  
**Authentication:** `Bearer {JWT_TOKEN}`

#### Query Parameters

| Parameter    | Type    | Required | Description                    | Values                           |
|--------------|---------|----------|--------------------------------|-----------------------------------|
| product_id   | integer | No       | Filter by specific product ID   | Valid product ID                 |
| category_id  | integer | No       | Filter by category ID           | Valid category ID                |

#### Request Headers

| Header          | Type   | Required | Description                    |
|-----------------|--------|----------|--------------------------------|
| Authorization   | string | Yes      | Bearer token for authentication |

#### Request Examples

**Get all products:**
```bash
curl -X GET "http://127.0.0.1:5001/products" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Get specific product by ID:**
```bash
curl -X GET "http://127.0.0.1:5001/products?product_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Get products by category:**
```bash
curl -X GET "http://127.0.0.1:5001/products?category_id=2" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Get products by category as staff:**
```bash
curl -X GET "http://127.0.0.1:5001/products?category_id=3" \
  -H "Authorization: Bearer STAFF_JWT_TOKEN_HERE"
```

#### Response

**Success Response (200 OK) - All Products:**
```json
{
  "status": "success",
  "message": {
    "user email": "alice.johnson@example.com",
    "products": [
      {
        "id": 1,
        "name": "Laptop",
        "quantity": 10,
        "price": 999.99,
        "price_type": "regular",
        "category_id": 1
      },
      {
        "id": 2,
        "name": "Mouse",
        "quantity": 25,
        "price": 29.99,
        "price_type": "discounted",
        "category_id": 1
      },
      {
        "id": 3,
        "name": "T-Shirt",
        "quantity": 50,
        "price": 19.99,
        "price_type": "taxed",
        "category_id": 2
      }
    ]
  }
}
```

**Success Response (200 OK) - Specific Product:**
```json
{
  "status": "success",
  "message": {
    "user_email": "alice.johnson@example.com",
    "product": {
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

**Success Response (200 OK) - Products by Category:**
```json
{
  "status": "success",
  "message": {
    "user_email": "alice.johnson@example.com",
    "products with category id: 1": [
      {
        "id": 1,
        "name": "Laptop",
        "quantity": 10,
        "price": 999.99,
        "price_type": "regular",
        "category_id": 1
      },
      {
        "id": 2,
        "name": "Mouse",
        "quantity": 25,
        "price": 29.99,
        "price_type": "discounted",
        "category_id": 1
      }
    ]
  }
}
```

**Error Response (200 OK) - Product Not Found:**
```json
{
  "status": "error",
  "message": {
    "response": "product with id 999 not found"
  }
}
```

**Error Response (401 Unauthorized)**
```json
{
  "detail": "Unauthorized to perform action, you are a unauthorized_role"
}
```

#### Response Fields

| Field                           | Type     | Description                                    |
|---------------------------------|----------|------------------------------------------------|
| status                          | string   | Response status ("success" or "error")         |
| message                         | object   | Contains user email and product data           |
| user email / user_email         | string   | Email of the authenticated user making request |
| products / product              | array/object | Product data (varies by query type)       |
| id                              | integer  | Unique product identifier                     |
| name                            | string   | Product name                                   |
| quantity                        | integer  | Product quantity in stock                     |
| price                           | float    | Product price                                  |
| price_type                      | string   | Price type ("regular", "taxed", "discounted")  |
| category_id                     | integer  | Associated category ID                         |

---

## 🚀 Usage Examples

### 1. Staff User Gets All Products

**Request:**
```bash
# First login as staff user
curl -X POST "http://127.0.0.1:5001/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.johnson@example.com",
    "password": "StaffPass123!"
  }'

# Use the token to get all products
curl -X GET "http://127.0.0.1:5001/products" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZS5qb2huc29uQGV4YW1wbGUuY29tIiwicm9sZSI6InN0YWZmIiwiZXhwIjoxNzA1MjQyNDAwfQ.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user email": "alice.johnson@example.com",
    "products": [
      {
        "id": 1,
        "name": "Laptop",
        "quantity": 10,
        "price": 999.99,
        "price_type": "regular",
        "category_id": 1
      },
      {
        "id": 2,
        "name": "Mouse",
        "quantity": 25,
        "price": 29.99,
        "price_type": "discounted",
        "category_id": 1
      }
    ]
  }
}
```

### 2. Manager User Gets Specific Product

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/products?product_id=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MDUyNDI0MDB9.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user_email": "bob.wilson@example.com",
    "product": {
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

### 3. Admin User Gets Products by Category

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/products?category_id=2" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTI0MjQwMH0.signature"
```

**Response:**
```json
{
  "status": "success",
  "message": {
    "user_email": "admin@example.com",
    "products with category id: 2": [
      {
        "id": 3,
        "name": "T-Shirt",
        "quantity": 50,
        "price": 19.99,
        "price_type": "taxed",
        "category_id": 2
      },
      {
        "id": 4,
        "name": "Jeans",
        "quantity": 30,
        "price": 49.99,
        "price_type": "regular",
        "category_id": 2
      }
    ]
  }
}
```

### 4. Product Not Found

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/products?product_id=999" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
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

### 5. Invalid Product ID Type

**Request:**
```bash
curl -X GET "http://127.0.0.1:5001/products?product_id=invalid" \
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
3. **User Identification**: Current user's email is extracted from token
4. **Query Processing**: Determines retrieval strategy based on parameters:
   - No parameters: Get all products
   - product_id only: Get specific product
   - category_id only: Get products by category
5. **Database Query**: Products are retrieved using SQLAlchemy ORM
6. **Response Construction**: Product data is formatted with user context

### Query Logic

- **All Products**: Returns all products in the system
- **Specific Product**: Returns single product object or error if not found
- **By Category**: Returns array of products in specified category
- **Parameter Priority**: product_id takes precedence over category_id if both provided

### Role-Based Access Control

The following roles can access this endpoint:
- **staff**: Read-only access to view products
- **manager**: Read-only access to view products
- **admin**: Read-only access to view products

### Data Processing

- **Price Types**: Products may have "regular", "taxed", or "discounted" prices
- **Category Filtering**: Uses foreign key relationship for efficient queries
- **Error Handling**: Consistent error responses for missing data
- **Response Format**: Varies based on query type (all vs specific vs filtered)

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

# Test get all products
curl -X GET "http://127.0.0.1:5001/products" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test get specific product
curl -X GET "http://127.0.0.1:5001/products?product_id=1" \
  -H "Authorization: Bearer $MANAGER_TOKEN"

# Test get products by category
curl -X GET "http://127.0.0.1:5001/products?category_id=2" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test product not found
curl -X GET "http://127.0.0.1:5001/products?product_id=999" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test invalid ID type
curl -X GET "http://127.0.0.1:5001/products?product_id=invalid" \
  -H "Authorization: Bearer $STAFF_TOKEN"

# Test without token (should fail)
curl -X GET "http://127.0.0.1:5001/products"

# Test with invalid token (should fail)
curl -X GET "http://127.0.0.1:5001/products" \
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

def test_get_products():
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
        
        # Test get all products
        response = requests.get(f"{base_url}/products", headers=headers)
        print(f"All Products: {json.dumps(response.json(), indent=2)}")
        
        # Test get specific product
        response = requests.get(f"{base_url}/products?product_id=1", headers=headers)
        print(f"Specific Product: {json.dumps(response.json(), indent=2)}")
        
        # Test get products by category
        response = requests.get(f"{base_url}/products?category_id=2", headers=headers)
        print(f"Products by Category: {json.dumps(response.json(), indent=2)}")
    
    # Test error cases
    print("\n=== Testing Error Cases ===")
    
    staff_token = get_auth_token("staff@example.com", "StaffPass123!")
    headers = {"Authorization": f"Bearer {staff_token}"}
    
    # Test product not found
    response = requests.get(f"{base_url}/products?product_id=999", headers=headers)
    print(f"Product Not Found: {json.dumps(response.json(), indent=2)}")
    
    # Test invalid ID type
    response = requests.get(f"{base_url}/products?product_id=invalid", headers=headers)
    print(f"Invalid ID Type: {json.dumps(response.json(), indent=2)}")
    
    # Test without authentication
    response = requests.get(f"{base_url}/products")
    print(f"No Authentication: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_get_products()
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

3. **Invalid Product ID Type**
   ```json
   {
     "detail": "id should be type int but got type: str"
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

5. **Unauthorized Role**
   ```json
   {
     "detail": "Unauthorized to perform action, you are a unauthorized_role"
   }
   ```

### Error Response Codes

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Products retrieved successfully  |
| 200         | Product not found (error status) |
| 401         | Unauthorized / Invalid token     |
| 422         | Validation error (invalid ID)    |
| 500         | Internal server error           |

---

## 🔄 Related Endpoints

- **POST /products**: Create new product (manager/admin only)
- **PUT /product**: Update existing product (manager/admin only)
- **DELETE /product**: Delete product (admin only)
- **PATCH /product/update_category**: Update product category (manager/admin only)

---

## 📝 Notes

- All authenticated users (staff, manager, admin) can view products
- The endpoint supports flexible filtering with multiple query options
- Product prices may be adjusted based on business logic (taxed, discounted)
- Category filtering uses the foreign key relationship for efficient queries
- Empty product lists return an empty array rather than null
- The response includes the current user's email for context
- Consider implementing pagination for large product catalogs
- Product data includes quantity information for inventory management
- Price type indicates if special pricing has been applied
- The endpoint is useful for building product catalogs and inventory views
