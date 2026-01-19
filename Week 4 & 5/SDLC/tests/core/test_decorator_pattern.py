# test_decorator_pattern.py - Tests for decorator pattern functionality
import pytest
from src.core.decorator_pattern import ConcretePrice, DiscountDecorator, TaxDecorator


class TestConcretePrice:
    """Test suite for ConcretePrice class"""

    def test_concrete_price_initialization(self):
        """Test ConcretePrice initialization with valid amount"""
        price = ConcretePrice(100.0)
        assert price.get_amount() == 100.0

    def test_concrete_price_zero_amount(self):
        """Test ConcretePrice with zero amount"""
        price = ConcretePrice(0.0)
        assert price.get_amount() == 0.0

    def test_concrete_price_negative_amount(self):
        """Test ConcretePrice with negative amount"""
        price = ConcretePrice(-50.0)
        assert price.get_amount() == -50.0

    def test_concrete_price_decimal_amount(self):
        """Test ConcretePrice with decimal amount"""
        price = ConcretePrice(99.99)
        assert abs(price.get_amount() - 99.99) < 0.0001

    def test_concrete_price_large_amount(self):
        """Test ConcretePrice with large amount"""
        price = ConcretePrice(999999.99)
        assert abs(price.get_amount() - 999999.99) < 0.0001


class TestDiscountDecorator:
    """Test suite for DiscountDecorator class"""

    def test_discount_decorator_initialization(self):
        """Test DiscountDecorator initialization"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 20.0)

        assert discount_price.get_amount() == 80.0  # 100 - 20% = 80

    def test_discount_decorator_zero_percentage(self):
        """Test DiscountDecorator with zero discount"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 0.0)

        assert discount_price.get_amount() == 100.0  # No discount

    def test_discount_decorator_hundred_percentage(self):
        """Test DiscountDecorator with 100% discount"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 100.0)

        assert discount_price.get_amount() == 0.0  # Free!

    def test_discount_decorator_fifty_percentage(self):
        """Test DiscountDecorator with 50% discount"""
        base_price = ConcretePrice(200.0)
        discount_price = DiscountDecorator(base_price, 50.0)

        assert discount_price.get_amount() == 100.0  # Half price

    def test_discount_decorator_small_percentage(self):
        """Test DiscountDecorator with small discount"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 5.0)

        assert discount_price.get_amount() == 95.0  # 5% discount

    def test_discount_decorator_large_percentage(self):
        """Test DiscountDecorator with large discount"""
        base_price = ConcretePrice(1000.0)
        discount_price = DiscountDecorator(base_price, 75.0)

        assert discount_price.get_amount() == 250.0  # 75% discount

    def test_discount_decorator_negative_percentage(self):
        """Test DiscountDecorator with negative percentage (should increase price)"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, -10.0)

        assert discount_price.get_amount() == 110.0  # -10% = +10%

    def test_discount_decorator_over_hundred_percentage(self):
        """Test DiscountDecorator with over 100% discount"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 150.0)

        assert discount_price.get_amount() == -50.0  # 150% discount = negative price

    def test_discount_decorator_decimal_percentage(self):
        """Test DiscountDecorator with decimal percentage"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 12.5)

        assert abs(discount_price.get_amount() - 87.5) < 0.0001


class TestTaxDecorator:
    """Test suite for TaxDecorator class"""

    def test_tax_decorator_initialization(self):
        """Test TaxDecorator initialization"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, 20.0)

        assert tax_price.get_amount() == 120.0  # 100 + 20% = 120

    def test_tax_decorator_zero_percentage(self):
        """Test TaxDecorator with zero tax"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, 0.0)

        assert tax_price.get_amount() == 100.0  # No tax

    def test_tax_decorator_standard_vat(self):
        """Test TaxDecorator with standard VAT (20%)"""
        base_price = ConcretePrice(50.0)
        tax_price = TaxDecorator(base_price, 20.0)

        assert tax_price.get_amount() == 60.0  # 50 + 20% = 60

    def test_tax_decorator_small_percentage(self):
        """Test TaxDecorator with small tax percentage"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, 5.0)

        assert tax_price.get_amount() == 105.0  # 5% tax

    def test_tax_decorator_large_percentage(self):
        """Test TaxDecorator with large tax percentage"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, 50.0)

        assert tax_price.get_amount() == 150.0  # 50% tax

    def test_tax_decorator_negative_percentage(self):
        """Test TaxDecorator with negative percentage (tax refund)"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, -10.0)

        assert tax_price.get_amount() == 90.0  # -10% tax = refund

    def test_tax_decorator_decimal_percentage(self):
        """Test TaxDecorator with decimal percentage"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, 8.25)

        assert abs(tax_price.get_amount() - 108.25) < 0.0001


class TestDecoratorPatternChaining:
    """Test suite for chaining decorators"""

    def test_discount_then_tax(self):
        """Test applying discount first, then tax"""
        base_price = ConcretePrice(100.0)
        discount_price = DiscountDecorator(base_price, 20.0)  # 20% off = 80
        tax_price = TaxDecorator(discount_price, 10.0)  # 10% tax on 80 = 88

        assert tax_price.get_amount() == 88.0

    def test_tax_then_discount(self):
        """Test applying tax first, then discount"""
        base_price = ConcretePrice(100.0)
        tax_price = TaxDecorator(base_price, 10.0)  # 10% tax = 110
        discount_price = DiscountDecorator(tax_price, 20.0)  # 20% off 110 = 88

        assert discount_price.get_amount() == 88.0

    def test_multiple_discounts(self):
        """Test applying multiple discounts"""
        base_price = ConcretePrice(100.0)
        first_discount = DiscountDecorator(base_price, 10.0)  # 90
        second_discount = DiscountDecorator(first_discount, 10.0)  # 81

        assert second_discount.get_amount() == 81.0

    def test_multiple_taxes(self):
        """Test applying multiple taxes"""
        base_price = ConcretePrice(100.0)
        first_tax = TaxDecorator(base_price, 10.0)  # 110
        second_tax = TaxDecorator(first_tax, 10.0)  # 121

        assert second_tax.get_amount() == 121.0

    def test_complex_chaining(self):
        """Test complex decorator chaining"""
        base_price = ConcretePrice(200.0)
        discount = DiscountDecorator(base_price, 25.0)  # 150
        tax = TaxDecorator(discount, 20.0)  # 180
        additional_discount = DiscountDecorator(tax, 10.0)  # 162

        assert additional_discount.get_amount() == 162.0

    def test_three_level_chain(self):
        """Test three-level decorator chain"""
        base_price = ConcretePrice(1000.0)
        level1 = DiscountDecorator(base_price, 30.0)  # 700
        level2 = TaxDecorator(level1, 15.0)  # 805
        level3 = DiscountDecorator(level2, 10.0)  # 724.5

        assert abs(level3.get_amount() - 724.5) < 0.0001


class TestDecoratorPatternEdgeCases:
    """Test suite for decorator pattern edge cases"""

    def test_zero_base_price_with_discount(self):
        """Test discount on zero base price"""
        base_price = ConcretePrice(0.0)
        discount_price = DiscountDecorator(base_price, 50.0)

        assert discount_price.get_amount() == 0.0

    def test_zero_base_price_with_tax(self):
        """Test tax on zero base price"""
        base_price = ConcretePrice(0.0)
        tax_price = TaxDecorator(base_price, 25.0)

        assert tax_price.get_amount() == 0.0

    def test_negative_base_price_with_discount(self):
        """Test discount on negative base price"""
        base_price = ConcretePrice(-100.0)
        discount_price = DiscountDecorator(base_price, 20.0)

        assert discount_price.get_amount() == -80.0

    def test_negative_base_price_with_tax(self):
        """Test tax on negative base price"""
        base_price = ConcretePrice(-100.0)
        tax_price = TaxDecorator(base_price, 20.0)

        assert tax_price.get_amount() == -120.0

    def test_very_small_amounts(self):
        """Test decorators with very small amounts"""
        base_price = ConcretePrice(0.01)
        discount_price = DiscountDecorator(base_price, 50.0)
        tax_price = TaxDecorator(discount_price, 20.0)

        assert abs(tax_price.get_amount() - 0.006) < 0.0001

    def test_very_large_amounts(self):
        """Test decorators with very large amounts"""
        base_price = ConcretePrice(1000000.0)
        discount_price = DiscountDecorator(base_price, 5.0)
        tax_price = TaxDecorator(discount_price, 8.0)

        expected = 1000000.0 * 0.95 * 1.08  # 1026000.0
        assert abs(tax_price.get_amount() - expected) < 0.01


class TestDecoratorPatternRealWorldScenarios:
    """Test suite for real-world pricing scenarios"""

    def test_black_friday_pricing(self):
        """Test Black Friday pricing scenario"""
        base_price = ConcretePrice(500.0)
        black_friday_discount = DiscountDecorator(base_price, 40.0)  # 40% off
        sales_tax = TaxDecorator(black_friday_discount, 8.5)  # 8.5% sales tax

        expected = 500.0 * 0.6 * 1.085  # 325.5
        assert abs(sales_tax.get_amount() - expected) < 0.0001

    def test_european_vat_pricing(self):
        """Test European VAT pricing scenario"""
        base_price = ConcretePrice(100.0)
        member_discount = DiscountDecorator(base_price, 15.0)  # 15% member discount
        vat = TaxDecorator(member_discount, 21.0)  # 21% VAT

        expected = 100.0 * 0.85 * 1.21  # 102.85
        assert abs(vat.get_amount() - expected) < 0.0001

    def test_bulk_purchase_pricing(self):
        """Test bulk purchase pricing scenario"""
        base_price = ConcretePrice(50.0)
        bulk_discount = DiscountDecorator(base_price, 25.0)  # 25% bulk discount
        loyalty_discount = DiscountDecorator(bulk_discount, 10.0)  # 10% loyalty
        tax = TaxDecorator(loyalty_discount, 7.5)  # 7.5% tax

        expected = 50.0 * 0.75 * 0.9 * 1.075  # 36.28125
        assert abs(tax.get_amount() - expected) < 0.0001

    def test_premium_product_pricing(self):
        """Test premium product pricing scenario"""
        base_price = ConcretePrice(1000.0)
        luxury_tax = TaxDecorator(base_price, 25.0)  # 25% luxury tax
        import_duty = TaxDecorator(luxury_tax, 10.0)  # 10% import duty
        clearance_discount = DiscountDecorator(import_duty, 30.0)  # 30% clearance

        expected = 1000.0 * 1.25 * 1.1 * 0.7  # 962.5
        assert abs(clearance_discount.get_amount() - expected) < 0.0001


class TestDecoratorPatternIntegration:
    """Integration tests for decorator pattern"""

    def test_price_calculation_consistency(self):
        """Test that price calculations are consistent across different approaches"""
        base_price = ConcretePrice(200.0)

        # Method 1: Chain decorators
        method1 = TaxDecorator(DiscountDecorator(base_price, 20.0), 10.0)

        # Method 2: Calculate manually
        method2_result = 200.0 * 0.8 * 1.1  # 176.0

        assert abs(method1.get_amount() - method2_result) < 0.0001

    def test_decorator_composition(self):
        """Test that decorators can be composed in different orders"""
        base_price = ConcretePrice(100.0)

        # Different compositions should yield different results
        composition1 = TaxDecorator(DiscountDecorator(base_price, 20.0), 10.0)
        composition2 = DiscountDecorator(TaxDecorator(base_price, 10.0), 20.0)

        # These should be equal (mathematically: (100 * 0.8) * 1.1 = (100 * 1.1) * 0.8 = 88)
        assert composition1.get_amount() == composition2.get_amount()

    def test_nested_decorator_reuse(self):
        """Test that decorated objects can be reused"""
        base_price = ConcretePrice(100.0)
        discount = DiscountDecorator(base_price, 25.0)  # 75

        # Use the same discount in multiple calculations
        tax1 = TaxDecorator(discount, 10.0)  # 82.5
        tax2 = TaxDecorator(discount, 20.0)  # 90

        assert tax1.get_amount() == 82.5
        assert tax2.get_amount() == 90.0
        assert discount.get_amount() == 75.0  # Original should be unchanged
