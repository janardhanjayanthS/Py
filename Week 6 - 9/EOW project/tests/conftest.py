# import os
# from unittest.mock import MagicMock, patch
#
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import StaticPool
# from src.core.database import get_db
# from src.core.jwt import create_access_token
# from src.core.utility import hash_password
# from src.models.base import Base
# from src.models.user import User
#
#
# # Environment variables are set by pytest_plugin_env.py before any imports
# # Mock constants to avoid import-time issues
# @pytest.fixture(scope="session", autouse=True)
# def ensure_test_environment():
#     """Ensure test environment is maintained throughout session"""
#     # Verify environment variables are set
#     assert os.getenv("OPENAI_API_KEY") is not None
#     assert os.getenv("JWT_SECRET_KEY") is not None
#     assert os.getenv("POSTGRESQL_PWD") is not None
#     yield
#
#
# # Mock vector store globally
# @pytest.fixture(scope="session", autouse=True)
# def mock_vector_store_global():
#     """Mock the vector store for all tests"""
#     mock_store = MagicMock()
#     mock_store.add_documents = MagicMock(return_value=None)
#     mock_store.similarity_search = MagicMock(return_value=[])
#
#     with patch("src.core.secrets.vector_db.get_vector_store", return_value=mock_store):
#         yield mock_store
#
#
# # Mock LangChain components
# @pytest.fixture(scope="session", autouse=True)
# def mock_langchain_components():
#     """Mock LangChain components globally"""
#     with (
#         patch("src.core.ai_utility.ChatOpenAI") as mock_openai,
#         patch("src.core.database_utility.PyMuPDFLoader") as mock_pdf_loader,
#         patch("src.core.database_utility.WebBaseLoader") as mock_web_loader,
#     ):
#         # Mock ChatOpenAI responses
#         mock_ai_instance = MagicMock()
#         mock_ai_instance.ainvoke = MagicMock()
#         mock_ai_instance.invoke = MagicMock()
#         mock_openai.return_value = mock_ai_instance
#
#         # Mock PDF loader
#         mock_pdf_instance = MagicMock()
#         mock_pdf_instance.load = MagicMock(return_value=[])
#         mock_pdf_loader.return_value = mock_pdf_instance
#
#         # Mock Web loader
#         mock_web_instance = MagicMock()
#         mock_web_instance.load = MagicMock(return_value=[])
#         mock_web_loader.return_value = mock_web_instance
#
#         yield {
#             "openai": mock_openai,
#             "pdf_loader": mock_pdf_loader,
#             "web_loader": mock_web_loader,
#         }
#
#
# # In-memory SQLite database for testing
# @pytest.fixture(scope="function")
# def test_db_engine():
#     """Create an in-memory SQLite database engine for testing"""
#     engine = create_engine(
#         "sqlite:///:memory:",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     Base.metadata.create_all(bind=engine)
#     yield engine
#     Base.metadata.drop_all(bind=engine)
#     engine.dispose()
#
#
# @pytest.fixture(scope="function")
# def test_db_session(test_db_engine):
#     """Create a database session for testing"""
#     TestingSessionLocal = sessionmaker(
#         autocommit=False, autoflush=False, bind=test_db_engine
#     )
#     session = TestingSessionLocal()
#     yield session
#     session.close()
#
#
# @pytest.fixture(scope="function")
# def client(test_db_session):
#     """Create a TestClient with database dependency override"""
#     from main import app
#
#     def override_get_db():
#         try:
#             yield test_db_session
#         finally:
#             pass
#
#     app.dependency_overrides[get_db] = override_get_db
#
#     with TestClient(app) as test_client:
#         yield test_client
#
#     app.dependency_overrides.clear()
#
#
# # Test user fixtures
# @pytest.fixture
# def test_user_data():
#     """Provides sample user data for registration"""
#     return {
#         "name": "Test User",
#         "email": "testuser@example.com",
#         "password": "securepassword123",
#     }
#
#
# @pytest.fixture
# def test_user(test_db_session, test_user_data):
#     """Create and return a test user in the database"""
#     user = User(
#         name=test_user_data["name"],
#         email=test_user_data["email"],
#         password_hash=hash_password(test_user_data["password"]),
#     )
#     test_db_session.add(user)
#     test_db_session.commit()
#     test_db_session.refresh(user)
#     return user
#
#
# @pytest.fixture
# def auth_token(test_user):
#     """Generate a valid JWT token for the test user"""
#     token = create_access_token(
#         data={"email": test_user.email, "id": test_user.id}, expires_delta=None
#     )
#     return token
#
#
# @pytest.fixture
# def auth_headers(auth_token):
#     """Return authorization headers with Bearer token"""
#     return {"Authorization": f"Bearer {auth_token}"}
#
#
# # Mock file fixtures
# @pytest.fixture
# def mock_pdf_file():
#     """Create a mock PDF file for upload testing"""
#     return b"%PDF-1.4 mock pdf content"
#
#
# @pytest.fixture
# def mock_pdf_upload(mock_pdf_file):
#     """Create a mock UploadFile for testing"""
#     from io import BytesIO
#
#     return ("test_document.pdf", BytesIO(mock_pdf_file), "application/pdf")
#
#
# # Mock AI response fixtures
# @pytest.fixture
# def mock_ai_response():
#     """Create a mock AI response object"""
#     mock_response = MagicMock()
#     mock_response.content = "This is a test AI response"
#     mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}
#     return mock_response
#
#
# @pytest.fixture
# def mock_rag_response():
#     """Create a mock RAG chain response"""
#     from langchain_core.documents import Document
#
#     mock_response = MagicMock()
#     mock_response.content = "This is a RAG response based on documents"
#     mock_response.usage_metadata = {"input_tokens": 500, "output_tokens": 200}
#
#     # Mock documents for context
#     mock_docs = [
#         Document(
#             page_content="Sample document content",
#             metadata={"title": "Test Document", "source": "test.pdf", "user_id": 1},
#         )
#     ]
#
#     return mock_response, mock_docs
#
#
# # Mock database operation fixtures
# @pytest.fixture
# def mock_psycopg_connection():
#     """Mock psycopg connection for hash checking"""
#     with patch("src.core.database_utility.psycopg.connect") as mock_connect:
#         mock_conn = MagicMock()
#         mock_cursor = MagicMock()
#         mock_cursor.fetchall = MagicMock(return_value=[])
#         mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
#         mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=None)
#         mock_connect.return_value.__enter__ = MagicMock(return_value=mock_conn)
#         mock_connect.return_value.__exit__ = MagicMock(return_value=None)
#         yield mock_cursor
#
#
# # Cache fixtures
# @pytest.fixture
# def setup_cache_table(test_db_session):
#     """Set up the cache table for testing"""
#     from src.models.cache import UserLLMCache
#
#     Base.metadata.create_all(bind=test_db_session.bind)
#     yield
#     test_db_session.query(UserLLMCache).delete()
#     test_db_session.commit()


from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# Mock the entire database module before any application imports
@pytest.fixture(scope="session", autouse=True)
def mock_database_modules():
    """Mock database modules for all tests"""
    with (
        patch("src.core.database.engine") as mock_engine,
        patch("src.core.database.session_local") as mock_session_local,
        patch("src.core.constants.get_database_connection_string") as mock_conn,
    ):
        # Mock connection string
        mock_conn.return_value = "sqlite:///:memory:"

        # Create a real SQLite engine for tests
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        mock_engine.return_value = test_engine

        # Create session factory
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=test_engine
        )
        mock_session_local.return_value = TestingSessionLocal()

        yield {
            "engine": mock_engine,
            "session_local": mock_session_local,
        }


# Mock external dependencies
@pytest.fixture(scope="session", autouse=True)
def mock_external_dependencies():
    """Mock external dependencies for all tests"""
    with (
        patch("src.core.constants.get_openai_key") as mock_openai_key,
        patch("src.core.constants.OpenAIEmbeddings") as mock_embeddings,
        patch("src.core.secrets.openai.get_openai_key") as mock_openai_key_secret,
    ):
        mock_openai_key.return_value = "test-openai-key"
        mock_openai_key_secret.return_value = "test-openai-key"

        # Mock embeddings
        mock_embedding_instance = MagicMock()
        mock_embeddings.return_value = mock_embedding_instance

        yield {
            "openai_key": mock_openai_key,
            "embeddings": mock_embeddings,
        }


# In-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db_engine():
    """Create an in-memory SQLite database engine for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Import all models to ensure they're registered with Base
    from src.models.base import Base
    from src.models.cache import UserLLMCache
    from src.models.user import User

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a database session for testing"""
    testing_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )
    session = testing_session_local()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(test_db_session):
    """Create a TestClient with database dependency override"""
    from src.api.main import app
    from src.core.database import get_db

    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Test user fixtures
@pytest.fixture
def test_user_data():
    """Provides sample user data for registration"""
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword123",
    }


@pytest.fixture
def test_user(test_db_session, test_user_data):
    """Create and return a test user in the database"""
    from src.core.utility import hash_password
    from src.models.user import User

    user = User(
        name=test_user_data["name"],
        email=test_user_data["email"],
        password_hash=hash_password(test_user_data["password"]),
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """Generate a valid JWT token for the test user"""
    from src.core.jwt import create_access_token

    token = create_access_token(
        data={"email": test_user.email, "id": test_user.id}, expires_delta=None
    )
    return token


@pytest.fixture
def auth_headers(auth_token):
    """Return authorization headers with Bearer token"""
    return {"Authorization": f"Bearer {auth_token}"}


# Mock file fixtures
@pytest.fixture
def mock_pdf_file():
    """Create a mock PDF file for upload testing"""
    return b"%PDF-1.4 mock pdf content"


# Mock vector store globally
@pytest.fixture(scope="session", autouse=True)
def mock_vector_store_global():
    """Mock the vector store for all tests"""
    mock_store = MagicMock()
    mock_store.add_documents = MagicMock(return_value=None)
    mock_store.similarity_search = MagicMock(return_value=[])

    with patch("src.core.secrets.vector_db.get_vector_store", return_value=mock_store):
        yield mock_store
