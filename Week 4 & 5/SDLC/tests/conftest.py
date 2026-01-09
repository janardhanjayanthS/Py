# conftest.py - Modified with JWT authentication helpers
from datetime import timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from src.api.main import app
from src.core.jwt import create_access_token
from src.models.category import Category
from src.models.product import Product
from src.models.user import User
from src.repository.database import Base, get_db, hash_password

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
def test_db():
    """
    Create a fresh database for each test function.
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
def client(test_db):
    """
    Create a test client with dependency override.
    Injects test_db instead of real database.

    Args:
        test_db: test database instance
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
# USER FIXTURES - Create users with different roles for testing
# ============================================================================


@pytest.fixture
def staff_user(test_db: Session) -> User:
    """
    Create a staff user in test database.
    Staff can only view products, cannot create/update/delete.
    """
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
def manager_user(test_db: Session) -> User:
    """
    Create a manager user in test database.
    Manager can view, create, and update products but cannot delete.
    """
    user = User(
        name="Manager User",
        email="manager@test.com",
        password=hash_password("password123"),
        role="manager",
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def admin_user(test_db: Session) -> User:
    """
    Create an admin user in test database.
    Admin has full CRUD access to all resources.
    """
    user = User(
        name="Admin User",
        email="admin@test.com",
        password=hash_password("password123"),
        role="admin",
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


# ============================================================================
# TOKEN FIXTURES - Generate JWT tokens for authentication
# ============================================================================


@pytest.fixture
def staff_token(staff_user: User) -> str:
    """
    Generate JWT token for staff user.
    Returns token string that can be used in Authorization header.
    """
    return create_access_token(
        data={"sub": staff_user.email, "role": staff_user.role},
        expires_delta=timedelta(minutes=30),
    )


@pytest.fixture
def manager_token(manager_user: User) -> str:
    """Generate JWT token for manager user"""
    return create_access_token(
        data={"sub": manager_user.email, "role": manager_user.role},
        expires_delta=timedelta(minutes=30),
    )


@pytest.fixture
def admin_token(admin_user: User) -> str:
    """Generate JWT token for admin user"""
    return create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role},
        expires_delta=timedelta(minutes=30),
    )


# ============================================================================
# HEADER FIXTURES - Pre-formatted authorization headers
# ============================================================================


@pytest.fixture
def staff_headers(staff_token: str) -> dict:
    """
    Create authorization headers for staff user.
    Returns dict ready to be used in requests: headers=staff_headers
    """
    return {"Authorization": f"Bearer {staff_token}"}


@pytest.fixture
def manager_headers(manager_token: str) -> dict:
    """Create authorization headers for manager user"""
    return {"Authorization": f"Bearer {manager_token}"}


@pytest.fixture
def admin_headers(admin_token: str) -> dict:
    """Create authorization headers for admin user"""
    return {"Authorization": f"Bearer {admin_token}"}


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
