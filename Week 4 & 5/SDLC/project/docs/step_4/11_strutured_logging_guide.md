# Logging Guide

This guide explains how to use the structlog-based logging system implemented in the SDLC Inventory Management project.

## Overview

The logging system provides:
- **Structured logging** with correlation IDs for request tracking
- **Dynamic log levels** configurable via environment variables
- **Context-aware logging** with automatic correlation ID injection
- **Request/response logging** middleware for FastAPI
- **Module-specific logging** with consistent formatting
- **Environment-based configuration** for easy deployment management

## Configuration

### Environment Variables

Configure logging behavior using these environment variables:

```bash
# Logging Configuration
LOG_LEVEL=INFO                    # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Default Values

- `LOG_LEVEL`: `INFO` 

## Architecture

### Core Components

1. **LogSettings**: Pydantic-based configuration management
2. **correlation_id**: Context variable for request tracking
3. **setup_logging()**: Initializes structlog configuration
4. **get_logger()**: Returns structured logger instance
5. **log_error()**: Utility function for error logging

### Log Levels

```python
class LogLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
```

## Usage

### Basic Logging Setup

```python
from src.core.log import setup_logging, get_logger

# Set up logging (typically called at application startup)
setup_logging()

# Get a logger for your module
logger = get_logger(__name__)
```

### Using Loggers

```python
logger = get_logger(__name__)

# Different log levels
logger.debug("Debug information for developers")
logger.info("General information about program execution")
logger.warning("Warning messages for potentially problematic situations")
logger.error("Error messages for serious problems")
logger.critical("Critical messages for fatal errors")

# Logging with context (structured logging)
logger.info("User logged in", user_email="user@example.com", ip_address="192.168.1.1")
logger.error("Failed to connect to database", error=str(e), table="products")
```

### Correlation ID Tracking

The system automatically generates correlation IDs for each HTTP request:

```python
# In middleware (automatically handled)
request_id = str(uuid.uuid4())
token = correlation_id.set(request_id)

# In any service or repository
logger.info("Processing request", operation="create_product", product_id=123)
# Output will include correlation_id automatically
```

## FastAPI Integration

### Automatic Request Logging

The system automatically logs all HTTP requests and responses:

```python
# src/api/main.py
@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = correlation_id.set(request_id)

    logger.info("Request started", path=request.url.path, method=request.method)

    try:
        response = await call_next(request)
        return response
    finally:
        correlation_id.reset(token)
```

## Log Formats

### Default Console Format
```
2024-01-15T10:30:45.123456Z [info     ] Request started [correlation_id=abc-123] path=/api/v1/products method=POST
2024-01-15T10:30:45.234567Z [info     ] Product created [correlation_id=abc-123] product_id=456 user_id=789
```

### JSON Format (Optional)
To enable JSON logging, uncomment the JSON renderer:

```python
# In setup_logging()
# TO LOG AS JSON
processors.append(structlog.processors.JSONRenderer())
# TO LOG IN CONSOLE
# processors.append(structlog.dev.ConsoleRenderer())
```

### Log Components

Each log entry includes:
- **Timestamp**: ISO 8601 format
- **Log Level**: [debug], [info], [warning], [error], [critical]
- **Message**: Log message
- **Context**: Additional key-value pairs
- **Correlation ID**: Request tracking identifier

## Best Practices

### 1. Use Structured Logging
```python
# Good - structured context
logger.info("User created product", user_id=123, product_id=456, product_name="Laptop")

# Avoid - string formatting
logger.info(f"User {user_id} created product {product_id} with name {product_name}")
```

### 2. Include Relevant Context
```python
# Good - business context
logger.info("Category deletion attempted", category_id=123, user_role="admin", has_products=True)

# Avoid - insufficient context
logger.info("Category deletion attempted")
```

### 3. Use Appropriate Log Levels
- **DEBUG**: Detailed information for debugging (database queries, variable values)
- **INFO**: Business operations and significant events (user actions, API calls)
- **WARNING**: Unexpected but recoverable situations (validation failures, missing data)
- **ERROR**: Serious problems that need attention (database failures, authentication errors)
- **CRITICAL**: Fatal errors that may stop the application (out of memory, disk full)

### 4. Don't Log Sensitive Information
```python
# Avoid logging sensitive data
logger.info("User logged in", email=user.email, password=user.password)

# Instead, log safe information
logger.info("User logged in successfully", user_id=user.id, email=user.email)
```

## Examples

### API Router Example
```python
# src/api/routes/product.py
from src.core.log import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/products")
async def create_product(product_data: ProductCreate):
    logger.info("Creating new product", 
                product_name=product_data.name, 
                category_id=product_data.category_id)
    
    try:
        product = await product_service.create_product(product_data)
        logger.info("Product created successfully", 
                    product_id=product.id, 
                    product_name=product.name)
        return product
    except Exception as e:
        logger.error("Failed to create product", 
                    product_name=product_data.name, 
                    error=str(e))
        raise
```

### Service Example
```python
# src/services/product_service.py
from src.core.log import get_logger

logger = get_logger(__name__)

class ProductService:
    async def create_product(self, product_data: dict, user_email: str) -> dict:
        logger.debug("Starting product creation", 
                    user_email=user_email, 
                    product_name=product_data.get("name"))
        
        # Validate category exists
        category = await self.category_repository.get_by_id(product_data["category_id"])
        if not category:
            logger.warning("Invalid category for product creation", 
                          category_id=product_data["category_id"], 
                          user_email=user_email)
            raise ValueError("Invalid category specified")
        
        logger.info("Creating product with valid category", 
                   category_id=category.id, 
                   category_name=category.name)
        
        return await self.product_repository.create_product(product_data)
```

### Repository Example
```python
# src/repository/utility.py
from src.core.log import get_logger

logger = get_logger(__name__)

async def get_initial_data_from_csv(csv_path: str) -> dict:
    logger.info("Loading initial data from CSV", csv_path=csv_path)
    
    try:
        data = pd.read_csv(csv_path)
        logger.info("CSV data loaded successfully", 
                   rows=len(data), 
                   columns=list(data.columns))
        return {"product_category": data.to_dict("records")}
    except FileNotFoundError:
        logger.error("CSV file not found", csv_path=csv_path)
        raise
    except Exception as e:
        logger.error("Failed to load CSV data", csv_path=csv_path, error=str(e))
        raise
```

### Database Operations Example
```python
# src/repository/database.py
from src.core.log import get_logger, log_error

logger = get_logger(__name__)

def seed_db():
    logger.info("Starting database seeding")
    
    initial_data = get_initial_data_from_csv(settings.INVENTORY_CSV_FILEPATH)
    with engine.connect() as connection:
        for tablename in ["product_category", "product"]:
            if tablename in initial_data and len(initial_data[tablename]) > 0:
                target = Base.metadata.tables[tablename]
                stmt = insert(target).values(initial_data[tablename])
                try:
                    connection.execute(stmt)
                    connection.commit()
                    logger.info("Successfully seeded table", 
                               table=tablename, 
                               records_count=len(initial_data[tablename]))
                except Exception as e:
                    connection.rollback()
                    logger.error("Error seeding table", 
                               table=tablename, 
                               error=str(e))
```

## Environment Configuration

### Development Environment
```bash
# .env
LOG_LEVEL=DEBUG
```

### Production Environment
```bash
# .env
LOG_LEVEL=INFO
```

### Testing Environment
```bash
# .env.test
LOG_LEVEL=WARNING
```

## Troubleshooting

### Common Issues

1. **Logs not appearing**: Check if `LOG_LEVEL` is set too high
2. **Missing correlation IDs**: Ensure middleware is properly configured
3. **Context not showing**: Use structured logging with keyword arguments

### Debug Mode

To enable debug logging temporarily:

```bash
export LOG_LEVEL=DEBUG
python -m src.api.main
```

### Viewing Logs in Production

```bash
# Follow application logs
tail -f /var/log/inventory_app/app.log

# Filter by correlation ID
grep "correlation_id=abc-123" /var/log/inventory_app/app.log

# Filter error logs
grep "ERROR" /var/log/inventory_app/app.log
```

## Advanced Features

### Custom Context Processors

You can modify the `add_context_processor` function to include additional context:

```python
def add_context_processor(_, __, event_dict):
    # Add custom context variables
    event_dict["correlation_id"] = correlation_id.get()
    event_dict["environment"] = os.getenv("ENVIRONMENT", "development")
    event_dict["service"] = "inventory-management"
    return event_dict
```

## Migration from Standard Logging

If you're migrating from the standard `logging.getLogger(__name__)` approach:

```python
# Old way
import logging
logger = logging.getLogger(__name__)
logger.info("User %s logged in", user.email)

# New way
from src.core.log import get_logger
logger = get_logger(__name__)
logger.info("User logged in", user_email=user.email)
```

The new system provides:
- Better performance with structured logging
- Automatic correlation ID tracking
- Environment-based configuration
- Consistent formatting across the application
