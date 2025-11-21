from inventory_manager import check_low_stock
import pytest


class TestCheckLowStock:
    def test_check_low_stock_success(self):
        """
        check for successful low quality check
        """
        high_qty, low_qty = 100, 1

        high_qty_result, low_qty_result = check_low_stock(high_qty), check_low_stock(low_qty)

        assert high_qty_result is False
        assert low_qty_result is True

    def test_check_low_stock_with_unknown_type(self):
        """
        test for check_low_stock with non int args
        """
        with pytest.raises(ValueError):
            check_low_stock('abc') # type: ignore

    