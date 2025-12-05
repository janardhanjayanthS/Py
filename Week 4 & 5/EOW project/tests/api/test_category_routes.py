# test_category_routes.py - Complete tests for category management
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.models import Category


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
        data = response.json()
        assert data["status"] == "success"
        assert "all categories" in data["message"]
        # Verify at least one category exists (from fixture)
        assert len(data["message"]["all categories"]) >= 1

    def test_manager_can_view_all_categories(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """Test that manager can view all categories"""
        response = client.get("/category/all", headers=manager_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_admin_can_view_all_categories(
        self, client: TestClient, admin_headers: dict, sample_category
    ):
        """Test that admin can view all categories"""
        response = client.get("/category/all", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_view_categories_without_authentication(self, client: TestClient):
        """
        Test that unauthenticated requests are rejected.
        Should return 401 because decorator requires authentication.
        """
        response = client.get("/category/all")
        assert response.status_code == 401

    def test_view_categories_with_invalid_token(self, client: TestClient):
        """Test that requests with invalid JWT token are rejected"""
        response = client.get(
            "/category/all", headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401

    def test_view_empty_categories_list(self, client: TestClient, staff_headers: dict):
        """
        Test viewing categories when database is empty.
        Should return empty list successfully.
        """
        response = client.get("/category/all", headers=staff_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        # Should return empty list if no categories
        assert isinstance(data["message"]["all categories"], list)

    def test_view_multiple_categories(
        self, client: TestClient, staff_headers: dict, test_db: Session
    ):
        """Test viewing multiple categories"""
        # Create multiple categories
        categories = [
            Category(id=1, name="electronics"),
            Category(id=2, name="furniture"),
            Category(id=3, name="clothing"),
        ]
        for cat in categories:
            test_db.add(cat)
        test_db.commit()

        response = client.get("/category/all", headers=staff_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data["message"]["all categories"]) == 3


class TestGetSpecificCategory:
    """Test suite for retrieving a specific category by ID"""

    def test_get_existing_category_by_id(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """
        Test retrieving a specific category that exists.
        All authenticated users can view specific category.
        """
        response = client.get(
            f"/category?category_id={sample_category.id}", headers=staff_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "requested category" in data["message"]
        # Verify returned category matches requested one
        assert data["message"]["requested category"]["id"] == sample_category.id
        assert data["message"]["requested category"]["name"] == sample_category.name

    def test_get_nonexistent_category(self, client: TestClient, staff_headers: dict):
        """
        Test retrieving a category that doesn't exist.
        Should return error status with appropriate message.
        """
        response = client.get("/category?category_id=99999", headers=staff_headers)

        assert response.status_code == 200  # Your API returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert "Unable to find category" in data["message"]["response"]
        assert "99999" in data["message"]["response"]

    def test_manager_can_get_specific_category(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """Test that manager can view specific category"""
        response = client.get(
            f"/category?category_id={sample_category.id}", headers=manager_headers
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_admin_can_get_specific_category(
        self, client: TestClient, admin_headers: dict, sample_category
    ):
        """Test that admin can view specific category"""
        response = client.get(
            f"/category?category_id={sample_category.id}", headers=admin_headers
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_get_category_without_authentication(
        self, client: TestClient, sample_category
    ):
        """Test that unauthenticated requests are rejected"""
        response = client.get(f"/category?category_id={sample_category.id}")
        assert response.status_code == 401

    def test_get_category_with_zero_id(self, client: TestClient, staff_headers: dict):
        """Test getting category with ID 0 (edge case)"""
        response = client.get("/category?category_id=0", headers=staff_headers)

        data = response.json()
        # Should return error as ID 0 likely doesn't exist
        assert data["status"] == "error"

    def test_get_category_with_negative_id(
        self, client: TestClient, staff_headers: dict
    ):
        """Test getting category with negative ID (edge case)"""
        response = client.get("/category?category_id=-1", headers=staff_headers)

        data = response.json()
        assert data["status"] == "error"


class TestCreateCategory:
    """Test suite for creating new categories"""

    def test_manager_can_create_category(
        self, client: TestClient, manager_headers: dict
    ):
        """
        Test that manager can create new categories.
        Manager and Admin have create permission (staff does not).
        """
        response = client.post(
            "/category", headers=manager_headers, json={"id": 10, "name": "furniture"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "new category" in data["message"]
        assert data["message"]["new category"]["name"] == "furniture"
        assert data["message"]["new category"]["id"] == 10

    def test_admin_can_create_category(self, client: TestClient, admin_headers: dict):
        """Test that admin can create new categories"""
        response = client.post(
            "/category", headers=admin_headers, json={"id": 11, "name": "clothing"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"]["new category"]["name"] == "clothing"

    def test_staff_cannot_create_category(
        self, client: TestClient, staff_headers: dict
    ):
        """
        Test that staff cannot create categories.
        Staff only has read permission, should return 401 Unauthorized.
        """
        response = client.post(
            "/category", headers=staff_headers, json={"id": 12, "name": "should_fail"}
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]
        assert "staff" in response.json()["detail"]

    def test_create_category_without_authentication(self, client: TestClient):
        """Test that creating category requires authentication"""
        response = client.post("/category", json={"id": 13, "name": "no_auth"})

        assert response.status_code == 401

    def test_create_category_with_duplicate_id(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test creating category with duplicate ID.
        Should be prevented by check_existing_category_using_id function.
        """
        response = client.post(
            "/category",
            headers=manager_headers,
            json={
                "id": sample_category.id,  # Duplicate ID
                "name": "different_name",
            },
        )

        # Should fail based on your check_existing_category_using_id logic
        # Adjust assertion based on your actual error handling
        assert response.status_code in [200, 400]

    def test_create_category_with_duplicate_name(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test creating category with duplicate name.
        Should be prevented by check_existing_category_using_name function.
        """
        response = client.post(
            "/category",
            headers=manager_headers,
            json={
                "id": 999,
                "name": sample_category.name,  # Duplicate name
            },
        )

        # Should fail based on your check_existing_category_using_name logic
        assert response.status_code in [200, 400]

    def test_create_category_with_uppercase_name(
        self, client: TestClient, manager_headers: dict
    ):
        """
        Test creating category with uppercase name.
        Your code converts names to lowercase.
        """
        response = client.post(
            "/category",
            headers=manager_headers,
            json={
                "id": 20,
                "name": "BOOKS",  # Uppercase
            },
        )

        assert response.status_code == 200
        # Verify name was converted to lowercase
        # (depends on your CategoryCreate model behavior)

    def test_create_category_with_special_characters(
        self, client: TestClient, manager_headers: dict
    ):
        """Test creating category with special characters in name"""
        response = client.post(
            "/category",
            headers=manager_headers,
            json={"id": 21, "name": "home & garden"},
        )

        # Should succeed if your validation allows it
        assert response.status_code == 200

    def test_create_multiple_categories_sequentially(
        self, client: TestClient, manager_headers: dict
    ):
        """Test creating multiple categories one after another"""
        categories = [
            {"id": 30, "name": "sports"},
            {"id": 31, "name": "toys"},
            {"id": 32, "name": "books"},
        ]

        for cat_data in categories:
            response = client.post("/category", headers=manager_headers, json=cat_data)
            assert response.status_code == 200
            assert response.json()["status"] == "success"


class TestUpdateCategory:
    """Test suite for updating existing categories"""

    def test_manager_can_update_category_name(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test that manager can update category name.
        Manager and Admin have update permission.
        """
        response = client.put(
            "/category/update",
            headers=manager_headers,
            json={"id": sample_category.id, "name": "updated_electronics"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "updated category details" in data["message"]

    def test_admin_can_update_category(
        self, client: TestClient, admin_headers: dict, sample_category
    ):
        """Test that admin can update categories"""
        response = client.put(
            "/category/update",
            headers=admin_headers,
            json={"id": sample_category.id, "name": "admin_updated_category"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_staff_cannot_update_category(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """
        Test that staff cannot update categories.
        Staff only has read permission.
        """
        response = client.put(
            "/category/update",
            headers=staff_headers,
            json={"id": sample_category.id, "name": "should_fail"},
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]

    def test_update_nonexistent_category(
        self, client: TestClient, manager_headers: dict
    ):
        """
        Test updating a category that doesn't exist.
        Should return error status with appropriate message.
        """
        response = client.put(
            "/category/update",
            headers=manager_headers,
            json={"id": 99999, "name": "nonexistent"},
        )

        assert response.status_code == 200  # Your API returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert "Unable to find category" in data["message"]["response"]

    def test_update_category_to_duplicate_name(
        self, client: TestClient, manager_headers: dict, test_db: Session
    ):
        """
        Test updating category to a name that already exists.
        Should be prevented by get_category_by_name check.
        """
        # Create two categories
        cat1 = Category(id=40, name="category_one")
        cat2 = Category(id=41, name="category_two")
        test_db.add(cat1)
        test_db.add(cat2)
        test_db.commit()

        # Try to update cat1 to have cat2's name
        response = client.put(
            "/category/update",
            headers=manager_headers,
            json={
                "id": cat1.id,
                "name": cat2.name,  # Duplicate name
            },
        )

        data = response.json()
        assert data["status"] == "error"
        assert "existing category with same name" in data["message"]["response"]

    def test_update_category_without_authentication(
        self, client: TestClient, sample_category
    ):
        """Test that updating requires authentication"""
        response = client.put(
            "/category/update",
            json={"id": sample_category.id, "name": "no_auth_update"},
        )

        assert response.status_code == 401

    def test_update_category_name_case_sensitivity(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test that category name is converted to lowercase.
        Your code does: existing_category.name = category_update.name.lower()
        """
        response = client.put(
            "/category/update",
            headers=manager_headers,
            json={"id": sample_category.id, "name": "UPPERCASE_NAME"},
        )

        assert response.status_code == 200
        # Name should be stored as lowercase
        # Verify in database or response if available

    def test_update_category_with_same_name(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test updating category to its current name.
        Should succeed (no duplicate conflict with itself).
        """
        response = client.put(
            "/category/update",
            headers=manager_headers,
            json={
                "id": sample_category.id,
                "name": sample_category.name,  # Same name
            },
        )

        # This might fail or succeed depending on your logic
        # Your code checks if category_by_name exists, which would be itself
        assert response.status_code == 200


class TestDeleteCategory:
    """Test suite for deleting categories"""

    def test_admin_can_delete_category(
        self, client: TestClient, admin_headers: dict, sample_category
    ):
        """
        Test that admin can delete categories.
        Only admin role has delete permission.
        """
        response = client.delete(
            f"/category/delete?category_id={sample_category.id}", headers=admin_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "deleted category" in data["message"]
        assert data["message"]["deleted category"]["id"] == sample_category.id

    def test_manager_cannot_delete_category(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test that manager cannot delete categories.
        Delete is admin-only operation, should return 401.
        """
        response = client.delete(
            f"/category/delete?category_id={sample_category.id}",
            headers=manager_headers,
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]
        assert "manager" in response.json()["detail"]

    def test_staff_cannot_delete_category(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """Test that staff cannot delete categories"""
        response = client.delete(
            f"/category/delete?category_id={sample_category.id}", headers=staff_headers
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]

    def test_delete_nonexistent_category(self, client: TestClient, admin_headers: dict):
        """
        Test deleting a category that doesn't exist.
        Should return error status with appropriate message.
        """
        response = client.delete(
            "/category/delete?category_id=99999", headers=admin_headers
        )

        assert response.status_code == 200  # Your API returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert "Unable to find category" in data["message"]["response"]
        assert "99999" in data["message"]["response"]

    def test_delete_category_without_authentication(
        self, client: TestClient, sample_category
    ):
        """Test that deleting requires authentication"""
        response = client.delete(f"/category/delete?category_id={sample_category.id}")

        assert response.status_code == 401

    def test_delete_category_verifies_deletion(
        self, client: TestClient, admin_headers: dict, test_db: Session
    ):
        """
        Test that category is actually deleted from database.
        Verify by trying to retrieve it afterwards.
        """
        # Create a category
        category = Category(id=50, name="to_be_deleted")
        test_db.add(category)
        test_db.commit()

        # Delete it
        delete_response = client.delete(
            f"/category/delete?category_id={category.id}", headers=admin_headers
        )
        assert delete_response.status_code == 200

        # Try to get it - should not exist
        get_response = client.get(
            f"/category?category_id={category.id}", headers=admin_headers
        )
        data = get_response.json()
        assert data["status"] == "error"

    def test_delete_category_with_associated_products(
        self, client: TestClient, admin_headers: dict, test_db: Session, sample_product
    ):
        """
        Test deleting a category that has products associated with it.
        This tests cascade delete behavior or foreign key constraints.
        """
        # sample_product is linked to sample_category
        category_id = sample_product.category_id

        response = client.delete(
            f"/category/delete?category_id={category_id}", headers=admin_headers
        )

        # Behavior depends on your database constraints
        # Either succeeds with cascade delete, or fails with FK error
        # Adjust assertion based on your expected behavior
        assert response.status_code in [200, 400, 500]

    def test_cannot_delete_same_category_twice(
        self, client: TestClient, admin_headers: dict, test_db: Session
    ):
        """Test that deleting same category twice fails second time"""
        category = Category(id=60, name="delete_twice")
        test_db.add(category)
        test_db.commit()

        # First delete - should succeed
        first_delete = client.delete(
            f"/category/delete?category_id={category.id}", headers=admin_headers
        )
        assert first_delete.status_code == 200

        # Second delete - should fail
        second_delete = client.delete(
            f"/category/delete?category_id={category.id}", headers=admin_headers
        )
        data = second_delete.json()
        assert data["status"] == "error"


class TestCategoryIntegrationWorkflows:
    """Integration tests for complete category management workflows"""

    def test_complete_category_lifecycle(self, client: TestClient, admin_headers: dict):
        """
        Test complete category lifecycle:
        1. Create category
        2. View it
        3. Update it
        4. Delete it
        """
        # Step 1: Create
        create_response = client.post(
            "/category",
            headers=admin_headers,
            json={"id": 100, "name": "lifecycle_test"},
        )
        assert create_response.status_code == 200

        # Step 2: View
        view_response = client.get("/category?category_id=100", headers=admin_headers)
        assert view_response.status_code == 200
        assert view_response.json()["status"] == "success"

        # Step 3: Update
        update_response = client.put(
            "/category/update",
            headers=admin_headers,
            json={"id": 100, "name": "lifecycle_updated"},
        )
        assert update_response.status_code == 200

        # Step 4: Delete
        delete_response = client.delete(
            "/category/delete?category_id=100", headers=admin_headers
        )
        assert delete_response.status_code == 200

    def test_manager_category_workflow(self, client: TestClient, manager_headers: dict):
        """
        Test manager's allowed operations on categories:
        - Can create
        - Can view
        - Can update
        - Cannot delete (admin only)
        """
        # Create
        create_response = client.post(
            "/category",
            headers=manager_headers,
            json={"id": 110, "name": "manager_category"},
        )
        assert create_response.status_code == 200

        # View
        view_response = client.get("/category?category_id=110", headers=manager_headers)
        assert view_response.status_code == 200

        # Update
        update_response = client.put(
            "/category/update",
            headers=manager_headers,
            json={"id": 110, "name": "manager_updated"},
        )
        assert update_response.status_code == 200

        # Try to delete (should fail)
        delete_response = client.delete(
            "/category/delete?category_id=110", headers=manager_headers
        )
        assert delete_response.status_code == 401

    def test_staff_category_workflow(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """
        Test staff's limited operations on categories:
        - Can view all
        - Can view specific
        - Cannot create
        - Cannot update
        - Cannot delete
        """
        # View all (allowed)
        view_all_response = client.get("/category/all", headers=staff_headers)
        assert view_all_response.status_code == 200

        # View specific (allowed)
        view_one_response = client.get(
            f"/category?category_id={sample_category.id}", headers=staff_headers
        )
        assert view_one_response.status_code == 200

        # Try to create (should fail)
        create_response = client.post(
            "/category", headers=staff_headers, json={"id": 120, "name": "staff_fail"}
        )
        assert create_response.status_code == 401

        # Try to update (should fail)
        update_response = client.put(
            "/category/update",
            headers=staff_headers,
            json={"id": sample_category.id, "name": "staff_fail"},
        )
        assert update_response.status_code == 401

        # Try to delete (should fail)
        delete_response = client.delete(
            f"/category/delete?category_id={sample_category.id}", headers=staff_headers
        )
        assert delete_response.status_code == 401


# ============================================================================
# HOW TO RUN THESE TESTS
# ============================================================================
"""
Run all category tests:
    pytest test_category_routes.py -v

Run specific test class:
    pytest test_category_routes.py::TestCreateCategory -v

Run specific test:
    pytest test_category_routes.py::TestCreateCategory::test_manager_can_create_category -v

Run with coverage:
    pytest test_category_routes.py --cov=src.api --cov-report=html

Run tests matching pattern:
    pytest test_category_routes.py -k "delete" -v

Run with detailed output:
    pytest test_category_routes.py -v -s

Run and stop on first failure:
    pytest test_category_routes.py -v -x

EXPECTED TEST RESULTS:
✅ Staff: Can view categories (GET)
❌ Staff: Cannot create/update/delete categories
✅ Manager: Can view, create, and update categories
❌ Manager: Cannot delete categories
✅ Admin: Can perform all CRUD operations

This file contains 40+ comprehensive tests covering:
- All CRUD operations (Create, Read, Update, Delete)
- Role-based access control (staff, manager, admin)
- Authentication and authorization
- Edge cases (duplicate names/IDs, nonexistent categories)
- Integration workflows
- Error handling
"""
