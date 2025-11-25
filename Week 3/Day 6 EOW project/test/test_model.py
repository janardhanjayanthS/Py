"""Tests for Pydantic model"""
from datetime import datetime, timedelta
from inventory_manager import BaseProduct, ProductTypes, FoodProduct, ElectronicProduct
from pydantic import ValidationError
import pytest


def test_regular_product(product: BaseProduct):
    """
    tests for a valid regualr product
    Args:
        prodcut: BaseProduct's object to test
    """
    assert product.product_id == "P01"
    assert product.product_name == "test_product"
    assert product.quantity == 10
    assert product.price == 10.00
    assert product.type == ProductTypes.RP


def test_food_product(food_product):
    """
    tests for a valid food product
    """
    product = food_product
    assert product.product_id == "P02"
    assert product.product_name == "some_food"
    assert product.quantity == 100
    assert product.price == 120.00
    assert product.type == ProductTypes.FP
    assert product.days_to_expire == 10
    assert not product.is_vegetarian


def test_electronic_product():
    """
    tests for a valid electronic product
    """
    product = ElectronicProduct(
        product_id="P010",
        product_name="wires",
        quantity=15,
        price=1000,
        type=ProductTypes.EP,
        warranty_period_in_years=1.75,
    )
    assert product.product_id == "P010"
    assert product.product_name == "wires"
    assert product.quantity == 15
    assert product.price == 1000
    assert product.type == ProductTypes.EP
    assert product.warranty_period_in_years == 1.75


def test_negative_product_quantity():
    """
    test for negative quantity value of a product
    """
    with pytest.raises(ValidationError):
        BaseProduct(
            product_id="P01",
            product_name="test_product",
            quantity=-10,
            price=10.00,
            type=ProductTypes.RP,
        )


def test_update_to_negative_product_quantity(product: BaseProduct):
    """
    test for assigning negative quantity value of a product
    Args:
        prodcut: BaseProduct's object to test
    """
    with pytest.raises(ValidationError):
        product.quantity = -10


def test_negative_product_price():
    """
    test for negative price value of a product
    """
    with pytest.raises(ValidationError):
        BaseProduct(
            product_id="P01",
            product_name="test_product",
            quantity=10,
            price=-10.00,
            type=ProductTypes.RP,
        )


def test_update_to_negative_product_price(product: BaseProduct):
    """
    test for assigning negative price value of a product
    Args:
        prodcut: BaseProduct's object to test
    """
    with pytest.raises(ValidationError):
        product.price = -10


def test_unknown_product_type():
    """
    test for unknown product type
    """
    with pytest.raises(ValidationError):
        BaseProduct(
            product_id="P01",
            product_name="test_product",
            quantity=10,
            price=-10.00,
            type="unknown product type",  # type: ignore
        )


def test_update_to_unknown_product_type(product: BaseProduct):
    """
    test for assigning empty product name for a product
    Args:
        prodcut: BaseProduct's object to test
    """
    with pytest.raises(ValidationError):
        product.type = "abc"  # type: ignore


def test_product_with_no_name():
    """
    test for product with no name
    """
    with pytest.raises(ValidationError):
        BaseProduct(
            product_id="P01",
            product_name="",
            quantity=10,
            price=-10.00,
            type=ProductTypes.RP,
        )


def test_update_to_unknown_product_name(product: BaseProduct):
    """
    test for assigning empty product name for a product
    Args:
        prodcut: BaseProduct's object to test
    """
    with pytest.raises(ValidationError):
        product.name = ""  # type: ignore


def test_product_data_string(product: BaseProduct):
    """
    test for product __str__ method
    Args:
        prodcut: BaseProduct's object to test
    """
    assert (
        f"{product}"
        == "product_id: P01 | product_name: test_product | quantity: 10 | price: 10.0 | type: regular | "
    )

def test_food_product_get_expirey_date(food_product):
    """
    test for get_expiry_date of FoodProduct class
    """
    expiry_date = food_product.get_expiry_date()
    assert expiry_date == '01-12-2025' # 10 days from now
