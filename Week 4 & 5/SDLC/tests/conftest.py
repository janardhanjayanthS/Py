# conftest.py - Modified with JWT authentication helpers and async support
from datetime import timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from src.api.main import app
from src.core.jwt import create_access_token
from src.models.category import Category
from src.models.product import Product
from src.models.user import User
from src.repository.database import Base, get_db, hash_password

# Sync database setup for legacy tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async database setup for new async tests
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=False,
)
AsyncTestingSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """
    Enable foreign key constraints.

    - For SQLite: Explicitly enables foreign keys (required)
    - For PostgreSQL: This is a no-op (foreign keys are always enabled)

    This makes the code portable across both databases.
    """
    # Check if it's SQLite by trying to execute PRAGMA
    try:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        # Not SQLite (probably PostgreSQL), which is fine - FK already enabled
        pass


@pytest.fixture
def get_csv_filepath() -> str:
    """
    Used to get csv filepath
    Returns:
        str: csv file path
    """
    return str(Path(__file__).parent.parent / "data/test_inventory.csv")


@pytest.fixture(scope="function")
async def async_test_db():
    """
    Create a fresh async database for each test function.
    This ensures test isolation - no test affects another.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncTestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client():
    """
    Create a test client with async dependency override.
    Uses SQLite in-memory database for testing with persistent session.
    """
    # Create a persistent session that will be shared across requests
    persistent_session = AsyncTestingSessionLocal()

    # Override the database dependency to use the persistent session
    async def override_get_db():
        # Create tables if they don't exist
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield persistent_session

    # Override the engine in database module for testing
    import src.repository.database

    original_engine = src.repository.database.engine
    original_session_local = src.repository.database.async_session_local

    # Set test engine and session
    src.repository.database.engine = async_engine
    src.repository.database.async_session_local = AsyncTestingSessionLocal

    # Create a test app without lifespan to avoid PostgreSQL connection
    from fastapi import FastAPI
    from src.api.routes import category, product, user
    from src.core.exception_handler import add_exception_handlers_to_app

    test_app = FastAPI()  # No lifespan for testing
    test_app.include_router(product.product)
    test_app.include_router(user.user)
    test_app.include_router(category.category)
    add_exception_handlers_to_app(app=test_app)

    test_app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app=test_app) as test_client:
            yield test_client
    finally:
        test_app.dependency_overrides.clear()
        # Clean up the persistent session
        await persistent_session.close()
        # Clean up tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        # Restore original engine and session
        src.repository.database.engine = original_engine
        src.repository.database.async_session_local = original_session_local


# ============================================================================
# LEGACY SYNC FIXTURES - For backward compatibility
# ============================================================================


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


@pytest.fixture(scope="function")
def db_session(test_db):
    """
    Alias for test_db fixture to match naming convention in service tests.
    Provides a database session for testing service layer functions.
    """
    return test_db


@pytest.fixture(scope="function")
def sync_client(test_db):
    """
    Create a test client with sync dependency override.
    For legacy tests that use sync database.
    """

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app=app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ============================================================================
# ASYNC FIXTURES - For new async architecture tests (using sync DB for simplicity)
# ============================================================================


@pytest.fixture(scope="function")
def async_test_db(test_db):
    """
    Reuse sync test_db for async tests.
    This simplifies testing by avoiding async SQLite dependencies.
    """
    return test_db


@pytest.fixture(scope="function")
def async_client(client):
    """
    Reuse sync client for async tests.
    This simplifies testing by avoiding async SQLite dependencies.
    """
    return client


@pytest.fixture
def regular_user(test_db: Session) -> User:
    """
    Create a regular user in test database.
    Regular user with basic permissions (no special roles).
    """
    user = User(
        name="Regular User",
        email="regular@test.com",
        password=hash_password("password123"),
        role="user",  # Regular user role
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def regular_token(regular_user: User) -> str:
    """
    Generate JWT token for regular user.
    Returns token string that can be used in Authorization header.
    """
    return create_access_token(
        data={"sub": regular_user.email, "role": regular_user.role},
        expires_delta=timedelta(minutes=30),
    )


@pytest.fixture
def regular_headers(regular_token: str) -> dict:
    """
    Create authorization headers for regular user.
    Returns dict ready to be used in requests: headers=regular_headers
    """
    return {"Authorization": f"Bearer {regular_token}"}


# ============================================================================
# USER FIXTURES - Create users with different roles for testing
# ============================================================================


@pytest.fixture
async def staff_user(async_test_db):
    """
    Create a staff user in async test database.
    Staff can only view products, cannot create/update/delete.
    """
    from src.models.user import User
    from src.repository.database import hash_password

    user = User(
        name="Staff User",
        email="staff@test.com",
        password=hash_password("password123"),
        role="staff",
    )
    async_test_db.add(user)
    await async_test_db.commit()
    await async_test_db.refresh(user)
    return user


@pytest.fixture
async def manager_user(async_test_db):
    """
    Create a manager user in async test database.
    Manager can view, create, and update products but cannot delete.
    """
    from src.models.user import User
    from src.repository.database import hash_password

    user = User(
        name="Manager User",
        email="manager@test.com",
        password=hash_password("password123"),
        role="manager",
    )
    async_test_db.add(user)
    await async_test_db.commit()
    await async_test_db.refresh(user)
    return user


@pytest.fixture
async def admin_user(async_test_db):
    """
    Create an admin user in async test database.
    Admin has full CRUD access to all resources.
    """
    from src.models.user import User
    from src.repository.database import hash_password

    user = User(
        name="Admin User",
        email="admin@test.com",
        password=hash_password("password123"),
        role="admin",
    )
    async_test_db.add(user)
    await async_test_db.commit()
    await async_test_db.refresh(user)
    return user


@pytest.fixture
async def regular_user(async_test_db):
    """
    Create a regular user in async test database.
    Regular user with basic permissions (no special roles).
    """
    from src.models.user import User
    from src.repository.database import hash_password

    user = User(
        name="Regular User",
        email="regular@test.com",
        password=hash_password("password123"),
        role="user",  # Regular user role
    )
    async_test_db.add(user)
    await async_test_db.commit()
    await async_test_db.refresh(user)
    return user


# ============================================================================
# TOKEN FIXTURES - Generate JWT tokens for authentication
# ============================================================================


@pytest.fixture
async def staff_token(staff_user):
    """
    Generate JWT token for staff user.
    Returns token string that can be used in Authorization header.
    """
    return create_access_token(
        data={"sub": staff_user.email, "role": staff_user.role},
        expires_delta=timedelta(minutes=30),
    )


@pytest.fixture
async def manager_token(manager_user):
    """Generate JWT token for manager user"""
    return create_access_token(
        data={"sub": manager_user.email, "role": manager_user.role},
        expires_delta=timedelta(minutes=30),
    )


@pytest.fixture
async def admin_token(admin_user):
    """Generate JWT token for admin user"""
    return create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role},
        expires_delta=timedelta(minutes=30),
    )


@pytest.fixture
async def regular_token(regular_user):
    """
    Generate JWT token for regular user.
    Returns token string that can be used in Authorization header.
    """
    return create_access_token(
        data={"sub": regular_user.email, "role": regular_user.role},
        expires_delta=timedelta(minutes=30),
    )


# ============================================================================
# HEADER FIXTURES - Pre-formatted authorization headers
# ============================================================================


@pytest.fixture
async def staff_headers(staff_token):
    """
    Create authorization headers for staff user.
    Returns dict ready to be used in requests: headers=staff_headers
    """
    return {"Authorization": f"Bearer {staff_token}"}


@pytest.fixture
async def manager_headers(manager_token):
    """Create authorization headers for manager user"""
    return {"Authorization": f"Bearer {manager_token}"}


@pytest.fixture
async def admin_headers(admin_token):
    """Create authorization headers for admin user"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
async def regular_headers(regular_token):
    """
    Create authorization headers for regular user.
    Returns dict ready to be used in requests: headers=regular_headers
    """
    return {"Authorization": f"Bearer {regular_token}"}


# ============================================================================
# DATA FIXTURES - Sample data for testing
# ============================================================================


@pytest.fixture
def sample_category(test_db: Session) -> Category:
    """
    Create a sample category in test database.
    Many product tests need a category to exist.
    """
    category = Category(id=1, name="electronics")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    return category


@pytest.fixture
def sample_product(test_db: Session, sample_category: Category) -> Product:
    """
    Create a sample product in test database.
    Linked to sample_category for proper foreign key relationship.
    """
    product = Product(
        id=1,
        name="Test Laptop",
        price=999,
        quantity=10,
        category_id=sample_category.id,
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)
    return product


@pytest.fixture
def multiple_products(test_db: Session, sample_category: Category) -> list:
    """
    Create multiple products for testing list endpoints.
    Returns list of Product objects.
    """
    products = [
        Product(
            id=1,
            name="Laptop",
            price=1500,
            quantity=5,
            category_id=sample_category.id,
        ),
        Product(
            id=2,
            name="Mouse",
            price=50,
            quantity=20,
            category_id=sample_category.id,
        ),
        Product(
            id=3,
            name="Keyboard",
            price=100,
            quantity=15,
            category_id=sample_category.id,
        ),
    ]
    for product in products:
        test_db.add(product)
    test_db.commit()
    for product in products:
        test_db.refresh(product)
    return products


# ============================================================================
# HELPER FUNCTION - For generating tokens on the fly
# ============================================================================


def create_test_token(email: str, role: str) -> str:
    """
    Helper function to create JWT token with custom email and role.
    Useful for testing edge cases with specific user attributes.

    Args:
        email: User email to encode in token
        role: User role to encode in token

    Returns:
        JWT token string
    """
    return create_access_token(
        data={"sub": email, "role": role}, expires_delta=timedelta(minutes=30)
    )


# ============================================================================
# ADDITIONAL FIXTURES FOR COMPREHENSIVE TESTING
# ============================================================================


@pytest.fixture
def multiple_categories(test_db: Session) -> list:
    """
    Create multiple categories for testing category-specific operations.
    Returns list of Category objects.
    """
    categories = [
        Category(id=1, name="electronics"),
        Category(id=2, name="clothing"),
        Category(id=3, name="books"),
        Category(id=4, name="home"),
    ]
    for category in categories:
        test_db.add(category)
    test_db.commit()
    for category in categories:
        test_db.refresh(category)
    return categories


@pytest.fixture
def products_with_different_categories(
    test_db: Session, multiple_categories: list
) -> list:
    """
    Create products across different categories for testing category filtering.
    Returns list of Product objects.
    """
    products = [
        Product(
            id=1, name="Laptop", price=1500, quantity=5, category_id=1
        ),  # electronics
        Product(id=2, name="T-Shirt", price=25, quantity=50, category_id=2),  # clothing
        Product(
            id=3, name="Python Book", price=45, quantity=20, category_id=3
        ),  # books
        Product(id=4, name="Coffee Maker", price=89, quantity=8, category_id=4),  # home
        Product(
            id=5, name="Mouse", price=30, quantity=25, category_id=1
        ),  # electronics
    ]
    for product in products:
        test_db.add(product)
    test_db.commit()
    for product in products:
        test_db.refresh(product)
    return products


@pytest.fixture
def expired_token():
    """
    Create an expired JWT token for testing authentication expiration.
    """
    return create_access_token(
        data={"sub": "expired@test.com", "role": "staff"},
        expires_delta=timedelta(seconds=-1),  # Already expired
    )


@pytest.fixture
def invalid_token():
    """
    Create an invalid JWT token for testing authentication failures.
    """
    return "invalid.jwt.token"


@pytest.fixture
def sample_product_data():
    """
    Sample product data for testing product creation.
    Returns dict with product fields.
    """
    return {
        "name": "Test Product",
        "description": "A test product for testing purposes",
        "price": 99.99,
        "stock": 10,
        "category_id": 1,
    }


@pytest.fixture
def sample_user_data():
    """
    Sample user data for testing user creation.
    Returns dict with user fields.
    """
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "TestPass123!",
        "role": "staff",
    }


@pytest.fixture
def sample_category_data():
    """
    Sample category data for testing category creation.
    Returns dict with category fields.
    """
    return {"name": "test_category"}
