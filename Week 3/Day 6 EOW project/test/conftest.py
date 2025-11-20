from inventory_manager import Inventory, BaseProduct, ProductTypes
import pytest

@pytest.fixture
def product() -> BaseProduct:
    """
    Fixture for a BaseProduct object with 
    valid attributes

    Returns:
        BaseProduct object
    """
    return BaseProduct(
        product_id="P01",
        product_name="test_product",
        quantity=10,
        price=10.00,
        type=ProductTypes.RP,
    )


@pytest.fixture
def valid_filepath() -> str:
    """
    returns a test inventory csv filepath

    Returns:
        str: test file's path
    """
    return "test_inventory.csv"


@pytest.fixture
def inventory_object() -> Inventory:
    """
    returns an Inventory instance

    Returns:
        Inventory's object
    """
    return Inventory()

@pytest.fixture
def product_dict() -> dict:
    """
    returns product information in dictionary format

    Returns:
        dict: containing product information
    """
    return {
        'product_id': '0008181',
        'product_name': 'office chair',
        'price': 8000.0,
        'quantity': 20,
        'type': 'regular',
        'days_to_expire': '',
        'is_vegetarian': '',
        'warranty_period_in_years': ''
    }