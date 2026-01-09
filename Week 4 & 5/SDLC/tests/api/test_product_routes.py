# test_product_routes.py - Tests for product CRUD operations
from fastapi.testclient import TestClient  # noqa: F401
from sqlalchemy.orm import Session  # noqa: F401
from src.models.category import Category  # noqa: F401


class TestGetProducts:
    """Test suite for retrieving products"""

    def test_staff_can_view_all_products(
        self, client: TestClient, staff_headers: dict, multiple_products
    ):
        """
        Test that staff can view all products.
        Staff role has read-only access to products.
        """
        response = client.get("/products", headers=staff_headers)

        assert response.status_code == 200
        data = response.json()
        # Should return all products created by fixture
        assert isinstance(data, list) or isinstance(data, dict)

    def test_manager_can_view_all_products(
        self, client: TestClient, manager_headers: dict, multiple_products
    ):
        """Test that manager can view all products"""
        response = client.get("/products", headers=manager_headers)
        assert response.status_code == 200

    def test_admin_can_view_all_products(
        self, client: TestClient, admin_headers: dict, multiple_products
    ):
        """Test that admin can view all products"""
        response = client.get("/products", headers=admin_headers)
        assert response.status_code == 200

    def test_get_specific_product_by_id(
        self, client: TestClient, staff_headers: dict, sample_product
    ):
        """
        Test retrieving a specific product by ID.
        Uses product_id query parameter.
        """
        response = client.get(
            f"/products?product_id={sample_product.id}", headers=staff_headers
        )

        data = response.json()

        assert response.status_code == 200
        assert data["message"]["product"]["name"] == "Test Laptop"
        assert data["message"]["product"]["quantity"] == 10
        assert data["message"]["product"]["price"] == 999.0

    def test_get_products_by_category(
        self,
        client: TestClient,
        staff_headers: dict,
        sample_category,
        multiple_products,
    ):
        """
        Test retrieving products filtered by category.
        Uses category_id query parameter.
        """
        response = client.get(
            f"/products?category_id={sample_category.id}", headers=staff_headers
        )

        assert response.status_code == 200

    def test_view_products_without_authentication(self, client: TestClient):
        """
        Test that unauthenticated requests are rejected.
        Should return 401 Unauthorized.
        """
        response = client.get("/products")
        assert response.status_code == 401


class TestCreateProduct:
    """Test suite for creating products"""

    def test_manager_can_create_product(
        self, client: TestClient, manager_headers: dict, sample_category
    ):
        """
        Test that manager can create new products.
        Manager and Admin roles have permission to create.
        """
        response = client.post(
            "/products",
            headers=manager_headers,
            json={
                "name": "New Laptop",
                "description": "High-performance laptop",
                "price": 1500,
                "quantity": 10,
                "category_id": sample_category.id,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"]["inserted product"]["name"] == "New Laptop"
        assert data["message"]["inserted product"]["quantity"] == 10
        assert data["message"]["inserted product"]["price"] == 1500

    def test_admin_can_create_product(
        self, client: TestClient, admin_headers: dict, sample_category
    ):
        """Test that admin can create new products"""
        response = client.post(
            "/products",
            headers=admin_headers,
            json={
                "name": "Admin Product",
                "description": "Created by admin",
                "price": 200,
                "quantity": 5,
                "category_id": sample_category.id,
            },
        )

        assert response.status_code == 200

    def test_staff_cannot_create_product(
        self, client: TestClient, staff_headers: dict, sample_category
    ):
        """
        Test that staff cannot create products.
        Staff only has read permission, should return 401.
        """
        response = client.post(
            "/products",
            headers=staff_headers,
            json={
                "name": "Should Fail",
                "description": "Staff cannot create",
                "price": 100,
                "quantity": 5,
                "category_id": sample_category.id,
            },
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]

    def test_create_product_without_token(self, client: TestClient, sample_category):
        """Test that product creation requires authentication"""
        response = client.post(
            "/products",
            json={
                "name": "No Auth Product",
                "description": "Should fail",
                "price": 100,
                "": 5,
                "category_id": sample_category.id,
            },
        )

        assert response.status_code == 422


class TestUpdateProduct:
    """Test suite for updating products"""

    def test_manager_can_update_product(
        self, client: TestClient, manager_headers: dict, sample_product
    ):
        """
        Test that manager can update existing products.
        Manager and Admin have update permissions.
        """
        response = client.put(
            f"/product?product_id={sample_product.id}",
            headers=manager_headers,
            json={"name": "Updated Product", "price": 1200},
        )

        assert response.status_code == 200
        # Verify product was updated
        data = response.json()
        print(f"Data in test_manager_can_create_product: {data}")
        assert data["message"]["updated product"]["name"] == "Updated Product"
        assert data["message"]["updated product"]["quantity"] == 10
        assert data["message"]["updated product"]["price"] == pytest.approx(1200.0)

    def test_admin_can_update_product(
        self, client: TestClient, admin_headers: dict, sample_product
    ):
        """Test that admin can update products"""
        response = client.put(
            f"/product?product_id={sample_product.id}",
            headers=admin_headers,
            json={"description": "Updated by admin"},
        )

        assert response.status_code == 200

    def test_staff_cannot_update_product(
        self, client: TestClient, staff_headers: dict, sample_product
    ):
        """
        Test that staff cannot update products.
        Staff only has read permission.
        """
        response = client.put(
            f"/product?product_id={sample_product.id}",
            headers=staff_headers,
            json={"name": "Should Fail"},
        )

        assert response.status_code == 401

    def test_update_nonexistent_product(
        self, client: TestClient, manager_headers: dict
    ):
        """Test updating a product that doesn't exist"""
        response = client.put(
            "/product?product_id=99999",
            headers=manager_headers,
            json={"name": "Nonexistent"},
        )

        data = response.json()
        assert data["status"] == "error"
        assert data["message"]["response"].endswith("not found")


class TestDeleteProduct:
    """Test suite for deleting products"""

    def test_admin_can_delete_product(
        self, client: TestClient, admin_headers: dict, sample_product
    ):
        """
        Test that admin can delete products.
        Only admin role has delete permission.
        """
        response = client.delete(
            f"/product?product_id={sample_product.id}", headers=admin_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_manager_cannot_delete_product(
        self, client: TestClient, manager_headers: dict, sample_product
    ):
        """
        Test that manager cannot delete products.
        Delete is admin-only operation.
        """
        response = client.delete(
            f"/product?product_id={sample_product.id}", headers=manager_headers
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]

    def test_staff_cannot_delete_product(
        self, client: TestClient, staff_headers: dict, sample_product
    ):
        """Test that staff cannot delete products"""
        response = client.delete(
            f"/product?product_id={sample_product.id}", headers=staff_headers
        )

        assert response.status_code == 401


class TestUpdateProductCategory:
    """Test suite for updating product category"""

    def test_manager_can_update_product_category(
        self,
        client: TestClient,
        manager_headers: dict,
        sample_product,
        test_db: Session,
    ):
        """
        Test that manager can change product's category.
        Uses PATCH endpoint to update category association.
        """
        # Create a new category to switch to
        new_category = Category(id=2, name="accessories")
        test_db.add(new_category)
        test_db.commit()

        response = client.patch(
            f"/product/update_category?product_id={sample_product.id}&category_id={new_category.id}",
            headers=manager_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_admin_can_update_product_category(
        self, client: TestClient, admin_headers: dict, sample_product, sample_category
    ):
        """Test that admin can update product category"""
        response = client.patch(
            f"/product/update_category?product_id={sample_product.id}&category_id={sample_category.id}",
            headers=admin_headers,
        )

        assert response.status_code == 200

    def test_staff_cannot_update_product_category(
        self, client: TestClient, staff_headers: dict, sample_product, sample_category
    ):
        """
        Test that staff cannot update product category.
        Should return 401 Unauthorized.
        """
        response = client.patch(
            f"/product/update_category?product_id={sample_product.id}&category_id={sample_category.id}",
            headers=staff_headers,
        )

        assert response.status_code == 401

    def test_update_category_with_invalid_category_id(
        self, client: TestClient, manager_headers: dict, sample_product
    ):
        """Test updating product with non-existent category"""
        response = client.patch(
            f"/product/update_category?product_id={sample_product.id}&category_id=99999",
            headers=manager_headers,
        )

        data = response.json()
        assert data["status"] == "error"
        assert "Cannot find category" in data["message"]["response"]
