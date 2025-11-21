from inventory_manager import check_low_stock, append_content
from unittest.mock import patch, mock_open
import pytest


class TestCheckLowStock:
    def test_check_low_stock_with_low_stock(self):
        """
        check for successful low quality check
        """
        low_qty = 1

        low_qty_result = check_low_stock(low_qty)

        assert low_qty_result is True

    def test_check_low_stock_with_high_stock(self):
        """
        check for successful high quality check
        """
        high_qty = 10000

        high_qty_result = check_low_stock(high_qty)

        assert high_qty_result is False

    def test_check_low_stock_as_low_qty_threshold(self):
        """
        test when qty is same as thershold(10)
        """
        qty = 10

        result = check_low_stock(qty)

        assert result is False

    def test_check_low_stock_with_unknown_type(self):
        """
        test for check_low_stock with non int args
        """
        with pytest.raises(ValueError):
            check_low_stock("abc")  # type: ignore


class TestAppendContent:
    def test_apppend_content_success(self):
        """
        testing appen_content() successful call
        """
        m = mock_open()
        with patch("builtins.open", m):
            append_content("test.txt", "test content")

        m.assert_called_once_with("test.txt", "a")

        handle = m()
        handle.write.assert_called_once_with("test content\n")
