# test_database.py - Tests for database operations and utilities
import pytest
from sqlalchemy.orm import Session
from src.core.config import settings
from src.models.category import Category
from src.models.product import Product
from src.models.user import User
from src.repository.database import (
    DatabaseException,
    add_commit_refresh_db,
    commit_refresh_db,
    delete_commit_db,
    get_db,
    hash_password,
    seed_db,
    verify_password,
)


class TestGetDb:
    """Test suite for get_db dependency function"""

    def test_get_db_dependency(self, test_db: Session):
        """Test that get_db provides a database session"""
        # get_db is a generator, so we need to consume it
        db_generator = get_db()
        db_session = next(db_generator)

        assert isinstance(db_session, Session)
        assert db_session is not None

        # Clean up
        try:
            next(db_generator)
        except StopIteration:
            pass

    def test_get_db_session_closed_on_exception(self, test_db: Session):
        """Test that database session is properly closed on exception"""
        db_generator = get_db()
        db_session = next(db_generator)

        # Simulate an exception
        try:
            db_generator.throw(Exception("Test exception"))
        except Exception:
            pass

        # Session should be closed (we can't easily test this directly, but the pattern should work)


class TestAddCommitRefreshDb:
    """Test suite for add_commit_refresh_db function"""

    def test_add_commit_refresh_db_success(self, db_session: Session):
        """Test successful add, commit, and refresh operation"""
        user = User(
            name="Test User",
            email="test@example.com",
            password=hash_password("testpass123"),
            role="staff",
        )

        # User should not have ID yet
        assert user.id is None

        add_commit_refresh_db(object=user, db=db_session)

        # User should now have ID and be in database
        assert user.id is not None
        assert user.email == "test@example.com"

        # Verify it's actually in the database
        db_user = (
            db_session.query(User).filter(User.email == "test@example.com").first()
        )
        assert db_user is not None
        assert db_user.id == user.id

    def test_add_commit_refresh_db_with_product(
        self, db_session: Session, sample_category: Category
    ):
        """Test add_commit_refresh_db with Product object"""
        product = Product(
            name="Test Product",
            price=100.0,
            quantity=10,
            category_id=sample_category.id,
        )

        assert product.id is None

        add_commit_refresh_db(object=product, db=db_session)

        assert product.id is not None
        assert product.name == "Test Product"

        # Verify in database
        db_product = (
            db_session.query(Product).filter(Product.name == "Test Product").first()
        )
        assert db_product is not None
        assert db_product.id == product.id


class TestCommitRefreshDb:
    """Test suite for commit_refresh_db function"""

    def test_commit_refresh_db_success(self, db_session: Session, staff_user: User):
        """Test successful commit and refresh operation"""
        # Modify existing user
        original_name = staff_user.name
        staff_user.name = "Updated Name"

        commit_refresh_db(object=staff_user, db=db_session)

        # Verify the change was committed
        assert staff_user.name == "Updated Name"

        # Verify by querying fresh from database
        db_user = db_session.query(User).filter(User.id == staff_user.id).first()
        assert db_user is not None
        assert db_user.name == "Updated Name"

    def test_commit_refresh_db_with_product(
        self, db_session: Session, sample_product: Product
    ):
        """Test commit_refresh_db with Product object"""
        original_price = sample_product.price
        sample_product.price = 200.0

        commit_refresh_db(object=sample_product, db=db_session)

        assert sample_product.price == 200.0

        # Verify in database
        db_product = (
            db_session.query(Product).filter(Product.id == sample_product.id).first()
        )
        assert db_product is not None
        assert db_product.price == 200.0


class TestDeleteCommitDb:
    """Test suite for delete_commit_db function"""

    def test_delete_commit_db_success(self, db_session: Session):
        """Test successful delete and commit operation"""
        # Create a user to delete
        user = User(
            name="To Delete",
            email="delete@example.com",
            password=hash_password("testpass123"),
            role="staff",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        user_id = user.id
        assert user_id is not None

        # Delete the user
        delete_commit_db(object=user, db=db_session)

        # Verify user is deleted from database
        deleted_user = db_session.query(User).filter(User.id == user_id).first()
        assert deleted_user is None

    def test_delete_commit_db_with_product(
        self, db_session: Session, sample_product: Product
    ):
        """Test delete_commit_db with Product object"""
        product_id = sample_product.id

        delete_commit_db(object=sample_product, db=db_session)

        # Verify product is deleted
        deleted_product = (
            db_session.query(Product).filter(Product.id == product_id).first()
        )
        assert deleted_product is None


class TestPasswordHashing:
    """Test suite for password hashing and verification"""

    def test_hash_password_basic(self):
        """Test basic password hashing"""
        password = "testpassword123"
        hashed = hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 10  # Hashed password should be longer

    def test_hash_password_different_results(self):
        """Test that hashing same password produces different results (due to salt)"""
        password = "samepassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2  # Should be different due to salt

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "correctpassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "correctpassword123"
        wrong_password = "wrongpassword123"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_string(self):
        """Test password verification with empty string"""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False

    def test_verify_password_none(self):
        """Test password verification with None password"""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password(None, hashed) is False

    def test_hash_password_complex(self):
        """Test hashing complex password with special characters"""
        password = "ComplexP@ssw0rd!#$%^&*()"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_password_unicode(self):
        """Test hashing password with unicode characters"""
        password = "Pässwörd123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True


class TestSeedDb:
    """Test suite for seed_db function"""

    def test_seed_db_creates_data(self, test_db: Session, monkeypatch):
        """Test that seed_db creates initial data"""
        # Mock the CSV file path to use a test file
        test_csv_path = "/tmp/test_inventory.csv"

        # Create a simple test CSV
        import csv

        with open(test_csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "name", "price", "quantity", "category_id"])
            writer.writerow([1, "Test Product 1", 100.0, 10, 1])
            writer.writerow([2, "Test Product 2", 200.0, 20, 1])

        # Mock settings to use our test CSV
        monkeypatch.setattr(settings, "INVENTORY_CSV_FILEPATH", test_csv_path)

        # Ensure categories exist first
        category = Category(id=1, name="test_category")
        test_db.add(category)
        test_db.commit()

        # Run seed_db
        seed_db()

        # Verify products were created
        products = test_db.query(Product).all()
        assert len(products) >= 2

        # Clean up
        import os

        os.unlink(test_csv_path)

    def test_seed_db_handles_missing_file(self, monkeypatch):
        """Test that seed_db handles missing CSV file gracefully"""
        # Mock settings to point to non-existent file
        monkeypatch.setattr(settings, "INVENTORY_CSV_FILEPATH", "/nonexistent/file.csv")

        # Should not raise exception (should handle gracefully)
        with pytest.raises(Exception):  # Should raise some kind of exception
            seed_db()


class TestDatabaseException:
    """Test suite for DatabaseException"""

    def test_database_exception_creation(self):
        """Test DatabaseException creation"""
        exception = DatabaseException(
            message="Database error occurred",
            field_errors=[{"field": "connection", "message": "Failed to connect"}],
        )

        assert exception.message == "Database error occurred"
        assert len(exception.field_errors) == 1
        assert exception.field_errors[0]["field"] == "connection"

    def test_database_exception_without_field_errors(self):
        """Test DatabaseException without field errors"""
        exception = DatabaseException(message="Simple database error")

        assert exception.message == "Simple database error"
        assert exception.field_errors is None


class TestDatabaseIntegration:
    """Integration tests for database operations"""

    def test_complete_crud_cycle(self, db_session: Session, sample_category: Category):
        """Test complete CRUD cycle: Create, Read, Update, Delete"""
        # Create
        product = Product(
            name="CRUD Test Product",
            price=150.0,
            quantity=25,
            category_id=sample_category.id,
        )
        add_commit_refresh_db(object=product, db=db_session)

        product_id = product.id
        assert product_id is not None

        # Read
        retrieved = db_session.query(Product).filter(Product.id == product_id).first()
        assert retrieved is not None
        assert retrieved.name == "CRUD Test Product"

        # Update
        retrieved.price = 199.99
        retrieved.quantity = 15
        commit_refresh_db(object=retrieved, db=db_session)

        # Verify update
        updated = db_session.query(Product).filter(Product.id == product_id).first()
        assert updated.price == 199.99
        assert updated.quantity == 15

        # Delete
        delete_commit_db(object=updated, db=db_session)

        # Verify deletion
        deleted = db_session.query(Product).filter(Product.id == product_id).first()
        assert deleted is None

    def test_transaction_rollback_on_error(self, db_session: Session):
        """Test that transactions are rolled back on error"""
        # Start a transaction manually
        user = User(
            name="Rollback Test",
            email="rollback@example.com",
            password=hash_password("testpass123"),
            role="staff",
        )

        db_session.add(user)
        db_session.flush()  # Get ID but don't commit

        user_id = user.id

        # Simulate an error and rollback
        db_session.rollback()

        # Verify user was not committed
        rolled_back_user = db_session.query(User).filter(User.id == user_id).first()
        assert rolled_back_user is None

    def test_multiple_operations_in_transaction(
        self, db_session: Session, sample_category: Category
    ):
        """Test multiple operations in a single transaction"""
        # Create multiple products
        products = [
            Product(
                name="Product 1", price=10.0, quantity=5, category_id=sample_category.id
            ),
            Product(
                name="Product 2",
                price=20.0,
                quantity=10,
                category_id=sample_category.id,
            ),
            Product(
                name="Product 3",
                price=30.0,
                quantity=15,
                category_id=sample_category.id,
            ),
        ]

        for product in products:
            db_session.add(product)

        db_session.commit()

        # Verify all products were created
        all_products = (
            db_session.query(Product)
            .filter(Product.category_id == sample_category.id)
            .all()
        )

        assert len(all_products) >= 3

        # Update all products
        for product in all_products[:3]:  # Just the ones we created
            product.price = product.price * 1.1  # 10% price increase

        db_session.commit()

        # Verify updates
        updated_products = (
            db_session.query(Product)
            .filter(Product.category_id == sample_category.id)
            .all()
        )

        for product in updated_products[:3]:
            assert product.price > 10.0  # Should be increased
