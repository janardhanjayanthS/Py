# SOLID Principles & Design Patterns

> **🎯 Learning Objective:** Understand how SOLID principles and design patterns create maintainable, testable, and scalable software architecture.

This document demonstrates the practical application of SOLID principles and design patterns through our SDLC Inventory Management FastAPI application, showcasing the transformation from coupled to decoupled architecture.

## 📚 Table of Contents

1. [Overview: Why SOLID Matters](#overview-why-solid-matters)
2. [Single Responsibility Principle (SRP)](#single-responsibility-principle-srp)
3. [Open/Closed Principle (OCP)](#openclosed-principle-ocp)
4. [Liskov Substitution Principle (LSP)](#liskov-substitution-principle-lsp)
5. [Interface Segregation Principle (ISP)](#interface-segregation-principle-isp)
6. [Dependency Inversion Principle (DIP)](#dependency-inversion-principle-dip)
7. [Design Patterns in Practice](#design-patterns-in-practice)
8. [Real-World Benefits](#real-world-benefits)


---

## Overview: Why SOLID Matters

Our SDLC Inventory Management project demonstrates two architectural approaches:

| **V1: Coupled Architecture** | **V2: Decoupled Architecture** |
|:---|:---|
| ❌ Monolithic routers handling everything | ✅ Layered architecture with clear separation |
| ❌ Direct database dependencies | ✅ Abstract interfaces and dependency injection |
| ❌ Difficult to test and maintain | ✅ Easy to test, extend, and maintain |
| ❌ Tight coupling between components | ✅ Loose coupling through abstractions |

**The Result:** V2 is more maintainable, testable, and ready for future growth.



## Single Responsibility Principle (SRP)

> **"A class should have one, and only one, reason to change."**

### ❌ Before SRP: The Overloaded User Router

In our initial implementation, the user router handled multiple responsibilities directly:

```python
# Before SOLID - Multiple Responsibilities in Router
from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.exceptions import AuthenticationException
from src.core.jwt import create_access_token, required_roles
from src.core.log import get_logger
from src.models.user import User
from src.repository.database import (
    add_commit_refresh_db,
    commit_refresh_db,
    delete_commit_db,
    get_db,
    hash_password,
)
from src.schema.user import (
    UserEdit,
    UserLogin,
    UserRegister,
    UserRole,
    WrapperUserResponse,
)
from src.services.models import ResponseStatus
from src.services.user_service import (
    authenticate_user,
    check_existing_user_using_email,
    fetch_user_by_email,
    handle_missing_user,
    update_user_name,
    update_user_password,
)

@user.post("/user/register", response_model=WrapperUserResponse)
async def register_user(create_user: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new user account.

    Args:
        create_user: User registration data.
        db: Database session dependency.

    Returns:
        WrapperUserResponse containing the created user.

    Raises:
        AuthenticationException: If user email already exists.
    """
    # 1. Validation Logic - Mixed in router
    logger.debug(f"Registration attempt for email: {create_user.email}")
    if await check_existing_user_using_email(user=create_user, db=db):
        message = f"User with email {create_user.email} already exists"
        logger.error(message)
        raise AuthenticationException(
            message=message,
            field_errors=[
                {
                    "field": "email id",
                    "message": f"{create_user.email} already exists in DB",
                }
            ],
        )

    # 2. Data Manipulation Logic - Direct in router
    db_user = User(
        name=create_user.name,
        email=create_user.email,
        password=hash_password(create_user.password),
        role=create_user.role.value,
    )

    # 3. Database Transaction Management - Direct in router
    await add_commit_refresh_db(object=db_user, db=db)
    logger.debug(f"Created new user with- {db_user.email} - email")
    logger.warning(f"Created new user with - {db_user.email} - email")

    # 4. Response Formatting - Direct in router
    return {"status": "success", "message": {"registered user": db_user}}
```

**Problems:**
- 4+ different reasons to change (validation, business rules, data manipulation, transactions, HTTP responses)
- Router directly handles database operations and business logic
- Mixing HTTP handling, business logic, and data access
- Direct database dependencies throughout router layer
- No separation between concerns
- Difficult to test individual components

### ✅ After SRP: Clear Separation of Concerns

Now each component has a single responsibility:

**1. API Router** - Only handles HTTP concerns:

```python
# src/api/routes/user.py (Current Implementation)
@user.post("/user/register", response_model=WrapperUserResponse)
async def register_user(
    create_user: UserRegister,
    user_service: AbstractUserService = Depends(get_user_service),
):
    """Registers a new user account in the system.

    Args:
        create_user: Data transfer object containing registration details.
        user_service: The user service business logic layer.

    Returns:
        A dictionary containing the success status and the registered user data.

    Raises:
        AuthenticationException: If the user email is already registered.
    """
    # Only responsibility: HTTP handling and input validation
    db_user = await user_service.register_user(user=create_user)
    return {"status": "success", "message": {"registered user": db_user}}
```

**2. Service Layer** - Only handles business logic:

```python
# src/services/user_service.py (Current Implementation)
class UserService(AbstractUserService):
    """Service layer for user business logic."""
    
    async def register_user(self, user: UserRegister) -> User:
        """Register a new user with validation and business rules.
        
        Args:
            user: User registration data.
            
        Returns:
            Created user entity.
            
        Raises:
            AuthenticationException: If user already exists.
        """
        # Only responsibility: Business rules and validation
        existing_user = await self.repo.get_user_by_email(user.email)
        if existing_user:
            raise AuthenticationException(
                message=f"User with email {user.email} already exists"
            )
        
        # Create user with hashed password
        hashed_password = hash_password(user.password)
        return await self.repo.create_user(user, hashed_password)
```

**3. Repository Layer** - Only handles data access:

```python
# src/repository/user_repo.py (Current Implementation)
class UserRepository:
    """Repository for user data access operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user_data: UserRegister, hashed_password: str) -> User:
        """Create a new user in the database.
        
        Args:
            user_data: User registration data.
            hashed_password: Hashed password.
            
        Returns:
            Created user entity.
        """
        # Only responsibility: Database operations
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role.value,
        )
        
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user
```

## Open/Closed Principle (OCP)

> **"Software entities should be open for extension, but closed for modification."**

### ❌ Before OCP: Modifying Existing Code

Adding new pricing features required changing working code:

```python
# Adding new pricing logic required modifying existing function
def apply_discount_or_tax(product: Product) -> Product:
    """
    Applies dicount or tax to product's price

    Args:
        product: db product object

    Returns:
        Product: db product object
    """
    price = ConcretePrice(amount=product.price)
    if product.id % 2 == 0:
        price = TaxDecorator(price=price, tax_percentage=0.2)
        product.price_type = "taxed"
    else:
        price = DiscountDecorator(price=price, discount_percentage=0.2)
        product.price_type = "discounted"
    product.price = price.get_amount()
    logger.info(f"Applied {product.price_type} to {price.get_amount()}")
    return product
```

### ✅ After OCP: Extending Without Modification

```python
# src/core/decorator_pattern.py (Current Implementation)
class Price(ABC):
    """Abstract base class for price calculations."""

    @abstractmethod
    def get_amount(self) -> float:
        """Calculate and return the price amount.

        Returns:
            Calculated price amount.
        """
        pass

class ConcretePrice(Price):
    """Concrete implementation of base price."""
    def __init__(self, amount: float) -> None:
        self.amount: float = amount

    def get_amount(self) -> float:
        return self.amount

class TaxDecorator(Decorator):
    """Decorator that adds tax to the base price."""
    def __init__(self, price: Price, tax_percentage: float) -> None:
        super().__init__(price)
        self.tax_percentage = tax_percentage

    def get_amount(self) -> float:
        return self._price.get_amount() + (
            self._price.get_amount() * self.tax_percentage
        )

class DiscountDecorator(Decorator):
    """Decorator that applies discount to the base price."""
    def __init__(self, price: Price, discount_percentage: float) -> None:
        super().__init__(price)
        self.discount_percentage = discount_percentage

    def get_amount(self) -> float:
        return self._price.get_amount() - (
            self._price.get_amount() * self.discount_percentage
        )
```

```python
# NEW: Add shipping cost decorator without changing existing decorators
class ShippingDecorator(Decorator):
    """Decorator that adds shipping cost to the base price."""
    def __init__(self, price: Price, shipping_cost: float) -> None:
        super().__init__(price)
        self.shipping_cost = shipping_cost

    def get_amount(self) -> float:
        return self._price.get_amount() + self.shipping_cost

# Usage: Chain decorators without modifying existing code
price = ConcretePrice(amount=100.0)
price_with_tax = TaxDecorator(price, 0.1)  # 110.0
price_with_shipping = ShippingDecorator(price_with_tax, 15.0)  # 125.0
```

**Benefits:**
- ✅ Original pricing logic remains untouched
- ✅ New pricing strategies added through composition
- ✅ System is stable and extensible

### 🏗️ Real-World Example: Settings Configuration Class

The `Settings` class demonstrates OCP by being extensible without modifying core functionality:

```python
# src/core/config.py (Current Implementation)
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.singleton_pattern import Singleton

class Settings(BaseSettings, metaclass=Singleton):
    """Application configuration settings.

    Handles environment variables and application-wide settings.
    """

    INVENTORY_CSV_FILEPATH: str = str(
        (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
    )

    # POSTGRESQL
    postgresql_pwd: str = Field(validation_alias="POSTGRESQL_PWD")

    # ENVIRONMENT
    environment: str = Field(validation_alias="ENVIRONMENT")

    @property
    def DATABASE_URL(self) -> str:
        """Generate PostgreSQL database URL.

        Returns:
            Database connection string.
        """
        return f"postgresql://postgres:{self.postgresql_pwd}@localhost:5432/inventory_manager"

    # JWT
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # .env settings
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )

# Global instance - singleton pattern ensures one configuration source
settings = Settings()
```

### 🚀 Extending Settings Without Modification

**Adding new configuration sections without changing existing code:**

```python
# NEW: Extend Settings for Redis configuration
class RedisSettings(Settings):
    """Extended settings with Redis configuration"""
    
    REDIS_HOST: str = Field(default="localhost", validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, validation_alias="REDIS_PORT")
    REDIS_DB: int = Field(default=0, validation_alias="REDIS_DB")
    
    @property
    def REDIS_URL(self) -> str:
        """Generate Redis connection URL."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

# NEW: Extend Settings for Email configuration
class EmailSettings(Settings):
    """Extended settings with Email configuration"""
    
    SMTP_HOST: str = Field(validation_alias="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, validation_alias="SMTP_PORT")
    SMTP_USERNAME: str = Field(validation_alias="SMTP_USERNAME")
    SMTP_PASSWORD: str = Field(validation_alias="SMTP_PASSWORD")
    EMAIL_FROM_ADDRESS: str = Field(validation_alias="EMAIL_FROM_ADDRESS")

# NEW: Extend Settings for Monitoring configuration
class MonitoringSettings(Settings):
    """Extended settings with Monitoring configuration"""
    
    SENTRY_DSN: str = Field(default="", validation_alias="SENTRY_DSN")
    PROMETHEUS_PORT: int = Field(default=9090, validation_alias="PROMETHEUS_PORT")
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")

# Usage: Each extension maintains original functionality while adding new features
redis_config = RedisSettings()
email_config = EmailSettings()
monitoring_config = MonitoringSettings()

# Original settings still work exactly as before
original_db_url = settings.DATABASE_URL  # Still works unchanged
new_redis_url = redis_config.REDIS_URL  # New functionality without touching original
```

### 🎯 OCP Benefits in Settings Implementation

**How Settings class follows OCP:**

- ✅ **Closed for Modification**: Core `Settings` class remains stable and unchanged
- ✅ **Open for Extension**: New configuration sections added through inheritance
- ✅ **Backward Compatible**: Existing code using `settings` continues to work
- ✅ **Environment Isolation**: Different environments can extend settings differently
- ✅ **Testable**: Each settings extension can be tested independently

**Real-world extension scenarios:**

```python
# Development environment - add debug settings
class DevelopmentSettings(Settings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    ENABLE_PROFILING: bool = True

# Production environment - add security settings
class ProductionSettings(Settings):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    ENABLE_SECURITY_HEADERS: bool = True
    RATE_LIMIT_REQUESTS: int = 100

# Testing environment - add test-specific settings
class TestSettings(Settings):
    DATABASE_URL: str = "sqlite:///:memory:"
    TESTING: bool = True
    DISABLE_AUTH: bool = True

# Environment-specific usage without modifying core code
def get_settings():
    env = os.getenv("ENVIRONMENT", "development")
    
    settings_classes = {
        "development": DevelopmentSettings,
        "production": ProductionSettings,
        "testing": TestSettings,
    }
    
    return settings_classes.get(env, Settings)()
```

**Key OCP Principles Demonstrated:**
- **Extensibility**: New configuration capabilities through inheritance
- **Stability**: Original `Settings` class never needs modification
- **Polymorphism**: Different settings implementations used interchangeably
- **Encapsulation**: Each settings class manages its own configuration domain


## Liskov Substitution Principle (LSP)

> **"Subtypes must be substitutable for their base types."**


### The Contract: BaseProduct Abstract Class
```python
# src/model.py (from inventory_manager package)
class BaseProduct(BaseModel, ABC):
    """
    Initializes base product
    Args:
        product_details: dataclass conatining product information
    """

    product_id: str
    product_name: str = Field(..., min_length=1)
    quantity: PositiveInt
    price: PositiveFloat
    type: ProductTypes

    def __str__(self):
        message = ""
        for key, value in self.__dict__.items():
            if key == "type":
                message += f"{key}: {value.value} | "
            else:
                message += f"{key}: {value} | "
        return message
```


### ✅ Demonstrating LSP: Substitutable Product Implementations


```python
# src/model.py (from inventory_manager package)
class RegularProduct(BaseProduct):
    """
    Initializes regular product
    Args:
        product_details: dataclass conatining product information
    """
    # Inherits all BaseProduct behavior without modification
    pass

class FoodProduct(BaseProduct):
    """
    Initializes a food product
    Args:
        product_details: dataclass conatining product information
    Additional Attributes:
        days_to_expire: food's expiry period in days
        is_vegetarian: food's classification
    """

    days_to_expire: PositiveInt
    is_vegetarian: bool

    def get_expiry_date(self) -> str:
        """
        returns exact expiry date
        Returns
            str representing expiry date
        """
        return datetime.strftime(
            timedelta(days=self.days_to_expire) + datetime.now(),  # type: ignore
            "%d-%m-%Y",  # type: ignore
        )

class ElectronicProduct(BaseProduct):
    """
    Initializes electronic product
    Args:
        product_details: dataclass conatining product information
    Additional Attributes:
        warrenty_period_in_years: in years
    """

    warranty_period_in_years: float
```



```python
# src/model.py (from inventory_manager package)
class ProductFactory:
    """
    Manages product types
    """

    def create_product(self, product_details: ProductDetails) -> BaseProduct:
        """
        Creates and returns product object based on product type

        Args:
            product_details : contains details about the product

        Returns:
            BaseProduct: the created object type
        """
        if product_details.type == ProductTypes.RP.value:
            return RegularProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                type=product_details.type,
            )
        elif product_details.type == ProductTypes.FP.value:
            return FoodProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                days_to_expire=product_details.days_to_expire,
                is_vegetarian=product_details.is_vegetarian,  # type: ignore
                type=product_details.type,
            )
        elif product_details.type == ProductTypes.EP.value:
            return ElectronicProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                warranty_period_in_years=product_details.warranty_period_in_years,
                type=product_details.type,
            )
        else:
            print(f"Requested product type: {type} not available")
            return  # type: ignore
```



```python
# All product types can be used interchangeably
def process_product(product: BaseProduct):
    """Process any product type - works with all subclasses."""
    print(f"Processing: {product.product_name}")
    print(f"Price: ${product.price}")
    print(f"Type: {product.type.value}")
    
    # LSP ensures all BaseProduct methods work
    print(product.__str__())

# Can use any product type
regular = RegularProduct(product_id="1", product_name="Laptop", quantity=10, price=999.99, type=ProductTypes.RP)
food = FoodProduct(product_id="2", product_name="Apple", quantity=50, price=1.50, type=ProductTypes.FP, days_to_expire=7, is_vegetarian=True)
electronic = ElectronicProduct(product_id="3", product_name="Phone", quantity=25, price=699.99, type=ProductTypes.EP, warranty_period_in_years=2)

# All work with the same function
process_product(regular)  # Works
process_product(food)     # Works  
process_product(electronic)  # Works
```




## Interface Segregation Principle (ISP)

> **"Clients should not be forced to depend on methods they do not use."**

### ❌ Before ISP: Large, Monolithic Dependencies 


```python
# Router was coupled to entire database session interface
@product.post("/products")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def post_products(
    request: Request,
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    # Service only needs specific database operations but gets entire session
    return post_product(user_email=current_user_email, product=product, db=db)
```


### ✅ After ISP: Specific, Focused Database Operations (not really interfaces just functions)


```python
# src/repository/database.py (Current Implementation)
def add_commit_refresh_db(object: BaseModel, db: Session):
    """Add, commit, and refresh database object."""
    db.add(object)
    db.commit()
    db.refresh(object)

def commit_refresh_db(object: BaseModel, db: Session) -> None:
    """Commit and refresh database object."""
    db.commit()
    db.refresh(object)

def delete_commit_db(object: BaseModel, db: Session) -> None:
    """Delete and commit database object."""
    db.delete(object)
    db.commit()

def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if plain text password matches bcrypt hash."""
    return pwt_context.verify(plain_password, hashed_password)
```



```python
# src/services/product_service.py (Current Implementation)
def post_product(
    user_email: str, product: Optional[ProductCreate], db: Session
) -> dict:
    # Only uses add_commit_refresh_db - not all database operations
    add_commit_refresh_db(object=db_product, db=db)
    return response

def put_product(
    current_user_email: str, product_id: int, product_update: BaseModel, db: Session
) -> dict:
    # Only uses commit_refresh_db - not all database operations  
    commit_refresh_db(object=db_product, db=db)
    return response

def delete_product(current_user_email: str, product_id: int, db: Session) -> dict:
    # Only uses delete_commit_db - not all database operations
    delete_commit_db(object=db_product, db=db)
    return response
```


**Benefits:**
- ✅ Reduced coupling between components
- ✅ Clear, focused database operations
- ✅ Easy to test individual operations
- ✅ Services only depend on operations they actually use



## Dependency Inversion Principle (DIP)

> **"High-level modules should not depend on low-level modules. Both should depend on abstractions."**

### ❌ Before DIP: Direct Dependencies

**Dependency Flow:** `API Router` → `Service Layer` → `SQLAlchemy Session` + `Database Models`


```python
# Initial Implementation - Direct Database Dependencies
def post_product(
    user_email: str, product: Optional[ProductCreate], db: Session
) -> dict:
    # High-level service directly depends on low-level database session
    check_existing_product_using_name(product=product, db=db)
    check_existing_product_using_id(product=product, db=db)
    
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        return handle_missing_category(category_id=product.category_id)
    
    # Direct SQLAlchemy operations throughout service
    db_product = Product(**product.model_dump())
    add_commit_refresh_db(object=db_product, db=db)
```

**Problems:**
- Business logic tied to specific database technology (SQLAlchemy)
- Service layer directly manipulates database sessions and models
- Difficult to test without real database
- Cannot easily swap database implementations
- High-level business logic depends on low-level infrastructure details


### ✅ After DIP: Inverted Dependencies Through Abstraction

**Dependency Flow:** `API Router` → `Service Layer` → `Repository Abstractions` ← `Repository Implementations`


```python
# src/services/product_service.py (Current Implementation)
def post_product(
    user_email: str, product: Optional[ProductCreate], db: Session
) -> dict:
    """
    Inserts product into db
    
    Args:
        user_email: current user's email id
        product: Pydnatic product model
        db: sqlalchemy db object
    
    Returns:
        dict: fastapi response
    """
    logger.debug(f"Creating product: {product.name if product else 'None'}")
    
    # Business logic doesn't know about specific database operations
    check_existing_product_using_name(product=product, db=db)
    check_existing_product_using_id(product=product, db=db)

    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        return handle_missing_category(category_id=product.category_id)

    db_product = Product(**product.model_dump())
    if product.id is not None:
        db_product = apply_discount_or_tax(product=db_product)

    # Depends on abstraction (add_commit_refresh_db function), not direct SQLAlchemy
    add_commit_refresh_db(object=db_product, db=db)
    logger.info(f"Product '{db_product.name}' created successfully")

    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": user_email, "inserted product": db_product},
    }
```



```python
# src/repository/database.py (Current Implementation)
def add_commit_refresh_db(object: BaseModel, db: Session):
    """Add, commit, and refresh database object.

    Performs the complete database transaction cycle for a new object:
    add to session, commit transaction, and refresh object with database values.

    Args:
        object: Pydantic model instance to insert into database.
        db: SQLAlchemy database session instance.
    """
    # Implements the abstraction - hides SQLAlchemy complexity
    db.add(object)
    db.commit()
    db.refresh(object)
```



```python
# src/api/routes/product.py (Current Implementation)
@product.post("/products")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def post_products(
    request: Request,
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    """Create a new product."""
    current_user_email: str = request.state.email
    logger.debug(f"Create product request by: {current_user_email}")
    logger.info(f"Creating new product: {product.name if product else 'None'}")
    
    # Router only knows about service interface, not implementation details
    return post_product(user_email=current_user_email, product=product, db=db)
```


**Note:** While our current implementation shows partial DIP through database abstraction functions, a full DIP implementation would involve creating abstract interfaces (like `IProductRepository`) and concrete implementations, but this level of abstraction isn't currently present in the codebase.



## Design Patterns in Practice

### 1. Factory Pattern (Registry-Based)

**What it is:** Creates objects without specifying their exact classes, using a registry for extensibility.


```python
# inventory_manager/src/model.py (Current Implementation)
class ProductFactory:
    """
    Manages product types
    """

    def create_product(self, product_details: ProductDetails) -> BaseProduct:
        """
        Creates and returns product object based on product type

        Args:
            product_details : contains details about the product

        Returns:
            BaseProduct: the created object type
        """
        if product_details.type == ProductTypes.RP.value:
            return RegularProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                type=product_details.type,
            )
        elif product_details.type == ProductTypes.FP.value:
            return FoodProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                days_to_expire=product_details.days_to_expire,
                is_vegetarian=product_details.is_vegetarian,  # type: ignore
                type=product_details.type,
            )
        elif product_details.type == ProductTypes.EP.value:
            return ElectronicProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                warranty_period_in_years=product_details.warranty_period_in_years,
                type=product_details.type,
            )
        else:
            print(f"Requested product type: {type} not available")
            return  # type: ignore
```


**Benefits:**
- ✅ Centralized object creation logic
- ✅ Easy to add new product types
- ✅ Consistent object creation process
- ✅ Separates object creation from business logic

### 2. Decorator Pattern

**What it is:** Adds behavior to objects without modifying their class.


```python
# src/core/decorator_pattern.py (Current Implementation)
class Price(ABC):
    """Abstract base class for price calculations."""

    @abstractmethod
    def get_amount(self) -> float:
        """Calculate and return the price amount."""
        pass

class ConcretePrice(Price):
    """Concrete implementation of base price."""
    def __init__(self, amount: float) -> None:
        self.amount: float = amount

    def get_amount(self) -> float:
        return self.amount

class TaxDecorator(Decorator):
    """Decorator that adds tax to the base price."""
    def __init__(self, price: Price, tax_percentage: float) -> None:
        super().__init__(price)
        self.tax_percentage = tax_percentage

    def get_amount(self) -> float:
        return self._price.get_amount() + (
            self._price.get_amount() * self.tax_percentage
        )

class DiscountDecorator(Decorator):
    """Decorator that applies discount to the base price."""
    def __init__(self, price: Price, discount_percentage: float) -> None:
        super().__init__(price)
        self.discount_percentage = discount_percentage

    def get_amount(self) -> float:
        return self._price.get_amount() - (
            self._price.get_amount() * self.discount_percentage
        )
```



```python
# src/services/product_service.py (Current Implementation)
def apply_discount_or_tax(product: Product) -> Product:
    """
    Applies dicount or tax to product's price

    Args:
        product: db product object

    Returns:
        Product: db product object
    """
    price = ConcretePrice(amount=product.price)
    if product.id % 2 == 0:
        price = TaxDecorator(price=price, tax_percentage=0.2)
        product.price_type = "taxed"
    else:
        price = DiscountDecorator(price=price, discount_percentage=0.2)
        product.price_type = "discounted"
    product.price = price.get_amount()
    logger.info(f"Applied {product.price_type} to {price.get_amount()}")
    return product
```


**Benefits:**
- ✅ Flexible pricing strategies
- ✅ Easy to add new pricing rules
- ✅ No modification to existing price classes
- ✅ Composable pricing logic

### 3. Singleton Pattern

**What it is:** Ensures only one instance of a class exists globally.


```python
# src/core/config.py (Current Implementation)
class Settings(BaseSettings, metaclass=Singleton):
    """Application configuration settings.

    Handles environment variables and application-wide settings.
    """

    INVENTORY_CSV_FILEPATH: str = str(
        (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
    )

    # POSTGRESQL
    postgresql_pwd: str = Field(validation_alias="POSTGRESQL_PWD")

    @property
    def DATABASE_URL(self) -> str:
        """Generate PostgreSQL database URL.

        Returns:
            Database connection string.
        """
        return f"postgresql://postgres:{self.postgresql_pwd}@localhost:5432/inventory_manager"

    # JWT
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # .env settings
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )

settings = Settings()  # Global singleton instance
```


**Benefits:**
- ✅ Single configuration source
- ✅ Consistent settings across application
- ✅ Memory efficient
- ✅ Thread-safe access

### 4. Repository Pattern

**What it is:** Mediates between business logic and data access layers.


```python
# src/repository/database.py (Current Implementation)
def get_db():
    """Get database session dependency for FastAPI.

    Provides a database session with proper error handling and cleanup.
    Uses FastAPI's dependency injection pattern for database access.

    Yields:
        Session: SQLAlchemy database session instance.

    Raises:
        DatabaseException: If database connection fails.
    """
    db = session_local()
    try:
        yield db
    except Exception as e:
        logger.error(str(e))
        raise DatabaseException(
            message="Database connection failed",
            field_errors=[
                {"field": "database", "message": f"Database error: {str(e)}"}
            ],
        )
    finally:
        db.close()
```


**Benefits:**
- ✅ Centralized data access logic
- ✅ Easy to swap database implementations
- ✅ Proper connection management
- ✅ Consistent error handling



## Real-World Benefits

### 🧪 Superior Testability


**Before (Direct Dependencies):**
```python
# Testing required real database and complex setup
async def test_create_product():
    # Need database setup, user creation, JWT tokens, cleanup, etc.
    user = await create_test_user()
    token = await get_auth_token(user.email)
    
    response = await client.post(
        "/products", 
        json=product_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    # Complex teardown required
```

**After (Separated Concerns):**
```python
# Test business logic in isolation
def test_product_validation():
    # Test validation logic without database
    with pytest.raises(DatabaseException):
        check_existing_product_using_name(mock_product, mock_db)
    
    # Test pricing logic independently
    product = Product(id=1, price=100.0)
    result = apply_discount_or_tax(product)
    assert result.price == 80.0  # 20% discount
    assert result.price_type == "discounted"
```


### 🔄 Effortless Maintenance


**Scenario:** Adding new product type

**Before:** Modify factory function, add new elif clause, risk breaking existing logic
**After:** Add new product class inheriting from BaseProduct, update ProductTypes enum

**Example:** Adding BookProduct
```python
# NEW: Add book product without modifying existing code
class BookProduct(BaseProduct):
    pages: int
    author: str
    genre: str

# Update ProductTypes enum
class ProductTypes(Enum):
    RP = "regular_product"
    FP = "food_product"
    EP = "electronic_product"
    BP = "book_product"  # New type

# Add to factory (single change)
elif product_details.type == ProductTypes.BP.value:
    return BookProduct(...)
```


### 🚀 Seamless Scalability


**Adding new features:**
- **Before:** Modify existing service functions, risk breaking working code
- **After:** Create new service classes, add new decorators, extend factory

**Technology migration:**
- **Before:** Rewrite entire application and all endpoints
- **After:** Implement new repository classes, update database functions

**Real Example:** Switching from PostgreSQL to MongoDB
- **Before:** Rewrite all SQLAlchemy queries in every service
- **After:** Create new database functions, update repository layer only


### 🎯 Developer Experience


**New team member onboarding:**
- **Before:** Must understand database queries, JWT handling, business logic all mixed together
- **After:** Can focus on one layer at a time (repository, service, or router)

**Parallel development:**
- **Before:** High risk of merge conflicts when multiple developers modify the same service files
- **After:** Different developers can work on different layers simultaneously without conflicts

**Code navigation:**
- **Before:** Difficult to find where specific logic is implemented
- **After:** Clear separation makes it easy to locate and modify specific functionality
