# Project Structure Overview

**Learning Objective:** Understand how our SDLC project structure reflects clean architecture principles and makes the codebase easy to navigate and maintain.

## Complete Directory Structure

```
SDLC/
├── alembic/                    # Database Migration Management
│   ├── versions/              # Alembic migration versions
│   ├── env.py                 # Migration environment configuration
│   └── script.py.mako         # Migration script template
├── data/                      # Application Data Files
│   └── new_inventory.csv      # Sample inventory data
├── docs/                      # Project Documentation
│   ├── step_1/                # Planning & Design Documentation
│   ├── step_2/                # Project Setup Documentation
│   ├── step_3/                # API Implementation Guides
│   └── step_4/                # Testing & Best Practices Documentation
│       └── project_structure_overview.md  # This file
├── requirements/               # Dependency Management
│   └── requirements.txt       # Production dependencies
├── src/                       # Application Source Code
│   ├── api/                   # HTTP Layer (FastAPI)
│   │   ├── main.py           # Application entry point & setup
│   │   └── routes/           # API endpoint definitions
│   │       ├── category.py  # Category management endpoints
│   │       ├── product.py   # Product management endpoints
│   │       └── user.py      # User management endpoints
│   ├── core/                  # Core Infrastructure
│   │   ├── app_utility.py    # Application lifecycle management
│   │   ├── config.py         # Environment configuration management
│   │   ├── decorator_pattern.py # Decorator pattern implementations
│   │   ├── excptions.py      # Custom exception classes
│   │   ├── filepath.py       # File path utilities
│   │   ├── jwt.py           # JWT token handling
│   │   └── log.py           # Logging configuration and utilities
│   ├── models/                # SQLAlchemy Data Models
│   │   ├── category.py      # Category entity model
│   │   ├── product.py       # Product entity model
│   │   └── user.py          # User entity model
│   ├── repository/            # Data Access Layer
│   │   ├── database.py       # Database connection & session management
│   │   └── utility.py        # Repository utilities and helpers
│   ├── schema/               # Pydantic Data Schemas
│   │   ├── category.py      # Category request/response schemas
│   │   ├── product.py       # Product request/response schemas
│   │   ├── token.py         # JWT token schemas
│   │   └── user.py          # User request/response schemas
│   └── services/              # Business Logic Layer
│       ├── category_service.py # Category business logic
│       ├── models.py        # Service layer models
│       ├── product_service.py  # Product business logic
│       ├── user_service.py     # User business logic
│       └── utility.py          # Service utilities
├── tests/                     # Comprehensive Test Suite
│   ├── api/                   # API layer tests
│   │   ├── test_category_routes.py  # Category API tests
│   │   ├── test_product_routes.py   # Product API tests
│   │   └── test_user_routes.py      # User API tests
│   ├── core/                  # Core infrastructure tests
│   │   └── test_utility.py    # Core utility tests
│   └── conftest.py           # Test configuration and fixtures
├── venv/                      # Virtual Environment (Python)
├── .env                       # Environment variables (local)
├── .gitignore                 # Git ignore patterns
├── .pre-commit.yaml           # Pre-commit hooks configuration
├── alembic.ini                # Database migration configuration
├── CHANGELOG.MD               # Project change history
├── env.example                # Environment variables template
├── errors.log                 # Application error log
└── README.MD                  # Project overview & setup instructions
```

## Architectural Layers & Responsibilities

### 1. **API Layer** (`src/api/`)

**Responsibility:** Handle HTTP requests and responses

**Components:**
- **`main.py`** - FastAPI application factory, middleware setup, router registration
- **`routes/category.py`** - Category CRUD endpoints
- **`routes/product.py`** - Product CRUD endpoints  
- **`routes/user.py`** - User management and authentication endpoints

**What it does:**
- Defines API endpoints and routes
- Validates incoming data using Pydantic schemas
- Delegates business logic to services
- Formats responses and handles HTTP status codes
- Manages authentication middleware and exception handling

**What it doesn't do:**
- Execute business rules
- Access databases directly
- Handle password hashing or validation

**Example:**
```python
# src/api/main.py
app = FastAPI(lifespan=lifespan)

app.include_router(product.product)
app.include_router(user.user)
app.include_router(category.category)

@app.exception_handler(WeakPasswordException)
async def handle_weak_password(request: Request, error: WeakPasswordException):
    return JSONResponse(
        status_code=400, content={"status": "Error", "message": error.message}
    )
```

### 2. **Schema Layer** (`src/schema/`)

**Responsibility:** Data validation and serialization contracts

**Components:**
- **`user.py`** - User registration, login, and response schemas
- **`product.py`** - Product creation, update, and response schemas
- **`category.py`** - Category creation, update, and response schemas
- **`token.py`** - JWT token schemas

**What it does:**
- Validates incoming request data
- Defines response data structures
- Provides type safety for API contracts
- Handles data serialization/deserialization

### 3. **Service Layer** (`src/services/`)

**Responsibility:** Execute business logic and orchestrate operations

**Components:**
- **`user_service.py`** - User authentication and management business logic
- **`product_service.py`** - Product business logic and validation
- **`category_service.py`** - Category business logic
- **`models.py`** - Service layer data models
- **`utility.py`** - Service utilities and helpers

**What it does:**
- Implements business rules and constraints
- Coordinates between repositories
- Handles complex workflows and validations
- Manages cross-cutting concerns

**Example:**
```python
# src/services/user_service.py
class UserService:
    async def create_user(self, user_data):
        # Business rule: validate password strength
        if not self.is_strong_password(user_data.password):
            raise WeakPasswordException("Password does not meet security requirements")
            
        # Business rule: check email uniqueness
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        return await self.user_repository.create_user(user_data)
```

### 4. **Repository Layer** (`src/repository/`)

**Responsibility:** Data access and persistence abstraction

**Components:**
- **`database.py`** - Database connection and session management
- **`utility.py`** - Repository utilities and common operations

**What it does:**
- Executes database queries using SQLAlchemy
- Handles data mapping between models and dictionaries
- Manages database transactions
- Abstracts database technology details

### 5. **Model Layer** (`src/models/`)

**Responsibility:** Database entity definitions

**Components:**
- **`user.py`** - User table structure with role-based access
- **`product.py`** - Product table structure with category relationships
- **`category.py`** - Category table structure

**What it does:**
- Defines SQLAlchemy ORM models
- Establishes database table structure
- Manages relationships between entities
- Provides database constraints and validations

**Example:**
```python
# src/models/user.py
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False, server_default="staff")
```

### 6. **Core Infrastructure** (`src/core/`)

**Responsibility:** Foundational services and configuration

**Components:**
- **`config.py`** - Environment configuration management with Pydantic
- **`app_utility.py`** - Application lifecycle management
- **`database.py`** - Database connection and session management
- **`jwt.py`** - JWT token creation and validation
- **`log.py`** - Structured logging with correlation IDs
- **`excptions.py`** - Custom exception classes
- **`decorator_pattern.py`** - Decorator pattern implementations
- **`filepath.py`** - File path utilities

**Example:**
```python
# src/core/config.py
class Settings(BaseSettings):
    postgresql_pwd: str = Field(validation_alias="POSTGRESQL_PWD")
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://postgres:{self.postgresql_pwd}@localhost:5432/inventory_manager"
```

## Testing Architecture (`tests/`)

### Test Categories

**API Tests:**
- `test_user_routes.py` - User management endpoints
- `test_product_routes.py` - Product CRUD endpoints
- `test_category_routes.py` - Category CRUD endpoints

**Core Tests:**
- `test_utility.py` - Core utility functions and helpers

**Test Configuration:**
- `conftest.py` - Test fixtures, database setup, and configuration

## Documentation Structure (`docs/`)

### Step-by-Step Development Process

**Step 1: Planning & Design**
- Project planning and requirements gathering
- System architecture and database design
- User stories and API specifications

**Step 2: Project Setup**
- Initial project structure and environment setup
- Development tools and configuration

**Step 3: API Implementation**
- Detailed implementation guides for each API endpoint
- Code examples and best practices

**Step 4: Testing & Best Practices**
- Testing strategies and quality assurance
- Project structure overview and maintenance guidelines

## Configuration & Deployment

### Environment Management
- **`.env`** - Local environment variables
- **`env.example`** - Template for environment variables
- **`requirements/requirements.txt`** - Production dependencies

### Database Management
- **`alembic/`** - Database migration scripts
- **`alembic.ini`** - Migration configuration
- **`data/`** - Sample data files

### Development Tools
- **`.pre-commit.yaml`** - Pre-commit hooks configuration
- **`.gitignore`** - Git ignore patterns
- **`CHANGELOG.MD`** - Project change history

## Data Flow Architecture

### Request Processing Flow
```
HTTP Request → FastAPI Router → Pydantic Schema → Service Layer → Repository → SQLAlchemy Model → PostgreSQL Database
```

### Response Processing Flow
```
PostgreSQL Database → SQLAlchemy Model → Repository → Service Layer → Pydantic Schema → FastAPI Router → HTTP Response
```

### Authentication Flow
```
Login Request → User Router → UserService → Password Validation → User Repository → JWT Token Generation
```

### Product Management Flow
```
Product Request → Product Router → ProductService → Category Validation → Product Repository → Database Operation
```

## Domain Model Overview

### Core Entities
- **User**: System users with role-based access (admin/staff)
- **Category**: Product categorization with hierarchical structure
- **Product**: Inventory items with category relationships

### Key Business Rules
- Users must have strong passwords
- Email addresses must be unique
- Products belong to categories
- Role-based access control for operations

## Benefits of This Structure

### 1. **Clear Separation of Concerns**
- Each directory has a single, well-defined purpose
- Easy to locate specific functionality
- No mixing of HTTP, business logic, and data access concerns

### 2. **Scalability & Maintainability**
- Modular architecture allows independent scaling
- Easy to add new features without affecting existing code
- Clear testing strategy for each layer

### 3. **Developer Experience**
- **Need to change an API endpoint?** → Look in `src/api/routes/`
- **Need to modify business rules?** → Look in `src/services/`
- **Need to change database queries?** → Look in `src/repository/`
- **Need to add validations?** → Look in `src/schema/` or `src/core/`

### 4. **Quality Assurance**
- Comprehensive test coverage across API and core layers
- Structured logging with correlation IDs
- Environment-based configuration management
- Database migration management with Alembic
