from inventory_manager import Inventory
import pytest


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