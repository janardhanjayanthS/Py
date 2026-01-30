# Local Setup and Testing Guide

This guide provides step-by-step instructions for setting up the SDLC Inventory Management API repository locally and running comprehensive tests.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - [Download Git](https://git-scm.com/downloads/)
- **Postman** - [Download Postman](https://www.postman.com/downloads/)

### Verify Installations
```bash
# Check Python version
python3 --version

# Check PostgreSQL version
psql --version

# Check Git version
git --version
```

## Repository Setup

### 1. Clone the Repository
```bash
# Clone the repository
git clone <your-repository-url>
cd "Week 4 & 5/SDLC"

# Or if you already have the repository
cd /path/to/Week\ 4\ \&\ 5/SDLC
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install production dependencies
pip install -r requirements/requirements.txt

# Install development dependencies (if dev_requirements.txt exists)
pip install -r dev_requirements.txt
```

## Database Setup

### 1. PostgreSQL Configuration
```bash
# Start PostgreSQL service
# On Linux:
sudo systemctl start postgresql

# On macOS:
brew services start postgresql

# On Windows:
# Start PostgreSQL service from Services
```

### 2. Create Database
```bash
# Connect to PostgreSQL as postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE inventory_manager;
CREATE USER inventory_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE inventory_manager TO inventory_user;
\q
```

### 3. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your database credentials
vim .env
```

**Required Environment Variables:**
```env
POSTGRESQL_PWD=your_secure_password
JWT_SECRET_KEY=your-jwt-secret-key-here
LOG_LEVEL=INFO
```

## Database Migrations

### 1. Run Migrations
```bash
# Ensure you're in the project root directory
cd /path/to/Week\ 4\ \&\ 5/SDLC

# Run database migrations
alembic upgrade head
```

### 2. Seed Database (Optional)
```bash
# If you have initial data in CSV format
# The application will automatically seed from data/new_inventory.csv
# You can also manually seed using the utility functions
python -c "from src.repository.database import seed_db; seed_db()"
```

### 3. Verify Database Setup
```bash
# Connect to database to verify tables
psql -U inventory_user -d inventory_manager -h localhost

# List tables
\dt

# Check user table structure
\d user

# Check product table structure
\d product

# Check product_category table structure
\d product_category

# Exit
\q
```

## Start the Application

### 1. Start API Server
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Start the server
uvicorn src.api.main:app --host 0.0.0.0 --port 5001 --reload
# or
python -m src.api.main
```

### 2. Verify Server is Running
```bash
# Test health endpoint
curl http://localhost:5001/

# Expected response:
# {"jello": "world"}
```

### 3. Access API Documentation
```bash
# Open browser for interactive API docs
# http://localhost:5001/docs
```

## Testing the Application

### 1. Automated Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/api/           # API tests
python -m pytest tests/core/          # Core infrastructure tests

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run tests with verbose output
python -m pytest tests/ -v
```

## Quick Reference Commands

### Essential Commands
```bash
# Start server
uvicorn src.api.main:app --host 0.0.0.0 --port 5001 --reload

# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Database migration
alembic upgrade head

# Activate virtual environment
source venv/bin/activate
```

### Development Commands
```bash
# Run specific test file
python -m pytest tests/api/test_user_routes.py

# Run tests with specific marker
python -m pytest tests/ -m "slow"

# Generate coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing

# Check code formatting
black src/ tests/
isort src/ tests/
```

### Database Commands
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history

# View current revision
alembic current
```

## Environment-Specific Configuration

### Development Environment
```env
LOG_LEVEL=DEBUG
POSTGRESQL_PWD=dev_password
JWT_SECRET_KEY=dev_secret_key
```

### Testing Environment
```env
LOG_LEVEL=INFO
POSTGRESQL_PWD=test_password
JWT_SECRET_KEY=test_secret_key
```

### Production Environment
```env
LOG_LEVEL=WARNING
POSTGRESQL_PWD=prod_secure_password
JWT_SECRET_KEY=prod_secure_jwt_secret
```


## Next Steps

After completing the local setup:

1. **Review the API Documentation** - Visit `http://localhost:5001/docs` for interactive API docs
2. **Run the Test Suite** - Ensure all tests pass before making changes
3. **Explore the Codebase** - Familiarize yourself with the project structure
4. **Test Business Logic** - Try creating users, categories, and products
5. **Review Documentation** - Check other documentation files in the `docs/step_4/` directory

For additional guidance, refer to the other documentation files in this directory, particularly:
- [Project Structure Overview](./project_structure_overview.md)
- [Complete Project Workflow](./2_complete_project_workflow.md)