from unittest.mock import create_autospec

from src.core.utility import get_initial_product_data_from_csv


class TestGetInitialProductDataFromCSV:
    def test_get_initial_data_fucntion_call(self, get_csv_filepath):
        """
        Test for get_initial_data_from_csv fucntion call

        Args:
            get_csv_filepath: filepath of test_inventory.csv file
        """
        mock_fucntion = create_autospec(get_initial_product_data_from_csv)

        mock_fucntion(get_csv_filepath)

        mock_fucntion.assert_called_once()
        mock_fucntion.assert_called_once_with(get_csv_filepath)

    def test_get_initial_data_return_value(self, get_csv_filepath):
        """
        Test for get_initial_data_from_csv function's return value

        Args:
            get_csv_filepath: filepath of test_inventory.csv file
        """

        return_value = get_initial_product_data_from_csv(get_csv_filepath)

        assert return_value["product"][0]["id"] == "P1"
        assert return_value["product"][0]["name"] == "Test product"
        assert return_value["product"][0]["quantity"] == 150
        assert return_value["product"][0]["price"] == 200
        assert return_value["product"][0]["type"] == "regular"
        assert return_value["product"][0]["days_to_expire"] is None
        assert return_value["product"][0]["is_vegetarian"] is None
        assert return_value["product"][0]["warranty_in_years"] is None

    def test_get_inital_data_with_empty_data(self, get_csv_filepath):
        """
        Test for get_initial_data_from_csv function's return value
        """
        mock_fucntion = create_autospec(
            get_initial_product_data_from_csv, return_value={"product": []}
        )

        return_value = mock_fucntion(get_csv_filepath)

        assert return_value == {"product": []}
