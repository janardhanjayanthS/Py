# test_user_routes.py - Tests for user registration, login, and management
from fastapi.testclient import TestClient


class TestUserRegistration:
    """Test suite for user registration endpoint"""

    def test_register_new_user_success(self, client: TestClient):
        """
        Test successful user registration.
        Should create user and return success response.
        """
        response = client.post(
            "/user/register",
            json={
                "name": "New User",
                "email": "newuser@test.com",
                "password": "securepass123",
                "role": "staff",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"]["registered user"]["email"] == "newuser@test.com"
        assert data["message"]["registered user"]["role"] == "staff"

    def test_register_duplicate_email_fails(self, client: TestClient, staff_user):
        """
        Test that registering with existing email fails.
        Should return 400 Bad Request.
        """
        response = client.post(
            "/user/register",
            json={
                "name": "Duplicate User",
                "email": staff_user.email,  # Using existing email
                "password": "password123",
                "role": "staff",
            },
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_register_with_admin_role(self, client: TestClient):
        """Test registering a user with admin role"""
        response = client.post(
            "/user/register",
            json={
                "name": "Admin User",
                "email": "newadmin@test.com",
                "password": "adminpass",
                "role": "admin",
            },
        )

        assert response.status_code == 200
        assert response.json()["message"]["registered user"]["role"] == "admin"


class TestUserLogin:
    """Test suite for user login endpoint"""

    def test_login_with_valid_credentials(self, client: TestClient, staff_user):
        """
        Test login with correct email and password.
        Should return JWT access token.
        """
        response = client.post(
            "/user/login",
            json={
                "email": staff_user.email,
                "password": "password123",  # This is the unhashed password
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_tokem" in data  # Note: There's a typo in your code
        assert data["token_type"] == "Bearer"

    def test_login_with_invalid_email(self, client: TestClient):
        """
        Test login with non-existent email.
        Should return 401 Unauthorized.
        """
        response = client.post(
            "/user/login",
            json={"email": "nonexistent@test.com", "password": "password123"},
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_with_wrong_password(self, client: TestClient, staff_user):
        """
        Test login with correct email but wrong password.
        Should return 401 Unauthorized.
        """
        response = client.post(
            "/user/login", json={"email": staff_user.email, "password": "wrongpassword"}
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]


class TestGetAllUsers:
    """Test suite for getting all users endpoint"""

    def test_staff_can_view_all_users(
        self,
        client: TestClient,
        staff_headers: dict,
        staff_user,
        manager_user,
        admin_user,
    ):
        """
        Test that staff user can view all users.
        All roles (staff, manager, admin) should have access.
        """
        response = client.get("/user/all", headers=staff_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        # Should return all 3 users created by fixtures
        assert len(data["message"]["users"]) == 3

    def test_manager_can_view_all_users(
        self, client: TestClient, manager_headers: dict
    ):
        """Test that manager can view all users"""
        response = client.get("/user/all", headers=manager_headers)
        assert response.status_code == 200

    def test_admin_can_view_all_users(self, client: TestClient, admin_headers: dict):
        """Test that admin can view all users"""
        response = client.get("/user/all", headers=admin_headers)
        assert response.status_code == 200

    def test_unauthorized_access_without_token(self, client: TestClient):
        """
        Test accessing endpoint without JWT token.
        Should return 401 Unauthorized.
        """
        response = client.get("/user/all")
        assert response.status_code == 401

    def test_unauthorized_access_with_invalid_token(self, client: TestClient):
        """Test accessing endpoint with invalid JWT token"""
        response = client.get(
            "/user/all", headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401


class TestUpdateUser:
    """Test suite for updating user details"""

    def test_manager_can_update_own_details(
        self, client: TestClient, manager_headers: dict
    ):
        """
        Test that manager can update their own name and password.
        Only managers and admins have access to this endpoint.
        """
        response = client.patch(
            "/user/update",
            headers=manager_headers,
            json={"name": "Updated Manager", "password": "newpassword123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"]["updated user detail"]["name"] == "Updated Manager"

    def test_admin_can_update_own_details(
        self, client: TestClient, admin_headers: dict
    ):
        """Test that admin can update their own details"""
        response = client.patch(
            "/user/update", headers=admin_headers, json={"name": "Updated Admin"}
        )

        assert response.status_code == 200

    def test_staff_cannot_update_details(self, client: TestClient, staff_headers: dict):
        """
        Test that staff user cannot update details.
        Should return 401 because decorator only allows manager and admin.
        """
        response = client.patch(
            "/user/update", headers=staff_headers, json={"name": "Should Fail"}
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]


class TestDeleteUser:
    """Test suite for deleting users"""

    def test_admin_can_delete_user(
        self, client: TestClient, admin_headers: dict, staff_user
    ):
        """
        Test that admin can delete any user.
        Only admin role has access to delete endpoint.
        """
        response = client.delete(
            f"/user/delete?user_id={staff_user.id}", headers=admin_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"]["deleted account"]["id"] == staff_user.id

    def test_manager_cannot_delete_user(
        self, client: TestClient, manager_headers: dict, staff_user
    ):
        """
        Test that manager cannot delete users.
        Should return 401 Unauthorized.
        """
        response = client.delete(
            f"/user/delete?user_id={staff_user.id}", headers=manager_headers
        )

        assert response.status_code == 401
        assert "Unauthorized to perform action" in response.json()["detail"]

    def test_staff_cannot_delete_user(
        self, client: TestClient, staff_headers: dict, manager_user
    ):
        """Test that staff cannot delete users"""
        response = client.delete(
            f"/user/delete?user_id={manager_user.id}", headers=staff_headers
        )

        assert response.status_code == 401

    def test_delete_nonexistent_user(self, client: TestClient, admin_headers: dict):
        """
        Test deleting a user that doesn't exist.
        Should handle gracefully with appropriate error message.
        """
        response = client.delete("/user/delete?user_id=99999", headers=admin_headers)

        # Based on your handle_missing_user function
        data = response.json()
        assert "message" in data
