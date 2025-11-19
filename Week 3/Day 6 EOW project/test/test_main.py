from inventory_manager import (
    Inventory,
    BaseProduct,
    ProductTypes,
    FoodProduct,
    ElectronicProduct,
)
from unittest.mock import MagicMock, patch, mock_open, Mock, create_autospec
import pytest
from pathlib import Path


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


class TestLoadFromCSV:
    def test_load_from_csv_file_success(self, valid_filepath, inventory_object):
        """
        test for successful test for loading inventory data
        """
        mock_function = create_autospec(inventory_object.load_from_csv)

        mock_function(valid_filepath)

        mock_function.assert_called_once()
        mock_function.assert_called_once_with(filepath=valid_filepath)

    def test_load_from_csv_file_extenstion_success(
        self, inventory_object, valid_filepath
    ):
        """
        test for valid csv extension from filepath
        """
        mock_function = create_autospec(inventory_object.load_from_csv)
        mock_function(filepath=valid_filepath)
        assert mock_function.call_args.kwargs['filepath'].endswith('.csv')

    def test_load_from_test_csv_file_with_unknown_file(self, inventory_object, capsys):
        """
        test for successful test for loading inventory data
        """
        invalid_filepath: str = ""
        inventory_object.load_from_csv(invalid_filepath)

        captured_output = capsys.readouterr()
        assert "File not found" in captured_output.out

    def test_loading_data_using_load_from_csv_file(
        self, inventory_object, valid_filepath
    ):
        """
        test for checking the loaded data from csv file
        """
        inventory_object.load_from_csv(valid_filepath)
        products = inventory_object.products

        first_prodcut = products[0]
        assert first_prodcut.product_id == "1"
        assert first_prodcut.product_name == "test_product"
        assert first_prodcut.quantity == 100
        assert first_prodcut.price == 20.0
        assert first_prodcut.type.value == "regular"

        second_product = products[1]
        assert second_product.product_id == "2"
        assert second_product.product_name == "test_product_new"
        assert second_product.quantity == 150
        assert second_product.price == 400.0
        assert second_product.type.value == "food"
        assert second_product.days_to_expire == 30
        assert not second_product.is_vegetarian

        third_product = products[2]
        assert third_product.product_id == "3"
        assert third_product.product_name == "test_product_3"
        assert third_product.quantity == 1000
        assert third_product.price == 1000.0
        assert third_product.type.value == "electronic"
        assert third_product.warranty_period_in_years == 4


class TestGenerateLowStockReport:
    def test_generate_low_stock_report_with_no_products(self, inventory_object):
        """
        testing fucntion call with no product
        """
        mock_function = create_autospec(inventory_object.generate_low_quantity_report)

        mock_function()

        mock_function.assert_called_once()

    def test_generate_low_quantity_report_with_valid_products(
        self, inventory_object, valid_filepath, capsys
    ):
        """
        testing generate low quantity report function with valid products - with quantity more than 10
        """
        inventory_object.load_from_csv(valid_filepath)
        inventory_object.generate_low_quantity_report()

        captured_outputs = capsys.readouterr()
        print(captured_outputs)

        assert "test_product" in captured_outputs.out

    def test_generate_low_quantity_report_with_low_stock_product(
        self, inventory_object
    ):
        """
        Testing generate_low_quantity_reprot with a product with less than 10 quantity
        """
        low_stock_report_filepath = "low_stock_report.txt"

        inventory_object.products.append(
            FoodProduct(
                product_id="0006",
                product_name="low_quantity_prod",
                quantity=2,
                price=100.0,
                type=ProductTypes.FP,
                days_to_expire=15,
                is_vegetarian=True,
            )
        )

        inventory_object.generate_low_quantity_report()

        assert Path(low_stock_report_filepath).exists()

        low_stock_file_content = Path(low_stock_report_filepath).read_text()
        assert "low_quantity_prod" in low_stock_file_content


# Day 4 Morining
class TestUpdateStock:
    def test_update_stock_call(self, inventory_object):
        """
        testing update_stock function call
        """

        mock_function = create_autospec(inventory_object.update_stock)

        mock_function(product_id=200, new_quantity=1500)
        mock_function.assert_called_once()
        mock_function.assert_called_once_with(product_id=200, new_quantity=1500)

    def test_update_stock_with_unknown_product(self, inventory_object, capsys):
        """
        test update_stock with unknowun product id
        """
        inventory_object.update_stock(product_id="p009", new_quantity=2000)

        captured_output = capsys.readouterr()

        assert "Cannot find product" in captured_output.out

    @pytest.mark.parametrize(
        "prod_id, new_qty",
        [
            ("1", 20),
            ("2", 200),
            ("3", 7),
        ],
    )
    def test_update_stock_with_valid_products(
        self, prod_id, new_qty, inventory_object, valid_filepath, capsys
    ):
        """
        testing update stock for products from test_inventory.csv
        """
        inventory_object.load_from_csv(valid_filepath)

        inventory_object.update_stock(product_id=prod_id, new_quantity=new_qty)

        captured_output = capsys.readouterr()
        assert "Product details before update" in captured_output.out
        assert "Product details after update" in captured_output.out
