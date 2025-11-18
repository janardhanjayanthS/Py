from inventory_manager import Inventory
from unittest.mock import MagicMock, patch, mock_open


def test_load_from_csv_success() -> None:
    """
    Tests successfull csv data load
    """
    csv_data = "product_id,product_name,quantity,price,type,days_to_expire,is_vegetarian,warranty_period_in_years\n1,test_product,100,20.00,regular,,,\n2,test_product_new,150,400.00,food,30,No,\n3,test_product_3,1000,1000.00,electronic,,,4"

    inventory_instance = Inventory()
    inventory_instance.add_product = MagicMock()

    with patch('builtins.open', mock_open(read_data=csv_data)):
        inventory_instance.load_from_csv('fake_filepath.csv')

    assert inventory_instance.add_product.call_count == 3

    first_call = inventory_instance.add_product.call_args_list[0][0][0]
    assert first_call['product_id'] == '1'
    assert first_call['product_name'] == 'test_product'
    assert first_call['quantity'] == '100'
    assert first_call['price'] == '20.00'

    second_call = inventory_instance.add_product.call_args_list[1][0][0]
    assert second_call['product_id'] == '2'
    assert second_call['product_name'] == 'test_product_new'
    assert second_call['quantity'] == '150'
    assert second_call['price'] == '400.00'
    assert second_call['type'] == 'food'
    assert second_call['days_to_expire'] == '30'
    assert second_call['is_vegetarian'] == 'No'
