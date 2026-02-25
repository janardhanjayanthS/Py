# class TestLoadFromCSV:
#     def test_load_from_csv_success(self) -> None:
#         """
#         Tests successfull csv data load
#         """
#         csv_data = "product_id,product_name,quantity,price,type,days_to_expire,is_vegetarian,warranty_period_in_years\n1,test_product,100,20.00,regular,,,\n2,test_product_new,150,400.00,food,30,No,\n3,test_product_3,1000,1000.00,electronic,,,4"

#         inventory_instance = Inventory()
#         inventory_instance.add_product = MagicMock()

#         with patch("builtins.open", mock_open(read_data=csv_data)):
#             inventory_instance.load_from_csv("fake_filepath.csv")

#         assert inventory_instance.add_product.call_count == 3

#         first_call = inventory_instance.add_product.call_args_list[0][0][0]
#         assert first_call["product_id"] == "1"
#         assert first_call["product_name"] == "test_product"
#         assert first_call["quantity"] == "100"
#         assert first_call["price"] == "20.00"
#         assert first_call["type"] == "regular"

#         second_call = inventory_instance.add_product.call_args_list[1][0][0]
#         assert second_call["product_id"] == "2"
#         assert second_call["product_name"] == "test_product_new"
#         assert second_call["quantity"] == "150"
#         assert second_call["price"] == "400.00"
#         assert second_call["type"] == "food"
#         assert second_call["days_to_expire"] == "30"
#         assert second_call["is_vegetarian"] == "No"

#         third_call = inventory_instance.add_product.call_args_list[2][0][0]
#         assert third_call["product_id"] == "3"
#         assert third_call["product_name"] == "test_product_3"
#         assert third_call["quantity"] == "1000"
#         assert third_call["price"] == "1000.00"
#         assert third_call["type"] == "electronic"
#         assert third_call["warranty_period_in_years"] == "4"

#     def test_load_from_csv_file_not_found(self, capsys):
#         """
#         test for FileNotFound error handling
#         """
#         inv_instance = Inventory()
#         inv_instance.add_product = MagicMock()

#         with patch("builtins.open", side_effect=FileNotFoundError("No such file")):
#             result = inv_instance.load_from_csv("non_existant.csv")

#         assert result is None

#         inv_instance.add_product.assert_not_called()

#         captured = capsys.readouterr()
#         assert "File not found" in captured.out

#     def test_load_from_csv_empty_file(self):
#         """
#         test for load_from_csv from an empty file
#         """
#         csv_data = "product_id,product_name,quantity,price,type,days_to_expire,is_vegetarian,warranty_period_in_years\n"

#         inv_object = Inventory()
#         inv_object.add_product = MagicMock()

#         with patch("builtins.open", mock_open(read_data=csv_data)):
#             inv_object.load_from_csv("empty_csv_path.csv")

#         inv_object.add_product.assert_not_called()


# # Code from claude
# ------------------------------------------
# class TestGenerateLowQuantityReport:
#     def test_generate_report_with_no_products(self):
#         """Test report generation when inventory is empty"""
#         inventory = Inventory()

#         with patch("inventory_manager.check_low_stock_or_print_details") as mock_check:
#             inventory.generate_low_quantity_report()

#         mock_check.assert_not_called()

#     def test_generate_report_with_single_product(self, capsys):
#         """Test report generation with one product"""
#         inventory = Inventory()

#         mock_product = MagicMock(spec=BaseProduct)
#         mock_product.product_id = "P001"
#         mock_product.product_name = "Apple"
#         mock_product.quantity = 0

#         inventory.products = [mock_product]

#         with patch("inventory_manager.check_low_stock_or_print_details", mock_open()) as mock_check:
#             inventory.generate_low_quantity_report()

#         mock_check.assert_called_once_with(product=mock_product)

#         captured_output = capsys.readouterr()
#         assert "available in less quantity" in captured_output.out

# def test_generate_report_with_multiple_products(self):
#     """Test report generation with multiple products"""
#     inventory = Inventory()

#     # Create multiple mock products
#     product1 = MagicMock(spec=BaseProduct)
#     product1.product_id = "P001"
#     product1.product_name = "test_prod_1"
#     product1.price = 200.00
#     product1.quantity = 5

#     product2 = MagicMock(spec=BaseProduct)
#     product2.product_id = "P002"
#     product1.product_name = "test_prod_2"
#     product1.price = 200.00
#     product2.quantity = 15

#     product3 = MagicMock(spec=BaseProduct)
#     product3.product_id = "P003"
#     product1.product_name = "test_prod_3"
#     product1.price = 200.00
#     product3.quantity = 3

#     inventory.products = [product1, product2, product3]

#     # Mock the file_manager function
#     with patch("inventory_manager.check_low_stock_or_print_details") as mock_check:
#         inventory.generate_low_quantity_report()

#     # Verify it was called for each product
#     assert mock_check.call_count == 3

#     # Verify the order and arguments of calls
#     expected_calls = [
#         call(product=product1),
#         call(product=product2),
#         call(product=product3)
#     ]
#     mock_check.assert_has_calls(expected_calls)

# def test_generate_report_calls_check_function_for_each_product(self):
#     """Test that check function is called for every product in inventory"""
#     inventory = Inventory()

#     # Create 5 mock products
#     products = [MagicMock(spec=BaseProduct) for _ in range(5)]
#     for i, product in enumerate(products):
#         product.product_id = f"P00{i}"

#     inventory.products = products

#     with patch('inventory.check_low_stock_or_print_details') as mock_check:
#         inventory.generate_low_quantity_report()

#     # Verify called exactly 5 times
#     assert mock_check.call_count == 5

#     # Verify each product was passed
#     for product in products:
#         mock_check.assert_any_call(product=product)


# class TestCheckLowStockOrPrintDetails:
#     """Test the file_manager function separately"""

#     def test_low_stock_product_triggers_report(self, capsys):
#         """Test that low stock product triggers append_low_stock_report"""
#         from file_manager import check_low_stock_or_print_details

#         mock_product = MagicMock(spec=BaseProduct)
#         mock_product.product_name = "Apple"
#         mock_product.quantity = 5

#         # Mock both helper functions
#         with patch('file_manager.check_low_stock', return_value=True) as mock_check, \
#              patch('file_manager.append_low_stock_report') as mock_append:

#             check_low_stock_or_print_details(product=mock_product)

#         # Verify check_low_stock was called
#         mock_check.assert_called_once_with(product_quantity=5)

#         # Verify append was called (because stock is low)
#         mock_append.assert_called_once_with(product=mock_product)

#     def test_normal_stock_product_prints_details(self, capsys):
#         """Test that normal stock product prints instead of reporting"""
#         from file_manager import check_low_stock_or_print_details

#         mock_product = MagicMock(spec=BaseProduct)
#         mock_product.product_name = "Orange"
#         mock_product.quantity = 50
#         mock_product.__str__ = MagicMock(return_value="Orange - 50 units")

#         # Mock check_low_stock to return False (not low stock)
#         with patch('file_manager.check_low_stock', return_value=False) as mock_check, \
#              patch('file_manager.append_low_stock_report') as mock_append:

#             check_low_stock_or_print_details(product=mock_product)

#         # Verify check was called
#         mock_check.assert_called_once_with(product_quantity=50)

#         # Verify append was NOT called (stock is normal)
#         mock_append.assert_not_called()

#         # Verify product details were printed
#         captured = capsys.readouterr()
#         assert "Orange - 50 units" in captured.out

#     def test_none_product_does_nothing(self):
#         """Test that None product is handled gracefully"""
#         from file_manager import check_low_stock_or_print_details

#         with patch('file_manager.check_low_stock') as mock_check, \
#              patch('file_manager.append_low_stock_report') as mock_append:

#             check_low_stock_or_print_details(product=None)

#         # Neither function should be called
#         mock_check.assert_not_called()
#         mock_append.assert_not_called()


# class TestCheckLowStock:
#     """Test the check_low_stock function"""

#     def test_quantity_below_threshold_returns_true(self):
#         """Test that quantity below threshold returns True"""
#         from file_manager import check_low_stock

#         # Mock the config to return threshold of 10
#         with patch('file_manager.config.get_low_quality_threshold', return_value=10):
#             result = check_low_stock(product_quantity=5)

#         assert result is True

#     def test_quantity_equal_to_threshold_returns_false(self):
#         """Test that quantity equal to threshold returns False"""
#         from file_manager import check_low_stock

#         with patch('file_manager.config.get_low_quality_threshold', return_value=10):
#             result = check_low_stock(product_quantity=10)

#         assert result is False

#     def test_quantity_above_threshold_returns_false(self):
#         """Test that quantity above threshold returns False"""
#         from file_manager import check_low_stock

#         with patch('file_manager.config.get_low_quality_threshold', return_value=10):
#             result = check_low_stock(product_quantity=50)

#         assert result is False

#     def test_invalid_quantity_handles_type_error(self, capsys):
#         """Test that invalid quantity type is handled gracefully"""
#         from file_manager import check_low_stock

#         with patch('file_manager.config.get_low_quality_threshold', return_value=10):
#             # Pass a value that can't be converted to int
#             result = check_low_stock(product_quantity=None)

#         # Should print error message
#         captured = capsys.readouterr()
#         assert "Encountered type error" in captured.out


# class TestAppendLowStockReport:
#     """Test the append_low_stock_report function"""

#     def test_append_to_existing_file(self, capsys):
#         """Test appending to existing low_stock_report.txt"""
#         from file_manager import append_low_stock_report

#         mock_product = MagicMock(spec=BaseProduct)
#         mock_product.product_name = "Banana"
#         mock_product.quantity = 3
#         mock_product.__str__ = MagicMock(return_value="Banana - 3 units")

#         mock_file = MagicMock()

#         # Mock open to succeed on first try
#         with patch('builtins.open', mock_open()) as mock_open_func, \
#              patch('file_manager.create_file') as mock_create:

#             append_low_stock_report(product=mock_product)

#         # Verify file was opened in append mode
#         mock_open_func.assert_called_with("low_stock_report.txt", "a")

#         # Verify write was called
#         mock_open_func().write.assert_called_once_with("Banana - 3 units\n")

#         # Verify create was NOT called (file exists)
#         mock_create.assert_not_called()

#         # Verify low stock message was printed
#         captured = capsys.readouterr()
#         assert "Product 'Banana' is available in less quantity 3" in captured.out

#     def test_append_creates_file_if_not_exists(self, capsys):
#         """Test that file is created if it doesn't exist"""
#         from file_manager import append_low_stock_report

#         mock_product = MagicMock(spec=BaseProduct)
#         mock_product.product_name = "Mango"
#         mock_product.quantity = 2
#         mock_product.__str__ = MagicMock(return_value="Mango - 2 units")

#         # First call raises FileNotFoundError, second succeeds
#         mock_open_func = MagicMock(side_effect=[
#             FileNotFoundError("File not found"),
#             mock_open()(None, None)
#         ])

#         with patch('builtins.open', mock_open_func), \
#              patch('file_manager.create_file') as mock_create, \
#              patch('file_manager.append_content') as mock_append:

#             append_low_stock_report(product=mock_product)

#         # Verify create_file was called
#         mock_create.assert_called_once_with(filename="low_stock_report.txt")

#         # Verify append_content was called twice (once failed, once after create)
#         assert mock_append.call_count == 2


# class TestAppendContent:
#     """Test the append_content function"""

#     def test_append_content_writes_to_file(self):
#         """Test that content is written to file with newline"""
#         from file_manager import append_content

#         mock_file = mock_open()

#         with patch('builtins.open', mock_file):
#             append_content(filename="test.txt", content="Test content")

#         # Verify file opened in append mode
#         mock_file.assert_called_once_with("test.txt", "a")

#         # Verify write was called with content + newline
#         mock_file().write.assert_called_once_with("Test content\n")


# class TestCreateFile:
#     """Test the create_file function"""

#     def test_create_file_success(self, capsys):
#         """Test successful file creation"""
#         from file_manager import create_file

#         mock_file = mock_open()

#         with patch('builtins.open', mock_file):
#             create_file(filename="new_file.txt")

#         # Verify file opened in exclusive create mode
#         mock_file.assert_called_once_with("new_file.txt", "x")

#         # Verify success message
#         captured = capsys.readouterr()
#         assert "File new_file.txt created successfully" in captured.out
