from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.api.main import app
from src.core.db_config import Base, get_db
from src.models.models import Product

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
    Create a fresh db for each test
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
    create a test client with dependency override

    Args:
        test_db: test db instance
    """

    def override_get_db():
        try:
            test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app=app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
