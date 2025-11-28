from src.models.models import Product


class TestProductEndPoints:
    """
    integration tests for product endpoints
    """

    def test_post_product(self, client, test_db):
        """
        Test product POST on /products

        Args:
            client: test application
            test_db: test db object
        """
        test_product_data = {
            "id": "P10",
            "name": "Test prod",
            "quantity": 300,
            "price": 120.0,
            "type": "regular",
            "days_tp_expire": 0,
            "is_vegetarian": False,
            "warranty_in_years": 0,
        }

        response = client.post("/products", json=test_product_data)

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["message"]["inserted product"]["name"] == "Test prod"
        assert response_data["message"]["inserted product"]["type"] == "regular"

        # db actions
        db_product = test_db.query(Product).filter_by(id="P10").first()
        assert db_product is not None
        assert db_product.name == "Test prod"
        assert db_product.type == "regular"

    def test_get_all_products_integration(self, client, test_db):
        """
        Testing GET all products end point

        Args:
            client: test application
            test_db: test db object
        """
        products = [
            Product(id="p1", name="Product 1", quantity=10, price=10.0, type="regular"),
            Product(id="p2", name="Product 2", quantity=20, price=20.0, type="food"),
        ]
        test_db.add_all(products)
        test_db.commit()

        response = client.get("/products")

        assert response.status_code == 200

        data = response.json()
        received_products = data["message"]["products"]
        assert len(received_products) == 2
        assert received_products[0]["name"] == "Product 1"
        assert received_products[1]["name"] == "Product 2"

    def test_get_speficif_product(self, client, sample_product):
        """
        Testing GET specific product using its id

        Args:
            client: test application
            sample_product: sample sqlalchemy db Product instanc
        """
        response = client.get(f"/products?product_id={sample_product.id}")

        assert response.status_code == 200
        received_product = response.json()["message"]["product"]

        assert received_product["name"] == sample_product.name
        assert received_product["type"] == sample_product.type

    def test_update_product_integration(self, client, test_db, sample_product):
        """
        Testing PUT product end point

        Args:
            client: test application
            test_db: test db object
            sample_product (_type_): _description_
        """
        update_data = {"name": "Updated Product Name", "quantity": 15, "price": 149.99}

        response = client.put(
            f"/product?product_id={sample_product.id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()["message"]["updated product"]

        assert data["name"] == update_data["name"]
        assert data["quantity"] == update_data["quantity"]
        assert data["price"] == update_data["price"]

    
