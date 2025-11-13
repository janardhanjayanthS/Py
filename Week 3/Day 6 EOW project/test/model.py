"""Tests for Pydantic model"""
from inventory_manager import BaseProduct, ProductTypes, FoodProduct, ElectronicProduct
from pydantic import ValidationError
import pytest


def test_regular_product():
    """
    tests for a valid regualr product
    """
    product = BaseProduct(
        product_id="P01",
        product_name="test_product",
        quantity=10,
        price=10.00,
        type=ProductTypes.RP,
    )
    assert product.product_id == "P01"
    assert product.product_name == "test_product"
    assert product.quantity == 10
    assert product.price == 10.00
    assert product.type == ProductTypes.RP


def test_food_product():
    """
    tests for a valid food product
    """
    product = FoodProduct(
        product_id="P02",
        product_name="some_food",
        quantity=100,
        price=120.00,
        type=ProductTypes.FP,
        days_to_expire=10,
        is_vegetarian=False,
    )
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

def  test_negative_quantity():
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

def test_negative_price():
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
