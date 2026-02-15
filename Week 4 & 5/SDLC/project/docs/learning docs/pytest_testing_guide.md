# Pytest Testing Guide

## What is Pytest?

**Pytest** is a powerful and popular testing framework for Python that makes it easy to write simple and scalable test cases. It's used in this project to ensure all code works correctly before deployment.

**Official Documentation**: [https://docs.pytest.org/](https://docs.pytest.org/)

---

## Why Use Pytest?

1. **Simple Syntax**: Write tests using plain Python `assert` statements
2. **Auto-Discovery**: Automatically finds and runs test files
3. **Fixtures**: Reusable setup code for tests
4. **Parametrization**: Run same test with different inputs
5. **Detailed Reports**: Clear error messages when tests fail
6. **Plugin Ecosystem**: Extend functionality with plugins

---

## Project Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── api/                     # API endpoint tests
│   ├── test_category_routes.py
│   ├── test_product_routes.py
│   └── test_user_routes.py
├── core/                    # Core functionality tests
│   ├── test_jwt.py
│   ├── test_exceptions.py
│   └── test_utility.py
├── repository/              # Database layer tests
│   ├── test_database.py
│   └── test_utility.py
└── services/                # Business logic tests
    ├── test_category_service.py
    ├── test_product_service.py
    ├── test_product_service_async.py
    └── test_user_service.py
```

---

## Pytest Features Used in This Project

### 1. Test Classes

**What it is**: Grouping related tests together using classes  
**Why use it**: Organizes tests logically and makes them easier to find

**Example from `test_category_routes.py`:**

```python
class TestGetAllCategories:
    """Test suite for retrieving all categories"""

    def test_staff_can_view_all_categories(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """Test that staff can view all categories"""
        response = client.get("/category/all", headers=staff_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_manager_can_view_all_categories(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """Test that manager can view all categories"""
        response = client.get("/category/all", headers=manager_headers)
        assert response.status_code == 200
```

**Benefits**:
- Tests are grouped by feature (e.g., "Get All Categories")
- Easy to run specific test groups
- Better organization in test reports

**Documentation**: [https://docs.pytest.org/en/stable/getting-started.html#group-multiple-tests-in-a-class](https://docs.pytest.org/en/stable/getting-started.html#group-multiple-tests-in-a-class)

---

### 2. Fixtures

**What it is**: Reusable setup code that runs before tests  
**Why use it**: Avoid repeating setup code, ensure consistent test environment

**Example from `conftest.py`:**

```python
@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh sync database for each test function.
    This ensures test isolation - no test affects another.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

**How it's used in tests:**

```python
def test_view_multiple_categories(
    self, client: TestClient, staff_headers: dict, test_db: Session
):
    # test_db fixture is automatically injected
    categories = [
        Category(id=1, name="electronics"),
        Category(id=2, name="furniture"),
    ]
    for cat in categories:
        test_db.add(cat)
    test_db.commit()
```

**Fixture Scopes**:
- `function` (default): Runs before each test function
- `class`: Runs once per test class
- `module`: Runs once per test file
- `session`: Runs once for entire test session

**Documentation**: [https://docs.pytest.org/en/stable/fixture.html](https://docs.pytest.org/en/stable/fixture.html)

---

### 3. Conftest.py - Shared Fixtures

**What it is**: Special file where fixtures are defined and shared across all tests  
**Why use it**: Centralize common setup code, avoid duplication

**Key Fixtures in This Project:**

#### Database Fixtures

```python
@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh SQLite in-memory database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

#### Test Client Fixture

```python
@pytest.fixture(scope="function")
def client(test_db):
    """Creates a FastAPI test client with database override"""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    test_app.dependency_overrides[get_db] = override_get_db
    with TestClient(app=test_app) as test_client:
        yield test_client
```

#### User Authentication Fixtures

```python
@pytest.fixture
def staff_user(test_db):
    """Create a staff user in test database"""
    user = User(
        name="Staff User",
        email="staff@test.com",
        password=hash_password("password123"),
        role="staff",
    )
    test_db.add(user)
    test_db.commit()
    return user

@pytest.fixture
def staff_headers(staff_user):
    """Generate JWT token headers for staff user"""
    token = create_access_token(
        data={"sub": staff_user.email, "role": staff_user.role}
    )
    return {"Authorization": f"Bearer {token}"}
```

**Documentation**: [https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files)

---

### 4. Async Testing with `@pytest.mark.asyncio`

**What it is**: Decorator to test asynchronous functions  
**Why use it**: Modern Python uses async/await for database and API operations

**Example from `test_product_service_async.py`:**

```python
import pytest
from unittest.mock import AsyncMock

class TestCheckExistingProductUsingName:
    """Test check_existing_product_using_name with async operations"""

    @pytest.mark.asyncio
    async def test_product_exists_raises_exception(self):
        """Test that function raises exception when product exists"""
        mock_db = AsyncMock(spec=AsyncSession)
        
        # Mock existing product
        mock_product = Product(
            id=1, 
            name="Existing Product", 
            price=100, 
            quantity=10, 
            category_id=1
        )
        
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_product
        mock_db.execute.return_value = mock_result
        
        product_data = ProductCreate(
            name="Existing Product",
            price=100.0,
            quantity=10,
            category_id=1,
        )
        
        with pytest.raises(DatabaseException) as exc_info:
            await check_existing_product_using_name(
                product=product_data, 
                db=mock_db
            )
        
        assert "already exists" in str(exc_info.value).lower()
```

**Key Points**:
- Use `@pytest.mark.asyncio` decorator for async tests
- Use `async def` for test function
- Use `await` when calling async functions
- Requires `pytest-asyncio` plugin

**Documentation**: [https://pytest-asyncio.readthedocs.io/](https://pytest-asyncio.readthedocs.io/)

---

### 5. Mocking with `unittest.mock`

**What it is**: Creating fake objects to simulate dependencies  
**Why use it**: Test code in isolation without real database/API calls

**Example from `test_product_service_async.py`:**

```python
from unittest.mock import AsyncMock, Mock, patch

@pytest.mark.asyncio
async def test_product_not_exists_no_exception(self):
    """Test that function doesn't raise exception when product doesn't exist"""
    mock_db = AsyncMock(spec=AsyncSession)
    
    # Mock no existing product
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result
    
    product_data = ProductCreate(
        name="New Product",
        price=100.0,
        quantity=10,
        category_id=1,
    )
    
    # Should not raise exception
    await check_existing_product_using_name(product=product_data, db=mock_db)
```

**Mock Types**:
- `Mock()`: Synchronous mock object
- `AsyncMock()`: Asynchronous mock object
- `patch()`: Replace real objects with mocks temporarily

**Documentation**: [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

---

### 6. Exception Testing with `pytest.raises`

**What it is**: Verify that code raises expected exceptions  
**Why use it**: Ensure error handling works correctly

**Example from `test_product_service_async.py`:**

```python
@pytest.mark.asyncio
async def test_product_exists_raises_exception(self):
    """Test that function raises exception when product exists"""
    mock_db = AsyncMock(spec=AsyncSession)
    
    # Setup mock to return existing product
    mock_product = Product(id=1, name="Existing Product")
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = mock_product
    mock_db.execute.return_value = mock_result
    
    product_data = ProductCreate(name="Existing Product", price=100.0)
    
    # Verify exception is raised
    with pytest.raises(DatabaseException) as exc_info:
        await check_existing_product_using_name(
            product=product_data, 
            db=mock_db
        )
    
    # Verify exception message
    assert "already exists" in str(exc_info.value).lower()
```

**Key Points**:
- Use `with pytest.raises(ExceptionType)` context manager
- Access exception details with `exc_info.value`
- Verify exception message or attributes

**Documentation**: [https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)

---

### 7. Fixture Dependencies

**What it is**: Fixtures that depend on other fixtures  
**Why use it**: Build complex test setups from simple building blocks

**Example from `conftest.py`:**

```python
@pytest.fixture
def staff_user(test_db):
    """Create staff user - depends on test_db fixture"""
    user = User(
        name="Staff User",
        email="staff@test.com",
        password=hash_password("password123"),
        role="staff",
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture
def staff_headers(staff_user):
    """Generate JWT headers - depends on staff_user fixture"""
    token = create_access_token(
        data={"sub": staff_user.email, "role": staff_user.role}
    )
    return {"Authorization": f"Bearer {token}"}
```

**Dependency Chain**:
```
test_db → staff_user → staff_headers → test function
```

**Documentation**: [https://docs.pytest.org/en/stable/fixture.html#fixtures-can-request-other-fixtures](https://docs.pytest.org/en/stable/fixture.html#fixtures-can-request-other-fixtures)

---

### 8. FastAPI TestClient

**What it is**: Special client for testing FastAPI applications  
**Why use it**: Make HTTP requests to API without running a server

**Example from `test_category_routes.py`:**

```python
def test_staff_can_view_all_categories(
    self, client: TestClient, staff_headers: dict, sample_category
):
    """Test API endpoint with TestClient"""
    # Make GET request to API
    response = client.get("/category/all", headers=staff_headers)
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "all categories" in data["message"]
```

**Available Methods**:
- `client.get(url, headers=...)` - GET request
- `client.post(url, json=..., headers=...)` - POST request
- `client.put(url, json=..., headers=...)` - PUT request
- `client.patch(url, json=..., headers=...)` - PATCH request
- `client.delete(url, headers=...)` - DELETE request

**Documentation**: [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)

---

### 9. Test Organization with Docstrings

**What it is**: Descriptive strings explaining what each test does  
**Why use it**: Makes test reports readable and helps debugging

**Example:**

```python
class TestGetAllCategories:
    """Test suite for retrieving all categories"""

    def test_staff_can_view_all_categories(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """
        Test that staff can view all categories.
        All authenticated roles (staff, manager, admin) can view categories.
        This is a read-only operation accessible to all users.
        """
        response = client.get("/category/all", headers=staff_headers)
        assert response.status_code == 200
```

**Best Practices**:
- Class docstring: Describe the feature being tested
- Function docstring: Describe the specific test case
- Keep docstrings concise but informative

---

### 10. Assertions

**What it is**: Statements that verify expected outcomes  
**Why use it**: Core of testing - checks if code behaves correctly

**Common Assertion Patterns in This Project:**

```python
# Status code assertions
assert response.status_code == 200
assert response.status_code == 500

# Data structure assertions
assert data["status"] == "success"
assert "error" in data
assert "all categories" in data["message"]

# Type assertions
assert isinstance(data["message"]["all categories"], list)

# Length assertions
assert len(data["message"]["all categories"]) >= 1

# Membership assertions
assert response.status_code in [200, 403]
```

**Documentation**: [https://docs.pytest.org/en/stable/how-to/assert.html](https://docs.pytest.org/en/stable/how-to/assert.html)

---

### 11. Database Testing with SQLAlchemy

**What it is**: Testing database operations with in-memory SQLite  
**Why use it**: Fast, isolated tests without affecting real database

**Example from `test_category_routes.py`:**

```python
def test_view_multiple_categories(
    self, client: TestClient, staff_headers: dict, test_db: Session
):
    """Test viewing multiple categories"""
    # Create test data directly in database
    categories = [
        Category(id=1, name="electronics"),
        Category(id=2, name="furniture"),
        Category(id=3, name="clothing"),
    ]
    for cat in categories:
        test_db.add(cat)
    test_db.commit()
    
    # Test API endpoint
    response = client.get("/category/all", headers=staff_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["message"]["all categories"]) == 3
```

**Key Points**:
- Each test gets a fresh database (scope="function")
- Use SQLite in-memory for speed
- Database is automatically cleaned up after test

---

### 12. JWT Authentication Testing

**What it is**: Testing endpoints that require authentication  
**Why use it**: Verify security and role-based access control

**Example from `conftest.py` and usage:**

```python
# Fixture creates authenticated headers
@pytest.fixture
def admin_headers(admin_user):
    """Generate JWT token headers for admin user"""
    token = create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}

# Usage in test
def test_admin_can_delete_category(
    self, client: TestClient, admin_headers: dict, sample_category
):
    """Test that admin can delete categories"""
    response = client.delete(
        f"/category/delete?category_id={sample_category.id}",
        headers=admin_headers  # JWT token included
    )
    assert response.status_code == 200
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/api/test_category_routes.py
```

### Run Specific Test Class

```bash
pytest tests/api/test_category_routes.py::TestGetAllCategories
```

### Run Specific Test Function

```bash
pytest tests/api/test_category_routes.py::TestGetAllCategories::test_staff_can_view_all_categories
```

### Run Tests by Directory

```bash
pytest tests/api/          # All API tests
pytest tests/core/         # All core tests
pytest tests/services/     # All service tests
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Print Statements

```bash
pytest -s
```

### Run and Stop on First Failure

```bash
pytest -x
```

### Run Only Failed Tests from Last Run

```bash
pytest --lf
```

### Disable Cache (for CI/CD)

```bash
pytest -p no:cacheprovider
```

**Documentation**: [https://docs.pytest.org/en/stable/how-to/usage.html](https://docs.pytest.org/en/stable/how-to/usage.html)

---

## Test Coverage Analysis

### What is Coverage?

**Coverage** measures how much of your code is tested. Higher coverage means more code is verified.

### Running Coverage

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/
```

### Viewing Coverage Report

After running with `--cov-report=html`, open `htmlcov/index.html` in a browser to see:
- Which lines are tested (green)
- Which lines are not tested (red)
- Coverage percentage per file

**Documentation**: [https://pytest-cov.readthedocs.io/](https://pytest-cov.readthedocs.io/)

---

## Best Practices Used in This Project

### 1. Test Isolation
- Each test gets a fresh database
- No test depends on another test
- Tests can run in any order

### 2. Descriptive Names
- Test functions start with `test_`
- Names describe what is being tested
- Example: `test_staff_can_view_all_categories`

### 3. Arrange-Act-Assert Pattern

```python
def test_create_category(self, client, admin_headers):
    # Arrange: Set up test data
    category_data = {"id": 1, "name": "electronics"}
    
    # Act: Perform the action
    response = client.post("/category", json=category_data, headers=admin_headers)
    
    # Assert: Verify the outcome
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

### 4. One Assertion Per Concept
- Test one thing at a time
- Multiple assertions OK if testing same concept
- Easier to debug when tests fail

### 5. Use Fixtures for Setup
- Don't repeat setup code
- Keep tests focused on behavior
- Reuse common configurations

### 6. Test Both Success and Failure
- Test happy path (everything works)
- Test error cases (invalid input, missing data)
- Test edge cases (empty lists, zero values)

---

## Common Testing Patterns in This Project

### Pattern 1: Testing CRUD Operations

```python
# Create
def test_create_category(self, client, admin_headers):
    response = client.post("/category", json={"id": 1, "name": "test"}, headers=admin_headers)
    assert response.status_code == 200

# Read
def test_get_category(self, client, staff_headers, sample_category):
    response = client.get(f"/category?category_id={sample_category.id}", headers=staff_headers)
    assert response.status_code == 200

# Update
def test_update_category(self, client, manager_headers, sample_category):
    response = client.put("/category/update", json={"id": sample_category.id, "name": "updated"}, headers=manager_headers)
    assert response.status_code == 200

# Delete
def test_delete_category(self, client, admin_headers, sample_category):
    response = client.delete(f"/category/delete?category_id={sample_category.id}", headers=admin_headers)
    assert response.status_code == 200
```

### Pattern 2: Testing Role-Based Access

```python
def test_staff_cannot_delete(self, client, staff_headers, sample_category):
    """Staff should not be able to delete"""
    response = client.delete(f"/category/delete?category_id={sample_category.id}", headers=staff_headers)
    assert response.status_code == 500  # Unauthorized

def test_admin_can_delete(self, client, admin_headers, sample_category):
    """Admin should be able to delete"""
    response = client.delete(f"/category/delete?category_id={sample_category.id}", headers=admin_headers)
    assert response.status_code == 200  # Success
```

### Pattern 3: Testing Error Handling

```python
def test_create_duplicate_category(self, client, admin_headers, sample_category):
    """Test that creating duplicate category fails"""
    response = client.post(
        "/category",
        json={"id": sample_category.id, "name": "duplicate"},
        headers=admin_headers
    )
    data = response.json()
    assert data["status"] == "error"
    assert "already exists" in data["message"]["response"].lower()
```

---

## Troubleshooting Common Issues

### Issue 1: Tests Pass Locally but Fail in CI/CD

**Cause**: Environment differences  
**Solution**: 
- Check Python version matches
- Verify all dependencies in `requirements.txt`
- Use same database (SQLite in-memory for both)

### Issue 2: Fixture Not Found

**Error**: `fixture 'test_db' not found`  
**Solution**: 
- Ensure `conftest.py` is in tests directory
- Check fixture name spelling
- Verify fixture scope is appropriate

### Issue 3: Async Tests Not Running

**Error**: Tests are skipped or fail with async errors  
**Solution**:
- Install `pytest-asyncio`: `pip install pytest-asyncio`
- Add `@pytest.mark.asyncio` decorator
- Use `async def` for test function

### Issue 4: Database Conflicts

**Error**: Database locked or constraint violations  
**Solution**:
- Use `scope="function"` for database fixtures
- Ensure database is cleaned up in fixture teardown
- Check for foreign key constraints

---

## Summary

This project uses pytest extensively with the following key features:

✅ **Test Classes** - Organize tests by feature  
✅ **Fixtures** - Reusable setup code in `conftest.py`  
✅ **Async Testing** - Test async functions with `@pytest.mark.asyncio`  
✅ **Mocking** - Isolate tests with `unittest.mock`  
✅ **Exception Testing** - Verify error handling with `pytest.raises`  
✅ **FastAPI TestClient** - Test API endpoints without running server  
✅ **Database Testing** - In-memory SQLite for fast, isolated tests  
✅ **JWT Authentication** - Test role-based access control  
✅ **Descriptive Docstrings** - Clear test documentation  
✅ **Best Practices** - Isolation, AAA pattern, one concept per test

**Key Takeaway**: Pytest makes testing simple and powerful. Tests ensure code quality, catch bugs early, and give confidence when making changes.

---

## Additional Resources

- **Pytest Official Docs**: [https://docs.pytest.org/](https://docs.pytest.org/)
- **Pytest Fixtures**: [https://docs.pytest.org/en/stable/fixture.html](https://docs.pytest.org/en/stable/fixture.html)
- **Pytest-Asyncio**: [https://pytest-asyncio.readthedocs.io/](https://pytest-asyncio.readthedocs.io/)
- **FastAPI Testing**: [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)
- **Python Mocking**: [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)
- **Pytest Best Practices**: [https://docs.pytest.org/en/stable/goodpractices.html](https://docs.pytest.org/en/stable/goodpractices.html)
