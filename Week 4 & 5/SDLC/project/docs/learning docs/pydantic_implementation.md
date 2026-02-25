# Pydantic Implementation in Inventory Manager

## Overview
Pydantic is a data validation library that uses Python type annotations to validate data and settings. This project extensively uses Pydantic for configuration management, API request/response validation, and ensuring data integrity.

## Why Pydantic?
- **Automatic Validation**: Data is validated automatically using Python type hints
- **Type Safety**: Catches type errors before runtime
- **Environment Variables**: Easy management of configuration from `.env` files
- **Clear Errors**: Provides detailed error messages when validation fails
- **FastAPI Integration**: Works seamlessly with FastAPI for API development

---

## Implementation Areas

### 1. Configuration Management (BaseSettings)

**Purpose**: Load and validate environment variables from `.env` files

**Files**:
- `src/core/config.py` - Application configuration
- `src/core/log.py` - Logging configuration

#### Example: Settings Class (`config.py:16`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    postgresql_pwd: str = Field(validation_alias=AliasChoices("POSTGRESQL_PWD", "db_password"))
    db_host: str = Field(default="localhost")

    # JWT
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuration
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()  # Automatically loads from .env
```

**Features Used**:
- `Field()` with `validation_alias` - allows multiple env variable names
- `default` values - fallback if not in .env
- `SettingsConfigDict` - configures where to load env vars from
- Type annotations - ensures correct data types (str, int, etc.)

#### Example: Log Settings (`log.py:22`)

```python
class LogSettings(BaseSettings, metaclass=Singleton):
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8"
    )
```

**What it does**:
1. Reads `LOG_LEVEL` from `.env` file
2. Validates it's a valid `LogLevel` enum value
3. Defaults to `INFO` if not specified
4. Ensures only one instance exists (Singleton pattern)

---

### 2. Request/Response Schemas (BaseModel)

**Purpose**: Validate incoming API requests and structure responses

**Files**:
- `src/schema/user.py` - User-related schemas
- `src/schema/product.py` - Product-related schemas
- `src/schema/category.py` - Category-related schemas
- `src/schema/token.py` - JWT token schemas

#### User Schemas (`schema/user.py`)

**BaseUser** - Base schema with common fields
```python
class BaseUser(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str
    role: UserRole
```

**UserRegister** - For user registration with password validation
```python
class UserRegister(BaseUser):
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, pwd: str) -> str:
        return validate_password(password=pwd)
```

**UserLogin** - For login (only email and password)
```python
class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

**UserResponse** - For API responses (hides password hash)
```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
```

#### Product Schemas (`schema/product.py`)

**ProductCreate** - Creating new products
```python
class ProductCreate(BaseModel):
    id: Optional[int] = None
    name: str
    quantity: PositiveInt  # Must be positive
    price: PositiveFloat   # Must be positive
    category_id: int
```

**ProductUpdate** - Updating existing products (all optional)
```python
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    quantity: Optional[PositiveInt] = None
    price: Optional[PositiveFloat] = None
    category_id: Optional[int] = None
```

#### Category Schemas (`schema/category.py`)

```python
class CategoryCreate(BaseModel):
    id: Optional[int] = None
    name: str

class CategoryRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
```

#### Token Schemas (`schema/token.py`)

```python
class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "JWT"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
```

---

### 3. Field Validation

Pydantic provides multiple validation methods:

#### Built-in Validators

```python
from pydantic import EmailStr, PositiveInt, PositiveFloat, Field

# Email validation
email: EmailStr  # Automatically validates email format

# Positive numbers
quantity: PositiveInt  # Must be > 0
price: PositiveFloat   # Must be > 0.0

# String length constraints
name: str = Field(min_length=5, max_length=100)
```

#### Custom Validators

```python
@field_validator("password")
@classmethod
def validate_password_strength(cls, pwd: str) -> str:
    pwd_strength = check_password_strength(password=pwd)
    if not pwd_strength:
        raise WeakPasswordException(message="Password too weak")
    return pwd
```

**What it does**:
1. Runs automatically when the model is instantiated
2. Checks password meets requirements (digit, uppercase, lowercase, special char)
3. Raises exception if validation fails
4. Returns validated value if successful

---

### 4. SQLAlchemy Integration

**Purpose**: Convert SQLAlchemy ORM objects to Pydantic models

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
```

**`from_attributes=True`** allows:
```python
# Convert database object to Pydantic model
db_user = db.query(User).first()
user_response = UserResponse.from_orm(db_user)
```

Used in:
- `UserResponse` (`user.py:120`)
- `ProductResponse` (`product.py:58`)
- `CategoryRead` (`category.py:49`)

---

## Key Pydantic Features Used

### 1. Type Annotations
```python
name: str              # Must be string
quantity: int          # Must be integer
email: EmailStr        # Must be valid email
price: PositiveFloat   # Must be positive float
```

### 2. Optional Fields
```python
id: Optional[int] = None  # Can be None or int
new_password: Optional[str] = None  # Optional field
```

### 3. Field Constraints
```python
name: str = Field(min_length=5, max_length=100)  # Length constraints
quantity: PositiveInt                            # Must be positive
```

### 4. Validation Aliases
```python
postgresql_pwd: str = Field(
    validation_alias=AliasChoices("POSTGRESQL_PWD", "db_password")
)
```
Accepts either `POSTGRESQL_PWD` or `db_password` from environment.

### 5. ConfigDict
```python
model_config = ConfigDict(from_attributes=True)
```
Configuration for model behavior.

---

## Advantages in This Project

### 1. **Data Integrity**
- All data is validated before processing
- Prevents invalid data from entering the database
- Catches errors early in the request lifecycle

### 2. **Type Safety**
- Type hints provide IDE autocomplete
- Catches type errors during development
- Makes code more maintainable

### 3. **Automatic Documentation**
- FastAPI uses Pydantic models to generate API docs
- Request/response examples in Swagger UI
- Clear API contracts

### 4. **Environment Management**
- Easy configuration through `.env` files
- Type-safe environment variables
- No need to manually parse env vars

### 5. **Clear Error Messages**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 6. **Code Reusability**
- Base schemas can be extended (inheritance)
- Common validation logic in one place
- DRY (Don't Repeat Yourself) principle

### 7. **Security**
- Hide sensitive fields in responses (password hash)
- Validate input before processing
- Prevent injection attacks through type validation

---

## Project Structure

```
src/
├── core/
│   ├── config.py          # BaseSettings - app configuration
│   └── log.py             # BaseSettings - logging configuration
│
├── schema/
│   ├── user.py            # BaseModel - user schemas
│   ├── product.py         # BaseModel - product schemas
│   ├── category.py        # BaseModel - category schemas
│   └── token.py           # BaseModel - token schemas
│
└── repository/
    └── database.py        # Uses BaseModel for type hints
```

---

## Usage Flow

### 1. Configuration Startup
```python
# App starts → loads settings from .env
settings = Settings()  # Reads and validates env vars
```

### 2. API Request
```python
@router.post("/users/register")
async def register(user: UserRegister):  # Pydantic validates input
    # user.name, user.email, user.password are validated
    # Password strength is checked automatically
```

### 3. Database Response
```python
# Get user from database
db_user = await get_user(email)

# Convert to Pydantic model
user_response = UserResponse.from_orm(db_user)  # Hides password hash
return user_response
```

---

## Best Practices Observed

### 1. Separate Schemas for Different Operations
- `UserRegister` - for registration (validates password)
- `UserLogin` - for login (minimal fields)
- `UserEdit` - for updates (optional fields)
- `UserResponse` - for responses (hides password)

### 2. Use Enums for Fixed Choices
```python
class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
```

### 3. BaseSettings with Singleton
```python
class Settings(BaseSettings, metaclass=Singleton):
    # Ensures only one instance of settings exists
```

### 4. Clear Naming Conventions
- `Base*` - Base schemas
- `*Create` - Creating new resources
- `*Update` - Updating resources
- `*Response` - API responses
- `*Read` - Reading/serializing data

### 5. Type Hints Everywhere
- All fields have type annotations
- Optional fields explicitly marked
- Improves code readability

---

## Common Patterns

### Pattern 1: Create Schema
```python
class ProductCreate(BaseModel):
    name: str
    quantity: PositiveInt
    price: PositiveFloat
    category_id: int
```
**Use**: Creating new resources via POST requests

### Pattern 2: Update Schema
```python
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[PositiveInt] = None
    price: Optional[PositiveFloat] = None
```
**Use**: Updating resources via PUT/PATCH (all fields optional)

### Pattern 3: Response Schema
```python
class ProductResponse(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)
```
**Use**: API responses, converts ORM objects

### Pattern 4: Settings Schema
```python
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")
```
**Use**: Configuration from environment variables

---

## Quick Reference

| Use Case | Class | File Location |
|----------|-------|---------------|
| App settings | `Settings` | `core/config.py:16` |
| Log settings | `LogSettings` | `core/log.py:22` |
| User registration | `UserRegister` | `schema/user.py:72` |
| User login | `UserLogin` | `schema/user.py:83` |
| User response | `UserResponse` | `schema/user.py:110` |
| Product creation | `ProductCreate` | `schema/product.py:27` |
| Product update | `ProductUpdate` | `schema/product.py:46` |
| Category creation | `CategoryCreate` | `schema/category.py:15` |
| JWT token | `Token` | `schema/token.py:6` |

---

## Summary

Pydantic is used throughout this project for:
1. **Configuration** - Loading environment variables safely
2. **Validation** - Ensuring data integrity for API requests
3. **Serialization** - Converting database objects to JSON responses
4. **Type Safety** - Catching errors early with type hints
5. **Documentation** - Auto-generating API documentation

This implementation makes the codebase more robust, maintainable, and easier to understand.
