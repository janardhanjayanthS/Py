# Inventory Management System

A RESTful API backend built with FastAPI for managing product inventory with role-based access control and JWT authentication.

## Features

- **User Authentication**: Registration, login with JWT tokens
- **Role-Based Access Control**: Staff, Manager, and Admin roles
- **Product Management**: CRUD operations for inventory items
- **Category Management**: Organize products by categories
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic migrations
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic schemas
- **Testing**: pytest with SQLite in-memory database

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd inventory-management-system
```

2. Install dependencies:
```bash
pip install -r requirements/requirements.txt
```

3. Set up environment variables:
```bash
cd src/api
cp .env.example .env
# Edit .env with your database credentials
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
cd src/api
python main.py
```

The API will be available at `http://127.0.0.1:5001`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:5001/docs

## Support

For issues and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test files for usage examples