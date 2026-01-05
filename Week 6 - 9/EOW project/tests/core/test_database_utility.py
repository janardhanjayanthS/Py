from unittest.mock import MagicMock, mock_open, patch

import pytest
from fastapi import HTTPException
from langchain_core.documents import Document
from src.core.utility import hash_password


class TestUserAuthentication:
    """Tests for user authentication functions"""

    def test_authenticate_user_success(self, test_db_session):
        """Test successful user authentication"""
        from src.core.database_utility import authenticate_user
        from src.models.user import User
        from src.schema.user import UserLogin

        # Create user
        user = User(
            name="Auth User",
            email="auth@test.com",
            password_hash=hash_password("correctpass"),
        )
        test_db_session.add(user)
        test_db_session.commit()

        # Authenticate
        login = UserLogin(email="auth@test.com", password="correctpass")
        result = authenticate_user(login, test_db_session)

        assert result is not None
        assert result.email == "auth@test.com"

    def test_authenticate_user_wrong_password(self, test_db_session):
        """Test authentication with wrong password"""
        from src.core.database_utility import authenticate_user
        from src.models.user import User
        from src.schema.user import UserLogin

        user = User(
            name="Auth User",
            email="auth@test.com",
            password_hash=hash_password("correctpass"),
        )
        test_db_session.add(user)
        test_db_session.commit()

        login = UserLogin(email="auth@test.com", password="wrongpass")

        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(login, test_db_session)

        assert exc_info.value.status_code == 401
        assert "Invalid email or password" in exc_info.value.detail

    def test_authenticate_user_not_found(self, test_db_session):
        """Test authentication with non-existent user"""
        from src.core.database_utility import authenticate_user
        from src.schema.user import UserLogin

        login = UserLogin(email="notfound@test.com", password="pass")

        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(login, test_db_session)

        assert exc_info.value.status_code == 401
        assert "Unable to find user" in exc_info.value.detail


class TestUserManagement:
    """Tests for user management functions"""

    def test_fetch_user_by_email_found(self, test_db_session, test_user):
        """Test fetching existing user by email"""
        from src.core.database_utility import fetch_user_by_email

        user = fetch_user_by_email(test_db_session, test_user.email)

        assert user is not None
        assert user.email == test_user.email
        assert user.id == test_user.id

    def test_fetch_user_by_email_not_found(self, test_db_session):
        """Test fetching non-existent user returns None"""
        from src.core.database_utility import fetch_user_by_email

        user = fetch_user_by_email(test_db_session, "nonexistent@test.com")

        assert user is None

    def test_check_existing_user_exists(self, test_db_session, test_user):
        """Test checking if user exists returns True"""
        from src.core.database_utility import check_existing_user_using_email
        from src.schema.user import UserCreate

        user_data = UserCreate(name="Test", email=test_user.email, password="pass")

        exists = check_existing_user_using_email(test_db_session, user_data)

        assert exists is True

    def test_check_existing_user_not_exists(self, test_db_session):
        """Test checking non-existent user returns False"""
        from src.core.database_utility import check_existing_user_using_email
        from src.schema.user import UserCreate

        user_data = UserCreate(name="New User", email="new@test.com", password="pass")

        exists = check_existing_user_using_email(test_db_session, user_data)

        assert exists is False

    def test_add_commit_refresh_db(self, test_db_session):
        """Test database add/commit/refresh helper"""
        from src.core.database_utility import add_commit_refresh_db
        from src.models.user import User

        new_user = User(
            name="New User",
            email="newuser@test.com",
            password_hash=hash_password("pass123"),
        )

        add_commit_refresh_db(new_user, test_db_session)

        # User should have ID after commit
        assert new_user.id is not None

        # Should be retrievable from DB
        retrieved = (
            test_db_session.query(User).filter_by(email="newuser@test.com").first()
        )
        assert retrieved is not None


class TestFileUpload:
    """Tests for file upload and processing functions"""

    @patch("src.core.database_utility.check_existing_hash")
    @patch("src.core.database_utility.get_documents_from_file_content")
    @patch("src.core.secrets.vector_db.get_vector_store")
    def test_add_file_as_embedding_success(
        self, mock_vector_store, mock_get_docs, mock_check_hash
    ):
        """Test successful file embedding addition"""
        from src.core.database_utility import add_file_as_embedding

        mock_check_hash.return_value = False
        mock_docs = [Document(page_content="Test", metadata={})]
        mock_get_docs.return_value = mock_docs

        mock_store = MagicMock()
        mock_vector_store.return_value = mock_store

        contents = b"PDF content"
        result = add_file_as_embedding(contents, "test.pdf", current_user_id=1)

        assert result.endswith("added successfully")

    @patch("src.core.database_utility.check_existing_hash")
    def test_add_file_as_embedding_duplicate(self, mock_check_hash):
        """Test adding duplicate file"""
        from src.core.database_utility import add_file_as_embedding

        mock_check_hash.return_value = True

        contents = b"PDF content"
        # Updated to match actual function signature
        result = add_file_as_embedding(contents, "duplicate.pdf", current_user_id=1)

        assert "already exists" in result

    @patch("src.core.database_utility.PyMuPDFLoader")
    @patch("builtins.open", new_callable=mock_open, read_data=b"PDF")
    def test_get_documents_from_file_content(self, mock_file, mock_loader):
        """Test extracting documents from PDF content"""
        from src.core.database_utility import get_documents_from_file_content

        mock_loader_instance = MagicMock()
        mock_doc = MagicMock()
        mock_doc.metadata = {}
        mock_doc.page_content = "PDF text"
        mock_loader_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_loader_instance

        contents = b"%PDF-1.4 content"
        result = get_documents_from_file_content(contents, "test.pdf", user_id=1)

        assert result is not None
        assert len(result) > 0

    @patch("src.core.database_utility.PyMuPDFLoader")
    def test_get_documents_from_file_content_error(self, mock_loader):
        """Test error handling in document extraction"""
        from src.core.database_utility import get_documents_from_file_content

        mock_loader.side_effect = Exception("PDF parsing error")

        contents = b"Invalid PDF"
        result = get_documents_from_file_content(contents, "bad.pdf", user_id=1)

        assert result is None


class TestWebContentUpload:
    """Tests for web content upload functions"""

    @patch("src.core.database_utility.check_existing_hash")
    @patch("src.core.database_utility.WebBaseLoader")
    @patch("src.core.secrets.vector_db.get_vector_store")
    @patch("src.core.database_utility.TEXT_SPLITTER")
    def test_add_web_content_success(
        self, mock_text_splitter, mock_vector_store, mock_web_loader, mock_check_hash
    ):
        """Test successful web content addition"""
        from src.core.database_utility import add_web_content_as_embedding

        mock_check_hash.return_value = False

        mock_loader_instance = MagicMock()
        mock_doc = Document(page_content="Web content", metadata={})
        mock_loader_instance.load.return_value = [mock_doc]
        mock_web_loader.return_value = mock_loader_instance

        # Mock text splitter
        chunked_doc = Document(page_content="Web content chunk", metadata={})
        mock_text_splitter.split_documents.return_value = [chunked_doc]

        mock_store = MagicMock()
        mock_vector_store.return_value = mock_store

        result = add_web_content_as_embedding(
            "https://example.com/article", current_user_id=1
        )

        assert "added successfully" in result

    @patch("src.core.database_utility.check_existing_hash")
    def test_add_web_content_duplicate(self, mock_check_hash):
        """Test adding duplicate web content"""
        from src.core.database_utility import add_web_content_as_embedding

        mock_check_hash.return_value = True

        result = add_web_content_as_embedding(
            "https://example.com/duplicate", current_user_id=1
        )

        assert "already exists" in result

    def test_get_base_url(self):
        """Test base URL extraction"""
        from src.core.database_utility import get_base_url

        url_with_fragment = "https://example.com/page#section"
        base = get_base_url(url_with_fragment)

        assert base == "https://example.com/page"
        assert "#" not in base

    def test_get_base_url_no_fragment(self):
        """Test base URL without fragment"""
        from src.core.database_utility import get_base_url

        url = "https://example.com/page"
        base = get_base_url(url)

        assert base == "https://example.com/page"

    def test_add_metadata_to_documents(self):
        """Test adding metadata to document list"""
        from src.core.database_utility import add_base_url_hash_user_id_to_metadata

        docs = [
            Document(page_content="Doc 1", metadata={}),
            Document(page_content="Doc 2", metadata={}),
        ]

        add_base_url_hash_user_id_to_metadata(
            base_url="https://example.com", hash="abc123", user_id=42, data=docs
        )

        # Check metadata was added
        for doc in docs:
            assert doc.metadata["source"] == "https://example.com"
            assert doc.metadata["hash"] == "abc123"
            assert doc.metadata["user_id"] == 42


class TestHashChecking:
    """Tests for hash existence checking"""

    @patch("src.core.database_utility.psycopg.connect")
    def test_check_existing_hash_found(self, mock_connect):
        """Test checking hash that exists"""
        from src.core.database_utility import check_existing_hash

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("row1",)]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=None)

        mock_connect.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_connect.return_value.__exit__ = MagicMock(return_value=None)

        result = check_existing_hash("existing_hash")

        assert result is True

    @patch("src.core.database_utility.psycopg.connect")
    def test_check_existing_hash_not_found(self, mock_connect):
        """Test checking hash that doesn't exist"""
        from src.core.database_utility import check_existing_hash

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=None)

        mock_connect.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_connect.return_value.__exit__ = MagicMock(return_value=None)

        result = check_existing_hash("nonexistent_hash")

        assert result is False

    @patch("src.core.database_utility.psycopg.connect")
    def test_check_existing_hash_connection_error(self, mock_connect):
        """Test hash check with connection error"""
        from src.core.database_utility import check_existing_hash

        mock_connect.side_effect = Exception("Connection failed")

        result = check_existing_hash("any_hash")

        # Should return False on error
        assert result is False
